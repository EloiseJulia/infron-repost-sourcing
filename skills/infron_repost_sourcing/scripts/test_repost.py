"""Behavior tests use only explicitly synthetic cases; no network or real approvals."""
import copy
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import repost as r

AT = '2026-10-26T15:00:00+08:00'


def candidate(pid='900000000000000001', lane='Model'):
    return {
        'url':'https://twitter.com/testauthor/status/'+pid+'?s=20', 'author':'@testauthor',
        'synthetic':True, 'lane':lane, 'post_type':'original', 'published_at':'2026-10-26T12:00:00+08:00',
        'event_key':'fixture:release:'+pid,'article_urls':[],'edit_ids':[],
        'evidence':{p:{'presence':'yes' if p=='text' else 'no',
                       'status':'full' if p=='text' else 'not_present',
                       'note':'Explicit synthetic material; no real post was fetched.',
                       'locator':'synthetic:test:'+pid if p=='text' else ''} for p in r.PARTS},
        'review':{'reviewer':'test-fixture-editor','checked_at':AT,'summary_zh':'合成样例：模型的可复现实测。',
                  'why_now':'Fixture reports a new release today.','brand_reason':'Model comparison, no platform promotion.',
                  'fact_reason':'All statements are explicitly supplied synthetic facts.',
                  'identity_reason':'Synthetic author stipulated by test case.',
                  'reason':'Useful new comparison with full stipulated evidence.',
                  'novelty_reason':'New fixture release.', 'decision':'recommend','identity':'verified',
                  'facts':'verified','brand':'acceptable','action':'pure_repost','priority':1,
                  'quality':{d:{'level':'high','reason':'Explicit synthetic evidence for '+d} for d in r.DIMENSIONS},
                  'entities':[{'name':'Model A','role':'model','behavior':'comparison','evidence':'synthetic:test'}],
                  'claims':[{'claim':'Fixture release includes reproducible setup.','status':'verified','evidence':'synthetic:test'}]}}


def bundle(*items, status='supplied_complete'):
    return {'schema_version':'1.0','mode':'manual',
            'coverage':{'discovery':'not_implemented','status':status,'window':'synthetic batch 2026-10-26',
                        'success':['synthetic fixture inputs'],'failed':['login-gated fixture source'] if status!='supplied_complete' else []},
            'candidates':list(items)}


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='repost-test-', dir=Path.cwd())
        self.base = Path(self.tmp.name)
        self.state = self.base/'fixture.sqlite'
        self.number = 0

    def tearDown(self):
        self.assertEqual(self.base.resolve().parent, Path.cwd().resolve())
        self.tmp.cleanup()

    def run_bundle(self, data, **kwargs):
        self.number += 1
        return r.process(data,self.state,self.base/str(self.number),fixture=True,as_of=AT,**kwargs)

    def test_normalization_and_bad_ids(self):
        c = r.normalize(candidate())
        self.assertEqual(c['post_id'],'900000000000000001')
        self.assertEqual(c['url'],'https://x.com/i/web/status/900000000000000001')
        self.assertEqual(r.article_url('https://Example.org/a?v=2&utm_source=x#z'),'https://example.org/a?v=2')
        for url in ('https://x.com.evil.test/u/status/1','https://x.com/home','javascript:alert(1)'):
            with self.assertRaises(r.Invalid): r.post_url(url)
        c = candidate(); c['post_id'] = 900000000000000001
        with self.assertRaises(r.Invalid): r.normalize(c)
        c = candidate(); c['author'] = '@another'
        with self.assertRaises(r.Invalid): r.normalize(c)

    def test_incomplete_evidence_is_held(self):
        for part in ('media','quote','links'):
            c = candidate()
            c['evidence'][part]={'presence':'yes','status':'unavailable','note':'Cannot read core material.'}
            out = self.run_bundle(bundle(c))
            self.assertEqual(out['candidates'][0]['verdict'],'hold')
            self.assertIn('incomplete_evidence',out['candidates'][0]['reason_codes'])

    def test_unknown_presence_cannot_pass(self):
        c=candidate(); c['evidence']['media']={'presence':'unknown','status':'unavailable','note':'Preview cannot establish absence.'}
        self.assertEqual(self.run_bundle(bundle(c))['summary']['recommended'],0)

    def test_malformed_evidence_and_evergreen(self):
        c=candidate(); c['evidence']['extra']='not an evidence object'
        with self.assertRaises(r.Invalid): self.run_bundle(bundle(c))
        c=candidate(); c['review']['evergreen_reason']=True
        with self.assertRaises(r.Invalid): self.run_bundle(bundle(c))

    def test_semantic_competitor_boundary(self):
        ranking=candidate(); ranking['review']['entities'].append({'name':'Model B','role':'model','behavior':'ranked comparison','evidence':'synthetic:chart'})
        self.assertEqual(self.run_bundle(bundle(ranking))['summary']['recommended'],1)
        promo=candidate('900000000000000002')
        promo['review']['brand']='overlap_promotion'
        promo['review']['brand_reason']='Image invites signup to an overlapping inference aggregator.'
        self.assertEqual(self.run_bundle(bundle(promo))['candidates'][0]['verdict'],'reject')

    def test_cross_run_and_edit_dedup(self):
        c=candidate()
        self.assertEqual(self.run_bundle(bundle(c))['summary']['recommended'],1)
        out=self.run_bundle(bundle(c))
        self.assertIn('historical_duplicate',out['candidates'][0]['reason_codes'])
        edit=candidate('900000000000000009'); edit['edit_ids']=[c['url'].split('/')[-1].split('?')[0]]
        self.assertEqual(self.run_bundle(bundle(edit))['summary']['recommended'],0)

    def test_article_and_material_update(self):
        a=candidate(); a['article_urls']=['https://example.org/release?v=1&utm_source=x']
        a['evidence']['links']={'presence':'yes','status':'full','note':'Synthetic full article.','locator':'synthetic:article'}
        self.run_bundle(bundle(a))
        b=copy.deepcopy(a); b['url']='https://x.com/testauthor/status/900000000000000010'; b['event_key']='fixture:another-event'
        b['article_urls']=['https://example.org/release?v=1&utm_source=y']
        self.assertEqual(self.run_bundle(bundle(b))['summary']['recommended'],0)
        b['review'].update(material_update=True,previous_reference=a['url'],update_evidence='Synthetic new measured revision in the article.')
        self.assertEqual(self.run_bundle(bundle(b))['summary']['recommended'],1)

    def test_two_slots_and_same_event(self):
        a=candidate(); b=candidate('900000000000000002'); b['event_key']=a['event_key']
        c=candidate('900000000000000003','Other')
        out=self.run_bundle(bundle(a,b,c))
        self.assertEqual(out['summary']['recommended'],2)
        self.assertEqual(out['summary']['hold'],1)
        self.assertIn('same_batch_event_duplicate',out['candidates'][1]['reason_codes'])

    def test_held_item_can_be_rechecked(self):
        c=candidate(); c['review']['facts']='unknown'
        self.assertEqual(self.run_bundle(bundle(c))['summary']['recommended'],0)
        c['review']['facts']='verified'
        self.assertEqual(self.run_bundle(bundle(c))['summary']['recommended'],1)

    def test_coverage_failure_vs_empty_scope(self):
        self.assertEqual(self.run_bundle(bundle(status='blocked'))['summary']['status'],'discovery_blocked')
        self.assertEqual(self.run_bundle(bundle(status='partial'))['summary']['status'],'partial_coverage')
        self.assertEqual(self.run_bundle(bundle())['summary']['status'],'manual_no_qualified_candidates')

    def test_feedback_accept_is_not_posted(self):
        self.run_bundle(bundle(candidate()))
        r.feedback(self.state,True,'900000000000000001','accept','synthetic human','Synthetic acceptance only','synthetic:feedback')
        with closing(sqlite3.connect(self.state)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM dedup WHERE kind='posted'").fetchone()[0],0)
        r.feedback(self.state,True,'900000000000000001','posted','synthetic human','Synthetic actual sharing','synthetic:publication')
        with closing(sqlite3.connect(self.state)) as db:
            self.assertGreater(db.execute("SELECT COUNT(*) FROM dedup WHERE kind='posted'").fetchone()[0],0)

    def test_atomic_validation_and_no_overwrite(self):
        c=candidate(); bad=candidate('900000000000000002'); del bad['review']['quality']
        with self.assertRaises(r.Invalid): self.run_bundle(bundle(c,bad))
        self.assertFalse(self.state.exists())
        self.run_bundle(bundle(c))
        with self.assertRaises(r.Invalid):
            r.process(bundle(c),self.state,self.base/'2',fixture=True,as_of=AT)

    def test_fixture_real_isolation(self):
        c=candidate()
        with self.assertRaises(r.Invalid): r.process(bundle(c),self.state,self.base/'real',as_of=AT)
        self.run_bundle(bundle(c))
        with self.assertRaises(r.Invalid): r.connect(self.state,False)

    def test_budget_stale_and_unknown_facts(self):
        with self.assertRaises(r.Invalid): self.run_bundle(bundle(*[candidate(str(900000000000000001+i)) for i in range(21)]))
        c=candidate(); c['review']['checked_at']='2026-10-23T12:00:00+08:00'
        self.assertIn('review_stale',self.run_bundle(bundle(c))['candidates'][0]['reason_codes'])
        c=candidate('900000000000000002'); c['review']['claims'][0]['status']='unknown'
        self.assertIn('facts_unverified',self.run_bundle(bundle(c))['candidates'][0]['reason_codes'])

    def test_exports_and_input_duplicates(self):
        c=candidate(); c['review']['summary_zh']='=SYNTHETIC_FORMULA'
        out=self.run_bundle(bundle(c,c))
        self.assertEqual(out['summary']['input_duplicates'],1)
        folder=self.base/'1'
        self.assertEqual(json.loads((folder/'result.json').read_text('utf-8'))['summary']['recommended'],1)
        self.assertIn('SYNTHETIC FIXTURE',(folder/'brief.md').read_text('utf-8'))
        self.assertIn("'=SYNTHETIC_FORMULA",(folder/'candidates.csv').read_text('utf-8-sig'))

    def test_history_seed_without_invented_action(self):
        c=candidate(); seed=self.base/'history.json'
        r.write(seed,[{'url':c['url'],'evidence_url':'https://x.com/InfronAI/status/900000000000000099',
                      'action':'quote','relationship_verified':True,'event_key':c['event_key']}])
        out=self.run_bundle(bundle(c),history=seed)
        self.assertEqual(out['summary']['recommended'],0)
        self.assertEqual(out['candidates'][0]['duplicate_matches'][0]['kind'],'history')

    def test_pure_repost_profile_proof(self):
        c=candidate(); seed=self.base/'repost-history.json'
        r.write(seed,[{'url':c['url'],'evidence_url':'https://x.com/InfronAI/reposts',
                      'action':'repost','relationship_verified':True,'event_key':c['event_key']}])
        out=self.run_bundle(bundle(c),history=seed)
        self.assertEqual(out['summary']['recommended'],0)
        self.assertEqual(out['candidates'][0]['duplicate_matches'][0]['reference'],'https://x.com/InfronAI/reposts')


if __name__=='__main__':
    unittest.main(verbosity=2)
