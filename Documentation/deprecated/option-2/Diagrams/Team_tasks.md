# Our tasks

These are five areas of ownership inside one project. We can pair up and move tasks around.

| Lead | Main work | Works closely with | First useful result |
| --- | --- | --- | --- |
| [Person 1 — Pages](01-person-1-pages.mmd) | Account pages, dashboard, all answer controls, game view, Privacy/Terms, mobile and keyboard use | 2 for live state, 3 for accounts, 4 for questions | Login → dashboard |
| [Person 2 — Matches](02-person-2-live-game.mmd) | Queue, rounds, timer, scoring, reconnects, final result | 4 for marking, 3 for saving, 1 for display | Two players finish one round |
| [Person 3 — Accounts/data](03-person-3-accounts-database.mmd) | Email/password, sessions, OAuth, database, user routes, leaderboard | 1 for forms, 2 for results, 4 for question storage | Secure registration and login |
| [Person 4 — Questions](04-person-4-questions-answers.mmd) | Question bank, checker, private-answer handling, protected question API | 1 for inputs, 2 for scoring, 3 for storage | One reviewed question of each type |
| [Person 5 — Setup/testing](05-person-5-setup-testing.mmd) | Containers, HTTPS, configuration, integration checks and fixes | Everyone | Clean checkout starts and runs |

Person 5 also pairs on application work. Everyone contributes to the mandatory part and selected modules.

## Useful pairs

- 1 + 3: accounts.
- 1 + 4: question display and inputs.
- 2 + 4: answer → mark → score.
- 2 + 3: save results without duplicates.
- 3 + 4: protected question API.
- 1 + 5: screens, keyboard, browsers.
- 2 + 5: remote play and reconnects.

## Build order

Accounts and setup → three question formats → one live round → complete saved match → reconnects and simultaneous matches → selected extras → evaluation rehearsal.

After each step, another teammate should try it.

## Team roles

We also need a Product Owner to keep feature choices clear, a Project Manager to coordinate work, and a Technical Lead to help settle shared technical decisions. Assign these within the five of us.

Subject: roles pp.4–6; contributions p.8; final README pp.27–29.
