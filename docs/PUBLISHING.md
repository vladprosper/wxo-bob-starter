# Publication checklist

Before publishing a reviewed revision:

- Run the unit suite, package checks and fresh-user examples.
- Review the diff for personal paths, credentials and unintended course files.
- Preserve Apache-2.0, upstream attribution and modification notices.
- Keep synthetic predictions labeled and live acceptance explicitly unverified
  until observed. Do not replace synthetic fixtures with operational exports.
- Verify the intended GitHub owner/repository and existing state before creating
  or updating anything. Publication needs the owner's explicit authorization.
- Verify remote contents against the reviewed local tree, then check CI to its
  terminal conclusion. Distinguish local success from hosted success.

A separate Bob acceptance record can be added after authorized live testing.
There is no need for additional repositories, accounts or services to use the
three components here.
