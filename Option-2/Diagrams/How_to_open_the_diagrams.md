# Open the diagrams

Open a .mmd file in an editor with Mermaid support, then use its preview command. In VS Code, a Mermaid preview extension can do this. Some viewers show raw .mmd text rather than rendering it.

| Diagram | What it shows |
| --- | --- |
| [00 — Overview](00-system-overview.mmd) | Main parts |
| [01 — Person 1](01-person-1-pages.mmd) | Pages and actions |
| [02 — Person 2](02-person-2-live-game.mmd) | Live matches |
| [03 — Person 3](03-person-3-accounts-database.mmd) | Accounts and data |
| [04 — Person 4](04-person-4-questions-answers.mmd) | Questions and marking |
| [05 — Person 5](05-person-5-setup-testing.mmd) | Setup and tests |
| [06 — Requests](06-normal-requests.mmd) | Login, reads, logout |
| [07 — Match](07-match-from-start-to-finish.mmd) | Queue to final result |
| [08 — Database](08-database.mmd) | Records and relations |
| [09 — Navigation](09-pages-and-navigation.mmd) | Website pages |
| [10 — Routes](10-backend-routes.mmd) | Backend addresses |

Solid arrows show actions or information. Two-way arrows mean both sides communicate. Dotted arrows show support or optional features. Read sequence diagrams top to bottom; their reconnect example illustrates what can happen during a match.

## Database notes

USERS, SESSIONS, and OAUTH_ACCOUNTS handle accounts. API_KEYS protects the public API. QUESTIONS is the bank; MATCH_QUESTIONS freezes private copies for a match. MATCH_PLAYERS records participants and scores; ANSWERS records submissions.

PK is an ID, FK links another record, and UK means unique. JSON holds structured data such as named gaps.

We also need these rules:

- Unique player per match, question position per match, and answer per player per round.
- Unique user/submission-ID pair for retries; unique provider/provider-user-ID pair.
- Two players initially; winner empty for draws/cancelled matches.
- Provider-only accounts may lack a password hash; local email/password signup remains available.
- Final result and lifetime totals saved together, once.
- Archived questions leave existing match copies intact.
- Deleted accounts are anonymized according to our Privacy policy.
- Private answer rules and snapshots are never sent directly to players.

The exact route fields and permissions are in [Routes](Routes_explained.md).
