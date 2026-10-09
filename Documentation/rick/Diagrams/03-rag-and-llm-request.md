# Finding an exercise with RAG and the LLM

This path starts when a student describes what they want to learn. It ends when the AI/RAG service returns an existing exercise ID or explains that no suitable exercise exists.

## What the service receives

The main backend checks the student's login and sends the AI/RAG service:

```json
{
  "level": 2,
  "query": "I want to understand how a function can change the original pointer"
}
```

The AI/RAG service receives the JSON through **FastAPI**.

## Diagram

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#fffdf7","primaryTextColor":"#1f2937","lineColor":"#84a98c","clusterBkg":"#f7fee7","clusterBorder":"#86efac"}}}%%
flowchart TD
    Key["LEGEND / HOW TO READ THIS MAP<br/>Rounded box = action<br/>Diamond = yes-or-no decision<br/>Database shape = stored information<br/>Gray arrow = another service<br/>Orange arrow = enters the AI/RAG service<br/>Soft green arrow = work inside the service<br/>Dark green arrow = leaves the service"]

    Student["STUDENT REQUEST<br/>The student chooses a level and writes<br/>what they want to learn"]
    Backend["MAIN BACKEND SERVICE<br/>Checks the login and sends<br/>{ level, query }"]

    subgraph AIService["AI/RAG SERVICE: FIND AND EXPLAIN AN EXERCISE"]
        Receive["1. RECEIVE THE LEARNING REQUEST<br/>Open the internal request<br/>(FastAPI)"]
        Validate{"2. IS THE REQUEST VALID?<br/>Level is 1-3 and text is acceptable<br/>(Pydantic)"}
        QueryVector["3. TURN THE REQUEST INTO NUMBERS<br/>Create a vector representing its meaning<br/>(Sentence Transformers)"]
        Search["4. SEARCH EXISTING EXERCISES<br/>Same level, enabled status,<br/>and closest vector meanings<br/>(SQLAlchemy + pgvector)"]
        Candidates["5. KEEP THE BEST RESULTS<br/>Create a short candidate list<br/>(Python)"]
        GoodMatch{"6. IS THE BEST RESULT CLOSE ENOUGH?<br/>Use a minimum similarity score<br/>(Python threshold)"}
        LLMRequest["7. ASK FOR A FINAL CHOICE<br/>Send only public candidate information<br/>(Python LLM library)"]
        LLM["8. CHOOSE AND EXPLAIN<br/>The AI chooses one candidate ID<br/>and writes a short reason<br/>(Configurable LLM API)"]
        Check{"9. IS THE CHOSEN ID ALLOWED?<br/>It must exist in the candidate list<br/>(Pydantic + Python)"}
        Found["10. PREPARE THE MATCH ANSWER<br/>{ matched: true, exercise_id,<br/>exercise_title, reason }<br/>(FastAPI JSON response)"]
        NoMatch["NO SUITABLE EXERCISE<br/>{ matched: false, exercise_id: null,<br/>reason }<br/>(FastAPI JSON response)"]
        Error["CONTROLLED ERROR<br/>Return a safe error message<br/>(FastAPI JSON response)"]
        DB[("WHERE SEARCH DATA LIVES<br/>Enabled exercises and their vectors<br/>(PostgreSQL + pgvector)")]
    end

    Receiver["MAIN BACKEND SERVICE<br/>Receives the match, no-match, or error"]
    Load["LOAD THE PUBLIC EXERCISE<br/>The main backend requests it from<br/>the AI/RAG service"]

    Key ~~~ Student
    Student --> Backend
    Backend -->|"{ level, query }"| Receive
    Receive --> Validate
    Validate -->|"No"| Error
    Validate -->|"Yes"| QueryVector
    QueryVector --> Search
    DB -->|"Exercises and vectors"| Search
    Search --> Candidates
    Candidates --> GoodMatch
    GoodMatch -->|"No"| NoMatch
    GoodMatch -->|"Yes"| LLMRequest
    LLMRequest --> LLM
    LLM -->|"Answer"| Check
    LLM -->|"Unavailable"| Error
    Check -->|"No"| Error
    Check -->|"Yes"| Found
    Found -->|"Match JSON"| Receiver
    NoMatch -->|"No-match JSON"| Receiver
    Error -->|"Error JSON"| Receiver
    Receiver --> Load
    Load --> Student

    classDef note fill:#fff7ed,stroke:#f59e0b,color:#1f2937,stroke-width:2px;
    classDef outside fill:#fffbeb,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef work fill:#ecfdf5,stroke:#4ade80,color:#1f2937,stroke-width:2px;
    classDef storage fill:#f0fdf4,stroke:#16a34a,color:#1f2937,stroke-width:2px;
    classDef decision fill:#fefce8,stroke:#84cc16,color:#1f2937,stroke-width:2px;
    classDef error fill:#fff1f2,stroke:#fb7185,color:#1f2937,stroke-width:2px;
    class Key note;
    class Student,Backend,Receiver,Load outside;
    class Receive,QueryVector,Search,Candidates,LLMRequest,LLM,Found work;
    class DB storage;
    class Validate,GoodMatch,Check decision;
    class NoMatch,Error error;
    style AIService fill:#f7fee7,stroke:#86efac,stroke-width:2px,color:#1f2937;

    linkStyle default stroke:#84a98c,stroke-width:2px;
```


## 1. Check the request

The AI/RAG service verifies that the level is `1`, `2`, or `3` and that the written request follows the agreed length and format rules (**Pydantic**).

Invalid requests receive a controlled error.

## 2. Turn the request into a vector

The service uses the same embedding model used for the exercises (**Sentence Transformers**). It converts the student's sentence into a vector.

Using the same model is necessary because the request vector must be comparable with the exercise vectors.

## 3. Search the exercise library

The service searches only exercises that:

- are `enabled`;
- have the student's selected level;
- have vectors close to the request vector.

Python sends the search using **SQLAlchemy**. SQLAlchemy connects through **Psycopg**, and PostgreSQL compares the vectors using **pgvector**.

The service keeps a small list of the closest exercises.

## 4. Decide whether there is a real match

The closest result is not automatically a good result. The service compares its similarity score with a minimum accepted score.

If it is too low, the service returns:

```json
{
  "matched": false,
  "exercise_id": null,
  "reason": "No suitable exercise was found for your request."
}
```

The exact minimum score will be decided by testing real requests.

## 5. Ask the LLM to choose

When useful matches exist, the service sends the LLM only their public information:

- exercise ID;
- title;
- level;
- tags;
- description.

The LLM is instructed to choose one of those IDs and write a short explanation. It cannot generate a new exercise.

This step uses a Python library for the chosen **LLM API**. The provider and model are still to be decided.

## 6. Check and return the answer

The service verifies that the LLM returned a valid candidate ID (**Pydantic and Python**). An invented or malformed ID becomes a controlled error.

A successful response looks like:

```json
{
  "matched": true,
  "exercise_id": "exercise-123",
  "exercise_title": "Change a pointer from a function",
  "reason": "This exercise practises changing a caller's pointer through a double pointer."
}
```

The AI/RAG service returns this JSON through **FastAPI**. The main backend then requests the exercise's public information from the same service.

If PostgreSQL, the vector model, or the LLM is unavailable, the service returns a temporary error. It does not return the closest exercise and does not call the failure “no match.”

This completes the RAG path: retrieve relevant exercises first, then generate a grounded explanation from that retrieved information.
