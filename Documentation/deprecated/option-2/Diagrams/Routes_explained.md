# Pages, routes, and live messages

We have three kinds of address: pages we open, requests for saved data, and live messages during a match. All use the same website address and HTTPS.

The backend checks who we are and what we can do. Hiding a button is not enough.

## Pages

Person 1 builds these screens.

| Page | Who can open it | What it shows |
| --- | --- | --- |
| `/` | Everyone | Redirect to login or dashboard |
| `/register` | Guests | Create an account |
| `/login` | Guests | Email/password or OAuth login |
| `/dashboard` | Signed-in players | Play button, account summary, leaderboard |
| `/game/:matchId` | Players in that match | Question, timer, progress, final result |
| `/privacy` | Everyone | Privacy Policy |
| `/terms` | Everyone | Terms of Service |

`:matchId` means the ID of a particular match. Unknown pages show a helpful 404 page. Privacy and Terms stay accessible before and after login.

## Account and saved-data requests

Person 3 owns these routes. Person 2 provides the live match state.

| Method and route | What we send | What comes back |
| --- | --- | --- |
| `POST /api/v1/auth/register` | Email, display name, password | Account summary; then go to login |
| `POST /api/v1/auth/login` | Email, password | Account summary and secure session cookie |
| `POST /api/v1/auth/logout` | Current session | Session ends; connected sockets close |
| `GET /api/v1/auth/oauth/:provider` | Chosen provider | Redirect to its login page |
| `GET /api/v1/auth/oauth/:provider/callback` | Provider code and one-use security value | Session cookie; redirect to dashboard |
| `GET /api/v1/users/me` | Current session | Our ID, name, total points |
| `DELETE /api/v1/users/me` | Session and confirmation | Delete/anonymize account data; revoke access |
| `GET /api/v1/leaderboard?limit=20&cursor=...` | Page size and position | Rankings and next-page position |
| `GET /api/v1/matches/:matchId/snapshot` | Session and match ID | Current match view or saved final result |

Apart from registration/login and OAuth entry, these require a session. Only participants can fetch a match snapshot. Account deletion returns a conflict while a match is active.

We validate inputs, protect cookie-based changes against forged requests, and check allowed origins. OAuth callbacks must match the login we started; matching email addresses alone must not link accounts.

## Public question API

Person 4 owns the routes; Person 3 helps with storage and keys. This serves the public API module: a key, request limits, documentation, and at least five endpoints covering create/read/update/delete (subject p.12).

Every route below requires `X-API-Key`. A normal player's cookie cannot edit questions. Keys stay out of frontend code.

| Method and route | Purpose |
| --- | --- |
| `GET /api/public/v1/questions` | List active question summaries, one page at a time |
| `GET /api/public/v1/questions/:questionId` | Read a question without its accepted answers |
| `POST /api/public/v1/questions` | Create a draft with its private accepted answers |
| `PUT /api/public/v1/questions/:questionId` | Replace fields using the expected version; activate after review |
| `DELETE /api/public/v1/questions/:questionId` | Archive a question |
| `GET /api/public/v1/leaderboard` | Read rankings |

Create/update replies return IDs, versions, and status without echoing private answers. Archiving or editing a question must not change a match already using it: each match keeps its own question copy.

Person 5 helps expose these public support routes:

| Route | Purpose |
| --- | --- |
| `GET /api-docs` | Readable API instructions |
| `GET /api/openapi.json` | API description for tools |
| `GET /health` | Minimal readiness status, without secrets |

Use consistent responses: 201 for creation, 204 for successful deletion/logout, 400 for invalid input, 401 for missing/invalid access, 403 for forbidden actions, 404 for missing items, 409 for conflicts, and 429 for too many requests.

## Live match messages

Person 2 owns the live connection. Socket.IO uses `/socket.io` on the same backend and checks the session cookie. It is a connection address, not a page.

Every request has a `requestId` so we can match errors to the action.

| Player sends | Extra information | Backend does |
| --- | --- | --- |
| `queue:join` | None | Add player once; reject if already playing |
| `queue:leave` | None | Remove player from queue |
| `match:join` | `matchId` | Check membership and send current state |
| `match:resume` | `matchId` | Restore current state after reconnecting |
| `match:submit` | `matchId`, `roundId`, `submissionId`, answer | Validate, check answer, save submission |
| `match:forfeit` | `matchId` | End participation using the agreed rules |

An answer is an option ID, an output string, or named gap values. We do not run submitted code. There is no `/run` route or separate HTTP route for official match answers.

| Backend sends | Meaning |
| --- | --- |
| `queue:status` | Waiting or removed |
| `match:found` | Match ID and players |
| `match:snapshot` | Full current view: phase, question, players, completed-round scores, our submission receipt, deadline, state version |
| `match:state` | Updated public state with an increasing version |
| `match:answer-received` | Private receipt; no mark yet |
| `match:round-result` | Marks after both players answer or time expires |
| `match:finished` | Winner/draw, reason, and permitted review |
| `match:error` | Request ID and a safe explanation |

The server checks membership, the current round, deadline, and duplicate submissions. Retrying the same submission returns its receipt; reusing its ID with a different answer is rejected. Two tabs do not create two players.

Current-round marks and accepted answers stay private until the round closes. Reconnecting restores the existing deadline; it does not restart the round. Logout or account deletion revokes the live connection too.

## Routes we add only if we choose the feature

| Feature | Pages and requests | Owners |
| --- | --- | --- |
| Spectators | `/watch/:matchId`; `GET /api/v1/matches?status=playing`; `match:watch` / `match:unwatch` | 1 + 2 |
| Search/practice | `/practice`, `/practice/:questionId`; `GET /api/v1/practice/questions?q=...&topic=...&sort=...&page=...`; `GET /api/v1/practice/questions/:questionId`; `POST /api/v1/practice/questions/:questionId/answers` | 1 + 4 + 3 |
| Match history | `/history`; `GET /api/v1/users/me/matches` | 1 + 3 |
| Profiles/settings | `/profile/:userId`, `/settings`; agree API after choosing scope | 1 + 3 |
| Tournaments | `/tournaments`, `/tournaments/:id`; agree API after choosing rules | 1 + 2 + 3 |

Spectators cannot submit or forfeit. Practice never changes competitive scores. History requests return our own matches.

See [the route diagram](10-backend-routes.mmd) and [the match flow](07-match-from-start-to-finish.mmd).
