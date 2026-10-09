# Saving a new exercise and preparing it for search

This path starts with an admin upload and ends when the AI/RAG service saves a validated, searchable exercise.

## Before the data reaches me

1. The admin uploads the complete exercise JSON.
2. The main backend checks that its required fields exist and creates the exercise ID.
3. The C tester inserts the reference solution and runs every private test.

If a test fails, the main backend rejects the upload. The AI/RAG service receives nothing.

## Diagram

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#fffdf7","primaryTextColor":"#1f2937","lineColor":"#84a98c","clusterBkg":"#f7fee7","clusterBorder":"#86efac"}}}%%
flowchart TD
    Key["LEGEND / HOW TO READ THIS MAP<br/>Rounded box = action<br/>Diamond = yes-or-no decision<br/>Database shape = stored information<br/>Gray arrow = another service<br/>Orange arrow = enters the AI/RAG service<br/>Soft green arrow = work inside the service<br/>Dark green arrow = leaves the service"]

    Admin["ADMIN UPLOAD<br/>The admin sends the complete exercise JSON"]
    Backend["MAIN BACKEND SERVICE<br/>Checks required fields and creates the exercise ID"]
    Tester["CODE-CHECKING SERVICE<br/>Runs the reference solution"]
    Passed{"DID EVERY TEST PASS?"}
    Rejected["UPLOAD REJECTED<br/>The backend returns the tester error<br/>Nothing is sent to the AI/RAG service"]

    subgraph AIService["AI/RAG SERVICE: SAVE A SEARCHABLE EXERCISE"]
        Receive["1. RECEIVE THE VALIDATED EXERCISE<br/>Check the received JSON again<br/>(FastAPI + Pydantic)"]
        Sentence["2. CREATE ONE SEARCH SENTENCE<br/>Join title, level, tags, and description<br/>(Python)"]
        Vector["3. TURN THE MEANING INTO NUMBERS<br/>Create the exercise vector<br/>(Sentence Transformers)"]
        VectorOK{"4. WAS THE VECTOR CREATED?"}
        Prepare["5. PREPARE THE FINAL RECORD<br/>Remove the reference solution<br/>add enabled status and the vector<br/>(Python)"]
        Save[("6. SAVE THE EXERCISE<br/>Use one database transaction<br/>(SQLAlchemy + PostgreSQL)")]
        Saved{"7. WAS IT SAVED?"}
        Success["8. PREPARE A SUCCESS ANSWER<br/>{ success, exercise_id, exercise_title }<br/>(FastAPI JSON response)"]
        VectorError["VECTOR CREATION FAILED<br/>Save nothing and prepare an error<br/>(FastAPI JSON response)"]
        SaveError["DATABASE SAVE FAILED<br/>Roll back and save nothing<br/>(FastAPI JSON response)"]
    end

    Receiver["MAIN BACKEND SERVICE<br/>Receives the success or error response"]

    Key ~~~ Admin
    Admin --> Backend
    Backend --> Tester
    Tester --> Passed
    Passed -->|"No"| Rejected
    Passed -->|"Yes: validated exercise JSON"| Receive
    Receive --> Sentence
    Sentence --> Vector
    Vector --> VectorOK
    VectorOK -->|"No"| VectorError
    VectorOK -->|"Yes"| Prepare
    Prepare --> Save
    Save --> Saved
    Saved -->|"Yes"| Success
    Saved -->|"No"| SaveError
    Success -->|"Success JSON"| Receiver
    VectorError -->|"Error JSON"| Receiver
    SaveError -->|"Error JSON"| Receiver

    classDef note fill:#fff7ed,stroke:#f59e0b,color:#1f2937,stroke-width:2px;
    classDef outside fill:#fffbeb,stroke:#fb923c,color:#1f2937,stroke-width:2px;
    classDef work fill:#ecfdf5,stroke:#4ade80,color:#1f2937,stroke-width:2px;
    classDef storage fill:#f0fdf4,stroke:#16a34a,color:#1f2937,stroke-width:2px;
    classDef decision fill:#fefce8,stroke:#84cc16,color:#1f2937,stroke-width:2px;
    classDef error fill:#fff1f2,stroke:#fb7185,color:#1f2937,stroke-width:2px;
    class Key note;
    class Admin,Backend,Tester,Receiver outside;
    class Receive,Sentence,Vector,Prepare,Success work;
    class Save storage;
    class Passed,VectorOK,Saved decision;
    class Rejected,VectorError,SaveError error;
    style AIService fill:#f7fee7,stroke:#86efac,stroke-width:2px,color:#1f2937;

    linkStyle default stroke:#84a98c,stroke-width:2px;
```


## 1. Receive the validated exercise

If all C tests pass, the main backend sends the validated exercise to the AI/RAG service as JSON.

The AI/RAG service receives fields such as its ID, title, type, level, tags, description, starter code, hints, forbidden functions, and private tests.

It checks the JSON again before using it (**FastAPI and Pydantic**).

## 2. Create the text used for searching

The service combines only the information that describes what the exercise teaches:

```text
Title + level + tags + description
```

It does not include the reference solution, private tests, expected outputs, or hints.

This step uses normal **Python** code.

## 3. Create the vector

The service sends the search text to an embedding model (**Sentence Transformers**). It returns a list of numbers called a vector.

The vector represents the meaning of the exercise and will later be compared with a student's request.

If vector creation fails, the service saves nothing and returns an error to the main backend.

## 4. Prepare and save the final exercise

The service discards the reference solution, adds the vector, and sets the exercise status to `enabled`.

It saves the exercise in **PostgreSQL**:

- normal values use ordinary database columns;
- lists and private tests use **JSONB**;
- the vector uses **pgvector**.

Python saves the exercise using **SQLAlchemy**. SQLAlchemy uses **Psycopg** to connect to PostgreSQL. If saving fails, the transaction is rolled back and no incomplete exercise remains.

## 5. Return the result

After a successful save, the service returns:

```json
{
  "success": true,
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen"
}
```

The response is returned through **FastAPI**. If vector creation or saving fails, the service returns an error and the exercise is not stored.
