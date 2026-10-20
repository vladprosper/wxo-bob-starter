"""Exact comparison, including missing cases and failure semantics."""
from .contracts import FIELDS, validate_results


def evaluate(expected, actual):
    truth = {r['case_id']: r for r in validate_results(expected)}
    predictions = {r['case_id']: r for r in validate_results(actual)}
    differences = []
    matched = 0
    field_matches = 0
    for ident, want in truth.items():
        got = predictions.get(ident)
        if got is None:
            differences.append({'case_id': ident, 'path': 'case', 'reason': 'missing'})
            continue
        changes = []
        for field in FIELDS:
            if got['fields'][field] == want['fields'][field]:
                field_matches += 1
            else:
                changes.append({'case_id': ident, 'path': f'fields.{field}',
                                'expected': want['fields'][field], 'actual': got['fields'][field]})
        for key in ('status', 'issues'):
            if got[key] != want[key]:
                changes.append({'case_id': ident, 'path': key, 'expected': want[key], 'actual': got[key]})
        differences.extend(changes)
        matched += not changes
    for ident in predictions.keys() - truth.keys():
        differences.append({'case_id': ident, 'path': 'case', 'reason': 'unexpected'})
    return {'passed': not differences, 'expected_cases': len(truth), 'matched_cases': matched,
            'field_matches': field_matches, 'expected_fields': len(truth) * len(FIELDS),
            'differences': sorted(differences, key=lambda d: (d['case_id'], d['path']))}
