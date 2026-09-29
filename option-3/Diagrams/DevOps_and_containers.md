# DevOps and containers

**Garance leads. Julien helps with Judge0. William helps with the database and backups.**

DevOps covers how we start, run, and maintain the platform.

After downloading the project and following the setup instructions, one command should start everything. We use containers to package each service with the tools it needs.

## The parts we run

| Part | What it does |
| --- | --- |
| Nginx | Receives website requests, provides HTTPS, and sends them to the right place |
| Express backend | Handles login, exercises, submissions, and saved progress |
| Background worker | Handles slower tasks, such as generating exercises and checking code |
| PostgreSQL with pgvector | Saves our data and helps find useful examples for the LLM |
| Judge0 | Compiles and runs C code in a separate environment |

The backend and worker use the same project code, but run separately. This is important because it lets the users continue using the website while code is being checked/corrected.

The Python recommendation code initially runs alongside the worker. Our chosen AI provider supplies the LLM and the model used to find similar exercises.

Judge0 needs several supporting services of its own. Garance and Julien will include these in the startup configuration and test them.

## Tasks that take time and we have to be careful of

Compiling code or generating an exercise.

Instead of making the page wait without a response:

1. The backend accepts the task and returns a tracking ID.
2. The worker starts processing it.
3. The page checks its progress every few seconds.
4. When it finishes, the page shows the result.

This repeated progress check is called **polling**. It does not need sockets.

We save student submissions and generation tasks in the database. If the server restarts, we can identify unfinished work and retry it. Each task is handled once, so a retry cannot give a student extra points.

## Temporary admin uploads

Uploaded exercise files stay in a temporary folder while we check them.

The admin sees which exercises passed and which failed. Only the passed exercises they confirm are added to the permanent exercise library.

Discarded or expired uploads are cleared from temporary storage. If an unfinished upload is lost after a restart, the admin uploads it again.

## Running code safely

Student code and LLM-generated code run inside Judge0, separately from the main application.

They cannot access our database, passwords, or API keys. We also restrict network access and limit memory, running time, files, processes, and output.

The student's browser sends code to our backend. Our worker sends it to Judge0. Students cannot control Judge0 directly.

Before connecting everything, Garance and Julien test:

- A correct C program.
- A program that never stops.
- A program that prints too much.
- A program that crashes.
- The memory-checking tool, if we include memory-leak detection.

## Starting the platform

The setup instructions must explain how to:

- Install the required tools.
- Fill in the configuration using `.env.example` as a template.
- Create the database tables.
- Add our fixed topics and initial admin accounts.
- Start all services with one command.

Real passwords and API keys stay out of Git. Admin accounts are assigned during setup; we do not need a user-management page.

## Showing whether the platform works

We add two simple checks:

- `/health`: lets our tools check whether the backend is ready.
- `/status`: shows users whether the main services are working.

If exercise generation stops working, students can still use saved exercises. If correction stops working, the page explains that submissions are waiting or need to be retried.

These pages show useful status information without exposing passwords, internal addresses, or detailed server errors.

## Backups and recovery

We automatically save copies of accounts, progress, exercises, and the information needed to restore RAG search.

Backups are stored separately from the live database. We also test restoring a backup, so we know it works if data is lost.

Logs record useful events and errors to help us fix problems. They should not contain passwords, private solutions, or complete student submissions.

Containers, HTTPS, protected credentials, and documented setup support the mandatory requirements on subject pages 8–9.

Health checks, a status page, automatic backups, and recovery instructions together support the proposed **1-point DevOps module** on page 19.

[System diagram](06-devops-and-containers.mmd)