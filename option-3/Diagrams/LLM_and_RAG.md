# Exercise generation with LLM and RAG

**Rick leads. Julien helps with exercise tests. William helps with storage.**

The LLM writes new exercise drafts. RAG helps it find useful examples from our collection first. Students receive an exercise, not an AI conversation.

## Two ways to supply content

We can prepare JSON ourselves, including with an outside AI tool, and upload it through the admin form. Those files follow the admin validation and confirmation flow.

Our platform also needs its own generation flow for the proposed custom module. A worker generates an exercise when an assignment needs content that the saved library cannot supply. There is no admin “chat with AI” page.

## Generation steps

1. Receive the chosen topic and appropriate level.
2. Find similar eligible examples and teaching notes.
3. Ask the LLM for the agreed JSON structure.
4. Check the fields, fixed topic, test template, and size limits.
5. Ask the correction system to compile the reference solution and run all tests.
6. Reject failed drafts, or retry within a small configured limit.
7. Save a passing draft as a trial and assign it to a student.
8. After a real student's solution passes, make that version eligible for RAG.

If generation fails, keep the student's progress unchanged and offer another saved exercise or a later retry. Use limits on generation requests and cost. The same need should not start many identical jobs at once.

## What belongs in RAG

Admin exercises enter after successful checks and confirmed import. LLM exercises enter only after successful technical checks and a passing student submission. Disabled versions are never retrieved.

We store the original exercise in PostgreSQL. A separate record holds its search vector, version ID, and indexing status. A vector is a numerical description of the text; pgvector lets us compare those descriptions inside PostgreSQL. Our backend combines similarity with topic, level, and ratings. [pgvector reference](https://github.com/pgvector/pgvector)

Keep private solutions and test material accessible only to the generation worker. Student pages get a separate public view. If indexing fails, the saved exercise can still work for students; mark indexing as pending and retry. Do not claim it is searchable until indexing succeeds.

## Votes help choose examples

Prefer useful, well-rated exercises when they also match the requested topic and level. Consider the number of ratings as well as their percentage, so one vote does not dominate.

This changes what we retrieve. It does not retrain the LLM. A student's passing solution is evidence for promotion; we do not automatically copy their code into the generation material.

## Connections and routes

The student uses `POST /api/v1/assignments`. If generation is needed, that returns a job ID. `GET /api/v1/jobs/:jobId` supplies progress and eventually the assignment ID. Internal worker functions handle retrieval, generation, checks, and indexing.

There is no public LLM prompt or chat route. Provider, embedding model, budget, and generation limits remain team choices.

The proposed custom major is **exercise creation, testing, and controlled reuse** (subject p.20). Acceptance is uncertain: the subject asks for a feature not already listed. We need to explain what this complete workflow adds beyond the listed RAG/LLM modules. We do not count either official AI module separately.

[System diagram](03-llm-and-rag.mmd)
