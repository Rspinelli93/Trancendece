# RAG System — Technology Stack

**Project:** C Programming Documentation Assistant

**Language:** Python

**Objective:** Build a RAG module that receives a question as a string, searches indexed C documentation, and returns an AI-generated answer as a string.

The architecture consists of two pipelines:

- **Initialization:** Documents → Chunking → Embeddings → Vector Database
- **Query:** Question + exercise keyword → Embedding → Retrieval → Reranking → LLM → Answer

---

## 1. Document Loading and Chunking

**Technology:** LangChain  
**Type:** Python framework  
**Libraries:** `langchain-community`, `langchain-text-splitters`, `pypdf`

LangChain will load the C documentation and divide it into chunks suitable for embedding.

Because the documentation contains function definitions, examples, and explanations, we should avoid splitting code examples or function descriptions unnecessarily.

We'll initially use `RecursiveCharacterTextSplitter`, which supports chunk size and overlap configuration.

**Example:**

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = DirectoryLoader(
    "./c_docs",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)
```

The default splitter measures chunks in characters, not tokens. The example loads PDF documentation; other file formats require the appropriate loaders.

**Custom work:** Select and prepare the C documentation, organize its files, and test the chunking strategy. We may eventually need custom splitting based on C functions, headings, or code blocks.

## 2. Vectorization (Embeddings)

**Technology:** Ollama  
**Type:** Local model runtime  
**Embedding model:** `nomic-embed-text`  
**Library:** `langchain-ollama`

Ollama runs the embedding model. LangChain provides an integration so we can use it directly in the indexing and query pipelines.

We will use the same embedding model when indexing the documentation and processing questions. For user questions, we will include the known exercise topic in the text being embedded to improve retrieval.

**Example:**

```python
from langchain_ollama import OllamaEmbeddings

embed_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Document indexing uses embed_model.embed_documents(...).
# When the user asks about an exercise:
question = "Why does this code give me an error?"
keyword = "pointers"
retrieval_query = f"{keyword}: {question}"

vector = embed_model.embed_query(retrieval_query)
```

**Custom work:** Configure the model and ensure it remains consistent with the vectors already stored in the database.

## 3. Vector Database and Storage

**Technology:** ChromaDB  
**Type:** Embedded vector database  
**Libraries:** `chromadb`, `langchain-chroma`

Chroma stores the generated embeddings, their corresponding text chunks, and metadata such as document sources.

We will use its persistent storage mode. The database will be saved as files in a directory rather than requiring a separate SQL server.

Chroma manages its own storage files and search indexes.

**Example:**

```python
from langchain_chroma import Chroma

vector_db = Chroma(
    collection_name="c_documentation",
    embedding_function=embed_model,
    persist_directory="./rag_data"
)

# Run during initialization when indexing new documents
vector_db.add_documents(chunks)
```

This generates and stores embeddings for the chunks. On subsequent executions, the existing database can be reopened using the same collection name and storage directory without regenerating the vectors.

**Custom work:** Decide when to initialize, reuse, update, or rebuild the database. Avoid inserting duplicate chunks during repeated initialization.

**Option B (later):** Store a topic as chunk metadata, such as `topic="pointers"`, and filter Chroma searches by this field. We will not implement metadata-based filtering initially.

## 4. Retrieval

**Technology:** LangChain + ChromaDB  
**Type:** Framework retrieval interface + database search  
**Libraries:** `langchain-core`, `langchain-chroma`

Chroma performs vector similarity searching, while LangChain provides the retriever interface.

We will initially retrieve the 10 most relevant chunks for each question.

**Example:**

```python
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}
)

question = "Why does this code give me an error?"
keyword = "pointers"
retrieval_query = f"{keyword}: {question}"

results = retriever.invoke(retrieval_query)
```

Each result contains a retrieved text chunk and metadata. Similarity scores can be obtained using Chroma's similarity-search methods when needed.

Using LangChain is convenient here because it handles query embedding and communication with the vector database.

**Custom work:** Decide the number of chunks to retrieve and whether additional filtering is needed. For example, filtering by C standard, documentation type, or library.

## 5. Reranking

**Technology:** SentenceTransformers  
**Type:** Python library for running local AI models  
**Model:** `cross-encoder/ms-marco-MiniLM-L6-v2`  
**Library:** `sentence-transformers`

After retrieval, a CrossEncoder model evaluates the question against the candidate chunks and reranks them.

We will retrieve 10 chunks and retain the 3 most relevant for the LLM.

**Example:**

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)

question = "Why does this code give me an error?"
keyword = "pointers"
retrieval_query = f"{keyword}: {question}"

scores = reranker.predict([
    (retrieval_query, doc.page_content)
    for doc in results
])

ranked = sorted(
    zip(results, scores),
    key=lambda item: item[1],
    reverse=True
)

best_chunks = [
    doc for doc, score in ranked[:3]
]
```

**Custom work:** Experiment with the number of retrieved and reranked chunks. Reranking improves relevance in many cases but adds processing time.

## 6. LLM — Answer Generation

**Technology:** Ollama + Llama  
**Type:** Local model runtime + language model  
**Model:** `llama3.1:8b` (initial candidate)  
**Libraries:** `langchain-ollama`, `langchain-core`

We will use Ollama to run a Llama language model locally.

The LLM receives three main inputs:

1. **System prompt:** Permanent instructions defining the chatbot's behavior.
2. **Additional context:** The known exercise topic (`keyword`) plus optional information such as the required C standard, user skill level, or response format.
3. **Retrieved documentation + user question:** The relevant content selected by the RAG pipeline and the original question.

**Example:**

```python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

system_prompt = """
You are a C programming assistant.
Use the retrieved C documentation as your reference.
Explain concepts and provide correct C examples.
Do not invent C library functions.
If the context is insufficient, acknowledge it.
"""

keyword = "pointers"  # Known exercise topic
question = "Why does this code give me an error?"

extra_context = """
C standard: C11
User level: Beginner
Prefer short explanations with code examples.
"""

retrieved_context = "\n\n".join(
    doc.page_content
    for doc in best_chunks
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """
Current exercise topic:
{keyword}

Additional context:
{extra_context}

Retrieved documentation:
{retrieved_context}

Question:
{question}
""")
])

chain = prompt | llm

response = chain.invoke({
    "keyword": keyword,
    "extra_context": extra_context,
    "retrieved_context": retrieved_context,
    "question": question
})

answer = response.content
```

The `question` variable contains the original user input. The exercise `keyword` is used both to enrich retrieval (Sections 2–5) and to inform the LLM here.

**Custom work:** Write the system prompt, define the optional context passed to the LLM, choose the final Llama model, and determine how retrieved chunks will be formatted.

## 7. RAG Orchestration

**Technology:** LangChain + Custom Python  
**Type:** Framework and custom application logic

LangChain provides the document loading, chunking, embedding, vector database, retrieval, and LLM integrations.

We will use custom Python to control when each operation happens and expose a minimal interface to the rest of the system.

**Conceptual interface:**

```python
class RAG:
    def initialize(self) -> None:
        # Load or create the vector index
        ...

    def query(self, question: str, keyword: str) -> str:
        # Enrich the retrieval query with the exercise keyword
        # Embed and retrieve
        # Rerank chunks
        # Build LLM messages
        # Generate and return answer
        ...
```

The complete RAG engine should be usable as:

```python
rag = RAG()
rag.initialize()

answer = rag.query(
    "Why does this code give me an error?",
    keyword="pointers"
)

print(answer)
```

No other part of the system needs to interact directly with the vector database, embedding model, or reranker.

---

## Final Technology Stack

| Process | Technology | Type |
|---|---|---|
| Document loading | LangChain Document Loaders | Library components |
| Chunking | LangChain RecursiveCharacterTextSplitter | Library component |
| Embeddings | Ollama + nomic-embed-text | Runtime + AI model |
| Vector storage | ChromaDB | Embedded database |
| Retrieval | LangChain + Chroma | Framework + database search |
| Reranking | SentenceTransformers CrossEncoder | Library + AI model |
| LLM | Ollama + Llama 3.1 8B | Runtime + AI model |
| Prompt construction | LangChain ChatPromptTemplate | Library component |
| Orchestration | LangChain + Python | Framework + custom code |
| External interface | `query(question: str, keyword: str) -> str` | Custom Python |

## Initial Parameters

| Parameter | Initial configuration |
|---|---|
| Chunk size | 2000 characters |
| Chunk overlap | 200 characters |
| Retrieved chunks | 10 |
| Reranked chunks | 3 |
| Embedding model | nomic-embed-text |
| Reranking model | ms-marco-MiniLM-L6-v2 |
| LLM | llama3.1:8b |
| Storage directory | ./rag_data |

These are starting values to evaluate using actual C programming questions.

## Notes for the C Documentation

C documentation contains different types of material: function references, syntax explanations, standard-library descriptions, and source code examples.

Chunking should ideally preserve complete function descriptions and their associated examples. Documentation should also retain useful metadata, especially function names, headers, and C standard versions.

Similarity search may not always be sufficient for exact function names or compiler errors. Keyword or hybrid retrieval can be considered later if testing reveals problems.

The initial implementation will use ordinary vector retrieval and reranking before introducing those additional techniques.
