
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

### Main Client Methods

| Method | Parameters | Purpose | Return Value |
|---|---|---|---|
| `heartbeat()` | None | Check if Chroma responds. | `int` — Timestamp in nanoseconds. |
| `create_collection()` | `name`, `schema`, `configuration`, `metadata`, `embedding_function`, `data_loader`, `get_or_create` | Create a new collection. | `Collection` object. |
| `get_collection()` | `name`, `embedding_function`, `data_loader` | Retrieve an existing collection. | `Collection` object. |
| `get_or_create_collection()` | `name`, `schema`, `configuration`, `metadata`, `embedding_function`, `data_loader` | Retrieve a collection or create it if missing. | `Collection` object. |
| `list_collections()` | `limit`, `offset` | List existing collections. | `list[Collection]` |
| `count_collections()` | None | Count collections. | `int` |
| `delete_collection()` | `name` | Delete a collection and its data. | `None` |
| `reset()` | None | Delete all collections and data (when permitted). | `bool` |
| `get_version()` | None | Get Chroma version. | `str` |
| `get_settings()` | None | Get client configuration. | `Settings` object. |

### Main Collection Methods

| Method | Parameters | Purpose | Return Value |
|---|---|---|---|
| `add()` | `ids`, `documents`, `embeddings`, `metadatas`, `images`, `uris` | Insert new records. | `None` |
| `upsert()` | `ids`, `documents`, `embeddings`, `metadatas`, `images`, `uris` | Insert new records or update existing ones. | `None` |
| `update()` | `ids`, `documents`, `embeddings`, `metadatas`, `images`, `uris` | Modify existing records by ID. | `None` |
| `get()` | `ids`, `where`, `where_document`, `limit`, `offset`, `include` | Retrieve stored records. | `GetResult` — Dictionary. |
| `query()` | `query_texts`, `query_embeddings`, `query_images`, `query_uris`, `ids`, `n_results`, `where`, `where_document`, `include` | Find nearest matching vectors. | `QueryResult` — Dictionary. |
| `delete()` | `ids`, `where`, `where_document` | Delete records matching IDs or filters. | `None` |
| `count()` | None | Count stored records. | `int` |
| `peek()` | `limit` | Preview the first records. | `GetResult` — Dictionary. |
| `modify()` | `name`, `metadata`, `configuration` | Change collection properties. | `None` |

### Parameters Reference

| Parameter | Example | Description |
|---|---|---|
| `name` | `"my_rag"` | Collection name. |
| `ids` | `["id1", "id2"]` | Unique record identifiers. |
| `documents` | `["text1", "text2"]` | Document text strings. |
| `embeddings` | `[[0.1, 0.2], [0.3, 0.4]]` | Numerical vectors representing documents. |
| `metadatas` | `[{"source": "book.pdf"}]` | Metadata dictionaries associated with records. |
| `metadata` | `{"description": "C book"}` | Metadata associated with a collection. |
| `embedding_function` | `embedding_fn` | Function used to generate embeddings automatically. |
| `data_loader` | `loader_fn` | Function used to load external data. |
| `schema` | `schema_object` | Collection schema configuration. |
| `configuration` | `config_object` | Collection indexing or other configuration settings. |
| `get_or_create` | `True` | Return existing collection if it already exists. |
| `query_texts` | `["What is a pointer?"]` | Text queries converted into embeddings before searching. |
| `query_embeddings` | `[[0.1, 0.2, 0.3]]` | Precomputed query embeddings. |
| `query_images` | `image_arrays` | Images used for similarity search. |
| `query_uris` | `["image.png"]` | URIs used as query inputs. |
| `images` | `image_arrays` | Image data to store. |
| `uris` | `["image.png"]` | References to external data. |
| `n_results` | `5` | Maximum number of matches per query. |
| `where` | `{"source": "book.pdf"}` | Filter records by metadata. |
| `where_document` | `{"$contains": "pointer"}` | Filter records by document content. |
| `include` | `["documents", "metadatas", "distances"]` | Specify fields returned by a query or get operation. |
| `limit` | `10` | Maximum number of records returned. |
| `offset` | `5` | Skip the first five records. |

### Return Values

### GetResult — `get()` and `peek()`

| Key | Description |
|---|---|
| `ids` | List of record IDs. |
| `documents` | List of stored document texts. |
| `metadatas` | List of metadata dictionaries. |
| `embeddings` | Stored numerical vectors, if requested. |
| `uris` | Stored URIs, if requested. |
| `data` | Loaded external data, if requested. |
| `included` | Fields requested in `include`. |

### QueryResult — `query()`

| Key | Description |
|---|---|
| `ids` | Nested lists of matching record IDs. |
| `documents` | Nested lists of matching texts. |
| `metadatas` | Nested lists of metadata dictionaries. |
| `distances` | Nested lists of vector distances. |
| `embeddings` | Matching embeddings, if requested. |
| `uris` | Matching URIs, if requested. |
| `data` | Loaded external data, if requested. |
| `included` | Fields requested in `include`. |

**Notes:**

- `ids` is required for `add()`, `update()`, and `upsert()`.
- Most other parameters are optional.
- `query()` requires one query input type, such as `query_texts` or `query_embeddings`.
- `query()` returns nested lists because it supports multiple queries.
- `add()`, `update()`, and `upsert()` can generate embeddings automatically if an embedding function is configured.
- Optional result fields may be `None` when not requested.
- Corresponding `ids`, `documents`, and `metadatas` must have matching lengths when inserting records.

## 5. Documentation

https://docs.trychroma.com/reference/python
