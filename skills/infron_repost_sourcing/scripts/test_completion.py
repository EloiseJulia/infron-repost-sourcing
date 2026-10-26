"""Synthetic process-integrity tests; no external reading is implied."""
import copy
import unittest
from pathlib import Path
import tempfile
import repost as r
from test_repost import candidate, bundle, AT


def ready():
    c=candidate()
    c['completion']={'state':'ready','note':'synthetic completion', 'checks':{
        p:{'disposition':'resolved' if p=='text' else 'not_present',
           'attempts':[{'method':'fixture','locator':'synthetic:text','outcome':'read stipulated text'}] if p=='text' else []}
        for p in r.PARTS}}
    return c


class Completion(unittest.TestCase):
    def test_batch_enforcement_and_deferred_export(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            path=Path(tmp); c=ready(); b=bundle(c); b['review_process_version']=1
            c['completion']['state']='blocked'
            with self.assertRaises(r.Invalid): r.process(b,path/'bad.db',path/'bad',fixture=True,as_of=AT)
            self.assertFalse((path/'bad.db').exists())
            c['completion']['state']='deferred'; c['review']['decision']='hold'
            c['completion']['checks']['text']['disposition']='pending'
            c['evidence']['text']['status']='partial'
            result=r.process(b,path/'ok.db',path/'ok',fixture=True,as_of=AT)
            self.assertTrue(result['completion_enforced'])
            self.assertEqual(result['summary']['status'],'review_incomplete')
            self.assertEqual(result['summary']['hold'],0)
            self.assertEqual(result['summary']['deferred'],1)
            self.assertIn('deferred（未完成）',(path/'ok/brief.md').read_text())

    def test_ready(self):
        r.validate_completion(ready())

    def test_missing_ledger(self):
        with self.assertRaises(r.Invalid): r.validate_completion(candidate())

    def test_pending_is_not_completed_hold(self):
        c=ready(); c['review']['decision']='hold'
        c['evidence']['text']['status']='partial'
        c['completion']['checks']['text']['disposition']='pending'
        with self.assertRaises(r.Invalid): r.validate_completion(c)
        c['completion']['state']='deferred'; r.validate_completion(c)

    def test_one_failed_method_needs_followup(self):
        c=ready(); c['review']['decision']='hold'; c['completion']['state']='blocked'
        c['evidence']['text']['status']='partial'
        x=c['completion']['checks']['text']; x.update(disposition='blocked',blocker='access_failed')
        with self.assertRaises(r.Invalid): r.validate_completion(c)
        x['attempts'].append({'method':'browser','locator':'synthetic:url','outcome':'also failed'})
        r.validate_completion(c)

    def test_hard_barrier_and_budget(self):
        c=ready(); c['review']['decision']='hold'; c['completion']['state']='blocked'
        c['evidence']['text']['status']='partial'
        x=c['completion']['checks']['text']; x.update(disposition='blocked',blocker='authentication')
        r.validate_completion(c)
        x['blocker']='budget_exhausted'
        with self.assertRaises(r.Invalid): r.validate_completion(c)
        c['completion']['state']='deferred'; r.validate_completion(c)

    def test_no_false_absence_or_early_recommendation(self):
        c=ready(); c['completion']['checks']['text']['disposition']='not_present'
        with self.assertRaises(r.Invalid): r.validate_completion(c)
        c=ready(); c['completion'].update(state='early_exit',early_exit={'reason':'stale','reference':'synthetic:old-date'})
        with self.assertRaises(r.Invalid): r.validate_completion(c)
        c['review']['decision']='hold'; r.validate_completion(c)


if __name__=='__main__': unittest.main(verbosity=2)
