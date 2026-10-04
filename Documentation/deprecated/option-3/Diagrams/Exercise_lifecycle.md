# From exercise draft to trusted example

We separate three questions: did the exercise pass our checks, can students receive it, and can the LLM reuse it as an example?

## Admin upload

Paste or upload JSON → check required fields → insert the reference solution into the compiler code → compile and run → compare with expected output → admin confirms → save → add to RAG.

The page shows which files passed and why others failed. The admin imports the passed exercises and discards the failed ones. Failed files never enter the exercise library. Uploading the same exercise again must not create a duplicate.

## LLM generation

Find useful RAG examples → generate JSON → check required fields → run the reference solution with `compiler_code` → compare with `expected_output` → save as trial → student passes → add to RAG.

The first passing student submission activates the generated exercise automatically in this working plan. No extra admin approval is needed. A student failing does not prove the exercise is broken, so it stays a trial until someone passes it or an admin disables it.

Several students can receive the same trial, but it enters the RAG only once. Every successful student can still receive their own first-completion reward. Trial limits remain a team choice.

## Status is kept simple

| Status | Students | RAG |
| --- | --- | --- |
| Trial | Can receive and attempt it | Excluded |
| Active | Can receive and attempt it | Added after RAG indexing finishes |
| Disabled | No new assignment or scoring | Excluded immediately |

“Checking” and “failed” describe uploads before they are saved. “Needs attention” is a warning created by reports or poor ratings.

## Editing and disabling

An edited exercise must pass the same compiler check before it replaces the current one. If it fails, keep the current exercise unchanged. The replacement starts with fresh votes and reports.

Earlier student results stay in their history. Disabling an exercise removes it from new assignments and RAG searches. Students working on it receive another exercise without a penalty.

We can keep a disabled exercise in the database for history, or delete it when no saved student result needs it. Re-enabling it requires the compiler check again. An LLM trial still needs a passing student solution before entering the RAG.

## Votes and reports

After a finished attempt, a student can vote up or down, whether they passed or failed. They can report a problem before submitting. A timeout or service outage in our infrastructure is not a completed learning attempt.

Allow one current vote and one counted report per student and exercise. Updating a vote replaces it rather than adding another. Store short report reasons with the exercise detail; no separate reports dashboard is needed.

Use negative-vote percentage with a minimum sample size. Five distinct reports is a provisional limit, still to be decided. Until we set these rules, show a needs-attention flag and allow manual disabling. Once configured, crossing a rule can disable the exercise and remove it from RAG searches.

Keep confirmed faulty exercises out of failure-based recommendations. Do not remove earned points or levels. An attempt interrupted by a disabled exercise should offer a replacement without a penalty.

The compiler check and a student's pass are useful evidence, but they cannot prove that the description is clear. Reports help us find mistakes that remain.

[Lifecycle diagram](07-exercise-lifecycle.mmd)
