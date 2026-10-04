# Coding Duel - Mermaid Architecture Pack

This folder defines the architecture for the five-person team. Open the folder in VS Code and preview each `.mmd` file with a Mermaid preview extension.

## VS Code preview

1. Open this folder in VS Code.
2. Install a Mermaid preview extension that supports `.mmd` files.
3. Open a diagram and run the extension's 
- `Ctl + Shift + P` and Select `Mermaid Preview: Preview Diagram`.
4. Use the preview zoom controls or `Ctrl/Cmd + mouse wheel`.

The raw Mermaid files are intentionally separated so each diagram remains readable when zoomed out.

## Project scope

- Real-time 1v1 C coding race.
- Both players receive the same 10 validated challenges in the same order.
- Each player starts with 3 lives.
- The first player to complete challenge 10 wins immediately.
- A player also wins when the opponent reaches 0 lives or forfeits.
- Overall match safety limit: 15 minutes.
- Disconnect grace period: 20 seconds.
- Leaderboard order: `users.total_points DESC`.
- No friends, recent-match interface, ELO, achievements, profiles, or admin page.
- LLM generation is an offline CLI workflow and never blocks a live match.

## Files

1. [`00-system-overview.mmd`](./00-system-overview.mmd) - all five people and every cross-role boundary.
2. [`01-person-1-frontend.mmd`](./01-person-1-frontend.mmd) - browser routes, pages, buttons, REST calls, socket events, and UI state.
3. [`02-person-2-game-engine.mmd`](./02-person-2-game-engine.mmd) - matchmaking, authoritative match state, submissions, reconnect, and finish logic.
4. [`03-person-3-backend-database.mmd`](./03-person-3-backend-database.mmd) - HTTP controllers, authentication, services, repositories, public API, and PostgreSQL.
5. [`04-person-4-c-runner.mmd`](./04-person-4-c-runner.mmd) - isolated compilation, public/hidden tests, security limits, and verdicts.
6. [`05-person-5-llm-infrastructure.mmd`](./05-person-5-llm-infrastructure.mmd) - offline LLM pipeline, validation gates, Docker Compose, HTTPS, and health checks.
7. [`06-rest-sequences.mmd`](./06-rest-sequences.mmd) - login, dashboard loading, Run Code, and account deletion.
8. [`07-websocket-lifecycle.mmd`](./07-websocket-lifecycle.mmd) - queue entry through match completion, including reconnect.
9. [`08-database-er.mmd`](./08-database-er.mmd) - tables, important fields, and relationships.

## Ownership

- Person 1 owns React, the browser router, user interaction, REST consumption, and the WebSocket client.
- Person 2 owns matchmaking, rooms, live match state, scoring, lives, timers, reconnection, and terminal results.
- Person 3 owns Express HTTP routes, sessions, OAuth, Prisma, PostgreSQL, leaderboard persistence, and the secured public API.
- Person 4 owns the isolated C runner, compiler/test harness, resource limits, and normalized verdicts.
- Person 5 owns offline LLM challenge generation, Docker Compose, Nginx/HTTPS, environment configuration, health checks, and integration rehearsals.

Ownership means leading a subsystem. It does not permit changing a shared contract without the consumers reviewing the change.

## Namespace conventions

- Player-facing HTTP API: `/api/v1/...`
- Secured public API: `/api/public/v1/...`
- Internal service API: `/internal/v1/...`
- Browser routes: `/login`, `/register`, `/dashboard`, `/game/:matchId`
- WebSocket events use `domain:action`, for example `queue:join` and `match:submit`.

## Authentication decision

- The backend creates a server-side session.
- The browser receives an `HttpOnly`, `Secure`, `SameSite=Lax` cookie.
- React never stores the session token in `localStorage`.
- The WebSocket handshake uses the same authenticated cookie.

## Exact player-facing HTTP routes

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
GET    /api/v1/auth/oauth/github
GET    /api/v1/auth/oauth/github/callback
GET    /api/v1/auth/oauth/google
GET    /api/v1/auth/oauth/google/callback

GET    /api/v1/users/me
DELETE /api/v1/users/me

GET    /api/v1/leaderboard?limit=20&cursor=...

GET    /api/v1/matches/:matchId/snapshot
POST   /api/v1/matches/:matchId/run
```

There are deliberately no endpoints that let a browser set points, lives, progress, or a winner.

## Exact WebSocket events

Client to server:

```text
queue:join
queue:leave
match:join
match:resume
match:submit
match:forfeit
```

Server to client:

```text
queue:status
match:found
match:snapshot
match:state
match:submission-result
match:finished
match:error
```

## Secured public API

All routes require `X-API-Key`, rate limiting, input validation, and OpenAPI documentation.

```text
GET    /api/public/v1/exercises
GET    /api/public/v1/exercises/:exerciseId
POST   /api/public/v1/exercises
PUT    /api/public/v1/exercises/:exerciseId
DELETE /api/public/v1/exercises/:exerciseId
GET    /api/public/v1/leaderboard
```

The public exercise serializer must never return hidden tests or reference solutions.

## Internal runner contract

```text
POST /internal/v1/execute
```

Request modes:

```text
PUBLIC_RUN
OFFICIAL_SUBMISSION
EXERCISE_VALIDATION
```

Normalized verdicts:

```text
ACCEPTED
WRONG_ANSWER
COMPILE_ERROR
RUNTIME_ERROR
TIMEOUT
INTERNAL_ERROR
```

## Scoring decision

```text
Easy base points:   100
Medium base points: 200
Hard base points:   300

Time bonus: 0-100 points
Awarded only after an ACCEPTED official submission
```

The game engine calculates the score. The runner only returns a verdict and execution measurements.

## Offline LLM interface

There is no admin page. Person 5 exposes challenge generation through a documented CLI:

```bash
npm run challenges:generate -- --topic pointers --difficulty medium --type fix_bug --count 10
```

The CLI accepts user input, streams generation progress, rate-limits requests, reports typed failures, validates candidates through Person 4's runner, and stores only approved exercises through Person 3's exercise service.

Confirm with the evaluators that a CLI satisfies their interpretation of the LLM interface module before relying on those two points.
