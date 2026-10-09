# AI/RAG technology guide

The AI/RAG service has three jobs:

1. store and retrieve exercises;
2. find exercises that match a student's request;
3. ask an LLM to choose from those matches.

The platform uses one PostgreSQL database. The main backend service owns users, attempts, and reports. The AI/RAG service owns exercises and their vectors.

The complete path is:

> JSON request → FastAPI and Pydantic → Python → SQLAlchemy → Psycopg → PostgreSQL and pgvector → Sentence Transformers → LLM → JSON response

## Confirmed technologies

| Technology | Use |
| --- | --- |
| Python | Write the exercise database, search, RAG, and LLM code |
| HTTP and JSON | Communicate with the main backend |
| FastAPI | Create the internal addresses that receive and return JSON |
| Pydantic | Check that JSON has the expected fields and types |
| PostgreSQL | Store the platform data in one database |
| SQL | Create tables and read or change rows |
| JSONB | Store exercise lists such as tests, tags, and hints |
| SQLAlchemy | Read and write PostgreSQL through Python objects |
| Alembic | Create and update the AI/RAG database tables |
| Psycopg | Connect SQLAlchemy to PostgreSQL |
| Sentence Transformers | Turn text into vectors |
| pgvector | Store vectors and find similar exercises |
| RAG | Retrieve trusted exercises before asking the LLM |

The LLM provider, model, and Python library are still `TBD`.

## 1. Python

**What it is:** The programming language used by the AI/RAG service.

**Use in the AI/RAG service:** Control exercise storage, create vectors, search exercises, call the LLM, and prepare JSON responses.

**Learn first:**

- variables, strings, lists, and dictionaries;
- conditions, loops, and functions;
- modules and imports;
- type hints;
- exceptions;
- virtual environments and package installation.

**First practice:** Read one exercise dictionary, check a few fields, and create a smaller public dictionary from it.

## 2. SQL and PostgreSQL

**What they are:** PostgreSQL is the database. SQL is the language used to work with it.

**Use in the AI/RAG service:** Understand the complete database structure and store exercises and vectors.

**Learn first:**

- tables, rows, columns, and data types;
- primary keys and foreign keys;
- `NOT NULL`, `UNIQUE`, and `CHECK` rules;
- `INSERT`, `SELECT`, `UPDATE`, and `JOIN`;
- transactions;
- simple indexes;
- migrations for database changes.

**JSONB:** Use it for real lists or nested values, such as tests and tags. Normal fields and table relationships should remain normal columns.

**First practice:** Create an exercise table, add one exercise, and read it again.

## 3. SQLAlchemy, Alembic, and Psycopg

**What they are:** SQLAlchemy is the ORM used by Python. Alembic manages database changes. Psycopg connects SQLAlchemy to PostgreSQL.

**Use in the AI/RAG service:** Describe the exercise table, save and retrieve exercises, and apply database changes in the same order on every computer.

**Learn first:**

- SQLAlchemy models, sessions, and basic queries;
- adding, reading, updating, and filtering rows;
- committing and rolling back a transaction;
- creating an Alembic migration;
- running `alembic upgrade head`;
- the PostgreSQL connection address.

**Main rule:** Use one transaction for one complete database change. If it fails, roll it back so incomplete data is not saved.

**First practice:** Create the exercise model, run its migration, save one exercise, and read it back using its ID.

## 4. HTTP and JSON

**What they are:** HTTP carries requests between services. JSON is the format of the information inside those requests.

**Use in the AI/RAG service:** The main backend sends checked JSON to the Python service. The service returns checked JSON.

This is required by the microservices plan because the main backend and AI/RAG service are separate programs. JSON is the message format; HTTP is how that message travels between them.

**Learn first:**

- request and response bodies;
- `GET` and `POST`;
- status codes;
- headers;
- validation, missing-record, and internal errors.

**First practice:** Send a small JSON request with `curl` or an API client and inspect the response.

## 5. FastAPI and Pydantic

**What they are:** FastAPI creates the Python web service. Pydantic describes and checks the data accepted by each route.

**Use in the AI/RAG service:** Receive validated exercises and student learning requests from the main backend service.

**Learn first:**

- routes, also called endpoints;
- request and response models;
- required and optional fields;
- lists and nested objects;
- allowed values;
- controlled errors;
- a simple health route.

**First practice:** Create one route that accepts a level and a query, rejects levels outside `1`–`3`, and returns checked JSON.

## 6. Sentence Transformers and embeddings

**What they are:** Sentence Transformers turns text into a fixed-size list of numbers. This list is called an embedding or vector. Texts with similar meanings should have similar vectors.

**Use in the AI/RAG service:** Create vectors from exercise information and student requests.

**Learn first:**

- loading one model once;
- encoding one text and several texts;
- vector dimensions;
- using the same model for exercises and requests.

Changing the model later means recreating every stored exercise vector. The exact model is still `TBD`.

**First practice:** Encode three short C-learning sentences and check which two are closest.

## 7. pgvector

**What it is:** A PostgreSQL extension that stores and compares vectors.

**Use in the AI/RAG service:** Filter enabled exercises by level and return the exercises whose vectors are closest to the student's request.

**Learn first:**

- enabling the extension;
- the `vector` column type;
- cosine distance;
- returning the closest results (`top-k`);
- combining vector search with normal SQL filters;
- using a minimum similarity limit.

Start with a normal vector search. HNSW or IVFFlat indexes are useful only when the dataset becomes large enough to need them.

**First practice:** Store several exercise vectors and return the closest three for one request vector.

## 8. RAG

**What it is:** RAG first retrieves trusted information. It then gives that information to an LLM so the answer stays connected to existing data.

**Use in the AI/RAG service:** Retrieve existing exercises. The LLM may choose only one returned exercise ID and explain the choice.

**Learn first:**

- creating the text used for search;
- filtering by level and enabled status;
- choosing how many results to keep;
- setting a minimum similarity limit;
- deciding which public fields go to the LLM;
- checking that the final ID exists in the retrieved list.

**First practice:** Build the complete search without an LLM. Given a level and request, return the closest exercise or `no match`.

## 9. LLM API — choice still TBD

**What it is:** A service interface that sends a prompt to a language model and returns generated text.

**Use in the AI/RAG service:** Choose from the retrieved exercise IDs and write a short reason.

**Learn after the RAG search works:**

- API keys stored in environment variables;
- prompts;
- structured JSON responses;
- timeouts and retries;
- rate limits;
- service errors;
- checking every returned ID;
- streaming if the team keeps the separate LLM-interface module.

**First practice:** Give the model three fixed exercise candidates, require one of their IDs, and reject an invented ID.

## Learning order

1. Learn basic Python and work with dictionaries that look like our JSON.
2. Learn the PostgreSQL table structure and basic SQL.
3. Create the exercise model and an Alembic migration with SQLAlchemy.
4. Put one database action behind a FastAPI route checked by Pydantic.
5. Create embeddings for a few exercises.
6. Store and search them with pgvector.
7. Build the complete RAG search without an LLM.
8. Add the LLM after the search returns reliable candidates.
9. Connect the service to the main backend.
10. Test valid, invalid, missing, failed-service, and simultaneous requests.

## Not needed yet

- A second vector database such as Pinecone or Weaviate. pgvector keeps the vectors in PostgreSQL.
- LangChain or LlamaIndex. This first RAG flow is small enough to write directly.
- Model training or fine-tuning. Sentence Transformers uses an existing model.
- A machine-learning recommendation system. It is outside the current plan.
- Frontend frameworks, OAuth implementation, C compiler internals, or the DevOps setup.
- PostgreSQL triggers, stored procedures, partitioning, replication, or other advanced features.

## Decisions to keep clear

The main backend service owns users, progress, attempts, and reports. The AI/RAG service owns exercises and vectors. The code-checking service does not access the application database.

SQLAlchemy is the selected ORM for the AI/RAG service. The ORM module is worth 1 planned point. The backend-as-microservices module is worth 2 points, but only if the three services have clear responsibilities and real REST interfaces. The planned complete RAG module is worth 2 points. The separate LLM-interface module remains provisional because the subject also requires streaming, error handling, and rate limiting.
