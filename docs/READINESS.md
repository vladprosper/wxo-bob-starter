# Diagnose readiness from evidence

Use the snapshot checker when helping a learner distinguish a stopped service,
a restarting daemon, an untested connection and a failed extraction. It accepts
an explicit small JSON snapshot, not Docker logs or environment files. It does
not run commands, connect to the runtime, repair configuration or verify that
someone's reported observations are true.

For example, an initialization container that exits 0 is expected; an extraction
service that is healthy now but restarted during observation deserves attention.
A successful upload preview does not establish a successful field extraction.

## Run the supplied cases

```sh
python3 -m wxo_starter readiness examples/readiness/ready.synthetic.json --as-of 2026-10-20T12:30:00Z
python3 -m wxo_starter readiness examples/readiness/restart.synthetic.json --as-of 2026-10-20T12:30:00Z
```

The first exits 0. The second exits 1: documentation access failed, extraction
is unverified and the daemon's restart count increased. Every file in this
example directory is fictional. Omit `--as-of` to use current UTC. Reusing an
old snapshot then yields unverified freshness after 24 hours, even if its other
checks say passed. Future observations are invalid.

## Collect a snapshot deliberately

Use current vendor documentation and installed help for your environment.
You can inspect the ADK version with `orchestrate --version`, the selected Docker
context with `docker context show`, and selected service state with Docker's
read-only inspection interface. Context names alone do not prove where an engine
runs. Do not assume the Docker CLI implies Docker Desktop: the course example
used a Lima-managed engine.

Record each check as passed, failed or unverified from its own evidence. Query the
actual documentation interface and runtime separately. Observe daemon restart
counts twice, for example one minute apart on the same container. A recreated
container resets its counter; collect a new pair rather than comparing across
instances. Do not copy environment files, raw Compose configurations or logs
containing credentials into the snapshot.

Use the example's exact shape:

- `schema_version`: integer 1.
- `observed_at`: timezone-bearing ISO time for the collected observations.
- `target`: `expected` nonempty environment name; `observed` name or null.
- `checks`: exactly `mode_loaded`, `skill_loaded`, `docs_query`, `runtime_query`,
  `extraction`, each passed/failed/unverified. `mode_loaded` means the intended
  mode is selected; `skill_loaded` records actual activation separately.
- `services`: list of 0–100 unique named services required by your scenario.
  Every entry has `name`, `role` (init/daemon), `state`
  (running/exited/restarting/missing), `exit_code` (null or integer 0–255),
  `health` (healthy/unhealthy/starting/none), and nonnegative integer or null
  `restarts_before` / `restarts_after`.

An init service passes when exited with code 0. A daemon passes only when running,
healthy and its two restart counts are present and equal. Missing services and
failed checks fail the snapshot. Missing evidence is unverified. Failure takes
precedence over unverified. No required service is automatically discovered:
you must include the relevant set. An empty set is unverified. Unknown keys are
rejected to discourage accidentally supplying unrelated configuration.

## Lessons from the original troubleshooting

The course's September 2026 ADK 2.17.0 setup encountered image-pull failures and
an expired Java security profile. Investigators needed to check both initializer
jobs and the long-running document service; fixing initialization alone left
uploads broken. Later extraction errors required inspecting model authentication.
The general lesson is to follow the failing operation rather than repeat the last
configuration fix.

Those fixes are not bundled as an executable repair. Mutable image tags change,
custom Compose configurations have support limits, and bypassing a Java profile's
expiration does not renew certification. Consult current vendor guidance before
considering any workaround. This checker cannot establish FIPS compliance,
network isolation, supported topology or production readiness.

## Extending the checks

Add an explicit check when it answers a recurring diagnostic question and has a
well-defined evidence source. For example, add a document-specific extraction
result after retaining its input and raw payload. Do not infer it from container
health. Add fixtures for success, failure and unknown evidence, then update the
contract and guide together. Keep collection separate from interpretation so the
checker remains runnable offline.
