# Python Classes & Connections Between Files

Practical guide for your C documentation RAG project.

## 1. Files, modules, and imports

Every `.py` file is a Python **module**. One file can use a function or class defined in another by importing it. **Imports share code; function arguments and return values pass data.**

**`embeddings.py`**

```python
def create_model():
    return "embedding-model"
```

**`rag.py`**

```python
from embeddings import create_model

model = create_model()
```

These imports work when the files are in the same importable directory. In a package, you can use a package-qualified import, such as `from rag.embeddings import create_model`.

## 2. What a class is

A **class** defines an object that groups data (**attributes**) and operations (**methods**). Creating an instance calls `__init__`; `self` refers to that particular instance.

```python
class Counter:
    def __init__(self, start=0):
        self.value = start

    def increment(self):
        self.value += 1
        return self.value

counter = Counter(5)
print(counter.increment())  # 6
```

`self.value` persists between method calls. A regular local variable inside `increment()` does not. Instance methods declare `self` as their first parameter, but callers do not pass it explicitly.

## 3. How files pass information

| Mechanism | Use | Example |
|---|---|---|
| Import | Make a function, class, or constant available | `from retrieval import retrieve` |
| Argument | Pass data into a function or method | `retrieve(db, question)` |
| Return | Send a value back to the caller | `return documents` |
| Object attribute | Keep shared state on one instance | `self.db = create_database()` |

## 4. Suggested file structure for the RAG

```text
project/
  main.py          # Terminal entry point
  rag.py           # RAG class, coordinates components
  embeddings.py    # Creates embedding model
  vector_db.py     # Opens Chroma database
  retrieval.py     # Retrieves document chunks
  reranker.py      # Ranks retrieved chunks
  llm.py           # Builds prompt and asks model
  chunking.py      # Splits documents during indexing
```

You do not need a class in every file. Use simple functions for isolated operations; use a class when you want to retain objects or configuration across calls.

## 5. A minimal cross-file example

These examples show how the modules connect. The retrieval and LLM functions are simplified examples, not a complete RAG implementation.

**`retrieval.py`**

```python
def retrieve(db, search_text):
    return db.similarity_search(search_text, k=10)
```

**`llm.py`**

```python
def generate(llm, question, keyword, documents):
    context = "\n\n".join(doc.page_content for doc in documents)
    prompt = f"Topic: {keyword}\nContext: {context}\nQuestion: {question}"
    return llm.invoke(prompt).content
```

**`rag.py`**

```python
from retrieval import retrieve
from llm import generate

class RAG:
    def __init__(self, db, llm):
        self.db = db
        self.llm = llm

    def query(self, question: str, keyword: str) -> str:
        search_text = f"{keyword}: {question}"
        documents = retrieve(self.db, search_text)
        # A reranker can refine documents here.
        return generate(self.llm, question, keyword, documents)
```

**`main.py`**

```python
from rag import RAG

# db and llm are created with their respective libraries.
rag = RAG(db, llm)
answer = rag.query("Why does this pointer fail?", "pointers")
print(answer)
```

**Flow:** `main.py` creates `RAG` → `rag.py` enriches the question → `retrieval.py` uses Chroma → `llm.py` generates the answer → the string returns to `main.py`.

## 6. Design guidance for this project

Keep expensive resources (Chroma connection, embedding model, CrossEncoder, LLM client) as `RAG` attributes so they are constructed once. Leave document indexing in a separate `initialize()` method: opening an existing index is different from rebuilding it. The public interface can remain `query(question: str, keyword: str) -> str`.

Avoid **circular imports** (for example, `rag.py` importing `retrieval.py` while `retrieval.py` imports `rag.py`). Let the coordinator import helpers, and pass objects into them instead of making helpers import the coordinator.
