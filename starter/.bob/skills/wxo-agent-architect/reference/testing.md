<!-- Copyright contributors to the Agent Skills project -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Adapted for portable IBM Bob use, 2026-10-20. -->

# Test the workflow and its presentation separately

Record input identity, expected fields, actual workflow payload, tool/flow
instance reference and agent response. Keep expected data outside the model's
prompt. Compare the payload first, then check the response for omitted warnings.

For example, use different values for previous balance, new charges and total
due. Include a leading-zero identifier, a missing field and an unsupported
document. A manually corrected value is not a model extraction result.

Distinguish upload, document processing, inference authentication, extraction and
agent invocation failures. Review logs around the relevant request, without
copying credentials or unrelated content. Fix the first demonstrated defect and
rerun both the failed input and a known passing input.

The repository's offline evaluator checks supplied JSON. It neither calls a
model nor verifies the origin of submitted predictions. Preserve the real run's
input hashes, model/version and invocation references in a separate run record.
