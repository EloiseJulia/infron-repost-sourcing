#!/usr/bin/env python3
"""Offline review/state/export engine. No network calls or language-model scoring."""
import argparse
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ('audience_value', 'substance', 'timeliness', 'brand_fit', 'increment')
PARTS = ('text', 'quote', 'media', 'links')


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def stamp(value):
    require(isinstance(value, str), 'timestamp must be an ISO string')
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise Invalid('invalid ISO timestamp') from None
    require(dt.tzinfo is not None, 'timestamp needs an explicit timezone')
    return dt


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def post_url(value):
    require(isinstance(value, str), 'post URL must be a string')
    p = urlsplit(value.strip())
    require(p.scheme in ('http', 'https') and p.hostname in
            ('x.com', 'www.x.com', 'twitter.com', 'www.twitter.com', 'mobile.twitter.com'),
            'expected an x.com/twitter.com post URL')
    require(not p.username and not p.password and p.port is None, 'unexpected URL credentials/port')
    m = re.fullmatch(r'/(?:[A-Za-z0-9_]{1,15}/status|i/web/status|i/status)/(\d{1,24})(?:/(?:photo|video)/\d+)?/?', p.path)
    require(m is not None, 'expected a concrete post status ID')
    pid = m.group(1)
    require(pid != '0' and not pid.startswith('0'), 'invalid post ID')
    return pid, 'https://x.com/i/web/status/' + pid


def article_url(value):
    p = urlsplit(value.strip())
    require(p.scheme in ('http', 'https') and p.hostname and not p.username and not p.password,
            'article URL must be http(s), without credentials')
    require(p.port in (None, 80, 443), 'unexpected article URL port')
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in ('fbclid', 'gclid', 'ref_src')]
    # Preserve meaningful parameters such as model version; never strip all query strings.
    return urlunsplit((p.scheme.lower(), p.hostname.lower(), p.path or '/', urlencode(sorted(query)), ''))


def normalize(candidate):
    require(isinstance(candidate, dict), 'each candidate must be an object')
    c = copy.deepcopy(candidate)
    pid, url = post_url(c.get('url'))
    if 'post_id' in c:
        require(isinstance(c['post_id'], str) and c['post_id'] == pid, 'post_id must match URL as a string')
    c.update(post_id=pid, url=url)
    require(type(c.get('synthetic')) is bool, 'synthetic must be explicit true/false')
    require(nonempty(c.get('author')), 'author is required')
    handle = c['author'].lstrip('@')
    require(re.fullmatch(r'[A-Za-z0-9_]{1,15}', handle) is not None, 'invalid author handle')
    original_path = urlsplit(candidate['url']).path.split('/')
    if original_path[1] != 'i':
        require(original_path[1].lower() == handle.lower(), 'author does not match URL handle')
    c['author'] = '@' + handle
    require(c.get('lane') in ('Model', 'Other'), 'lane must be Model/Other')
    require(c.get('post_type') in ('original', 'quote', 'reply', 'repost', 'unknown'), 'invalid post_type')
    require(nonempty(c.get('event_key')), 'provide a specific, semantic event_key')
    c['article_urls'] = sorted(set(article_url(u) for u in c.get('article_urls', [])))
    ids = c.get('edit_ids', [])
    require(isinstance(ids, list) and all(isinstance(i, str) and re.fullmatch(r'[1-9]\d{0,23}', i) for i in ids),
            'edit_ids must be strings')
    c['edit_ids'] = sorted(set(ids + [pid]))
    if c.get('quote_url'):
        c['quote_id'], c['quote_url'] = post_url(c['quote_url'])
    return c


def keys(c):
    return (['post:' + p for p in c['edit_ids']] + ['event:' + c['event_key']] +
            ['article:' + u for u in c['article_urls']])


def validate_review(c, at, config):
    r = c.get('review')
    require(isinstance(r, dict), 'review is required; use prepare then let an agent/editor review')
    for name in ('reviewer', 'summary_zh', 'why_now', 'brand_reason', 'fact_reason', 'identity_reason',
                 'reason', 'novelty_reason'):
        require(nonempty(r.get(name)), 'review.' + name + ' is required')
    checked = stamp(r.get('checked_at'))
    require(checked <= at, 'review time cannot be in the future')
    require(r.get('decision') in ('recommend', 'hold', 'reject'), 'invalid editorial decision')
    require(r.get('identity') in ('verified', 'unknown'), 'invalid identity verdict')
    require(r.get('facts') in ('verified', 'unknown', 'false'), 'invalid facts verdict')
    require(r.get('brand') in ('acceptable', 'overlap_promotion', 'unknown'), 'invalid brand verdict')
    require(r.get('action') in ('pure_repost', 'quote', 'none'), 'invalid action')
    require(isinstance(r.get('priority'), int) and not isinstance(r['priority'], bool) and r['priority'] >= 1,
            'priority must be an editor-assigned positive ordinal; no auto-score')
    for d in DIMENSIONS:
        rating = r.get('quality', {}).get(d, {})
        require(rating.get('level') in ('high', 'medium', 'low') and nonempty(rating.get('reason')),
                'provide level and evidence reason for quality.' + d)
    evidence = c.get('evidence', {})
    require(isinstance(evidence, dict) and set(evidence) == set(PARTS), 'evidence must contain exactly text/quote/media/links')
    for part in PARTS:
        e = evidence.get(part, {})
        require(isinstance(e, dict), 'evidence part must be an object')
        require(e.get('presence') in ('yes', 'no', 'unknown'), 'missing presence for ' + part)
        require(e.get('status') in ('full', 'partial', 'unavailable', 'not_present'), 'invalid status for ' + part)
        require(nonempty(e.get('note')), 'explain reading scope for ' + part)
        if e['presence'] == 'no':
            require(e['status'] == 'not_present', 'absent content must have not_present status')
        else:
            require(e['status'] != 'not_present', 'unknown/present content cannot be not_present')
        if e['status'] in ('full', 'partial'):
            require(nonempty(e.get('locator')), 'read evidence requires a locator: ' + part)
    require(evidence['text']['presence'] == 'yes', 'the original post text is always required')
    if c['post_type'] == 'quote' or c.get('quote_id'):
        require(evidence['quote']['presence'] != 'no', 'quoted post cannot be marked absent')
    if c['article_urls']:
        require(evidence['links']['presence'] != 'no', 'article links cannot be marked absent')
    entities = r.get('entities')
    require(isinstance(entities, list), 'entities must be an explicit list')
    for e in entities:
        require(all(nonempty(e.get(k)) for k in ('name', 'role', 'behavior', 'evidence')), 'incomplete entity review')
    claims = r.get('claims')
    require(isinstance(claims, list) and claims, 'provide at least one core claim with evidence')
    for claim in claims:
        require(nonempty(claim.get('claim')) and claim.get('status') in ('verified', 'unknown', 'false')
                and nonempty(claim.get('evidence')), 'invalid claim audit')
    require(type(r.get('material_update', False)) is bool, 'material_update must be boolean')
    if 'evergreen_reason' in r:
        require(nonempty(r['evergreen_reason']), 'evergreen_reason must be an actual explanation')
    if r.get('material_update'):
        require(nonempty(r.get('previous_reference')) and nonempty(r.get('update_evidence')),
                'material update requires previous_reference and update_evidence')
    reasons = []
    # A known disqualifier is sufficient to reject; unread material is never declared safe.
    if r['brand'] == 'overlap_promotion':
        return 'reject', ['overlap_promotion']
    if r['facts'] == 'false' or any(x['status'] == 'false' for x in claims):
        return 'reject', ['false_claim']
    if r['decision'] == 'reject':
        return 'reject', ['editorial_reject']
    if any(e['presence'] == 'unknown' or (e['presence'] == 'yes' and e['status'] != 'full')
           for e in evidence.values()):
        reasons.append('incomplete_evidence')
    if r['identity'] != 'verified':
        reasons.append('identity_unverified')
    if r['facts'] != 'verified' or any(x['status'] != 'verified' for x in claims):
        reasons.append('facts_unverified')
    if r['brand'] != 'acceptable':
        reasons.append('brand_unknown')
    if c['post_type'] == 'unknown':
        reasons.append('post_type_unknown')
    if not c.get('published_at'):
        reasons.append('publication_time_unknown')
    else:
        published = stamp(c['published_at'])
        if published > at:
            reasons.append('publication_time_future')
        age = (at - published).total_seconds() / 3600
        if age > config['freshness_hours'][c['lane']] and not r.get('evergreen_reason'):
            reasons.append('outside_editorial_window')
    if (at - checked).total_seconds() > config['review_ttl_hours'] * 3600:
        reasons.append('review_stale')
    if r['decision'] == 'hold':
        reasons.append('editorial_hold')
    if r['decision'] == 'recommend' and r['action'] == 'none':
        reasons.append('action_missing')
    return ('hold', reasons) if reasons else ('recommend', ['editorial_pass'])


def connect(path, fixture):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=5)
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('''
      CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, at TEXT, rules TEXT, digest TEXT, result TEXT);
      CREATE TABLE IF NOT EXISTS decisions (run_id TEXT, post_id TEXT, verdict TEXT, record TEXT,
          PRIMARY KEY(run_id,post_id), FOREIGN KEY(run_id) REFERENCES runs(id));
      CREATE TABLE IF NOT EXISTS dedup (key TEXT, post_id TEXT, kind TEXT, reference TEXT,
          PRIMARY KEY(key,post_id,kind));
      CREATE TABLE IF NOT EXISTS feedback (id TEXT PRIMARY KEY, post_id TEXT, action TEXT,
          actor TEXT, reason TEXT, at TEXT, reference TEXT);
    ''')
    mode = 'fixture' if fixture else 'real'
    old = db.execute("SELECT value FROM metadata WHERE key='mode'").fetchone()
    if old is not None and old[0] != mode:
        db.close()
        raise Invalid('fixture and real state must use separate databases')
    db.execute("INSERT OR IGNORE INTO metadata VALUES ('mode',?)", (mode,))
    db.commit()
    return db


def seed_history(db, path):
    if not path:
        return
    for item in read(path):
        require(item.get('relationship_verified') is True, 'only verified historical actions may seed dedup')
        require(item.get('action') in ('quote', 'repost', 'original'), 'invalid historical action')
        pid, url = post_url(item['url'])
        reference = item['evidence_url']
        if not (item['action'] == 'repost' and reference == 'https://x.com/InfronAI/reposts'):
            _, reference = post_url(reference)
        for key in ['post:' + pid] + (['event:' + item['event_key']] if item.get('event_key') else []):
            db.execute('INSERT OR IGNORE INTO dedup VALUES (?,?,?,?)', (key, pid, 'history', reference))


def safe_md(text):
    return str(text).replace('\n', ' ').replace('\r', ' ').replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;')


def brief(result):
    s = result['summary']
    lines = ['# Infron Repost Sourcing v0.1', '',
             ('**SYNTHETIC FIXTURE — 非真实候选。**' if result['fixture'] else '**手工输入复核 — 未实现自动发现。**'), '',
             f"Run `{result['run_id']}` · {result['as_of']} · rules `{result['rules_version']}`", '',
             f"状态：{s['status']}；输入 {s['input']}，同批重复 {s['input_duplicates']}，深读 {s['reviewed']}。",
             f"主推荐 {s['recommended']}；Hold {s['hold']}；Reject {s['reject']}；合格备选 {s['alternates']}。", '',
             '本结果仅覆盖所供材料；不代表全 X 搜索结论。recommend 不等于批准或已发布。', '',
             '## 主推荐', '']
    chosen = [c for c in result['candidates'] if c['selected']]
    if not chosen:
        lines += ['无主推荐。见下列缺口；不凑满两个槽位。', '']
    for c in chosen:
        r = c['review']
        lines += [f"### {c['lane']} · [{c['author']}]({c['url']})", '',
                  f"发布时间：{c.get('published_at')}；核查：{r['checked_at']}。", '',
                  safe_md(r['summary_zh']), '', '分享理由：' + safe_md(r['why_now']), '',
                  f"建议：{r['action']}。增量：{safe_md(r['novelty_reason'])}", '',
                  '品牌：' + safe_md(r['brand_reason']), '', '事实：' + safe_md(r['fact_reason']), '',
                  '身份：' + safe_md(r['identity_reason']), '',
                  '证据范围：' + '; '.join(f"{p}={e['status']} ({safe_md(e['note'])})" for p,e in c['evidence'].items()), '']
        for d in DIMENSIONS:
            lines.append(f"- {d}: {r['quality'][d]['level']} — {safe_md(r['quality'][d]['reason'])}")
        lines += ['', '关键主张：']
        lines += [f"- {safe_md(cl['claim'])}：{cl['status']}；{safe_md(cl['evidence'])}" for cl in r['claims']]
        lines += ['', ('剩余缺口：仅为合成材料验证；链接不能当作真实帖子，不可发布。' if result['fixture'] else
                       '剩余缺口：无核心读取缺口；发布前仍需重开原帖复核。'), '']
    lines += ['## Hold / Reject / 备选', '', '| 帖子 | 结论 | 原因 |', '|---|---|---|']
    for c in result['candidates']:
        if not c['selected']:
            label = 'alternate' if c['verdict'] == 'recommend' else c['verdict']
            detail = '; '.join(c['reason_codes']) + ' — ' + c['review']['reason']
            lines.append(f"| [{safe_md(c['author'])}]({c['url']}) | {label} | {safe_md(detail)} |")
    lines += ['', '## 覆盖与资源', '', f"窗口：{safe_md(result['coverage']['window'])}。", '',
              f"已成功：{safe_md(', '.join(result['coverage']['success'])) or '无'}。", '',
              f"未覆盖/失败：{safe_md('; '.join(result['coverage']['failed'])) or '所供范围无记录失败'}。", '',
              '自动发现：not_implemented；API 请求 0；本地脚本模型调用 0；本地脚本付费消耗 0。', '',
              f"预算：输入上限 {result['budget']['max_input']}；深读上限 {result['budget']['max_reviewed']}。", '',
              '语义判断由运行该 skill 的 agent/editor 提供，未测量其 token、耗时或成本。', '',
              '反馈：使用 feedback 命令记录 accept/reject/defer/posted；只记录用户明确给出的事实。', '']
    return '\n'.join(lines)


def process(bundle, state, out, history=None, fixture=False, as_of=None):
    config = read(ROOT / 'assets/config.json')
    at = stamp(as_of or now())
    require(bundle.get('schema_version') == '1.0', 'unsupported schema_version')
    require(bundle.get('mode') == 'manual', 'v0.1 supports only manual input; discovery is not implemented')
    coverage = bundle.get('coverage', {})
    require(coverage.get('discovery') == 'not_implemented', 'cannot claim automated discovery')
    require(coverage.get('status') in ('blocked', 'partial', 'supplied_complete'), 'invalid coverage status')
    require(nonempty(coverage.get('window')), 'coverage.window is required')
    for k in ('success', 'failed'):
        require(isinstance(coverage.get(k), list) and all(nonempty(x) for x in coverage[k]), 'invalid coverage.' + k)
    require(coverage['status'] != 'supplied_complete' or not coverage['failed'], 'complete supplied scope cannot have failures')
    items = bundle.get('candidates')
    require(isinstance(items, list), 'candidates must be a list')
    require(len(items) <= config['max_input'], 'input budget exceeded; narrow the batch explicitly')
    require(len(items) <= config['max_reviewed'], 'deep-read budget exceeded; narrow the batch explicitly')
    normalized = [normalize(c) for c in items]
    require(all(c['synthetic'] == fixture for c in normalized), 'real/fixture flags do not match run mode')
    verdicts = [validate_review(c, at, config) for c in normalized]
    # Validate the entire batch before creating state or outputs.
    out = Path(out)
    require(not out.exists(), 'output directory already exists; choose a fresh run directory')
    db = connect(state, fixture)
    run_id = at.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:8]
    results, seen_ids, input_duplicates = [], set(), 0
    try:
        db.execute('BEGIN IMMEDIATE')
        seed_history(db, history)
        for c, (verdict, reasons) in zip(normalized, verdicts):
            if seen_ids.intersection(c['edit_ids']):
                input_duplicates += 1
                continue
            seen_ids.update(c['edit_ids'])
            matches = []
            for key in keys(c):
                matches += db.execute('SELECT key,post_id,kind,reference FROM dedup WHERE key=?', (key,)).fetchall()
            if matches and verdict != 'reject':
                exact = any(x[0].startswith('post:') for x in matches)
                # Only a new post carrying independently evidenced progress can bypass event/article repetition.
                if exact or not c['review'].get('material_update'):
                    verdict, reasons = 'hold', reasons + ['historical_duplicate']
            c.update(verdict=verdict, reason_codes=reasons, selected=False,
                     duplicate_matches=[dict(zip(('key','post_id','kind','reference'), m)) for m in matches])
            results.append(c)
        # Priority is an explicit semantic editor ordinal, never a keyword or random score.
        selected_keys, lanes, selected = set(), set(), 0
        for c in sorted(results, key=lambda c:(c['review']['priority'], c['post_id'])):
            if c['verdict'] != 'recommend':
                continue
            if selected_keys.intersection(keys(c)):
                c.update(verdict='hold', reason_codes=c['reason_codes'] + ['same_batch_event_duplicate'])
                continue
            if c['lane'] not in lanes and selected < config['max_recommendations']:
                c['selected'] = True
                selected_keys.update(keys(c))
                lanes.add(c['lane'])
                selected += 1
        count = lambda v: sum(c['verdict'] == v for c in results)
        status = ('discovery_blocked' if coverage['status'] == 'blocked' else
                  'partial_coverage' if coverage['status'] == 'partial' else
                  'manual_review_complete' if selected else 'manual_no_qualified_candidates')
        result = dict(run_id=run_id, as_of=at.isoformat(), fixture=fixture, mode='manual',
                      automatic_discovery=False, rules_version=config['rules_version'],
                      source_pool_version=config['source_pool_version'], coverage=coverage,
                      budget={k:config[k] for k in ('max_input','max_reviewed','max_recommendations')},
                      usage={'api_requests':0,'script_model_calls':0,'script_cost_usd':0,'agent_cost':'not_measured'},
                      summary=dict(status=status,input=len(items),input_duplicates=input_duplicates,
                                   reviewed=len(normalized),recommended=selected,hold=count('hold'),reject=count('reject'),
                                   alternates=count('recommend')-selected), candidates=results)
        digest = hashlib.sha256(json.dumps(bundle,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        db.execute('INSERT INTO runs VALUES (?,?,?,?,?)', (run_id,at.isoformat(),config['rules_version'],digest,json.dumps(result,ensure_ascii=False)))
        for c in results:
            db.execute('INSERT INTO decisions VALUES (?,?,?,?)', (run_id,c['post_id'],c['verdict'],json.dumps(c,ensure_ascii=False)))
            if c['selected']:
                for key in keys(c):
                    db.execute('INSERT OR IGNORE INTO dedup VALUES (?,?,?,?)',(key,c['post_id'],'recommended',run_id))
        out.mkdir(parents=True)
        write(out / 'result.json', result)
        (out / 'brief.md').write_text(brief(result),encoding='utf-8')
        with (out / 'candidates.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w = csv.writer(f)
            w.writerow(['post_id','url','author','lane','verdict','selected','reason_codes','summary_zh'])
            for c in results:
                # Prefix spreadsheet formula payloads without modifying canonical JSON.
                row = [c['post_id'],c['url'],c['author'],c['lane'],c['verdict'],c['selected'],
                       ';'.join(c['reason_codes']),c['review']['summary_zh']]
                w.writerow(["'"+x if isinstance(x,str) and x.startswith(('=','+','-','@','\t','\r')) else x for x in row])
        db.commit()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def feedback(state, fixture, pid, action, actor, reason, reference):
    require(isinstance(pid,str) and re.fullmatch(r'[1-9]\d{0,23}',pid), 'post ID must be a string')
    require(action in ('accept','reject','defer','posted'), 'invalid feedback action')
    require(nonempty(actor) and nonempty(reason), 'feedback needs named actor and explicit reason')
    require(nonempty(reference), 'feedback needs a source reference; never invent mentor approval')
    db = connect(state,fixture)
    try:
        row = db.execute('SELECT record FROM decisions WHERE post_id=? ORDER BY rowid DESC LIMIT 1',(pid,)).fetchone()
        require(row is not None,'unknown post; import/review it first')
        c = json.loads(row[0])
        with db:
            db.execute('INSERT INTO feedback VALUES (?,?,?,?,?,?,?)',
                       (uuid4().hex,pid,action,actor,reason,now(),reference))
            if action == 'posted':
                for key in keys(c):
                    db.execute('INSERT OR IGNORE INTO dedup VALUES (?,?,?,?)',(key,pid,'posted',reference))
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    p = sub.add_parser('prepare',help='Normalize raw records; do not make editorial judgments')
    p.add_argument('--input',required=True); p.add_argument('--output',required=True)
    p = sub.add_parser('run',help='Validate a reviewed bundle and export a manual shortlist')
    p.add_argument('--input',required=True); p.add_argument('--state',required=True); p.add_argument('--out',required=True)
    p.add_argument('--history'); p.add_argument('--fixture',action='store_true'); p.add_argument('--as-of')
    p = sub.add_parser('feedback',help='Record explicit human feedback without changing rules')
    for name in ('state','post-id','action','actor','reason','reference'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--fixture',action='store_true')
    sub.add_parser('preflight',help='Report implementation/access requirements; no credential scan/network')
    args = parser.parse_args()
    try:
        if args.command == 'preflight':
            print(json.dumps({'manual_mode':'implemented','automatic_discovery':False,'network_calls':0,
                              'credentials_examined':False,'missing':['authorized X data adapter/configuration',
                              'explicit trial spending cap'],'browser_history':'not probed by this command; consult dated access log'},indent=2))
        elif args.command == 'prepare':
            require(not Path(args.output).exists(),'output exists; refusing overwrite')
            bundle = read(args.input)
            bundle['candidates'] = [normalize(c) for c in bundle['candidates']]
            write(args.output,bundle)
            print('Normalized. Supply semantic reviews and reading evidence before run.')
        elif args.command == 'run':
            result = process(read(args.input),args.state,args.out,args.history,args.fixture,args.as_of)
            print(json.dumps(result['summary'],ensure_ascii=False))
        else:
            feedback(args.state,args.fixture,args.post_id,args.action,args.actor,args.reason,args.reference)
            print('Feedback recorded; approval and publication remain separate.')
    except (Invalid,ValueError,KeyError,TypeError,OSError,sqlite3.Error) as e:
        print('ERROR: '+str(e),file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
