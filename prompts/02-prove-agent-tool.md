# 2. Prove one agent can invoke one tool

**Use when:** separating connection/tool-wiring problems from extraction problems.
**Inputs:** passed setup record; an isolated authorized project namespace.
**Run in:** Bob for source creation; runtime invocation only after explicit approval.

```text
In [PROJECT FOLDER], propose a minimal agent and deterministic tool that adds two
integers. Give the tool a unique name in [NAMESPACE]. Reject strings and booleans
rather than silently coercing them. No network calls or business-system writes.
Check the current installed ADK's supported schema/import/test interfaces using
actual documentation. Show the agent-tool reference, input/output contract,
source files and unit tests. Explain how to distinguish an actual tool invocation
from the model calculating the answer itself. Create and test local artifacts
only; do not import or deploy until I approve the exact target and changes.
```

Review the files and tests. If approved, replace the placeholders in this follow-up:

```text
For the reviewed assets [FILES/REVISION], my approved development target is
[TARGET] and approved scope is [EXACT IMPORT/DEPLOY/INVOCATION ACTIONS]. Perform
only those actions. Invoke the tool through the agent with 7 and 5, and capture
the real tool-call reference, input, tool result and final response. Test an
invalid input containing a string and record the actual failure. Do not claim
success from source review, an import acknowledgment or an answer of 12 alone.
Stop on any target mismatch, denial or action outside the approved scope.
```

**Expected artifacts:** source, local test results, reviewed deployment plan,
actual invocation evidence and invalid-input behavior. The numbers above are a
deterministic smoke test, not extraction answers.
**Review gate:** the trace shows the tool was called and the response uses its result.
**Stop if:** Bob cannot expose invocation evidence; mark the tool check unverified.
For example, a fluent answer without a tool-call record is not a passed wiring test.

Next: [plan the document workflow](03-plan-document-workflow.md).
