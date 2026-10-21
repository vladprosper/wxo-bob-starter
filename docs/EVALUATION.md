# Evaluate document extraction

Use this kit to regression-test field definitions, output mappings and missing
values after changing a workflow. For example, changing a prompt to improve one
invoice must not cause another invoice's zero balance to become null.
Do not use six synthetic cases to claim a general extraction accuracy rate.

**Evaluator-only material:** this guide contains fixture answers. Do not attach it
to the extraction task. Give that task [OUTPUT_CONTRACT.md](OUTPUT_CONTRACT.md)
instead. Keep evaluator reports and synthetic predictions separate too.

## Inputs and expected values

`examples/extraction/documents/` contains six synthetic documents as readable
text and one-page PDFs. `expected.json` is the manually defined answer key.
The two `predictions-*.synthetic.json` files are hand-built comparator examples;
no model generated them. Keep the answer key and predictions outside model context.

| Case | What it tests |
|---|---|
| invoice-basic | Total due 28.09 differs from new charges 18.09; identifier begins with zeros |
| invoice-zero | Observed amount 0.00 is known, not missing |
| missing-due | Missing due date becomes null with a missing issue |
| ambiguous-total | Conflicting total labels become null with an ambiguous issue |
| document-instruction | A printed instruction must not override the actual total 31.25 |
| unsupported | An agenda produces an explicit failed result with all fields null |

These PDFs are digitally generated text, not scans. They do not test OCR quality.
The printed-instruction case is one regression case, not proof of injection
resistance. No real customer names, bills or accounts are included.

## Contract version 1

The authoritative written format is the answer-free
[output contract](OUTPUT_CONTRACT.md). The executable validator is
[contracts.py](../wxo_starter/contracts.py). Keep the contract, not this guide,
in the extraction context.

## Run and interpret

```sh
python3 -m wxo_starter evaluate --expected examples/extraction/expected.json --actual examples/extraction/predictions-good.synthetic.json
python3 -m wxo_starter evaluate --expected examples/extraction/expected.json --actual examples/extraction/predictions-bad.synthetic.json
```

The first exits 0 with 6/6 cases and 36/36 fields matching. The second exits 1
with 3/6 cases and 33/36 fields matching: wrong total, lost leading zeros and the
printed instruction's invented amount. Differences identify the case and path.
A missing or unexpected case fails the run. Case ordering does not matter.

The evaluator validates both files before comparison. Duplicate JSON keys,
duplicate case IDs, non-finite numbers, invalid dates, extra keys and inconsistent
status/issue combinations exit 2. Files are bounded to 2 MB. The CLI writes no
files. Reports contain expected and actual values: treat reports as data if you
substitute your own documents.

## Evaluate a real workflow

1. Run your authorized workflow on each input document, retaining the raw output.
2. Map the raw payload into this contract. Do not fill missing fields from the
   answer key. Record the mapping and original output separately.
3. Save the results as one JSON file; compare it using `--actual your-results.json`.
4. Inspect each difference against the source. Fix the first demonstrated defect
   and rerun all cases, not just the one that failed.
5. Record model/version, source hashes and tool/flow invocation references using
   [the acceptance guide](BOB_ACCEPTANCE.md).

The evaluator cannot tell whether supplied values were extracted, copied or
fabricated. Exact matching deliberately does not trim names, round amounts or
accept fuzzy dates. If normalization is justified, document and test it in your
adapter. Add representative examples and independent expected values before
changing comparison semantics.
