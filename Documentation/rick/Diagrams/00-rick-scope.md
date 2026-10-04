# My part of the platform

My work starts when the main backend sends me checked data. I do not need to manage the pages, the student's login screen, or the C tester.

## What sends data to me

The **main backend** sends me a JSON request. Depending on the request, I will:

1. read or save normal database information;
2. prepare a validated exercise for future searches;
3. find an exercise that matches what a student wants to learn.

## Diagram

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#fffdf7","primaryTextColor":"#1f2937","lineColor":"#84a98c","clusterBkg":"#f7fee7","clusterBorder":"#86efac"}}}%%
flowchart TD
    Key["LEGEND / HOW TO READ THIS MAP<br/>Rounded box = action<br/>Diamond = choose a path<br/>Database shape = stored information<br/>Orange arrow = enters my work<br/>Soft green arrow = work inside my part<br/>Dark green arrow = leaves my work"]
    Sender["WHO SENDS THE DATA?<br/>The main backend<br/>"]

    subgraph Rick["MY PART"]
        Receive["1. RECEIVE AND CHECK THE DATA<br/>Accept JSON and check its format<br/>(Python, FastAPI, Pydantic)"]
        Choose{"2. WHAT KIND OF REQUEST IS IT?<br/>Database, new exercise, or exercise search<br/>(Python)"}
        Database["3A. READ OR SAVE INFORMATION<br/>Users, exercises, attempts, and reports<br/>(PostgreSQL, SQL, Psycopg)"]
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
    style Rick fill:#f7fee7,stroke:#86efac,stroke-width:2px,color:#1f2937;

    linkStyle default stroke:#84a98c,stroke-width:2px;
    linkStyle 1 stroke:#f59e0b,stroke-width:4px;
    linkStyle 13 stroke:#15803d,stroke-width:4px;
```


I receive these requests through an internal web address (**FastAPI endpoint**). I check that every required value has the correct format (**Pydantic validation**).

## Case 1: normal database work

Examples include creating a user, saving an attempt, storing a report, or reading an exercise.

I choose the correct table and run the required database instruction (**SQL through Psycopg**). The information is stored in one database (**PostgreSQL**).

I return either the requested data or a clear success or error result as JSON.

## Case 2: a new validated exercise

The main backend sends the exercise only after the reference solution passes the C tests.

I create a numerical description of the exercise's meaning (**Sentence Transformers embedding**) and store it with the exercise. This makes the exercise searchable later (**PostgreSQL with pgvector**).

I return the exercise ID, title, and whether saving succeeded.

## Case 3: a student wants an exercise

The main backend sends the student's selected level and written request.

I turn the request into numbers, compare it with saved exercise vectors, and keep the closest results (**Sentence Transformers and pgvector**). I then ask an AI model to choose from those results and explain the choice (**LLM API**).

I check the AI response and return an existing exercise ID with the explanation. The main backend loads the complete exercise afterward.

## Technologies used in my part

| Technology | Used for |
| --- | --- |
| Python | Controls my database, RAG, and LLM steps |
| FastAPI | Receives JSON requests and returns JSON responses |
| Pydantic | Checks incoming and outgoing data |
| PostgreSQL | Stores the application data |
| JSONB | Stores lists such as tests, tags, hints, and badges |
| Psycopg + SQL | Lets Python read and write PostgreSQL |
| pgvector | Stores vectors and compares their similarity |
| Sentence Transformers | Creates vectors from exercise text and student requests |
| LLM API | Chooses one retrieved exercise and explains why |

[Read my beginner technology guide](../Technology_guide.md).
