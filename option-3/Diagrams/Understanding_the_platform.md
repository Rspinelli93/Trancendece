# How the platform works

We want students to learn C by solving exercises. They choose a topic, write code, submit it, and see whether it passes. Their progress is saved separately for each topic.

We start with free accounts, C only, and at most five topics. Badges, levels, and a leaderboard give students progress to follow. There are no live matches or sockets.

## A few words we will use

| Word | Meaning here |
| --- | --- |
| Frontend | The pages students and admins use |
| Backend | Our program that checks requests and runs the platform |
| Route | An address for a page or a backend action |
| Controller | The function that handles a backend request |
| Database | Where accounts, exercises, and results are saved |
| JSON | A text format with named fields, used for exercise files |
| LLM | The AI model that writes new exercise drafts |
| RAG | Finding useful saved examples and giving them to the LLM |
| Worker | A background process that handles slower jobs |
| Polling | Asking again after a short wait to see if a job is finished |

## The student's path

Create an account → choose a topic → open an exercise → write C → submit → see the result → continue learning.

The student sees a loading message while correction runs. Our backend returns a job ID immediately. The page checks that job until it is finished. Several students can work at once.

After three unsuccessful attempts, we can offer an easier exercise. We do not remove an earned level. The exact scoring and level rules are still for us to decide.

## Where exercises come from

**Admin uploads:** we paste JSON or upload one or many files. The platform checks their structure, compiles the reference solutions, and runs the tests. We see passed and failed files, then confirm which passed files to save. Only then do those exercises enter the database and RAG.

**Generated exercises:** when we need more content, a background job finds suitable RAG examples and asks the LLM for a new exercise. After technical validation, a student can receive it as a trial. It enters the RAG only after a student's solution passes.

For the first build, we can request generation when a student needs an exercise and no suitable saved one is available. The topic and level come from the page; there is no chat or admin prompt screen. Generation limits and provider are still to be chosen.

## The tools

| Tool | Its job |
| --- | --- |
| React + shared CSS | Pages and our reusable buttons, forms, cards, and other controls |
| Express + Node.js | Accounts, routes, exercise rules, and results |
| Prisma + PostgreSQL | Read and save normal application data |
| pgvector in PostgreSQL | Find similar approved material for RAG |
| LLM and an embedding model | Generate drafts; turn text into numbers for similarity search |
| Judge0 with a C compiler | Run code in isolation and return execution results |
| Python + scikit-learn | Train and run the exercise recommendation model |
| Nginx + Docker Compose | HTTPS, page files, and starting the services together |

These are the working technology choices. The LLM provider, code editor, and exact versions still need a small setup check.

## How the parts talk

The browser talks only to our Express backend. Express reads the database and asks the worker to handle generation or correction. The worker talks to the LLM, Judge0, and the recommendation code as needed.

The API and worker can share the same codebase and database. The worker uses a different start command so a slow compilation does not hold up login or page requests. Python recommendation scripts can run inside the worker; we do not need a separate ML website or public server.

The database is our main record of each exercise. RAG is a searchable collection of eligible exercise versions inside that database. Disabling an exercise makes it unavailable to both new students and RAG retrieval.

See [the overview](00-system-overview.mmd) and [routes](Routes_explained.md).

## What we keep simple

We keep one main backend, ordinary HTTP requests, a small admin page, a fixed topic list, and simple correction messages. The backend uses routes → controllers → shared functions → database access.

We leave out live game logic, chat, a student AI assistant, a full user-management panel, and a compiler written by us. We still write the tests and the code that connects our platform to Judge0.

The subject requires a complete web app and simultaneous users (pp.7–9). Our proposed modules and their conditions are in [Subject and points](Subject_and_points.md).
