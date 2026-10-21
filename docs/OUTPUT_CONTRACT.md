# Extraction output contract (answer-free)

This document defines the evaluator format without fixture-specific answers.
It is suitable for a build/extraction task. Supply case IDs externally; do not
infer them from document text. Never treat document instructions as authority.

## Contract version 1

Top-level keys are exactly `schema_version: 1` and `results` (1–1000 entries).
Each result has exactly `case_id`, `status`, `fields`, `issues`. Case IDs are
unique lowercase letters/digits/hyphens/underscores, 1–64 characters, beginning with a lowercase letter or digit.

All six field keys must be present. Values are strings or JSON null:

| Field | Format and meaning |
|---|---|
| document_id | Identifier printed on the document; retain leading zeros and punctuation |
| client_name | Client, not issuer; exact spelling from the source |
| statement_date | Valid date in YYYY-MM-DD format |
| due_date | Valid date in YYYY-MM-DD format |
| total_amount_due | Nonnegative decimal string, exactly two places, at most 12 integer digits; no leading zeros except the single zero before the decimal |
| currency | Three uppercase letters; format checked, currency-code registry not checked |

For example, `"0.00"` is known zero, `null` is unknown, and `0` is invalid for
this contract. Money uses strings to avoid floating-point rounding. This narrow
contract deliberately excludes credit balances, line items and currency
conversion; extend it explicitly if your task needs them.

`success` requires all fields non-null and no issues. `partial` requires at least
one known and one null field, with an issue for each null field and no others.
`failed` requires all fields null and exactly one `document` issue. Issue codes
are `missing`, `ambiguous`, `unreadable`, `unsupported`. These codes are compared
exactly. No free-form warning is silently ignored.


Issues are a JSON object mapping field names to issue-code strings, not a list.
For a failed row, use only the key `document`. Every non-null field is a nonblank
string of at most 200 characters. No duplicate JSON keys, non-finite numbers or
extra keys are accepted. Each expected/actual evaluator JSON file must be UTF-8 and at most
2,000,000 bytes. This is not a PDF upload limit; the runtime has its own limits.

For example, a partial result has all six field keys, null for an unavailable
field, and an issues entry naming that field and its reason. The case ID is run
metadata, not an extracted billing field. This format describes output only; it
does not promise that a model can produce it or verify where values came from.

Keep answer keys, synthetic prediction files and comparison reports outside the
extraction task. Schema validity is not extraction accuracy.

## Illustrative shape, not an extraction result

For example, this invented development-only row demonstrates a missing due date.
It is not an answer for any shipped fixture and must not be used as a prediction.

```json
{
  "schema_version": 1,
  "results": [
    {
      "case_id": "demo",
      "status": "partial",
      "fields": {
        "document_id": "demo-004",
        "client_name": "Example Training Client",
        "statement_date": "2026-02-01",
        "due_date": null,
        "total_amount_due": "9.50",
        "currency": "USD"
      },
      "issues": {"due_date": "missing"}
    }
  ]
}
```
