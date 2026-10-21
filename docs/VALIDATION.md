# Validation record

This record describes offline checks, not a real Bob acceptance run.
Live mode activation, documentation MCP access, runtime queries, tool invocation
and model extraction remain unverified for this portable starter.

## Review passes

1. Functional pass: 25 unittest methods passed, including strict input validation,
   exact comparisons, missing/extra cases, role-aware service checks, stale evidence
   and refusal to overwrite staged projects.
2. Skeptical correctness/usefulness pass: oversized JSON integers could escape
   the clean CLI error path; parsing now converts those failures to Invalid.
   Decimal strings now reject non-ASCII digits. Staged projects now include their
   acceptance guide rather than pointing to a file available only in the source
   checkout. Negative regression cases cover the parser corrections.
3. Fresh-user pass: execute the README shell examples in a clean copied checkout
   and a fresh virtual environment with no installed packages. Check documented
   successful and intentional failing exits, then attempt repeated staging and
   verify that the original configuration remains unchanged.

4. Independent model review: a separate reviewing agent ran all 25 tests, package
   and fresh-user checks in a temporary copy. Recursive JSON-node mutations with
   14 alternate values produced no uncaught exceptions. Instruction review found
   an ambiguous CLI fallback after MCP denial; the skill now stops on access
   denial and limits technical retries. Documentation now says staging requires
   a nonexistent destination and explicitly locates extraction assets in the
   retained source checkout. No comparator or readiness correctness defect was
   demonstrated by this review.

This includes independent model review, not independent human review. Offline
execution does not establish live Bob acceptance.

Six PDF fixtures were generated from their text sources, rendered and inspected.
The initial contact sheet mistakenly flattened transparent backgrounds to black;
compositing the rendered pages onto white corrected the inspection image. The PDFs
were unchanged. Fixtures are text PDFs, not OCR scans.

## Reproduce

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
python3 scripts/fresh_user_check.py
```

For the development-only YAML check, install PyYAML 6.0.3 in an isolated environment
and run `python3 scripts/check_yaml.py`. This also rejects several intentionally
invalid mode configurations. It does not emulate Bob's loader.

CI is configured for 12 OS/Python combinations. Hosted conclusions must be read
from the actual workflow run for the published commit; local results alone do
not establish those results. The workflow does not contact Bob, Docker or a model.

## Limits

The result checker trusts its expected file and cannot authenticate predictions.
The readiness checker trusts the supplied observations and service selection.
Neither test suite certifies production deployment, authentication, data isolation,
FIPS compliance, or general model accuracy. See BOB_ACCEPTANCE.md for the separate
live verification work.

## Hosted checkout correction

The first hosted run passed Linux but Windows package checks detected altered
PDF bytes after checkout. Small generated PDFs can be classified as text by Git.
Explicit `.gitattributes` now marks PDFs binary and keeps text line endings LF.
The byte-level manifest check remains strict; it was not relaxed to mask this
failure. A fresh checkout with `core.autocrlf=true` is checked before republishing.

## Build with Bob walkthrough repair — 2026-10-21

The six-step walkthrough adds task prompts, review gates, a worked scenario and
five troubleshooting prompts. Staging includes these guides and an answer-free
output contract, but excludes fixture answers, predictions and evaluation reports.
Prompts are reviewed, not live-validated. No Bob or Orchestrate request was made.

Offline verification for this repair: 29 unittest methods (25 existing plus four
documentation/staging tests), package manifest/link checks, the five README
commands in a copied checkout and fresh no-package virtual environment, and YAML
syntax/negative-mutation checks passed. Intentional bad-prediction exit 1 and
repeat-stage refusal exit 2 are expected, not test failures.

Independent model review found and corrected a single-PDF/full-answer-key mismatch,
an ambiguous JSON-size limit and an omitted monetary leading-zero restriction.
Staged guide links and exclusion of answer-bearing files were inspected. The new
static leakage check initially flagged the required issue-code word `unsupported`,
which is also a fixture ID; it now permits that schema keyword while still checking
fixture-specific identifiers, names, dates and selected amounts. This check is a
regression aid, not a guarantee against contamination or a model-security boundary.
The illustrative JSON row is parsed by the actual contract validator in tests.

The repair preserves raw-output capture, approval boundaries and separate live
acceptance. Public synthetic fixtures remain known-case regression material;
held-out documents are needed for an unseen evaluation. Hosted CI for the published
commit must be checked separately; this local record does not imply it passed.
