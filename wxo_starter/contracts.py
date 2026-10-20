"""Strict, bounded JSON input and extraction contract version 1."""
import json
import re
from datetime import date
from pathlib import Path

MAX_BYTES = 2_000_000
FIELDS = ('document_id', 'client_name', 'statement_date', 'due_date', 'total_amount_due', 'currency')
ISSUES = {'missing', 'ambiguous', 'unreadable', 'unsupported'}


class Invalid(ValueError):
    """A malformed input, distinct from a valid but incorrect prediction."""


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid('Duplicate JSON key')
        result[key] = value
    return result


def load(path):
    with Path(path).open('rb') as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise Invalid('Input exceeds 2 MB limit')
    try:
        return json.loads(data.decode('utf-8'), object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(Invalid('Non-finite JSON number')))
    except Invalid:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise Invalid('Input must be UTF-8 JSON with bounded nesting') from exc


def keys(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise Invalid(f'{label}: exact keys required: {", ".join(required)}')


def text(value, label, limit=200):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Invalid(f'{label}: nonempty string up to {limit} characters required')


def validate_results(value):
    keys(value, ('schema_version', 'results'), 'result file')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise Invalid('Unsupported schema_version')
    rows = value['results']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 1000:
        raise Invalid('results: 1 to 1000 entries required')
    seen = set()
    for row in rows:
        keys(row, ('case_id', 'status', 'fields', 'issues'), 'result')
        ident = row['case_id']
        if not isinstance(ident, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', ident):
            raise Invalid('case_id: use 1 to 64 lowercase letters, digits, hyphens or underscores')
        if ident in seen:
            raise Invalid('Duplicate case_id')
        seen.add(ident)
        if row['status'] not in ('success', 'partial', 'failed'):
            raise Invalid('status: success, partial or failed required')
        fields = row['fields']
        keys(fields, FIELDS, 'fields')
        for field, val in fields.items():
            if val is None:
                continue
            text(val, field)
            if field in ('statement_date', 'due_date'):
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', val):
                    raise Invalid(f'{field}: YYYY-MM-DD required')
                try:
                    date.fromisoformat(val)
                except ValueError as exc:
                    raise Invalid(f'{field}: invalid date') from exc
            if field == 'total_amount_due' and not re.fullmatch(r'(0|[1-9][0-9]{0,11})\.[0-9]{2}', val):
                raise Invalid('total_amount_due: nonnegative decimal string with exactly two places required')
            if field == 'currency' and not re.fullmatch(r'[A-Z]{3}', val):
                raise Invalid('currency: three uppercase letters required')
        issues = row['issues']
        if not isinstance(issues, dict) or any(k not in (*FIELDS, 'document') for k in issues):
            raise Invalid('issues: map field name (or document) to issue code')
        if any(not isinstance(v, str) or v not in ISSUES for v in issues.values()):
            raise Invalid('Unknown issue code')
        nulls = {k for k, v in fields.items() if v is None}
        status = row['status']
        if status == 'success' and (nulls or issues):
            raise Invalid('success requires every field and no issues')
        if status == 'partial':
            if not 0 < len(nulls) < len(FIELDS) or set(issues) != nulls:
                raise Invalid('partial requires some known fields and one issue per null field')
        if status == 'failed':
            if len(nulls) != len(FIELDS) or set(issues) != {'document'}:
                raise Invalid('failed requires all fields null and one document issue')
    return rows
