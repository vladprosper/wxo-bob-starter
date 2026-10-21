# 4. Build the reviewed design

**Use when:** the plan is accepted and local implementation is authorized.
**Inputs:** approved plan/revision, clean contract, target/version record.
**Run in:** Bob; keep deployment as a separate decision.

```text
Implement the approved plan [PLAN/REVISION] in [PROJECT FOLDER]. Preserve existing
assets and settings. Create the agent, tools and workflow artifacts required by
that plan; do not invent extra components. Verify syntax and schema against the
actual installed ADK and current official documentation. Record doc references.
Add deterministic tests for contracts, file-reference handoff, missing values and
error paths using fabricated development inputs, not the evaluator answer key.
Show changed files, agent-tool/workflow references, dependencies, validation
commands and their actual results. Separate checks run from checks proposed.
Explain any generated code you could not validate. Do not install, import,
deploy, change permissions or invoke a live model. Prepare an exact deployment
plan for my review, including target, affected assets and rollback considerations.
```

**Expected artifacts:** implementation, tests, evidence, dependency list and a
reviewable deployment plan. Generated source is not deployment evidence.
**Review gate:** inspect schemas, file handoff, failure paths and configuration
changes. Approve only specific imports/deployments in your authorized target.
**Stop if:** required tests fail, target changes, unsupported APIs remain, or a new
permission/installation is needed. Resolve separately, not via a guessed fallback.
For example, a local parser test cannot prove that the runtime accepted a workflow.

After explicit approval, ask Bob to execute only the reviewed deployment plan,
retain actual responses and verify the deployed asset identities. Do not assume
an import acknowledgment proves that the deployed agent can run the workflow.

Next: [run and capture](05-run-and-capture.md).
