# Current MVP

This resumes the last changes made.

## Objective

The project is a C learning platform with accounts, validated exercises, saved progress, and a controlled AI search.

A student chooses a level and writes what they want to learn. RAG searches a library of existing exercises. The LLM selects one of those exercises and gives a short reason for the choice. It cannot create an exercise or invent an exercise ID.

This design avoids repeated AI-generated exercises and keeps every available exercise under our control.

## Student flow

1. Create an account with email and password, or log in with GitHub.
2. Choose level `1`, `2`, or `3`.
3. Write what to practise in a text box.
4. Receive an existing enabled exercise, or a clear message when there is no good match.
5. Write and submit C code.
6. Receive a simple success or failure result.
7. Save the attempt and update progress when needed.

Students can also use predefined avatars, read hints, report a broken exercise, and view their score, MMR, badges, level, and leaderboard position.

## Exercise flow

An exercise can ask for a function or a complete C program.

The admin uploads exercise JSON containing the instructions, starter code, hints, forbidden functions, a reference solution, private tests, compiler code, inputs, and expected outputs.

Before anything is stored:

1. the JSON fields and allowed values are checked;
2. the reference solution must pass every test;
3. forbidden functions are checked;
4. the RAG vector must be created successfully.

If one of these steps fails, the exercise is rejected. If all of them pass, the reference solution is discarded and the validated exercise is saved with a unique ID that is never reused.

When a student submits code, the backend uses the private tests stored with the exercise. The submitted code and complete compiler response are temporary. The database keeps only the attempt result, attempt number, and time taken.

## Admin page

The admin page has only four jobs:

- upload exercise JSON;
- search the exercise list;
- read student reports;
- disable an exercise.

The admin cannot edit or permanently delete an exercise. A wrong exercise is disabled. A corrected version is uploaded as a new exercise with a new ID.

Reports are stored separately, one report per row. Each report contains the exercise ID, the user ID, and a message of at most 100 characters. Reports do not disable an exercise automatically.

## Accounts and progress

The platform keeps local accounts and GitHub OAuth accounts separate. Local users have a password hash. GitHub users have a GitHub ID and no local password. Accounts are never joined automatically.

There is one admin created during setup. Students use predefined avatars. Disabled accounts cannot log in, but their attempts and progress remain stored.

Score, MMR, badges, levels, and leaderboards are included. Their exact rules are `TBD` and will be defined by the teammates responsible for those systems.

## Included

The features below and the work listed in the 15-point module plan are inside the current project scope. Details marked `TBD` still need a team decision.

- Responsive frontend, backend, database, and support for simultaneous users.
- Secure email and password login plus GitHub OAuth.
- Clear database relations and validation in the frontend and backend.
- HTTPS, ignored secrets, `.env.example`, Privacy Policy, and Terms of Service.
- Containerized setup that starts with one documented command.
- C function and complete-program exercises.
- JSON exercise upload and compiler validation before storage.
- RAG search over a controlled exercise library.
- An LLM limited to selecting retrieved exercise IDs and explaining its choice.
- Code submission through an existing isolated compiler runner.
- Attempts, reports, progress, score, MMR, badges, levels, and leaderboards.

## Left out

- Real-time games, WebSockets, matchmaking, and multiplayer logic.
- LLM-generated exercises.
- A machine-learning recommendation system based on student behaviour.
- Manual topic or exercise-type selection by students.
- Building our own C compiler.
- AI-generated correction messages or tutoring chat.
- Exercise votes, likes, and dislikes.
- Admin editing, permanent deletion, downloads, topic management, role management, or user management.
- Saving submitted code, full compiler errors, or submission dates.
- Uploaded avatars, friends, online status, chat, payments, and subscriptions.

## Still to decide

- Rules for score, MMR, badges, levels, and leaderboard ties.
- The frontend and main backend technologies.
- The compiler runner and deployment technologies.
- The LLM provider and model.
- The final exercise dataset, tags, and RAG similarity limit.
- How `time_taken` is measured.
- Product Owner, Project Manager, Technical Lead, and exact pull-request reviewers.

## Planned module points

The subject requires at least 14 module points. The current target is **15 points**. These points are planned and are not earned until every requirement is implemented and demonstrated.

| Module | Points | Current plan |
| --- | ---: | --- |
| Frontend and backend frameworks | 2 | Both technologies are `TBD`. |
| Public API | 2 | `TBD`; requires an API key, rate limits, documentation, at least five endpoints, and GET, POST, PUT, and DELETE. |
| ORM | 1 | `TBD`; normal SQL access does not earn this point. |
| GitHub OAuth | 1 | Selected. Email and password login remains mandatory. |
| Complete RAG | 2 | Core feature: large exercise library, retrieval, and a grounded answer. |
| Complete LLM interface | 2 | Provisional; must also provide streaming, errors, and rate limiting. |
| Advanced search | 1 | Admin search must include filters, sorting, and pagination. |
| Gamification | 1 | Badges, level or XP, and leaderboard with persistent rules and visual feedback. |
| Custom design system | 1 | At least ten reused components plus colours, typography, and icons. |
| Activity analytics | 1 | A real student activity and insights dashboard. |
| Health, status, backup, and recovery | 1 | All four parts must work, including a tested restore. |
| **Planned total** | **15** | **Nothing is counted until it works and passes evaluation.** |

The separate LLM module is the least certain part of this count because it shares the same student request with RAG. If evaluators do not accept it as a complete separate module, the plan falls to 13 points and needs a replacement before evaluation.

Mandatory requirements do not give module points. They still have to be complete or the project can be rejected.
