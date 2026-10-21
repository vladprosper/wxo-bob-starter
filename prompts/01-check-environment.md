# 1. Check the environment

**Use when:** starting a staged project or returning after a setup change.
**Inputs:** filled `wxo-project.md`, intended target and current project folder.
**Run in:** a fresh Bob task using WXO Agent Architect. No runtime mutation.

```text
Load wxo-agent-architect and read wxo-project.md. Check setup only.
Intended target: [TARGET]. Project: [PROJECT FOLDER].
Show evidence that the skill loaded, the ADK executable and observed version,
and the intended versus observed runtime. Perform one relevant documentation
query and one authorized read-only runtime query, identifying the interface,
query and actual result of each. Distinguish configured, attempted and verified.
Do not change settings, install packages, create credentials or deploy anything.
Mark each check passed, failed or unverified. If access is denied, stop that
operation; do not switch interfaces to bypass it. Report the smallest next step.
```

**Expected artifacts:** a nonsecret setup record with date, versions, target,
interface/query names and evidence references. Keep unavailable checks unverified.
**Review gate:** correct target and usable docs/runtime access demonstrated.
**Stop if:** target mismatch, missing access, absent skill or unsupported command.
For example, a mode visible in Bob's menu does not show that its skill loaded;
a server URL in a config file does not prove that a query succeeded.

Next: [prove a tool invocation](02-prove-agent-tool.md).
