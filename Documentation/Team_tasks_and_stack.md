# Team tasks and technologies

The responsibilities below follow the application flow: frontend, backend, exercise checking, AI and database, then DevOps. Each lead builds their system and checks its connection with the next person.

Every team member must also contribute to the mandatory core. Product Owner, Project Manager, Technical Lead, and exact pull-request reviewers are still `TBD`.

The backend is split into three services. William leads the main backend, Rick leads the AI/RAG service, and Julien leads the code-checking service with Garance handling its safe execution. The services communicate through REST APIs using JSON.

## 1. Frontend — Eliott

Eliott leads the student pages, admin page, progress pages, and shared visual components.

The connected feature owners check their pages:

- William checks registration, login, and account pages.
- Julien checks exercise upload, exercise view, submission, and result pages.
- Rick checks the learning request and RAG answer.

## 2. Main backend and accounts — William

William leads email/password accounts, sessions, GitHub OAuth, permissions, and the main application routes.

He connects the frontend with exercise checking, the database, and AI. Eliott checks the page-to-backend flow, Julien checks exercise routes, and Rick checks the database formats.

## 3. Exercises and code checking — Julien

Julien leads the exercise JSON format, upload validation, forbidden-function checks, private tests, compiler integration, and student submission results.

For every reference solution or student submission, this system must:

1. insert the code into the prepared compiler code;
2. reject forbidden functions;
3. run every test inside the isolated runner;
4. compare the real output with the expected output;
5. return one controlled success or failure result.

Garance checks safe execution and runner limits. William checks the backend route. Eliott checks the result shown on the page. The AI/RAG service handles exercise data, while the main backend stores attempts.

## 4. Database, AI, and RAG — Rick

Rick leads the database structure, exercise vectors, RAG search, LLM communication, and the internal Python API.

Julien checks that only valid exercises and IDs enter this flow. Eliott checks what the student sends and receives. William checks how accounts and the main backend use the database.

Rick designs the shared database structure. Normal account, progress, attempt, and report actions pass through the main backend. The AI/RAG service uses the exercise information and vectors needed for search. The code-checking service does not access the application database directly.

## 5. DevOps and safe execution — Garance

Garance leads containers, HTTPS, startup, runner isolation, health checks, backups, and recovery.

Julien checks that the C runner starts and handles valid code, wrong output, compilation errors, infinite loops, excessive output, and crashes. William checks health routes and database restoration.

## Who checks each system

| System | Lead | Connection checked by |
| --- | --- | --- |
| Frontend | Eliott | William for accounts; Julien for exercises; Rick for AI |
| Main backend and accounts | William | Eliott for pages; Julien for exercise routes; Rick for database data |
| Exercises and C checking | Julien | Garance for isolation; William for routes; Eliott for results; Rick for stored data |
| Database, AI, and RAG | Rick | William for backend use; Julien for valid exercises; Eliott for the student answer |
| Containers and startup | Garance | William for health and recovery; Julien for the runner |

Every complete flow must also be tested once by someone who did not build it. Exact source-code approval pairs remain `TBD`.

## Technology choices

Technologies outside the database and AI work remain `TBD` until next meeting.

| Part | Owner | Technology |
| --- | --- | --- |
| Frontend and styling | Eliott | `TBD` |
| Main backend and sessions | William | `TBD` |
| GitHub login | William | GitHub OAuth; library is `TBD` |
| Exercise checking | Julien | Existing isolated C runner; product is `TBD` |
| Database and ORM | Rick | PostgreSQL, pgvector, JSONB, SQLAlchemy, Alembic, and Psycopg |
| AI and RAG API | Rick | Python, FastAPI, and Pydantic |
| Exercise vectors | Rick | Sentence Transformers |
| LLM connection | Rick | Provider, model, and Python library are `TBD` |
| Containers, HTTPS, health, and backups | Garance | `TBD` |
| Communication format | Everyone | REST APIs with checked JSON; browser connections use HTTPS |

## First shared milestones

1. Eliott and William: register, log in, and open the student page.
2. Main backend service: create and read a user in its owned tables.
3. Julien and Garance: run a prepared C test safely and return a controlled result.
4. Eliott, William, Julien, and Rick: upload one exercise, validate it, create its vector, store it, and show the result.
5. Eliott, William, and Rick: send a learning request and display an existing matched exercise.
6. Eliott, William, Julien, and Rick: submit C code, display the result, and save one attempt.
7. The full team: test simultaneous users, failed services, invalid uploads, disabled exercises, hidden test protection, and clean startup.
