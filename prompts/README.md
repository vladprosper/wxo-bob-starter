# Build with Bob: a guided workflow

Use this sequence when you want to **build an agentic document workflow**, not
just run the offline checker. It gives Bob specific jobs with review gates.
These prompts are reviewed instructions, **not live-validated Bob transcripts**.
No agent, tool, deployment or extraction result is supplied or implied.

## Before you start

You need authorized IBM Bob access, the Orchestrate ADK available to Bob and an
authorized development target. A shared target is fine. Staging does not install
or provision them. Fill `wxo-project.md` in the staged project with observed values;
do not paste credentials into prompts, logs or Git. Select WXO Agent Architect.

Keep two separate workspaces:
- **Build/run workspace:** the staged project, this walkthrough and the clean
  [output contract](../docs/OUTPUT_CONTRACT.md). Add only the input documents
  authorized for a run. Do not open the entire starter checkout in extraction Bob.
- **Evaluator workspace:** the original checkout, answer key, synthetic prediction
  examples, evaluation guide and comparison reports. Those contain answers.

This separation reduces accidental answer leakage; it is not a security boundary
or proof that a model has never seen these public fixtures. For a meaningful
unseen test, use independent held-out documents and independently prepared answers.

## Sequence

| Step | Where | Required result before continuing |
|---|---|---|
| [1. Check environment](01-check-environment.md) | Bob, read-only | Observed versions, working interfaces and correct target |
| [2. Prove agent and tool](02-prove-agent-tool.md) | Bob, then authorized runtime | Actual deterministic tool invocation, not merely agent prose |
| [3. Plan document workflow](03-plan-document-workflow.md) | Bob, no deployment | Reviewed responsibilities, contracts and failure handling |
| [4. Build and review](04-build-and-review.md) | Bob, local implementation first | Reviewed artifacts and explicit deployment decision |
| [5. Run and capture](05-run-and-capture.md) | Runtime, then evaluator shell | Raw outputs, evidence references and honest comparison |
| [6. Diagnose and repair](06-diagnose-and-repair.md) | Bob, bounded correction | Failed case rerun and regression checks |

Use the [worked scenario](WORKED_SCENARIO.md) for a concrete learning exercise and
[troubleshooting prompts](TROUBLESHOOTING.md) when a gate fails. Record live evidence
in [Bob acceptance](../docs/BOB_ACCEPTANCE.md).

## How to use a prompt

Copy one fenced text block into Bob, replace every `[BRACKETED INPUT]`, and attach
only the files named for that step. If a value is unknown, say UNVERIFIED instead
of guessing. Read Bob's response before proceeding. A prompt requesting a proposal
does not authorize its execution. Explicitly approve the intended target and
changes through your normal controls before import, deployment or live invocation.
Never bypass an access denial by switching interfaces.

For example, a good plan names the component that receives the PDF and the
component that extracts its fields. “Build an AI agent for invoices” leaves that
critical handoff unspecified. If Bob produces invented command names or evidence,
stop and verify them against the installed version and actual tool output.

## Recommended uses and limits

- Workshop: work through one step at a time and compare the plan with artifacts.
- New prototype: establish the target and a minimal tool call before a larger flow.
- Existing workflow: use capture/repair steps after a change, preserving known-good assets.
- Not a production rollout checklist, compliance certification or OCR benchmark.

The configuration supplies persistent guidance; these prompts supply task-specific
requests. Neither replaces current IBM documentation, your deployment permissions
or human review. Alternative IBM tutorial skills are not assumed installed.
