# Subject and our 15-point proposal

Reference: [subject v21.2](../../en.subject.pdf). Page numbers below are the printed numbers. These documents are a proposal; they do not show implemented or validated points.

A learning platform is allowed. Live play and sockets are optional modules, not mandatory architecture (pp.7–12). Multiple students working safely at once is still required.

## Proposed modules

| Module | Points | What we must show |
| --- | ---: | --- |
| React + Express frameworks, p.12 | 2 | Both frontend and backend used in the working app |
| Public API, p.12 | 2 | API keys, request limits, documentation, at least five endpoints and GET/POST/PUT/DELETE |
| Prisma ORM, p.12 | 1 | Real database use through Prisma |
| OAuth login, p.14 | 1 | Working provider login alongside mandatory email/password |
| ML recommendations, p.15 | 2 | Personalized suggestions from behaviour, filtering/ranking, and improvement over time |
| Advanced search, p.13 | 1 | Search, filters, sorting, and pagination working together |
| Gamification, p.18 | 1 | Saved badges, levels, leaderboard; visible feedback and clear earning rules |
| Custom design system, p.12 | 1 | At least ten reused components, colour palette, typography, and icons |
| Activity dashboard, p.14 | 1 | Useful student activity summaries and trends |
| Health, status, backups, recovery, p.19 | 1 | All four parts, including a demonstrated restore |
| Custom exercise creation and validation, p.20 | 2 proposed | A substantial original workflow, separately justified |
| **Target** | **15** | **13 from listed modules + 2 conditional custom points** |

## The custom module needs a clear argument

We propose: structured C exercises → existing-example retrieval → generation → reference-code tests → student trial → controlled reuse of the successful version, with feedback and version handling.

The subject's custom module must be **not already listed** and needs a README explanation of its value, technical challenges, and why it deserves 2 points. Complexity alone does not guarantee acceptance. Evaluators could consider our workflow too close to the listed RAG/LLM modules; we must explain the distinct exercise-authoring and validation system honestly.

We do not claim the official RAG or LLM interface points. There is no student question-answer assistant or streaming generation interface in this scope. The ordinary “three failed attempts” rule and a library of saved examples also do not count as a trained ML recommender.

The subject minimum is 14. If the custom module is rejected, the proposed total is 13. This needs a team decision before we rely on the plan. A replacement to discuss is two additional browsers (1 point, p.13) plus complete import/export (1 point, p.19). That would keep a 15-point target; it is not selected extra work.

For import/export, our existing JSON upload is only part of the module. We would also need exports in multiple formats, such as JSON and CSV, with a documented representation for nested tests. Extra-browser support means testing all features and documenting limitations, not only opening the homepage.

## Required whatever modules we choose

- Frontend, backend, database, simultaneous users, meaningful commits from everyone, containers, and one-command startup (p.8).
- Current stable Chrome with no JavaScript warnings/errors (p.8).
- Relevant, accessible Privacy and Terms pages; empty placeholders are not enough (p.8).
- Responsive and accessible pages, chosen styling solution, secure salted password hashes, input checks on both sides, clear schema, ignored secrets with `.env.example`, and HTTPS for external backend access (p.9).
- Named coordination roles and participation from the whole team (pp.4–6).
- Complete English root README (pp.27–29): prescribed italic opening with actual logins, description, setup, resources and AI use, team roles, work organization, stack reasons, schema, features, modules, and individual contributions.

This Option-3 README is a proposal index, not a replacement for the final project README.

## Counting correctly

We do not add separate frontend/backend minor points on top of the combined framework major. Basic admin permission does not complete advanced permissions. One JSON file type does not complete file management. Learning history is not the game-statistics module. Running several containers does not automatically earn microservices.

Only complete working modules count (p.11). Keep an implementation checklist and demonstration for each selected module as we build.
