"""Stage a template into a new directory, without merging existing Bob settings."""
import shutil
from pathlib import Path
from .contracts import Invalid

ROOT = Path(__file__).resolve().parents[1]


def stage(destination):
    target = Path(destination)
    if target.exists() or target.is_symlink():
        raise Invalid('Destination already exists; staging never merges or overwrites')
    if not target.parent.is_dir():
        raise Invalid('Destination parent must exist')
    # mkdir is exclusive: another process winning the race cannot be overwritten.
    target.mkdir()
    try:
        shutil.copytree(ROOT / 'starter', target, dirs_exist_ok=True)
        (target / 'docs').mkdir()
        for name in ('BOB_ACCEPTANCE.md', 'OUTPUT_CONTRACT.md'):
            shutil.copyfile(ROOT / 'docs' / name, target / 'docs' / name)
        shutil.copytree(ROOT / 'prompts', target / 'prompts')
        for name in ('LICENSE', 'NOTICE.md', 'PROVENANCE.md'):
            shutil.copyfile(ROOT / name, target / name)
    except Exception:
        # Leave partial output for inspection. Never recursively delete a destination.
        raise
    return {'staged': str(target), 'live_verified': False,
            'next': 'Fill wxo-project.md and follow prompts/README.md in Bob; record docs/BOB_ACCEPTANCE.md.'}
