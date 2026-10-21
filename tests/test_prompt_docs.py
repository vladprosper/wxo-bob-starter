"""Offline documentation/staging checks, not Bob or model acceptance."""
import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote
from wxo_starter.staging import stage
from wxo_starter.contracts import FIELDS, validate_results

ROOT = Path(__file__).resolve().parents[1]

class PromptDocsTests(unittest.TestCase):
    def test_six_steps_have_operational_guidance(self):
        steps = sorted((ROOT/'prompts').glob('[0-9][0-9]-*.md'))
        self.assertEqual(len(steps), 6)
        for path in steps:
            content = path.read_text(encoding='utf-8')
            for required in ('**Use when:**', '**Inputs:**', '**Run in:**',
                             '```text', '**Expected artifacts:**', '**Review gate:**',
                             '**Stop if:**', 'For example,'):
                self.assertIn(required, content, str(path))

    def test_staged_guides_resolve_without_answer_material(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/'project'
            result = stage(target)
            self.assertFalse(result['live_verified'])
            self.assertEqual((target/'docs/OUTPUT_CONTRACT.md').read_bytes(),
                             (ROOT/'docs/OUTPUT_CONTRACT.md').read_bytes())
            self.assertEqual(len(list((target/'prompts').glob('*.md'))), 9)
            for source in (ROOT/'prompts').glob('*.md'):
                self.assertEqual(source.read_bytes(), (target/'prompts'/source.name).read_bytes())
            for path in [*target.glob('prompts/*.md'), *target.glob('docs/*.md')]:
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                    if '://' not in link and not link.startswith('#'):
                        self.assertTrue((path.parent/unquote(link.split('#')[0])).exists(), (path,link))
            for name in ('examples', 'docs/EVALUATION.md', 'output', '.git'):
                self.assertFalse((target/name).exists(), name)
            self.assertFalse(list(target.rglob('expected.json')))
            self.assertFalse(list(target.rglob('predictions-*.json')))

    def test_clean_contract_excludes_fixture_specific_values(self):
        content = (ROOT/'docs/OUTPUT_CONTRACT.md').read_text(encoding='utf-8')
        rows = json.loads((ROOT/'examples/extraction/expected.json').read_text())['results']
        for row in rows:
            if row['case_id'] != 'unsupported':  # also a required issue-code keyword
                self.assertNotIn(row['case_id'], content)
            for field in ('document_id', 'client_name', 'statement_date', 'due_date'):
                value = row['fields'][field]
                if value: self.assertNotIn(value, content)
        for field in FIELDS: self.assertIn(field, content)
        self.assertNotIn('28.09', content)
        self.assertNotIn('31.25', content)
        # Guard against an accidental answer-key dump, not a security proof.

    def test_contract_examples_match_validator(self):
        content = (ROOT/'docs/OUTPUT_CONTRACT.md').read_text(encoding='utf-8')
        examples = re.findall(r'```json\n(.*?)```', content, re.S)
        self.assertTrue(examples)
        for example in examples: validate_results(json.loads(example))
        # Construct non-fixture examples for the documented status semantics.
        fields = dict(zip(FIELDS, ['demo-004', 'Example Training Client',
                                 '2026-02-01', '2026-03-01', '9.50', 'USD']))
        success = {'case_id':'demo','status':'success','fields':fields,'issues':{}}
        validate_results({'schema_version':1,'results':[success]})
        partial = dict(success, status='partial', fields=dict(fields, due_date=None),
                       issues={'due_date':'missing'})
        validate_results({'schema_version':1,'results':[partial]})
        failed = dict(success, status='failed', fields=dict.fromkeys(FIELDS),
                      issues={'document':'unsupported'})
        validate_results({'schema_version':1,'results':[failed]})
