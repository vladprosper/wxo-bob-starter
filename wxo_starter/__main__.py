"""CLI: JSON stdout; malformed input exit 2, check failures exit 1."""
import argparse
import json
import sys
from datetime import datetime, timezone
from .contracts import Invalid, load
from .evaluate import evaluate
from .readiness import diagnose
from .staging import stage


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    compare = sub.add_parser('evaluate', help='Compare supplied extraction JSON; no model calls')
    compare.add_argument('--expected', required=True)
    compare.add_argument('--actual', required=True)
    doctor = sub.add_parser('readiness', help='Interpret a supplied snapshot; no live inspection')
    doctor.add_argument('snapshot')
    doctor.add_argument('--as-of', default=None, help='Timezone-bearing ISO time; defaults to current UTC')
    template = sub.add_parser('stage', help='Copy starter files into a NEW project directory')
    template.add_argument('destination')
    args = parser.parse_args(argv)
    try:
        if args.command == 'evaluate':
            result = evaluate(load(args.expected), load(args.actual))
            code = 0 if result['passed'] else 1
        elif args.command == 'readiness':
            result = diagnose(load(args.snapshot), args.as_of or datetime.now(timezone.utc).isoformat())
            code = 0 if result['status'] == 'passed' else 1
        else:
            result, code = stage(args.destination), 0
    except (Invalid, OSError) as exc:
        # Do not echo arbitrary file contents or raw platform exception messages.
        message = str(exc) if isinstance(exc, Invalid) else f'File operation failed ({type(exc).__name__})'
        print(json.dumps({'error': message}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
