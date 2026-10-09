# Database structure and ownership

The platform uses one PostgreSQL database. The information is separated into four tables, and each table has one service responsible for changing it.

## How a database request moves

1. The main backend service reads and changes users, attempts, and reports directly.
2. The AI/RAG service reads and changes exercises and vectors.
3. The services exchange exercise information through REST APIs using JSON.

The AI/RAG service uses **SQLAlchemy**. SQLAlchemy connects to PostgreSQL through **Psycopg**.

## Diagram

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#fffdf7","primaryTextColor":"#1f2937","lineColor":"#84a98c","clusterBkg":"#f7fee7","clusterBorder":"#86efac"}}}%%
flowchart TD
    Key["LEGEND / HOW TO READ THIS MAP<br/>Rounded box = service<br/>Database shape = one table<br/>Orange = main backend data<br/>Green = AI/RAG data<br/>Dotted line = ID connection"]
    Backend["MAIN BACKEND SERVICE<br/>Accounts, progress, attempts, and reports"]
    AI["AI/RAG SERVICE<br/>Exercises, vectors, and search"]

    subgraph Database["ONE POSTGRESQL DATABASE"]
        Users[("USERS TABLE<br/>One row = one account<br/><br/>ID, username, email, login information,<br/>role, status, avatar, score, MMR, badges<br/>(PostgreSQL)")]
        Exercises[("EXERCISES TABLE<br/>One row = one validated exercise<br/><br/>ID, title, level, tags, instructions, hints,<br/>private tests, status, search vector<br/>(PostgreSQL + JSONB + pgvector)")]
        Attempts[("EXERCISE ATTEMPTS TABLE<br/>One row = one submitted attempt<br/><br/>User ID, exercise ID, success,<br/>attempt number, time taken<br/>(PostgreSQL)")]
        Reports[("REPORTS TABLE<br/>One row = one report message<br/><br/>User ID, exercise ID,<br/>message of at most 100 characters<br/>(PostgreSQL)")]
    end

    Key ~~~ Backend
    Backend --> Users
    Backend --> Attempts
    Backend --> Reports
    AI --> Exercises

    Attempts -. "user_id" .-> Users
    Attempts -. "exercise_id" .-> Exercises
    Reports -. "user_id" .-> Users
    Reports -. "exercise_id" .-> Exercises

    classDef note fill:#fff7ed,stroke:#f59e0b,color:#1f2937,stroke-width:2px;
    classDef backend fill:#fff7ed,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef ai fill:#ecfdf5,stroke:#22c55e,color:#1f2937,stroke-width:2px;
    classDef users fill:#fff7ed,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef exercises fill:#f0fdf4,stroke:#22c55e,color:#1f2937,stroke-width:2px;
    classDef joining fill:#fefce8,stroke:#84cc16,color:#1f2937,stroke-width:2px;
    class Key note;
    class Backend backend;
    class AI ai;
    class Users users;
    class Exercises exercises;
    class Attempts,Reports joining;
    style Database fill:#fffdf7,stroke:#86efac,stroke-width:2px,color:#1f2937;

    linkStyle default stroke:#84a98c,stroke-width:2px;
    linkStyle 1,2,3 stroke:#fb923c,stroke-width:3px;
    linkStyle 4 stroke:#22c55e,stroke-width:3px;
```


## Users table

One row represents one account.

It stores the user ID, username, email, protected login information, role, status, predefined avatar, total score, MMR, and earned badge IDs.

Local accounts have a password hash. GitHub accounts have a GitHub ID instead.

**Technology:** PostgreSQL. Badge IDs are stored as a list (**JSONB**).

**Owner:** Main backend service.

## Exercises table

One row represents one exercise that has already passed the tester and vector creation.

It stores the exercise ID, title, type, level, tags, description, starter code, hints, forbidden functions, private tests, status, and vector.

The private tests and vector never go to the student page.

**Technology:** PostgreSQL, **JSONB** for lists and tests, and **pgvector** for the vector.

**Owner:** AI/RAG service.

## Exercise attempts table

One row represents one submitted attempt.

It stores:

- which student submitted it (`user_id`);
- which exercise was submitted (`exercise_id`);
- whether it passed;
- the attempt number;
- the time taken.

The student's code and compiler error are not stored.

**Technology:** PostgreSQL.

**Owner:** Main backend service.

## Reports table

One row represents one report message.

It stores the student ID, exercise ID, and a message of at most 100 characters. The username is loaded from the users table when the admin reads reports.

**Technology:** PostgreSQL.

**Owner:** Main backend service.

## How the tables connect

The attempt and report tables contain two IDs:

```text
user_id     → identifies one row in the users table
exercise_id → identifies one row in the exercises table
```

This lets several students attempt or report the same exercise without copying the complete user or exercise into every row.

## Common cases

| What happened | Table used | Service responsible |
| --- | --- | --- |
| A student registers | Users | Main backend service |
| A validated exercise is saved | Exercises | AI/RAG service |
| A student submits code | Exercise attempts | Main backend service |
| A student reports a problem | Reports | Main backend service |
