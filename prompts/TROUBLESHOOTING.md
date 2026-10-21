# Troubleshooting prompts: isolate the first failed boundary

Use these in a separate diagnostic Bob task. Supply only relevant nonsecret
artifacts. They authorize investigation, not installs, runtime changes or retries
of denied actions. Mark missing evidence unverified. Preserve raw failures.

## Mode visible, skill unavailable

```text
Inspect the staged project's mode and skill paths and the actual Bob loading
error [ERROR]. Distinguish a visible mode from loaded instructions. Compare with
current Bob documentation. Report the mismatch and proposed local correction;
do not overwrite other modes, install plugins or claim activation without evidence.
```
For example, a menu entry can exist while the skill file is unavailable.

## Documentation works, runtime does not

```text
Compare intended target [TARGET] with the observed runtime query [RESULT].
Identify the interface and first failing request. Separate docs access, configured
connections and successful runtime access. Do not print secrets, change credentials
or switch routes after a denial. Report the smallest authorized diagnostic.
```
For example, a documentation response does not establish deployment permissions.

## Workflow waits for another file

```text
Trace input reference [REFERENCE] from the agent invocation through workflow
collection and extraction using [LOGS/ARTIFACTS]. Identify whether the file was
passed, lost, or a second collection step was introduced. Show the first missing
handoff and a proposed targeted test. Do not invent a runtime result or restart services.
```
For example, a PDF displayed in chat is not proof that an extraction step received it.

## Valid JSON, incorrect or missing values

```text
Compare raw workflow payload [PAYLOAD] with mapped output [OUTPUT] and mapping
code [ADAPTER]. Identify whether the difference originated in extraction, mapping
or the agent's final explanation. Do not copy expected answers into either output.
Propose one contract-level regression test and the smallest correction.
```
For example, mapping the wrong monetary field is different from a model misreading it.

## Import or runtime failure

```text
Use the first error [ERROR], asset revision [REVISION], installed version [VERSION]
and relevant logs [REFERENCES]. Check the failing artifact/interface against current
version-appropriate documentation. Separate unsupported schema, missing dependency
and unhealthy service hypotheses. Propose bounded diagnostics; do not upgrade,
restart, delete or redeploy without the specific approval and target.
```
For example, “container running” and “extraction component ready” are different
observations. The original checkout's readiness utility can assess a supplied
snapshot, but cannot collect live health or fix a runtime.

After a proven correction, return to [repair and retest](06-diagnose-and-repair.md).
