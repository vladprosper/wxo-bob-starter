# Develop and verify locally

Python 3.11+ is sufficient for all runtime commands and unit tests. Run from the
checkout root; no pip install or network is needed. Use a fresh virtual environment
if desired: `python3 -m venv .venv`, then its Python executable for the commands.
No dependencies need installing into it.

| Module | Responsibility |
|---|---|
| contracts.py | Bounded JSON reader and extraction contract |
| evaluate.py | Exact case/field/status/issue comparison |
| readiness.py | Pure snapshot interpretation |
| staging.py | Copy template to a new directory only |
| __main__.py | CLI arguments, JSON output and exit semantics |

Public functions raise `Invalid` for malformed input. File loading/staging can
also raise `OSError`; the CLI converts either to exit 2. The evaluator and
readiness functions do no I/O. Extend them with explicit contract changes rather
than embedding platform calls.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
python3 scripts/fresh_user_check.py
```

`check_package.py` checks the maintained starter against its reviewed file
manifest, local Markdown links (including the prompt walkthrough) and fixture coverage.
The prompt documentation tests check six-step structure, staged guide links,
exclusion of answer-bearing files and selected fixture-specific answer leakage.
These are static regression checks, not a security boundary or live prompt test. A changed template requires
review and a refreshed manifest. It is not a general-purpose YAML validator.
CI also parses YAML using PyYAML as a development-only dependency.

`fresh_user_check.py` copies the distribution to an isolated temporary directory
without Git metadata, creates a new staged project and executes the README
commands. It checks intentional failures too. This is a clean-checkout test,
not a claim that Bob installed or loaded the mode.

Optional PDF regeneration: install ReportLab in a separate development environment
and run `python3 scripts/build_fixture_pdfs.py`. It reads only the six checked-in
text fixtures. Inspect all pages after regeneration and update fixture hashes.
PDF generation is not required to use the shipped PDFs or evaluator.

No tests run Docker, Orchestrate, Bob, browser automation or live models. The
workflow matrix exercises CLI and filesystem behavior on supported Python
versions; [BOB_ACCEPTANCE.md](BOB_ACCEPTANCE.md) covers live acceptance separately.
