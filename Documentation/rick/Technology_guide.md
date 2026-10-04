# My technology guide

My part has three jobs:

1. store the platform data;
2. find exercises that match a student's request;
3. ask an LLM to choose from those matches.

I use one PostgreSQL database. Normal data and exercise vectors live in the same database.

The complete path is:

> JSON request → FastAPI and Pydantic → Python → Psycopg and SQL → PostgreSQL and pgvector → Sentence Transformers → LLM → JSON response

## Confirmed technologies

| Technology | What I use it for |
| --- | --- |
| Python | Write my database, search, RAG, and LLM code |
| HTTP and JSON | Communicate with the main backend |
| FastAPI | Create the internal addresses that receive and return JSON |
| Pydantic | Check that JSON has the expected fields and types |
| PostgreSQL | Store users, exercises, attempts, and reports |
| SQL | Create tables and read or change rows |
| JSONB | Store lists and nested data such as tests, tags, hints, and badges |
| Psycopg | Let Python send SQL to PostgreSQL |
| Sentence Transformers | Turn text into vectors |
| pgvector | Store vectors and find similar exercises |
| RAG | Retrieve trusted exercises before asking the LLM |

The LLM provider, model, and Python library are still `TBD`. The final database migration tool is also `TBD`; numbered SQL files are enough while learning the first version.

## 1. Python

**What it is:** The programming language used for my service.

**My use:** Control the database work, create vectors, search exercises, call the LLM, and prepare JSON responses.

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

**My use:** Store users, exercises, attempts, and reports in related tables.

**Learn first:**

- tables, rows, columns, and data types;
- primary keys and foreign keys;
- `NOT NULL`, `UNIQUE`, and `CHECK` rules;
- `INSERT`, `SELECT`, `UPDATE`, and `JOIN`;
- transactions;
- simple indexes;
- numbered files for database changes.

**JSONB:** Use it for real lists or nested values, such as tests and tags. Normal fields and table relationships should remain normal columns.

**First practice:** Create the four tables, add one user and one exercise, then save and read one attempt.

## 3. Psycopg

**What it is:** The Python library that communicates with PostgreSQL.

**My use:** Send SQL from Python and receive database results.

**Learn first:**

- opening and closing a connection;
- parameterized queries;
- committing and rolling back a transaction;
- reading returned rows;
- connection pools.

**Main rule:** Always pass values as query parameters. Never join user text directly into an SQL command.

**First practice:** Insert an exercise from Python and read it back using its ID.

## 4. HTTP and JSON

**What they are:** HTTP carries requests between services. JSON is the format of the information inside those requests.

**My use:** The main backend sends checked JSON to my Python service. My service returns checked JSON.

**Learn first:**

- request and response bodies;
- `GET` and `POST`;
- status codes;
- headers;
- validation, missing-record, and internal errors.

**First practice:** Send a small JSON request with `curl` or an API client and inspect the response.

## 5. FastAPI and Pydantic

**What they are:** FastAPI creates the Python web service. Pydantic describes and checks the data accepted by each route.

**My use:** Receive database requests, validated exercises, and student learning requests from the main backend.

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

**My use:** Create vectors from exercise information and student requests.

**Learn first:**

- loading one model once;
- encoding one text and several texts;
- vector dimensions;
- using the same model for exercises and requests.

Changing the model later means recreating every stored exercise vector. The exact model is still `TBD`.

**First practice:** Encode three short C-learning sentences and check which two are closest.

## 7. pgvector

**What it is:** A PostgreSQL extension that stores and compares vectors.

**My use:** Filter enabled exercises by level and return the exercises whose vectors are closest to the student's request.

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

**My use:** Retrieve existing exercises. The LLM may choose only one returned exercise ID and explain the choice.

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

**My use:** Choose from the retrieved exercise IDs and write a short reason.

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
2. Create the PostgreSQL tables with SQL.
3. Read and write those tables from Python with Psycopg.
4. Put one database action behind a FastAPI route checked by Pydantic.
5. Create embeddings for a few exercises.
6. Store and search them with pgvector.
7. Build the complete RAG search without an LLM.
8. Add the LLM after the search returns reliable candidates.
9. Connect the service to the main backend.
10. Test valid, invalid, missing, failed-service, and simultaneous requests.

## What I do not need yet

- A second vector database such as Pinecone or Weaviate. pgvector keeps the vectors in PostgreSQL.
- LangChain or LlamaIndex. This first RAG flow is small enough to write directly.
- Model training or fine-tuning. Sentence Transformers uses an existing model.
- A machine-learning recommendation system. It is outside the current plan.
- Frontend frameworks, OAuth implementation, C compiler internals, or the DevOps setup.
- PostgreSQL triggers, stored procedures, partitioning, replication, or other advanced features.

## Decisions to keep clear

The main backend and my FastAPI service should not both write the same tables independently. The team needs one clear owner for every write path.

Raw SQL through Psycopg does not satisfy the planned ORM module. If the team keeps that point, it must select and use an ORM separately.

The database work supports mandatory requirements and gives no module points by itself. The planned complete RAG module is worth 2 points. The separate LLM-interface module remains provisional because the subject also requires streaming, error handling, and rate limiting.
