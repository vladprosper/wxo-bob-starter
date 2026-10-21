# WXO Bob Starter

Prepare an IBM Bob project for watsonx Orchestrate development, test document
extraction outputs against known answers, and distinguish runtime readiness from
an environment that merely starts. The Python tools run offline with Python
3.11+ and its standard library. They require no accounts or model calls.

This repository grew out of a document-workflow teaching exercise. Its most
useful lesson was concrete: a visible PDF, a healthy container and a plausible
agent answer are three different kinds of evidence.

## What you need

**Offline tools:** Python 3.11+ and this checkout are sufficient for staging,
evaluating supplied extraction outputs and checking supplied readiness snapshots.
No IBM account, Bob, ADK, runtime or model access is required for those commands.

**Live Bob–Orchestrate workflow:** you need authorized
[IBM Bob access and installation](https://bob.ibm.com/docs/ide/getting-started/install),
a compatible [Orchestrate Agent Development Kit (ADK)](https://developer.watson-orchestrate.ibm.com/getting_started/installing)
installed and available to Bob, and authorized access to a suitable Orchestrate
environment. You can use an existing shared environment if its owner grants the
required access; each reader does not need to provision a new personal instance.
For example, workshop participants can use their organization's development
environment while running the offline evaluator on their own laptops.

This starter supplies project configuration, not IBM software, accounts,
licenses, credentials or a provisioned runtime. You or your administrator arrange
access, provisioning when needed, credentials and any service charges. See the
[setup prerequisites](docs/STARTER.md#prerequisites) for environment choices,
installation links and the additional requirements for local Developer Edition.

## Build with Bob

Start the [six-step Build with Bob walkthrough](prompts/README.md) to verify your
environment, prove a tool invocation, plan and build an agentic document workflow,
capture genuine outputs, then diagnose and retest. Each step provides copy-and-paste
prompts, inputs, expected artifacts, review gates and stopping conditions.
The [worked scenario](prompts/WORKED_SCENARIO.md) explains recommended uses with
concrete examples. These prompts are reviewed, **not live-validated**.

Keep the extraction workspace separate from answer keys and evaluator reports.
Use the [answer-free output contract](docs/OUTPUT_CONTRACT.md) with Bob, not the
answer-bearing evaluation guide. The walkthrough explains this separation.

## Choose a starting point

| Your task | Use | What you get |
|---|---|---|
| Configure project-specific Orchestrate guidance in Bob | [Starter](docs/STARTER.md) | Mode, skill, project profile and a live acceptance checklist |
| Check whether extracted fields match a document | [Evaluation kit](docs/EVALUATION.md) | Six synthetic cases, strict JSON contract and field-level differences |
| Diagnose a setup that starts but cannot extract | [Readiness guide](docs/READINESS.md) | Role-aware service checks and explicit passed/failed/unverified results |

For example, an extraction can return new charges instead of total due while
producing perfectly valid JSON. The evaluator catches that difference. It also
catches lost leading zeros, missing cases and an invented amount prompted by
text inside a document.

## Run the offline examples

From the downloaded or cloned repository root:

```sh
python3 -m wxo_starter evaluate --expected examples/extraction/expected.json --actual examples/extraction/predictions-good.synthetic.json
python3 -m wxo_starter readiness examples/readiness/ready.synthetic.json --as-of 2026-10-20T12:30:00Z
python3 -m unittest discover -s tests -v
```

The comparison reports `passed: true`, 6 matched cases and 36 matched fields.
The readiness report says `passed`, **based on the supplied fictional snapshot**.
Neither result is a live Bob or model test. On Windows use `py -3` instead of
`python3`. JSON is written to stdout; invalid input is reported on stderr.

Try a valid but incorrect extraction:

```sh
python3 -m wxo_starter evaluate --expected examples/extraction/expected.json --actual examples/extraction/predictions-bad.synthetic.json
```

It exits **1**, with three differences and three fully matching cases. Exit **2**
means malformed input or a file error; it does not mean a model failed an
accuracy test. Full contract and examples are in [the evaluation guide](docs/EVALUATION.md).

## Prepare a new Bob project

Choose a destination that does not exist, with an existing parent directory:

```sh
python3 -m wxo_starter stage ../my-wxo-project
```

This creates project files only. It does not open Bob, connect MCP, install the
ADK, create credentials, or deploy an agent. It refuses existing directories,
including empty ones, to avoid overwriting configuration. Existing-project
installation requires the manual merge described in [the starter guide](docs/STARTER.md).

Fill `wxo-project.md` from the example, then follow the
[Build with Bob walkthrough](prompts/README.md) and record the
[Bob acceptance checks](docs/BOB_ACCEPTANCE.md). Generated files cannot prove
skill activation, documentation access or successful tool invocation.

## What this does not provide

There is no invoice-extraction model, deployed Orchestrate workflow, automatic
installer, production approval service or live health monitor here. The evaluator
checks supplied outputs; it does not authenticate their origin. The six clean
synthetic documents are a regression starting point, not a representative accuracy
benchmark for scans, layouts, languages or adversarial documents.

The readiness utility reads only the file explicitly supplied. It neither runs
Docker commands nor diagnoses historical Java/MinIO errors without evidence.
The [troubleshooting guide](docs/READINESS.md) explains where those observations
help and where they do not.

## Development and evidence

[Development guide](docs/DEVELOPMENT.md) · [Review and test record](docs/VALIDATION.md)
· [Provenance](PROVENANCE.md) · [Publication checklist](docs/PUBLISHING.md).

Python runtime dependencies: none. Optional PDF fixture regeneration uses
ReportLab; ordinary evaluation and staging do not. CI is configured for Python
3.11–3.14 on Linux, Windows and macOS. A workflow file is not a passing run;
consult the validation record for actual results.

Apache-2.0. IBM-derived instructions retain their attribution; see
[NOTICE.md](NOTICE.md) and [LICENSE](LICENSE). This is an independent Bob adaptation.
