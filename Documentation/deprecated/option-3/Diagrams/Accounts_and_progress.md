# Accounts and progress

**William leads. Eliott builds the pages.** They share the progress and activity work.

Students register with email and password, or use the extra OAuth login option. A secure cookie keeps them signed in.

## What we build

- Registration, login, logout, and a profile summary.
- One progress record for each student and topic.
- A dashboard showing progress over time, badges and leaderboard (this is like the list of top winners)
- A simple admin permission, assigned through setup rather than a user-management page.
- Privacy and Terms pages that remain accessible without logging in. (This is bs but i think its mandatory for the subject)

React displays the information. Express checks who is asking. Prisma reads and saves it in PostgreSQL.

## Main connections

| Other system | Information we exchange |
| --- | --- |
| Correction | A finished submission and its result |
| Rewards | First successful completion, topic, and exercise level |
| Recommendations | Earlier results and topic progress, without passwords or emails |
| Admin | Whether this account can edit exercises |

Correction saves a result and its reward together. A repeated request cannot award the same exercise twice. Changing an exercise version should not become a way to farm points.

## Pages and routes

(We can still discuss if we want to do less and merge some of them together)

Pages: `/register`, `/login`, `/dashboard`, `/progress`, `/profile`, `/privacy`, `/terms`.

Backend routes: `/api/v1/auth/*`, `GET /api/v1/users/me`, `GET /api/v1/progress`, and `GET /api/v1/activity`. The [route guide](Routes_explained.md) lists every action and its access rules.

We validate forms in the page and again on the backend. Passwords are stored as salted hashes. Students cannot read another person's private submissions by changing an ID in the address.

## What we should demonstrate

Two students can register and work independently. Logout ends access. A completed exercise changes the right student's progress once. Refreshing the page keeps their results.

Basic secure accounts are mandatory (subject p.9). OAuth is 1 point and an activity dashboard is another possible 1 point (p.14). Basic admin access alone does not earn the advanced permissions module.

[System diagram](01-accounts-and-progress.mmd)
