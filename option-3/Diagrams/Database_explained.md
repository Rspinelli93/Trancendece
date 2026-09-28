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
| `EXERCISES` | Stable ID/slug, topic, current version, enabled flag |
| `EXERCISE_VERSIONS` | Exercise, version number, origin, publication path, public JSON, private tests/solution, level, trial/active status, validation result |
| `RAG_ENTRIES` | Eligible version, search vector, embedding-model name, indexing status |
| `ASSIGNMENTS` | Student, exact exercise version, assignment time, state |
| `SUBMISSIONS` | Assignment, source code, request ID, queued/final state, safe result, timing |
| `COMPLETIONS` | Student, exercise, first successful submission, points awarded |
| `TOPIC_PROGRESS` | Student, topic, earned progress and level |
| `BADGES`, `USER_BADGES` | Badge definitions, student awards, award date |
| `VOTES`, `REPORTS` | Student, exercise version, vote/reason, date |
| `JOBS` | Accepted background task, owner, type, state, retry information |
| `MODEL_VERSIONS` | Training date, model file reference, feature definition, evaluation results |
| `RECOMMENDATIONS` | Student, exercise, model version if used, reason, date |

IDs link records. Dates use timestamps, code/descriptions use text, structured exercise fields use JSON, scores use numbers, and flags use booleans. The Mermaid diagram shows representative fields rather than every column.

## Rules that prevent confusion

- One numbered version per exercise/version pair.
- One counted completion per student/exercise, across versions.
- One topic-progress record per student/topic.
- One current vote and one counted report per student/version.
- One badge award per student/badge unless its rule explicitly allows repeats.
- One submission per student request ID, checked through its assignment owner.
- One provider/provider-account pair for OAuth.
- One indexed RAG record per version and chosen embedding model.

Save a successful completion, topic progress, and its points together in one database transaction: they all succeed or none of them do. Concurrent requests must not award twice. Trial promotion checks the exact version that passed and whether it is still enabled.

## Versions and temporary files

Students keep the exercise version they were assigned. An admin edit changes the current-version pointer only after validation and confirmation. Old votes remain historical; the new version starts at zero.

Admin candidate files, results, and unconfirmed drafts stay in temporary batch storage, not these exercise tables. Confirmed imports create database records. Generated trial exercises are saved because they must survive while students work on them.

We do not let the submitted program connect to this database. The student API selects public fields explicitly instead of returning the whole private exercise JSON.

[Database diagram](09-database.mmd)
