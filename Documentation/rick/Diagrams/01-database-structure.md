# My database structure

I use one PostgreSQL database. The information is separated into four tables so each type of record has a clear place.

## How a database request moves

1. The main backend sends me a checked request.
2. My Python code decides which table is needed.
3. I read, add, or update a row using SQL.
4. I return the result to the main backend as JSON.

Python communicates with PostgreSQL using **Psycopg**.

## Diagram

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#fffdf7","primaryTextColor":"#1f2937","lineColor":"#84a98c","clusterBkg":"#f7fee7","clusterBorder":"#86efac"}}}%%
flowchart TD
    Key["LEGEND / HOW TO READ THIS MAP<br/>Rounded box = action<br/>Database shape = one table of stored information<br/>Orange arrow = enters Rick's work<br/>Soft green arrow = connection inside Rick's work<br/>Dark green arrow = leaves Rick's work"]
    Request["WHO SENDS DATABASE WORK?<br/>The main backend sends a checked request"]

    subgraph Rick["RICK'S DATABASE PART"]
        Logic["1. UNDERSTAND THE REQUEST<br/>Choose what must be read or saved<br/>(Python + SQL through Psycopg)"]

        Users[("USERS TABLE<br/>One row = one account<br/><br/>ID, username, email, login information,<br/>role, status, avatar, score, MMR, badges<br/>(PostgreSQL)")]
        Exercises[("EXERCISES TABLE<br/>One row = one validated exercise<br/><br/>ID, title, level, tags, instructions, hints,<br/>private tests, status, search vector<br/>(PostgreSQL + JSONB + pgvector)")]
        Attempts[("EXERCISE ATTEMPTS TABLE<br/>One row = one submitted attempt<br/><br/>User ID, exercise ID, success,<br/>attempt number, time taken<br/>(PostgreSQL)")]
        Reports[("REPORTS TABLE<br/>One row = one report message<br/><br/>User ID, exercise ID,<br/>message of at most 100 characters<br/>(PostgreSQL)")]

        Result["2. PREPARE THE DATABASE RESULT<br/>Return success, failure, or requested data<br/>(Python + JSON)"]
    end

    Receiver["WHO RECEIVES THE RESULT?<br/>The main backend continues the request"]

    Key ~~~ Request
    Request -->|"Database request"| Logic
    Logic -->|"Account action"| Users
    Logic -->|"Exercise action"| Exercises
    Logic -->|"Save attempt"| Attempts
    Logic -->|"Save or read report"| Reports

    Attempts -->|"user_id means this student"| Users
    Attempts -->|"exercise_id means this exercise"| Exercises
    Reports -->|"user_id means this student"| Users
    Reports -->|"exercise_id means this exercise"| Exercises

    Users --> Result
    Exercises --> Result
    Attempts --> Result
    Reports --> Result
    Result -->|"Database response"| Receiver

    classDef note fill:#fff7ed,stroke:#f59e0b,color:#1f2937,stroke-width:2px;
    classDef outside fill:#fffbeb,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef work fill:#ecfdf5,stroke:#4ade80,color:#1f2937,stroke-width:2px;
    classDef users fill:#fff7ed,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef exercises fill:#f0fdf4,stroke:#22c55e,color:#1f2937,stroke-width:2px;
    classDef joining fill:#fefce8,stroke:#84cc16,color:#1f2937,stroke-width:2px;
    class Key note;
    class Request,Receiver outside;
    class Logic,Result work;
    class Users users;
    class Exercises exercises;
    class Attempts,Reports joining;
    style Rick fill:#f7fee7,stroke:#86efac,stroke-width:2px,color:#1f2937;

    linkStyle default stroke:#84a98c,stroke-width:2px;
    linkStyle 1 stroke:#f59e0b,stroke-width:4px;
    linkStyle 14 stroke:#15803d,stroke-width:4px;
```


## Users table

One row represents one account.

It stores the user ID, username, email, protected login information, role, status, predefined avatar, total score, MMR, and earned badge IDs.

Local accounts have a password hash. GitHub accounts have a GitHub ID instead.

**Technology:** PostgreSQL. Badge IDs are stored as a list (**JSONB**).

## Exercises table

One row represents one exercise that has already passed the tester and vector creation.

It stores the exercise ID, title, type, level, tags, description, starter code, hints, forbidden functions, private tests, status, and vector.

The private tests and vector never go to the student page.

**Technology:** PostgreSQL, **JSONB** for lists and tests, and **pgvector** for the vector.

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

## Reports table

One row represents one report message.

It stores the student ID, exercise ID, and a message of at most 100 characters. The username is loaded from the users table when the admin reads reports.

**Technology:** PostgreSQL.

## How the tables connect

The attempt and report tables contain two IDs:

```text
user_id     → identifies one row in the users table
exercise_id → identifies one row in the exercises table
```

This lets several students attempt or report the same exercise without copying the complete user or exercise into every row.

## Common cases

| What happened | Table used |
| --- | --- |
| A student registers | Users |
| A validated exercise is saved | Exercises |
| A student submits code | Exercise attempts |
| A student reports a problem | Reports |
