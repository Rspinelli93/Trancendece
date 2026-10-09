# AI/RAG service

This service starts working when the main backend sends checked JSON. It does not manage pages, accounts, attempts, reports, or C compilation.

## What sends data to me

The **main backend service** sends a JSON request. Depending on the request, the AI/RAG service will:

1. save or retrieve an exercise;
2. prepare a validated exercise for future searches;
3. find an exercise that matches what a student wants to learn.

## Diagram

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#fffdf7","primaryTextColor":"#1f2937","lineColor":"#84a98c","clusterBkg":"#f7fee7","clusterBorder":"#86efac"}}}%%
flowchart TD
    Key["LEGEND / HOW TO READ THIS MAP<br/>Rounded box = action<br/>Diamond = choose a path<br/>Database shape = stored information<br/>Orange arrow = enters the service<br/>Soft green arrow = work inside the service<br/>Dark green arrow = leaves the service"]
    Sender["WHO SENDS THE DATA?<br/>The main backend<br/>"]

    subgraph AIService["AI/RAG SERVICE"]
        Receive["1. RECEIVE AND CHECK THE DATA<br/>Accept JSON and check its format<br/>(Python, FastAPI, Pydantic)"]
        Choose{"2. WHAT KIND OF REQUEST IS IT?<br/>Exercise data, new exercise, or exercise search<br/>(Python)"}
        Database["3A. READ OR SAVE AN EXERCISE<br/>Only exercise data and vectors<br/>(SQLAlchemy + PostgreSQL)"]
        Indexer["3B. PREPARE AN EXERCISE FOR SEARCH<br/>Turn its meaning into numbers<br/>(Sentence Transformers)"]
        Search["3C. FIND MATCHING EXERCISES<br/>Compare the request with saved exercises<br/>(PostgreSQL, pgvector)"]
        AI["4. CHOOSE AND EXPLAIN A MATCH<br/>Select only from the exercises found<br/>(LLM API)"]
        Answer["5. PREPARE THE ANSWER<br/>Return clear, checked JSON<br/>(Python, FastAPI, Pydantic)"]
        Store[("WHERE THE DATA LIVES<br/>One database<br/>(PostgreSQL + pgvector)")]
    end

    Receiver["WHO RECEIVES THE ANSWER?<br/>The main backend<br/>It continues the frontend flow"]

    Key ~~~ Sender
    Sender -->|"JSON request"| Receive
    Receive --> Choose
    Choose -->|"Read or save"| Database
    Choose -->|"New validated exercise"| Indexer
    Choose -->|"Student learning request"| Search
    Database <--> Store
    Indexer --> Store
    Search <--> Store
    Search --> AI
    Database --> Answer
    Indexer --> Answer
    AI --> Answer
    Answer -->|"JSON response"| Receiver

    classDef note fill:#fff7ed,stroke:#f59e0b,color:#1f2937,stroke-width:2px;
    classDef outside fill:#fffbeb,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef work fill:#ecfdf5,stroke:#4ade80,color:#1f2937,stroke-width:2px;
    classDef storage fill:#f0fdf4,stroke:#16a34a,color:#1f2937,stroke-width:2px;
    class Key note;
    class Sender,Receiver outside;
    class Receive,Choose,Database,Indexer,Search,AI,Answer work;
    class Store storage;
    style AIService fill:#f7fee7,stroke:#86efac,stroke-width:2px,color:#1f2937;

    linkStyle default stroke:#84a98c,stroke-width:2px;
    linkStyle 1 stroke:#f59e0b,stroke-width:4px;
    linkStyle 13 stroke:#15803d,stroke-width:4px;
```


The AI/RAG service receives these requests through an internal web address (**FastAPI endpoint**). It checks that every required value has the correct format (**Pydantic validation**).

## Case 1: exercise database work

Examples include saving, reading, searching, or disabling an exercise.

The service uses **SQLAlchemy** to work with the exercise table. SQLAlchemy connects to **PostgreSQL** through **Psycopg**.

It returns either the requested data or a clear success or error result as JSON.

## Case 2: a new validated exercise

The main backend sends the exercise only after the reference solution passes the C tests.

The service creates a numerical description of the exercise's meaning (**Sentence Transformers embedding**) and stores it with the exercise. This makes the exercise searchable later (**PostgreSQL with pgvector**).

It returns the exercise ID, title, and whether saving succeeded.

## Case 3: a student wants an exercise

The main backend sends the student's selected level and written request.

The service turns the request into numbers, compares it with saved exercise vectors, and keeps the closest results (**Sentence Transformers and pgvector**). It then asks an AI model to choose from those results and explain the choice (**LLM API**).

The service checks the AI response and returns an existing exercise ID with the explanation. If there is no close match, it returns a normal “not found” response.

## Technologies used by the AI/RAG service

| Technology | Used for |
| --- | --- |
| Python | Controls the exercise database, RAG, and LLM steps |
| FastAPI | Receives JSON requests and returns JSON responses |
| Pydantic | Checks incoming and outgoing data |
| PostgreSQL | Stores exercises and vectors for this service |
| JSONB | Stores lists such as tests, tags, and hints |
| SQLAlchemy | Reads and writes exercise data |
| Alembic | Creates and updates the exercise table |
| Psycopg | Connects SQLAlchemy to PostgreSQL |
| pgvector | Stores vectors and compares their similarity |
| Sentence Transformers | Creates vectors from exercise text and student requests |
| LLM API | Chooses one retrieved exercise and explains why |

[Read the beginner technology guide](../Technology_guide.md).
