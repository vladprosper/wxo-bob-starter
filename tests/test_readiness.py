import copy
import unittest
from pathlib import Path
from wxo_starter.contracts import Invalid, load
from wxo_starter.readiness import diagnose

ROOT = Path(__file__).resolve().parents[1]
NOW = '2026-10-20T12:30:00Z'

class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = load(ROOT / 'examples/readiness/ready.synthetic.json')

    def test_init_exit_zero_is_success(self):
        self.assertEqual(diagnose(self.snapshot, NOW)['status'], 'passed')

    def test_restart_growth_fails(self):
        self.snapshot['services'][1]['restarts_after'] = 3
        self.assertEqual(diagnose(self.snapshot, NOW)['status'], 'failed')

    def test_extraction_not_implied_by_health(self):
        self.snapshot['checks']['extraction'] = 'unverified'
        self.assertEqual(diagnose(self.snapshot, NOW)['status'], 'unverified')

    def test_old_snapshot_not_passed(self):
        self.assertEqual(diagnose(self.snapshot, '2026-10-22T12:00:00Z')['status'], 'unverified')

    def test_unknown_health_or_restart_evidence(self):
        for key, value in [('health','none'), ('restarts_before',None)]:
            sample=copy.deepcopy(self.snapshot);sample['services'][1][key]=value
            self.assertEqual(diagnose(sample,NOW)['status'],'unverified')

    def test_target_mismatch(self):
        self.snapshot['target']['observed']='remote'
        self.assertEqual(diagnose(self.snapshot,NOW)['status'],'failed')

    def test_missing_target(self):
        self.snapshot['target']['observed']=None
        self.assertEqual(diagnose(self.snapshot,NOW)['status'],'unverified')

    def test_init_failure(self):
        self.snapshot['services'][0]['exit_code']=1
        self.assertEqual(diagnose(self.snapshot,NOW)['status'],'failed')

    def test_empty_services_not_passed(self):
        self.snapshot['services']=[]
        self.assertEqual(diagnose(self.snapshot,NOW)['status'],'unverified')

    def test_invalid_snapshots(self):
        mutations=[lambda x:x.update(observed_at='2026-10-21T12:00:00Z'),
                   lambda x:x.update(observed_at='2026-10-20'),
                   lambda x:x['services'][0].update(exit_code=True),
                   lambda x:x['services'][1].update(restarts_after=1),
                   lambda x:x['services'].append(copy.deepcopy(x['services'][0])),
                   lambda x:x['checks'].update(extraction=True),
                   lambda x:x.update(credentials='must not be accepted')]
        for mutate in mutations:
            sample=copy.deepcopy(self.snapshot);mutate(sample)
            with self.subTest(mutation=mutate), self.assertRaises(Invalid): diagnose(sample,NOW)
