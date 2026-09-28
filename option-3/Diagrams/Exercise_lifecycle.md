# From exercise draft to trusted example

We separate three questions: did our checks pass, can students receive this version, and can the LLM reuse it as an example?

## Admin upload

Paste or upload JSON → temporary batch → structure checks → reference solution compiles → tests pass → admin confirms → save active version → index for RAG.

Failed files stay in the temporary batch for correction or error download. They never enter the permanent exercise library. Importing a passed batch twice must return the earlier result rather than duplicate exercises.

## LLM generation

Retrieve eligible examples → generate JSON → structure checks → reference solution compiles → tests pass → save trial → assign to student → student passes → promote version → index for RAG.

The first passing student submission promotes the version automatically in this working plan. No extra admin approval is needed. A student failing does not prove the exercise is broken, so it stays trial until it passes or is disabled.

One trial can have several assignments, but only one promotion happens. Every successful student can still receive their own first-completion reward. Trial allocation limits remain a team choice.

## Status is kept simple

| Status | Students | RAG |
| --- | --- | --- |
| Trial | Can receive and attempt it | Excluded |
| Active | Can receive and attempt it | Eligible after indexing completes |
| Disabled | No new assignment or scoring | Excluded immediately |

“Validating” and “failed” describe jobs before publication. “Needs attention” is a report flag, not a second competing publication status. This avoids an exercise being both disabled and trusted by mistake.

## Editing and disabling

Validate edits in temporary storage. The old published version remains until a passed edit is confirmed. A confirmed edit creates a new version with fresh votes and reports; it does not rewrite earlier submissions.

An existing assignment keeps its version. RAG uses only the latest eligible version of an enabled exercise. Disabling the exercise blocks all its versions from new grading and retrieval; students keep access to their history and get another exercise.

Prefer archiving over permanent deletion. Admin reactivation must recheck the version's validation and original eligibility: an unpassed LLM trial must not become RAG-eligible just because it was re-enabled.

## Votes and reports

After a finished attempt, a student can vote up or down, whether they passed or failed. They can report a problem before submitting. A timeout or service outage in our infrastructure is not a completed learning attempt.

Allow one current vote and one counted report per student per version. Updating a vote replaces it rather than adding another. Store short report reasons with the exercise detail; no separate reports dashboard is needed.

Use negative-vote percentage with a minimum sample size. Five distinct reports is a provisional limit, still to be decided. Until we set these rules, show a needs-attention flag and allow manual disabling. Once configured, crossing a rule can disable the exercise and remove it from RAG searches.

Keep confirmed faulty exercises out of failure-based recommendations. Do not remove earned points or levels. An attempt interrupted by a disabled exercise should offer a replacement without a penalty.

Compiler checks and a student's pass are useful evidence, not proof that every instruction or test is correct. Reports are how we handle mistakes that remain.

[Lifecycle diagram](07-exercise-lifecycle.mmd)
