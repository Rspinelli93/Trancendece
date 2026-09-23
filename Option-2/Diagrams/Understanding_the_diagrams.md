# How it fits together

| Part | Job | Tool |
| --- | --- | --- |
| Frontend | Pages, questions, buttons, scores | React |
| Backend | Accounts, matches, answer checking | Express + Socket.IO |
| Database | Users, questions, answers, results | PostgreSQL through Prisma |
| Front door | HTTPS, page files, forwarding requests | Nginx |

[Whole-system diagram](00-system-overview.mmd)


## Keeping the structure simple


- **Page:** what the player sees and interacts with.
- **Route:** the backend address the page contacts to request an action, such as logging in.
- **Controller:** the function that handles that request.
- **Database:** where we save accounts, questions, and results.
- **Prisma:** the tool our backend uses to read and update the database.

For example, when someone logs in:
>Login page → login route → controller checks the account → database returns the account → backend replies to the page.

Accounts and game logic stay in separate folders inside one backend. We share functions when several parts need the same behaviour.

### What we left out
- Separate backends for different features.
- Extra layers that only pass information between functions.
- The LLM and the system for running submitted C code.

## Two ways to communicate

**Normal requests:** log in, load the leaderboard, read a saved result.

**Live messages:** join the queue, receive a question, submit an answer, receive updated scores. Socket.IO keeps this conversation open.

[Routes](Routes_explained.md) lists both.

## One match

>Two or more players log in → join the queue → receive the same questions → answer → receive scores → finish → see the saved result.

>The backend controls deadlines, marking, and scores. The browser displays them.

>We keep live connections and timers in memory. We save questions, submissions, and results in the database. Each match has its own state, so several matches can run together.

>A reconnect receives the current state. A whole-server crash is different: for a first version, we could cancel interrupted matches without awarding unfinished results.

## Running it

- Three containers: Nginx, our backend, and PostgreSQL, started together with Compose. React's built files are served by Nginx.

- One secure login cookie identifies the player for both normal requests and live messages. Private answers, password hashes, and access keys stay on the server.

- The required architecture, containers, and HTTPS are on subject pp.8–9. Frameworks, live features, and Prisma's ORM module are on p.12.
