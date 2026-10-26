"""Offline candidate queue and narrow history snapshot; no network or semantic scoring."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
from repost import require, nonempty, post_url, read, write


def plan(data):
    require(isinstance(data, dict), 'triage must be an object')
    queries = data.get('queries', [])
    require(isinstance(queries, list) and 4 <= len(queries) <= 6, 'record four to six actual queries')
    require(all(isinstance(q, dict) for q in queries), 'query records must be objects')
    for lane in ('Model', 'Other'):
        require(sum(q.get('lane') == lane and nonempty(q.get('query')) and nonempty(q.get('outcome'))
                    for q in queries) >= 2, 'reserve at least two actual queries per lane')
    items = data.get('candidates', [])
    require(isinstance(items, list) and len(items) <= 30, 'candidate limit is 30')
    seen, excluded, lanes = set(), [], {'Model': [], 'Other': []}
    for c in items:
        require(isinstance(c, dict), 'candidate must be an object')
        pid, url = post_url(c.get('url'))
        if pid in seen:
            continue
        seen.add(pid)
        require(c.get('lane') in lanes and nonempty(c.get('reason')), 'lane and triage reason required')
        require(c.get('value') in ('high', 'medium', 'low') and c.get('effort') in ('low', 'medium', 'high'),
                'supply editorial value and reading effort')
        require(c.get('action') in ('inspect', 'skip'), 'inspect or skip required')
        row = dict(c, post_id=pid, url=url)
        if c['action'] == 'skip' or c['value'] == 'low':
            excluded.append(row)
        else:
            lanes[c['lane']].append(row)
    for rows in lanes.values():
        rows.sort(key=lambda c: (c['effort'] == 'high', c['value'] != 'high',
                                {'low': 0, 'medium': 1, 'high': 2}[c['effort']]))
    queue = [lanes[lane][i] for i in range(2) for lane in ('Model', 'Other') if len(lanes[lane]) > i]
    return {'note': 'Based on agent triage declarations, not automated quality assessment.',
            'discovered': len(seen), 'queue': queue, 'excluded': excluded,
            'reserves': {lane: rows[2:] for lane, rows in lanes.items()},
            'lane_gaps': [lane for lane, rows in lanes.items() if len(rows) < 2]}


def snapshot(path):
    require(Path(path).is_file(), 'existing state required')
    with closing(sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)) as db:
        rows = db.execute('SELECT key,post_id,kind,reference FROM dedup ORDER BY key,post_id').fetchall()
    return {'dedup': [dict(zip(('key', 'post_id', 'kind', 'reference'), row)) for row in rows]}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('plan'); a.add_argument('--input', required=True); a.add_argument('--output', required=True)
    a = sub.add_parser('history'); a.add_argument('--state', required=True); a.add_argument('--output', required=True)
    args = p.parse_args(); target = Path(args.output)
    require(not target.exists(), 'choose a new output file')
    result = plan(read(args.input)) if args.command == 'plan' else snapshot(args.state)
    target.parent.mkdir(parents=True, exist_ok=True); write(target, result)
    print(json.dumps({'output': str(target), 'queued': len(result.get('queue', []))}))
