# Use the Bob starter

Use this component when a Bob project needs explicit Orchestrate development
boundaries: which runtime is intended, which existing assets must stay intact,
and what constitutes a successful test. It is useful for a workshop or a small
agent/tool project. It does not provision a runtime or enforce an access-control
boundary. Bob's permission system and your environment remain authoritative.

## Prerequisites

Offline staging needs Python 3.11+ and this checkout. Using the staged project
requires IBM Bob, a compatible Orchestrate ADK/runtime, an authorized development
interface and access to the applicable documentation. Model inference may be
remote even when the deployment endpoint is local. Existing service access can
have costs; none of the offline commands initiates it.

## New project

Run `python3 -m wxo_starter stage ../my-wxo-project` from this repository.
The parent folder must exist; the destination must not. A successful result
reports `live_verified: false`. A repeated command exits 2 without changing the
existing destination. If copying fails part-way, inspect the partial new folder;
the utility deliberately does not recursively delete it.

The staged folder contains:

- `.bob/custom_modes.yaml`: one mode, `wxo-agent-architect`.
- `.bob/skills/wxo-agent-architect/`: skill and three focused references.
- `wxo-project.example.md`: facts to establish for this specific project.
- License, attribution and provenance files.

Copy the profile example to `wxo-project.md` and fill it with observed facts.
For example, record the executable/version and target returned by a read-only
query, rather than assuming that launching Bob from SaaS selected a local target.
Do not put API keys in the profile. An unfilled profile is intentionally not a
valid deployment target.

Open the folder in Bob. Check that the mode appears and start a fresh task to
verify skill loading. Follow [BOB_ACCEPTANCE.md](BOB_ACCEPTANCE.md).

## Existing project

Stage into a new, nonexistent destination first. Review differences, then manually
merge the single mode entry into the existing `customModes` list. Preserve other
entries and use a unique slug. Copy the skill only after checking for a same-name
skill. Merge applicable project-profile facts rather than replacing project rules.
The utility has no overwrite or force flag.

The mode permits read/edit/execute/MCP/skill/todo tool groups. Installing those
instructions is not permission to perform every available operation. Review the
groups against the intended project. This package does not change MCP settings,
permission defaults, credentials or runtime configuration.

## Common failures

| Symptom | Next check |
|---|---|
| Mode missing | Confirm the project folder and `.bob/custom_modes.yaml`; check Bob's mode UI |
| Mode visible but skill unavailable | Check the skill folder, front matter and fresh-task activation separately |
| Documentation configured but queries fail | Record the actual server error; do not count an unrelated search as a successful query |
| CLI and MCP list different assets | Compare their environment and installed version before changing either |
| Source files generated but agent does not work | Inspect import result, actual invocation and returned output separately |

## Adaptation

Edit the profile for each project. Extend the skill references only when a
specific repeated task needs them. For example, add an output-contract reference
for your chosen document type instead of adding a general production-governance
manual. Keep runtime-specific workarounds out of shared instructions.

The templates follow the [Bob mode](https://bob.ibm.com/docs/ide/configuration/custom-modes)
and [skill](https://bob.ibm.com/docs/ide/features/skills) formats checked on
2026-10-20. Static checks are limited to this package's files and YAML syntax;
they cannot certify Bob discovery or behavior.
