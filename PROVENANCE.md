# Provenance and verification boundary

The starting point was a September 2026 project-specific Bob adaptation of
[IBM's skill at a pinned commit](https://github.com/IBM/agentic-ai-labs-skills/tree/7a96fcd752f8ed2c0cacb61567679b7917c84777/plugins/wxo-agent-architect).
Its 14-file manifest was checked before this work; every digest matched.
The upstream Apache-2.0 license is retained in LICENSE.

This edition removes personal paths, fixed model choices, automatic environment
activation and preservation of one workstation's historical container fixes.
It keeps component selection, documentation checks, workflow-owned uploads,
explicit output contracts, observed tool calls and targeted repair.
The local profile is now an unfilled example. The mode and skill are templates,
not evidence that Bob loaded them.

The Python evaluator, snapshot diagnostics, tests and synthetic fixtures are
new work. The document-extraction course supplied the design problem:
distinguish the total due from other amounts, preserve identifiers, represent
missing values, and check workflow output separately from chat presentation.
The course files and original deployment configurations remain unchanged.

## Format references checked on 2026-10-20

- [Bob custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes):
  project YAML mode configuration, slug uniqueness and tool groups.
- [Bob skills](https://bob.ibm.com/docs/ide/features/skills):
  project skill directory and required front matter.
- [Orchestrate documentation](https://developer.watson-orchestrate.ibm.com/):
  consult the installed version's documentation before implementing a tool.

No live Bob, Orchestrate, Docker or model request is part of the offline tests.
The prior course's successful extraction on ADK 2.17.0 is historical context,
not certification of this starter or current vendor workarounds.
See [acceptance checks](docs/BOB_ACCEPTANCE.md) for the remaining live evidence.
