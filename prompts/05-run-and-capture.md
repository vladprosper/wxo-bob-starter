# 5. Run documents and preserve real outputs

**Use when:** approved assets are deployed and live test invocations are authorized.
**Inputs:** selected input PDFs, their external case IDs and hashes, clean contract,
verified target/asset revisions. No answer key, prediction examples or evaluator report.
**Run in:** Bob/runtime first; comparison separately in the original checkout shell.

Before running, copy only the input PDFs into the build/run workspace. A fresh
extraction task must not inherit answer-bearing evaluation context. The six public
fixtures are a regression exercise, not a blinded benchmark. See the walkthrough's
[context separation](README.md#before-you-start).

```text
Run the reviewed workflow [ASSET/REVISION] on target [TARGET] for only these
authorized inputs: [INPUT FILES, CASE IDS, HASHES]. Use docs/OUTPUT_CONTRACT.md.
The case ID is supplied by the caller, not extracted from document content.
Capture the original structured workflow payload and invocation reference for
each input before any mapping. Also retain the final agent response separately.
Do not read answer keys, synthetic predictions or comparison reports. Do not
repair outputs by guessing or using a known answer. Mark an unexecuted or blocked
case as unverified in a separate run log, never as a fabricated extraction row.
If mapping is needed, show and retain the adapter and tests; it may only transform
observed data under documented rules. Stop on access denial or unexpected costs.
Report what actually ran, what failed and what remains unverified.
```

**Expected artifacts:** raw payloads, invocation references, versions, input hashes,
agent responses, mapping code if needed and one contract-shaped predictions file.
**Review gate:** raw payloads support mapped fields; prose retains uncertainty.
**Stop if:** raw output cannot be retrieved, invocation is unverified or mapping
would fill absent information. Record the gap; do not create a successful row.
For example, if the workflow has no due date, an adapter must not borrow one from
the answer key just to satisfy the schema.

## Separate evaluator step

A single selected PDF is a smoke test only. The command below expects **all six**
shipped case IDs, one actual result per case. Collect all six before using the
full answer key; otherwise the absent cases correctly fail comparison. For a
scoped subset, an evaluator must prepare a separate subset answer key outside
Bob, record its scope, and use that path instead. Never call a subset a full run.

Only after outputs are frozen, an evaluator outside the extraction context runs
this command from the original starter checkout, where `output/predictions.json`
is the mapped actual output (the CLI does not create that file):

```sh
python3 -m wxo_starter evaluate --expected examples/extraction/expected.json --actual output/predictions.json
```

Exit 0 means exact match, 1 means a valid comparison with differences, and 2 means
invalid input/file error. Reports include expected values; keep them out of later
blind extraction runs. A missing case fails comparison rather than disappearing.
Do not label hand-built supplied predictions as live workflow outputs.

Next: [diagnose and repair](06-diagnose-and-repair.md).
