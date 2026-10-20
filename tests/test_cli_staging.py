import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from wxo_starter.contracts import Invalid
from wxo_starter.staging import stage

ROOT = Path(__file__).resolve().parents[1]

class CliTests(unittest.TestCase):
    def run_cli(self,*args):
        return subprocess.run([sys.executable,'-m','wxo_starter',*map(str,args)],cwd=ROOT,capture_output=True,text=True)

    def test_cli_exits(self):
        for actual, code in [('predictions-good.synthetic.json',0),('predictions-bad.synthetic.json',1),('missing.json',2)]:
            r=self.run_cli('evaluate','--expected','examples/extraction/expected.json','--actual','examples/extraction/'+actual)
            self.assertEqual(r.returncode,code,r.stderr)
            json.loads(r.stdout if code!=2 else r.stderr)
            self.assertNotIn('Traceback',r.stderr)

    def test_readiness_exit(self):
        for name,code in [('ready.synthetic.json',0),('restart.synthetic.json',1)]:
            r=self.run_cli('readiness','examples/readiness/'+name,'--as-of','2026-10-20T12:30:00Z')
            self.assertEqual(r.returncode,code,r.stderr)

    def test_stage_preserves_existing(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'new'
            stage(target)
            self.assertTrue((target/'.bob/skills/wxo-agent-architect/SKILL.md').is_file())
            before={str(p.relative_to(target)):p.read_bytes() for p in target.rglob('*') if p.is_file()}
            with self.assertRaises(Invalid): stage(target)
            self.assertEqual(before,{str(p.relative_to(target)):p.read_bytes() for p in target.rglob('*') if p.is_file()})
            self.assertFalse((target/'.bob/mcp.json').exists())
            self.assertFalse((target/'wxo-project.md').exists())

    def test_missing_parent_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(Invalid):stage(Path(d)/'absent'/'new')

    def test_symlink_destination_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            link=Path(d)/'link'
            try: link.symlink_to(Path(d)/'absent',target_is_directory=True)
            except OSError: self.skipTest('Symlinks unavailable')
            with self.assertRaises(Invalid):stage(link)

    def test_wrong_json_type_is_clean_error(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'bad.json';path.write_text('null')
            r=self.run_cli('evaluate','--expected','examples/extraction/expected.json','--actual',path)
            self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
