<!-- Copyright contributors to the Agent Skills project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Adapted for portable IBM Bob use, 2026-10-20. -->

# Architecture review

Describe the task and current boundary. Include only decisions relevant to it.

| Decision | Evidence to record |
|---|---|
| Target | Environment, ADK version and query confirming access |
| Components | Agent, tools, workflow, connections; existing assets reused |
| Data flow | Who collects the file; which step produces each output |
| Contract | Field meaning, type, format, missing/ambiguous behavior |
| Failure | Success, partial and failure payloads; first-failure visibility |
| Test | Source input, expected output, invocation evidence and variation |

A generated diagram and schema should use the same names. An unresolved
extraction schema need not block a separate one-tool environment test.
