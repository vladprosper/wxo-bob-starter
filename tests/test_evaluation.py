import copy
import json
import tempfile
import unittest
from pathlib import Path
from wxo_starter.contracts import Invalid, load, validate_results
from wxo_starter.evaluate import evaluate

ROOT = Path(__file__).resolve().parents[1]

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.good = load(ROOT / 'examples/extraction/expected.json')
        self.actual = copy.deepcopy(self.good)

    def test_exact_match(self):
        result = evaluate(self.good, self.actual)
        self.assertTrue(result['passed'])
        self.assertEqual((result['matched_cases'], result['field_matches']), (6, 36))

    def test_wrong_amount_and_identifier_detected(self):
        bad = load(ROOT / 'examples/extraction/predictions-bad.synthetic.json')
        result = evaluate(self.good, bad)
        self.assertFalse(result['passed'])
        self.assertEqual((result['matched_cases'], len(result['differences'])), (3, 3))

    def test_missing_and_unexpected_cases_fail(self):
        self.actual['results'][0]['case_id'] = 'unexpected'
        result = evaluate(self.good, self.actual)
        self.assertEqual({x['reason'] for x in result['differences']}, {'missing', 'unexpected'})
        self.assertEqual(result['expected_fields'], 36)

    def test_order_irrelevant(self):
        self.actual['results'].reverse()
        self.assertTrue(evaluate(self.good, self.actual)['passed'])

    def test_issue_semantics_count(self):
        self.actual['results'][2]['issues']['due_date'] = 'ambiguous'
        self.assertFalse(evaluate(self.good, self.actual)['passed'])

    def test_invalid_contracts(self):
        mutations = [
            lambda x: x.update(schema_version=True),
            lambda x: x.update(results=[]),
            lambda x: x['results'].append(copy.deepcopy(x['results'][0])),
            lambda x: x['results'][0]['fields'].update(document_id=42),
            lambda x: x['results'][0]['fields'].update(total_amount_due=28.09),
            lambda x: x['results'][0]['fields'].update(total_amount_due='NaN'),
            lambda x: x['results'][0]['fields'].update(total_amount_due='1.٢٣'),
            lambda x: x['results'][0]['fields'].update(total_amount_due='-1.00'),
            lambda x: x['results'][0]['fields'].update(statement_date='2026-02-30'),
            lambda x: x['results'][0]['fields'].update(currency='usd'),
            lambda x: x['results'][0]['fields'].update(total_amount_due=None),
            lambda x: x['results'][2]['issues'].clear(),
            lambda x: x['results'][5]['fields'].update(client_name='fabricated'),
            lambda x: x['results'][0].update(extra='unknown'),
            lambda x: x['results'][0].update(case_id='../escape'),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                sample = copy.deepcopy(self.good); mutate(sample)
                with self.assertRaises(Invalid): validate_results(sample)

    def test_strict_json_loading(self):
        for content in [b'{"x":1,"x":2}', b'[NaN]', b'\xff', b'[' * 2000, b'1' * 5000, b'x' * 2_000_001]:
            with self.subTest(content=content[:20]), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'input.json'; path.write_bytes(content)
                with self.assertRaises(Invalid): load(path)

    def test_wrong_expected_file_also_rejected(self):
        self.good['results'][0]['status'] = 'made-up'
        with self.assertRaises(Invalid): evaluate(self.good, self.actual)

    def test_null_distinct_from_zero(self):
        row = self.actual['results'][1]
        row['status'] = 'partial'
        row['fields']['total_amount_due'] = None
        row['issues'] = {'total_amount_due':'missing'}
        result = evaluate(self.good, self.actual)
        self.assertEqual(len(result['differences']), 3)
