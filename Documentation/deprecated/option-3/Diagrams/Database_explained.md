# What we save

PostgreSQL is our main record. Prisma handles ordinary data access. A small, shared database function handles vector queries for RAG where the chosen Prisma version needs direct SQL.

## Main records

| Record | Information |
| --- | --- |
| `USERS` | ID, unique email, display name, password hash if local, admin/student role |
| `SESSIONS` | Hashed session token, user, expiry |
| `OAUTH_ACCOUNTS` | User, provider, provider's account ID |
| `API_KEYS` | Hashed key, author/read scope, enabled flag |
| `TOPICS` | Fixed topic ID, name, and ordering |
| `EXERCISES` | Name, topic, level, description, starter code, reference solution, compiler code, expected output, source, and status |
| `RAG_ENTRIES` | Eligible exercise, search vector, embedding-model name, and indexing status |
| `ASSIGNMENTS` | Student, exercise, saved exercise copy, assignment time, and state |
| `SUBMISSIONS` | Assignment, source code, request ID, queued/final state, safe result, timing |
| `COMPLETIONS` | Student, exercise, first successful submission, points awarded |
| `TOPIC_PROGRESS` | Student, topic, earned progress and level |
| `BADGES`, `USER_BADGES` | Badge definitions, student awards, award date |
| `VOTES`, `REPORTS` | Student, exercise, vote/reason, date |
| `JOBS` | Accepted background task, owner, type, state, retry information |
| `MODEL_VERSIONS` | Training date, model file reference, feature definition, evaluation results |
| `RECOMMENDATIONS` | Student, exercise, model version if used, reason, date |

IDs link records. Dates use timestamps, code/descriptions use text, structured exercise fields use JSON, scores use numbers, and flags use booleans. The Mermaid diagram shows representative fields rather than every column.

## Rules that prevent confusion

- One counted completion per student/exercise.
- One topic-progress record per student/topic.
- One current vote and one counted report per student/exercise.
- One badge award per student/badge unless its rule explicitly allows repeats.
- One submission per student request ID, checked through its assignment owner.
- One provider/provider-account pair for OAuth.
- One indexed RAG record per eligible exercise and chosen embedding model.

Save a successful completion, topic progress, and its points together: they all succeed or none of them do. Two requests at the same time must not award twice. A generated trial enters RAG only if the exercise is still enabled when a student passes.

## Exercise changes and temporary files

An assignment stores a copy of the exercise as it was when the student received it. This prevents an admin edit from changing an exercise while the student is solving it.

An edited exercise replaces the current exercise only after the reference solution passes. Votes and reports are reset. Earlier student submissions remain in their history. A disabled exercise stays out of new assignments and RAG searches.

Admin uploads and unconfirmed batch results stay in temporary storage. Confirmed imports create database records. Generated trial exercises are saved because they must remain available while students work on them.

Submitted programs cannot connect to this database. The student API returns only the name, topic, level, description, and starter code. It never returns the reference solution, compiler code, or expected output.

[Database diagram](09-database.mmd)
