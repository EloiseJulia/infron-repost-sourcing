import tempfile
from contextlib import closing
from pathlib import Path
import sqlite3
import unittest
from sourcing_plan import plan, snapshot
from repost import Invalid


def sample():
    return {'queries': [{'lane': lane, 'query': str(i), 'outcome': 'synthetic results'}
                        for lane in ('Model', 'Other') for i in range(2)],
            'candidates': [{'url': f'https://x.com/fixture/status/{900000000000000000+i}',
                            'lane': lane, 'reason': 'synthetic useful item', 'value': 'high',
                            'effort': effort, 'action': 'inspect'}
                           for i, (lane, effort) in enumerate([('Other', 'high'), ('Other', 'low'),
                               ('Other', 'medium'), ('Model', 'low'), ('Model', 'medium')], 1)]}


class Planning(unittest.TestCase):
    def test_both_lanes_before_deep_dive(self):
        r = plan(sample())
        self.assertEqual([c['lane'] for c in r['queue']], ['Model', 'Other', 'Model', 'Other'])
        self.assertNotIn('high', [c['effort'] for c in r['queue']])

    def test_unbalanced_search_rejected(self):
        b = sample(); b['queries'][0]['lane'] = 'Other'
        with self.assertRaises(Invalid): plan(b)

    def test_duplicates_and_exclusions(self):
        b = sample(); b['candidates'] += b['candidates'][:1]; b['candidates'][1]['action'] = 'skip'
        r = plan(b); self.assertEqual(r['discovered'], 5); self.assertEqual(len(r['excluded']), 1)

    def test_gap_not_fabricated(self):
        b = sample(); b['candidates'] = [c for c in b['candidates'] if c['lane'] == 'Other']
        self.assertIn('Model', plan(b)['lane_gaps'])

    def test_history_does_not_read_prior_reviews(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            p = Path(tmp) / 'state.db'
            with closing(sqlite3.connect(p)) as db:
                db.execute('create table dedup (key,post_id,kind,reference)')
                db.execute("insert into dedup values ('event:a','1','recommended','run')")
                db.execute('create table decisions (payload)')
                db.execute("insert into decisions values ('old review payload')")
                db.commit()
            r = snapshot(p); self.assertEqual(len(r['dedup']), 1)
            self.assertNotIn('old review', str(r))


if __name__ == '__main__': unittest.main(verbosity=2)
