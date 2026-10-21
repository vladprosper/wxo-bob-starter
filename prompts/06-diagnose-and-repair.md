# 6. Diagnose, make a targeted repair and retest

**Use when:** an observed failure or comparison difference needs explanation.
**Inputs:** first failing invocation/error, raw output, reviewed implementation and
sanitized defect description. Evaluator reports contain answers: use a separate
debug task, not the blind extraction task.
**Run in:** Bob for diagnosis/local repair; redeployment and reruns require their
specific approved scope. If everything passed, record that; do not invent a defect.

```text
Investigate this observed defect: [DEFECT, INPUT REFERENCE, INVOCATION, ERROR].
Use [RAW OUTPUT/IMPLEMENTATION/LOG REFERENCES]. Identify the first failing operation
and distinguish environment, file handoff, workflow, extraction, mapping and final
response defects. State evidence versus hypotheses. Propose the smallest change
and a regression test; do not broadly rewrite, upgrade, restart or reconfigure.
Do not hard-code a fixture's expected values or case IDs into the solution.
Explain whether this debug context has seen expected answers. Do not claim an
accuracy improvement until fresh executions support it. Make only the approved
local repair [SCOPE], and show the diff and actual local test results. Stop before
any unapproved installation, redeployment, invocation or permission change.
```

**Expected artifacts:** diagnosis, bounded diff, test, rerun plan and evidence.
**Review gate:** correction addresses the cause rather than editing captured results.
**Stop if:** evidence does not distinguish plausible causes; collect a narrow
read-only diagnostic instead. See [troubleshooting](TROUBLESHOOTING.md).
For example, correct a wrong field mapping in the adapter rather than rewriting
the raw model payload to make the comparison pass.

After the exact redeployment/rerun is approved, rerun the failing case and all
previously tested regression cases. Retain before/after raw outputs and compare
outside the extraction context. Start clean extraction sessions without the answer
key, reports or debug conversation. If the developer has seen expected answers,
call these known-case regression checks, not blind evaluation. Add independent
held-out cases before broader accuracy claims. Record remaining failures honestly.

Finish the [acceptance record](../docs/BOB_ACCEPTANCE.md); offline checks and live
checks have separate statuses. No production-readiness claim follows from six cases.
