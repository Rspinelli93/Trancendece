# Subject checklist

Based on [our subject, version 21.2](../../en.subject.pdf). Page numbers are the printed numbers.

## Required whatever we choose

| Requirement | Page | What we need to check |
| --- | --- | --- |
| Frontend, backend, database | 8 | Complete application with saved data |
| Multiple users at once | 8 | Independent matches, safe simultaneous actions, no duplicate scores |
| Containers; one-command startup | 8 | Start from a clean checkout |
| Current Chrome; no JS warnings/errors | 8 | Test the complete journey |
| Privacy Policy and Terms | 8 | Relevant content, easy to find before and after login |
| Responsive, accessible pages | 9 | Mobile, keyboard, labels, clear errors |
| A styling solution | 9 | Shared CSS or chosen styling tool |
| Secure email/password accounts | 9 | Salted password hashing, login, logout, invalid credentials |
| Frontend and backend validation | 9 | Forms, API requests, and live messages |
| Clear database schema | 9 | Relations, constraints, and migrations |
| Ignored secrets; .env.example | 9 | Setup works without committing secrets |
| HTTPS for external backend access | 9 | HTTPS/WSS; backend-internal traffic may be unencrypted |
| Meaningful Git contributions | 8 | Real work from all five people |
| PO, PM, Tech Lead, developers | 4–6 | Named responsibilities and work organization |
| Complete English root README | 27–29 | Required opening line, names, description, setup, resources/AI use, roles, stack rationale, schema, features, modules, contributions |

Extra points do not compensate for missing mandatory work.

## Starting module list

| Module | Points | Page |
| --- | ---: | --- |
| React + Express | 2 | 12 |
| Live features: updates, connections, efficient broadcasting | 2 | 12 |
| Public database API: key, limits, docs, at least five endpoints | 2 | 12 |
| ORM: Prisma | 1 | 12 |
| OAuth login | 1 | 14 |
| Complete live game with win/loss rules | 2 | 16 |
| Remote players with latency/disconnect/reconnect handling | 2 | 16 |
| **Total** | **12** | |

The subject minimum is 14; our target is 15. We need three more if we keep this list. Page 30 explains bonus treatment beyond 14.

## Counting carefully

- The combined framework module is 2, not 2 plus both framework minors.
- Two OAuth providers do not double the point.
- Three question formats are one game.
- Basic login, a leaderboard, account deletion, or /health alone do not complete the larger related modules.
- Several containers do not automatically mean microservices.
- Only complete working modules count (p.11).

Spectators, tournaments, customization, multiplayer 3+, game statistics, and other game extensions need a working game. Advanced chat needs basic chat; game invitations also need a game. SSR and the ICP backend cannot be combined.

Use [Extra-point options](Extra_points_options.md) to choose the remaining work. As we build, record who owns each feature, how to demonstrate it, and what still needs fixing.
