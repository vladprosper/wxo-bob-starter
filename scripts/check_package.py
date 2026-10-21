"""Check shipped files and links without network access or runtime imports."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def check():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    for name, digest in manifest.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f'Changed reviewed asset: {name}'
    for doc in [ROOT/'README.md', ROOT/'PROVENANCE.md', *ROOT.glob('docs/*.md'), *ROOT.glob('prompts/*.md'), *ROOT.glob('starter/**/*.md')]:
        content = doc.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in link or link.startswith('#'):
                continue
            assert (doc.parent / unquote(link.split('#')[0])).exists(), f'Broken link in {doc.name}: {link}'
    expected = json.loads((ROOT/'examples/extraction/expected.json').read_text(encoding='utf-8'))
    ids = {x['case_id'] for x in expected['results']}
    for suffix in ('txt','pdf'):
        assert {p.stem for p in (ROOT/'examples/extraction/documents').glob('*.'+suffix)} == ids
    for path in [*ROOT.glob('wxo_starter/*.py'), *ROOT.glob('starter/**/*.md'), *ROOT.glob('starter/**/*.yaml')]:
        content = path.read_text(encoding='utf-8')
        assert '/Users/' not in content and '/home/' not in content, f'Personal path in {path.name}'
    print(f'Package checks passed; {len(manifest)} reviewed assets match; document coverage and local links resolve.')


if __name__ == '__main__':
    check()
