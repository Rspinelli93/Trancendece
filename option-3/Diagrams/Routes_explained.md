# Pages and backend routes

A **page route** opens a screen. An **API route** asks the backend to do something. `:exerciseId` means the ID of the selected exercise.

`GET` reads, `POST` starts or creates, `PUT` replaces or updates, and `DELETE` removes or archives. All external requests use HTTPS. There are no socket routes.

## Pages

| Address | What opens |
| --- | --- |
| `/` | Login or dashboard, depending on the session |
| `/register`, `/login` | Account forms |
| `/dashboard` | Continue learning, recommendations, and progress |
| `/topics`, `/topics/:topicId` | Fixed topics and their exercise lists |
| `/exercises/:exerciseId` | Public exercise description and start button |
| `/learn/:assignmentId` | Assigned exercise version, code editor, results, voting, and reporting |
| `/progress` | Topic levels and activity over time |
| `/badges`, `/leaderboard`, `/profile` | Rewards, rankings, and account summary |
| `/admin/exercises` | Searchable exercise list |
| `/admin/exercises/new` | Paste/upload JSON and view batch results |
| `/admin/exercises/:exerciseId` | Inspect, edit, validate, or disable |
| `/privacy`, `/terms`, `/status` | Public information and service status |

Learning pages require login. Admin pages require an admin account. Unknown addresses show a useful 404 page. Privacy and Terms are accessible before and after login.

## Accounts — William with Eliott

| Method and route | Request → result |
| --- | --- |
| `POST /api/v1/auth/register` | Email, display name, password → account created; go to login |
| `POST /api/v1/auth/login` | Email/password → account summary and secure session cookie |
| `POST /api/v1/auth/logout` | Current session → revoke session and clear cookie |
| `GET /api/v1/auth/oauth/:provider` | Supported provider → redirect to its login |
| `GET /api/v1/auth/oauth/:provider/callback` | Code and one-use state → verified account session |
| `GET /api/v1/users/me` | Session → our ID, display name, and role |

Never take the requested role from a signup form. OAuth must check the one-use state; it must not merge accounts based only on matching email text. Cookie-based changes need protection against forged requests, as well as input checks and request limits.

## Learning — William, Julien, and Rick

| Method and route | Request → result |
| --- | --- |
| `GET /api/v1/topics` | Session → fixed topic list |
| `GET /api/v1/exercises?q=...&topic=...&level=...&sort=...&page=...` | Search choices → allowed exercise summaries and page count |
| `GET /api/v1/exercises/:exerciseId` | Exercise ID → current public description |
| `POST /api/v1/assignments` | Topic/level or chosen exercise ID, request ID → assignment, or pending generation job |
| `GET /api/v1/jobs/:jobId` | Job ID → our job's progress and eventual assignment ID |
| `GET /api/v1/assignments/:assignmentId` | Assignment ID → our fixed exercise version and earlier attempt results |
| `POST /api/v1/assignments/:assignmentId/submissions` | C source and request ID → submission ID, queued |
| `GET /api/v1/submissions/:submissionId` | Submission ID → our status and safe result |
| `PUT /api/v1/assignments/:assignmentId/vote` | Up or down → saved vote for this version |
| `POST /api/v1/assignments/:assignmentId/reports` | Reason, optional short note → report recorded |

Check assignment/job ownership on the backend. Public descriptions omit private tests and reference solutions. Votes need a finished attempt; reports can be sent before any submission. Counts are per student and exercise version.

Repeated assignment/submission request IDs return the existing result. Reusing an ID with changed content returns a conflict. Pending jobs are polled with a short delay and stop at a final state. Disabled versions cannot earn new points.

## Progress — Eliott and William

| Method and route | Result |
| --- | --- |
| `GET /api/v1/recommendations` | Suitable exercise IDs and a simple reason |
| `GET /api/v1/progress` | Our topic levels and completions |
| `GET /api/v1/activity?from=...&to=...` | Our attempts, completions, and activity by date/topic |
| `GET /api/v1/badges` | Our badges, progress, and earning rules |
| `GET /api/v1/leaderboard?topic=...&page=...` | Display names, ranks, points; no email addresses |

These require a session. Model training is an internal worker job, with no student route to alter results or rewards.

## Admin — William and Julien

Every route below requires an admin session. A hidden button alone does not protect it.

| Method and route | Request → result |
| --- | --- |
| `GET /api/v1/admin/exercises?id=...&q=...&topic=...&sort=...&page=...` | Filters → exercise list including disabled items |
| `GET /api/v1/admin/exercises/:exerciseId` | ID → JSON, version, votes, reports, and status |
| `POST /api/v1/admin/imports` | Pasted object/array or JSON files → temporary batch ID; validation starts |
| `GET /api/v1/admin/imports/:batchId` | Batch ID → progress, passed items, failed items |
| `GET /api/v1/admin/imports/:batchId/errors` | Batch ID → failed JSON with `validation_errors` |
| `POST /api/v1/admin/imports/:batchId/commit` | Selected passed item IDs, request ID → saved exercises/versions and indexing status |
| `DELETE /api/v1/admin/imports/:batchId/failed` | Batch ID → discard failed temporary items |
| `DELETE /api/v1/admin/imports/:batchId` | Batch ID → cancel and discard uncommitted batch |
| `PUT /api/v1/admin/exercises/:exerciseId` | Edited JSON and expected current version → temporary validation batch |
| `PUT /api/v1/admin/exercises/:exerciseId/status` | Disabled/enabled, expected version → changed availability after checks |

Editing uses the same batch result and commit routes. Commit rechecks that the tested content and base version are unchanged. It imports exactly the passed items shown to the admin. The page confirms before disabling. Re-enable preserves whether a version still needs a student pass.

## Public exercise API — William with Julien

This is the subject's documented API for scripts, separate from browser sessions. It uses scoped API keys, request limits, and documentation. Normal students never receive author keys.

| Method and route | Purpose |
| --- | --- |
| `GET /api/public/v1/exercises` | Paginated public summaries of active exercises |
| `GET /api/public/v1/exercises/:exerciseId` | Public fields of one active exercise |
| `POST /api/public/v1/exercises` | With author key: stage JSON for validation |
| `PUT /api/public/v1/exercises/:exerciseId` | With author key: stage an edit using expected version |
| `DELETE /api/public/v1/exercises/:exerciseId` | With author key: archive, retaining history |
| `GET /api/public/v1/imports/:batchId` | Author's own validation progress |
| `GET /api/public/v1/imports/:batchId/errors` | Author's failed JSON and diagnostics |
| `POST /api/public/v1/imports/:batchId/commit` | Author confirms passed items for publication |

This covers at least five endpoints and all required methods. Public writes use the same validation and confirmation rules as the admin form. A script cannot bypass the compiler by using the public API. Key management can be a setup command for the first version.

## Support and internal connections

`GET /health` gives minimal readiness; `GET /api-docs` and `GET /api/openapi.json` document the public API. These are public and reveal no secrets.

The worker calls Judge0's submission and result endpoints over the private service network. LLM calls, embedding calls, and Python model execution are internal operations. The browser never gets a runner token, LLM key, or database connection.

Use 201 for account creation, 202 for queued work, 204 for successful actions with no response body, 400 for invalid input, 401/403 for access problems, 404 for missing items, 409 for version conflicts, 410 for expired batches, 413 for oversized uploads, 429 for request limits, and 503 for unavailable services. A finished correction job may report a failed exercise even though the HTTP request itself succeeded.

[Route diagram](11-backend-routes.mmd) · [Page diagram](10-pages.mmd)
