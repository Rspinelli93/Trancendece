
# ChromaDB Cheatsheet

## 1. Chroma Client

A Chroma client is the Python object used to interact with a Chroma vector database.

A **collection** stores document texts, embeddings, metadata, and IDs.

## 2. Types of Chroma Clients

| Client | Purpose |
|---|---|
| `Client()` | In-memory database, not persistent. |
| `EphemeralClient()` | Explicit in-memory client for testing. |
| `PersistentClient()` | Stores data locally on disk. |
| `HttpClient()` | Connects to a running Chroma server. |
| `AsyncHttpClient()` | Asynchronous HTTP client. |
| `CloudClient()` | Connects to Chroma Cloud. |

### Persistent Client

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
```

### Client-Server Mode

Chroma runs as a separate process. Python communicates with it over HTTP.

Start the server:

```bash
chroma run --path ./chroma_db
```

Connect from Python:

```python
client = chromadb.HttpClient(
    host="localhost",
    port=8000
)
```

Use client-server mode when multiple applications need access to the database or Chroma runs on another machine.

## 3. Main Client Methods

| Method | Purpose |
|---|---|
| `heartbeat()` | Check if Chroma responds. |
| `create_collection()` | Create a new collection. |
| `get_collection()` | Retrieve an existing collection. |
| `get_or_create_collection()` | Retrieve or create a collection. |
| `list_collections()` | List existing collections. |
| `count_collections()` | Count collections. |
| `delete_collection()` | Delete a collection and its data. |
| `reset()` | Delete all collections and data (when permitted). |
| `get_version()` | Get Chroma version. |
| `get_settings()` | Get client configuration. |

## 4. Main Collection Methods

| Method | Purpose |
|---|---|
| `add()` | Insert documents, embeddings, and metadata. |
| `upsert()` | Insert new records or update existing ones. |
| `update()` | Modify existing records. |
| `get()` | Retrieve stored records. |
| `query()` | Search for similar vectors. |
| `delete()` | Delete records. |
| `count()` | Count stored records. |
| `peek()` | Preview stored records. |
| `modify()` | Change collection properties, such as its name. |

## 5. Documentation

https://docs.trychroma.com/reference/python
