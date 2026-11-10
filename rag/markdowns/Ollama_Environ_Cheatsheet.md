# Project Setup & Command Reference

**Project:** C Programming RAG · **Python:** 3.12

**Reference:** [The C Programming Language, 2nd Edition](https://www.cs.sfu.ca/~ashriram/Courses/CS295/assets/books/C_Book_2nd.pdf)

## 1. Python virtual environment

All commands assume you're in the project root, where `.venv` lives.

| Action | Command |
|---|---|
| Create environment (once) | `python3 -m venv .venv` |
| Activate | `source .venv/bin/activate` |
| Deactivate | `deactivate` |
| Check active Python | `which python` |
| Install direct dependencies | `python -m pip install -r requirements.txt` |
| Check installed packages | `python -m pip list` |
| Check dependency compatibility | `python -m pip check` |
| Export exact installed versions | `python -m pip freeze > requirements-lock.txt` |

**Current Python dependencies:** `langchain`, `langchain-community`, `langchain-text-splitters`, `pymupdf`, `chromadb`, `langchain-ollama`, `sentence-transformers` (for reranking). Chroma's default embedding model is included through `chromadb` and downloaded on first use; it does not require a separate pip package.

## 2. Ollama

Ollama is installed **outside** the venv. It is used for Llama text generation, **not** embeddings; Chroma generates those locally.

| Action | Command |
|---|---|
| Start service | `sudo systemctl start ollama` |
| Stop service | `sudo systemctl stop ollama` |
| Restart service | `sudo systemctl restart ollama` |
| Check running | `systemctl is-active ollama` |
| Check boot startup | `systemctl is-enabled ollama` |
| Disable boot startup and stop now | `sudo systemctl disable --now ollama` |
| Show downloaded models | `ollama list` |
| Show loaded models | `ollama ps` |
| Download chat model | `ollama pull llama3.1:8b` |
| Chat | `ollama run llama3.1:8b` |
| Leave chat | `/bye` |
| Unload a model | `ollama stop llama3.1:8b` |
| Remove old embedding model | `ollama rm nomic-embed-text` |

On a CPU-only machine with limited RAM, `llama3.1:8b` may be slow or fail to load. Optional smaller model: `ollama pull llama3.2:3b`, then `ollama run llama3.2:3b`.

## 3. Chroma embedding setup

| Action | Command |
|---|---|
| Verify Chroma installation | `python -m pip show chromadb` |
| Install Chroma only if missing | `python -m pip install chromadb` |
| Download/test default embedding model | `python -c "from chromadb.utils.embedding_functions import DefaultEmbeddingFunction; print(len(DefaultEmbeddingFunction()(['C pointers'])[0]))"` |

Expected dimensions: `384`. First use downloads Chroma's ONNX `all-MiniLM-L6-v2` model; a network connection is needed for that initial download. Chroma can automatically embed stored documents and search queries. Use `chromadb.PersistentClient(path='./rag_data')` to save the database to disk.

## 4. Dependency handoff

- `requirements.txt` lists **direct Python dependencies**; install them inside the future container.
- `requirements-lock.txt` (generated with `pip freeze`) records **exact installed versions** for repeatability.
- Ollama and downloaded Llama models are **not Python dependencies** and are not listed by pip.
- Chroma's ONNX embedding model is cached separately from the vector database; account for its initial download in deployment.
