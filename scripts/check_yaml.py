"""Development-only syntax/shape check using PyYAML, not Bob runtime validation."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class UniqueLoader(yaml.SafeLoader):
    pass


def mapping(loader, node):
    pairs = loader.construct_pairs(node, deep=True)
    result = {}
    for key, val in pairs:
        if key in result:
            raise ValueError('Duplicate YAML key')
        result[key] = val
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def validate_mode(text):
    value = yaml.load(text, Loader=UniqueLoader)
    if not isinstance(value, dict) or set(value) != {'customModes'}:
        raise ValueError('customModes root required')
    modes = value['customModes']
    if not isinstance(modes, list) or not modes:
        raise ValueError('Nonempty modes required')
    seen = set()
    for mode in modes:
        if not isinstance(mode, dict) or not {'slug','name','roleDefinition','groups'} <= set(mode):
            raise ValueError('Required mode fields missing')
        slug = mode['slug']
        if not isinstance(slug,str) or not slug or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slug) or slug in seen:
            raise ValueError('Invalid or duplicate slug')
        seen.add(slug)
        groups = mode['groups']
        if not isinstance(groups,list) or not groups or any(x not in ['read','edit','execute','mcp','skill','todo'] for x in groups):
            raise ValueError('Unsupported group for this starter')
    return value


def check():
    validate_mode((ROOT/'starter/.bob/custom_modes.yaml').read_text(encoding='utf-8'))
    doc = (ROOT/'starter/.bob/skills/wxo-agent-architect/SKILL.md').read_text(encoding='utf-8')
    assert doc.startswith('---\n')
    meta = yaml.load(doc.split('---',2)[1],Loader=UniqueLoader)
    assert meta['name']=='wxo-agent-architect' and isinstance(meta['description'],str) and meta['description']
    original = (ROOT/'starter/.bob/custom_modes.yaml').read_text(encoding='utf-8')
    for bad in ['customModes: []', original.replace('- todo','- invented'), original+'\ncustomModes: []\n']:
        try: validate_mode(bad)
        except (ValueError,yaml.YAMLError): pass
        else: raise AssertionError('Invalid mode accepted')
    print('Mode/front matter syntax and negative mutations passed; live Bob acceptance remains unverified.')


if __name__=='__main__':
    check()
