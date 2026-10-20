# Record a real Bob acceptance run

These checks are pending until performed in the intended Bob installation.
Offline fixture results do not satisfy them. Use an isolated authorized project;
do not change a working runtime merely to make the starter's examples pass.

Before starting, confirm authorized Bob access, a compatible ADK installed and
available to Bob, and an authorized Orchestrate target with the credentials and
permissions needed for the planned checks. An existing shared development
environment is sufficient; a new personal instance is not required. The owner or
administrator supplies access and approves any provisioning and costs. For
installation, use IBM's [Bob guide](https://bob.ibm.com/docs/ide/getting-started/install)
and [ADK/environment guide](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
Local Developer Edition additionally requires its documented license, inference
provider and machine prerequisites in the
[official setup guide](https://developer.watson-orchestrate.ibm.com/developer_edition/wxOde_setup).

Offline staging installs none of these products. If a prerequisite is missing,
record the affected live checks as unverified and resolve setup separately; do
not treat this acceptance checklist as authorization to install or provision.
There is no verified minimum Bob/ADK version for this starter. Record actual
versions below. The offline evaluator remains usable with Python 3.11+ alone.

Start a fresh Bob task in the staged project, select WXO Agent Architect and ask:

> Load wxo-agent-architect and read my project profile. Check setup only. Report
> skill loading, the ADK executable/version, intended and observed runtime,
> one relevant documentation query and one read-only runtime query. Identify
> each interface used. Do not change settings, install packages or deploy assets.
> Mark each check passed, failed or unverified and point to the actual evidence.

Record date, Bob version, ADK version, target, query/tool names, outcome and
nonsecret evidence references. A visible mode and successful skill activation are
separate checks. A connection listed in configuration is not a successful query.

After setup passes and the owner authorizes implementation, choose one agent and
one tool. For example, a small deterministic arithmetic tool can separate tool
invocation from reliance on a network service. Record its input, actual tool call,
returned value and agent response. Then run a deliberately invalid input and
confirm the documented failure behavior. Preserve generated source and test
results. This repository does not supply that deployed agent.

Keep the source checkout: staging copies the Bob configuration and this guide,
not the evaluator or fixtures. The following paths and command are relative to
the original wxo-bob-starter checkout. Use PDFs in
`examples/extraction/documents/`, the contract in `docs/EVALUATION.md`, and
`examples/extraction/expected.json` as the answer key. After saving mapped results
as `output/predictions.json`, run from that checkout:

```sh
python3 -m wxo_starter evaluate --expected examples/extraction/expected.json --actual output/predictions.json
```

For extraction acceptance, send only the synthetic input PDFs to your workflow.
Keep expected.json outside the agent's context. Capture the actual workflow JSON,
normalize it to the evaluator contract with a documented mapping, and run the
comparison. Preserve the original payload so mapping cannot hide missing fields.
Check the agent's prose separately for dropped warnings or changed amounts.

Use a run record with these fields:

```json
{
  "date": "UNVERIFIED",
  "bob_version": "UNVERIFIED",
  "adk_version": "UNVERIFIED",
  "target": "UNVERIFIED",
  "model_version": "UNVERIFIED",
  "input_hashes": {},
  "invocation_references": [],
  "checks": {"skill": "unverified", "docs": "unverified", "runtime": "unverified", "tool": "unverified", "extraction": "unverified"}
}
```

This is a recording template, not a result file consumed by the evaluator.
