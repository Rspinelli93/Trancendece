# How the database and Docker setup work together

## The idea in one sentence

The services save their information in one PostgreSQL database, and Docker Compose starts the database before starting the services.

```text
Main backend service ── users, attempts and reports ──> PostgreSQL
AI/RAG service ──────── exercises and vectors ───────> PostgreSQL
Code-checking service ─ no database connection
```

There is only **one database**. Inside it, tables separate the different types of information.

## Which service uses each table

### Main backend service

The main backend connects directly to PostgreSQL for:

- users;
- attempts;
- reports;
- scores, MMR, badges, and levels.

### AI/RAG service

The AI/RAG service connects directly to PostgreSQL for:

- exercises;
- exercise vectors.

When the main backend needs exercise information, it asks the AI/RAG service through an internal API. When the AI/RAG service needs student information, the main backend includes the necessary values in its JSON request.

### Code-checking service

The code-checking service does not connect to PostgreSQL. It receives temporary C code and tests, runs them, and returns a result.

## What the technologies mean

### PostgreSQL

PostgreSQL is the program that stores the data. A table works like a spreadsheet: every row is one saved item and every column is one value.

For example, one row in the exercises table is one exercise.

### pgvector

pgvector is an extra feature added to PostgreSQL. It lets the exercises table store the list of numbers used by RAG to compare meanings.

This means normal exercise data and vectors can stay in the same database.

### SQLAlchemy

SQLAlchemy is the ORM used by the AI/RAG service. An ORM lets Python work with database rows as Python objects.

For example, the service creates an `Exercise` object in Python. SQLAlchemy translates that action into the SQL needed to save a row in PostgreSQL.

### Psycopg

Psycopg is the connection between SQLAlchemy and PostgreSQL. SQLAlchemy prepares the database operation, and Psycopg sends it to PostgreSQL.

Most of the AI/RAG code uses SQLAlchemy directly. Psycopg works underneath it.

### Alembic and migrations

Alembic manages changes to the database structure.

A migration is a file containing one change, such as:

- create the exercises table;
- add the `embedding` column;
- add the `status` column.

The migration files are saved in Git. This lets every team member create the same database structure in the same order.

### Docker Compose

Docker Compose starts the parts of the project in the correct order. For the database, it must:

1. start PostgreSQL with pgvector;
2. keep the data in a persistent volume;
3. check that PostgreSQL is ready;
4. run the migrations;
5. start the application services only if the migrations succeed.

A persistent volume is the folder managed by Docker where PostgreSQL keeps its data. Restarting the container must not erase the database.

## What needs to be prepared

### The AI/RAG service provides

- the SQLAlchemy model for the exercises table;
- the Alembic migration files;
- the Python functions that save, read, search, and disable exercises;
- a `DATABASE_URL` setting telling the service where PostgreSQL is;
- clear success and error responses.

### The main backend service provides

- the structure and database code for users, attempts, reports, and progress;
- its migration command after its backend technology is selected;
- the JSON requests sent to the AI/RAG and code-checking services.

### The DevOps setup provides

- the PostgreSQL container with pgvector;
- the database name, username, and password through environment variables;
- the persistent volume;
- the PostgreSQL health check;
- the command that runs migrations before the services start;
- backups and recovery later in the project.

Real passwords stay in a local `.env` file. The repository contains only an `.env.example` showing which values are needed.

## The seven build steps

### Step 1: decide who owns the data

This is already decided:

- the main backend owns user, attempt, report, and progress data;
- the AI/RAG service owns exercises and vectors;
- the code-checking service stores nothing.

Ownership means that one service is responsible for changing that data. This avoids two services changing the same row in different ways.

### Step 2: describe the tables

The service defines what one row contains and which values are required.

For an exercise, this includes its ID, title, level, tags, instructions, tests, status, and vector.

In the AI/RAG service, this description is written as a SQLAlchemy model.

### Step 3: create a migration

Alembic compares the SQLAlchemy model with the current database structure and creates a migration file.

The migration is reviewed before it is used. It explains exactly what will be created or changed.

### Step 4: start PostgreSQL

Docker Compose starts PostgreSQL and its persistent volume. The services do not start immediately because PostgreSQL may need a few seconds before it can accept connections.

### Step 5: run the migrations

After the PostgreSQL health check succeeds, Docker runs:

```bash
alembic upgrade head
```

This means: apply every migration that has not been applied yet.

If a migration fails, startup stops. The services must not run with the wrong database structure.

### Step 6: write the database functions

The AI/RAG service needs small Python functions for actions such as:

- save an exercise;
- find an exercise by ID;
- search exercises by vector;
- disable an exercise.

These functions use SQLAlchemy. A complete change runs inside a transaction.

A transaction means “save everything or save nothing.” If saving fails halfway, PostgreSQL cancels the complete change. This is called a rollback.

### Step 7: connect the API

FastAPI receives JSON from the main backend. It checks the JSON, calls the correct database function, and returns JSON.

```text
Main backend
    ↓ JSON request
FastAPI route
    ↓ checked Python data
Database function
    ↓ SQLAlchemy and Psycopg
PostgreSQL
    ↓ result
FastAPI JSON response
    ↓
Main backend
```

## Complete example: saving one exercise

Suppose an admin uploads an `ft_strlen` exercise.

1. The main backend checks that the JSON has the required fields.
2. The code-checking service compiles the reference solution and runs every test.
3. If a test fails, the upload stops. Nothing is sent to the AI/RAG service.
4. If every test passes, the main backend sends the validated exercise to the AI/RAG service.
5. The AI/RAG service checks the JSON again.
6. It creates the exercise vector.
7. It creates an `Exercise` object with SQLAlchemy.
8. SQLAlchemy uses Psycopg to save the row in PostgreSQL.
9. PostgreSQL confirms the save.
10. The AI/RAG service returns the exercise ID and a success response.

The exercise is saved only after the compiler tests and vector creation succeed.

## What happens when something fails

### PostgreSQL is still starting

Docker waits. The application services do not start yet.

### A migration fails

Startup stops and the migration error appears in the logs. The database problem must be corrected before restarting.

### Exercise JSON is wrong

The AI/RAG service rejects it and explains which field is missing or invalid. Nothing is saved.

### Vector creation fails

The exercise is not saved because it would not work with RAG.

### Saving fails

The transaction is rolled back. No incomplete exercise remains in the database.

### No exercise matches a student's request

The search completed correctly but found nothing suitable. This is a normal answer:

```json
{
  "matched": false,
  "exercise_id": null,
  "reason": "No suitable exercise was found for your request."
}
```

### PostgreSQL, the vector model, or the LLM is unavailable

This is a technical failure, so it must not be called “no match.” The service returns:

```json
{
  "success": false,
  "error_code": "SERVICE_UNAVAILABLE",
  "message": "The exercise service is temporarily unavailable.",
  "request_id": "request-123"
}
```

The request ID is a simple identifier added to the request. It helps find the related technical message in the logs.

## First test to do together

1. Start PostgreSQL with Docker Compose.
2. Check that Docker reports PostgreSQL as healthy.
3. Check that the migration finishes successfully.
4. Send one validated exercise to the AI/RAG service.
5. Read the exercise back using its ID.
6. Stop and restart the containers.
7. Read the exercise again to prove that the volume kept the data.

SQLAlchemy supports the planned **1-point ORM module**. The separate services and REST APIs support the planned **2-point backend-as-microservices module**. These points are planned until the complete behaviour is implemented and demonstrated.
