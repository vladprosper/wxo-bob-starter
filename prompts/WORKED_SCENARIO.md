# Worked scenario: document intake into structured fields

This is an **illustrative build brief**, not a transcript or deployed solution.
Use it for a workshop or prototype whose goal is to make file handoffs, extraction
contracts and failure evidence visible. It is unsuitable as a ready-made billing
system, OCR benchmark or production approval workflow.

## Brief to supply at step 3

A training team wants to upload one synthetic billing document and receive its
identifier, client, statement date, due date, total amount due and currency.
The document may omit a field, show conflicting totals or be an unsupported type.
Return structured results under `docs/OUTPUT_CONTRACT.md` and a short explanation
that preserves uncertainty. Do not pay bills, update systems or send messages.
Use workflow-controlled document collection/extraction, an agent for interaction,
and only the tools justified by the reviewed plan. Unsupported or unreadable
inputs must not be converted into plausible successful bills.

## Work through it

1. Complete setup verification and the arithmetic tool proof. For example, an
   actual tool trace separates bad wiring from a later extraction-quality problem.
2. At planning, compare two choices: a single conversational agent versus an
   agent plus ordered document workflow. Ask where the PDF reference lives and
   which component owns collection. Accept or revise that decision explicitly.
3. During build review, trace one file reference through the generated artifacts.
   Verify each interface in your installed ADK instead of copying a historic command.
4. After deployment approval, supply a selected synthetic PDF and caller case ID.
   Observe the workflow invocation, not just the final chat answer.
5. Repeat for all six shipped cases before the full-key comparison (one PDF
   alone is only a smoke test). Freeze raw output, map only observed values and
   evaluate separately. For example,
   an absent field stays unknown; successful schema validation is not field accuracy.
6. If a defect appears, determine whether it is a handoff, extraction or mapping
   defect. Repair that boundary and rerun known cases. If no defect appears, record
   the passed scope without manufacturing a repair exercise.

## What a completed learning exercise hands over

- Reviewed plan and the design choice you accepted or changed.
- Versioned agent/tool/workflow artifacts and local test evidence.
- Actual target, software/model versions and invocation references.
- Input hashes, raw outputs, documented adapter and evaluator results.
- Before/after evidence for any repair, plus explicit unverified checks.

For example, “the tool ran and returned a structured payload, but extraction is
unverified because the workflow never received the file” is a useful outcome.
“Everything works” without those distinctions is not.

No sample live result is shown here because this repository has not performed
this portable starter's live Bob–Orchestrate acceptance run.
