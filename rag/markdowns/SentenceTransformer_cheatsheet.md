
# CrossEncoder Cheatsheet — SentenceTransformers

## 1. What is a CrossEncoder?

A CrossEncoder evaluates two texts together and assigns a relevance score.

In RAG, it is used **after vector retrieval** to rerank the retrieved documents more accurately.

CrossEncoders are generally more computationally expensive than embedding similarity searches, so they are best used on a smaller set of retrieved candidates.

Other SentenceTransformers model types include `SentenceTransformer`, `SparseEncoder`, and `MultiVectorEncoder`, primarily used for different retrieval strategies.

## 2. Initialization

`CrossEncoder(model_name_or_path, ...)`

Creates a CrossEncoder instance and loads the selected model.

| Parameter | Purpose |
|---|---|
| `model_name_or_path` | Hugging Face model name or local path. |
| `device` | Processing device: `cpu`, `cuda`, `mps`, or automatic. |
| `max_length` | Maximum number of input tokens; longer inputs are truncated. |
| `num_labels` | Number of output labels/scores. |
| `trust_remote_code` | Allows execution of custom model code. |

**Model used:** `cross-encoder/ms-marco-MiniLM-L6-v2`

A relatively lightweight reranking model suitable for retrieval tasks.

## 3. Main Functions

### `predict()`

**Purpose:** Calculate relevance scores for query-document pairs without ranking them.

**Parameters:**

- `sentences`: List of `(query, document)` pairs.
- `batch_size`: Number of pairs processed per batch.
- `show_progress_bar`: Whether to display progress.
- `activation_fn`: Function applied to model outputs.
- `apply_softmax`: Whether to apply softmax to multi-label outputs.
- `convert_to_numpy`: Return results as NumPy arrays.
- `convert_to_tensor`: Return results as PyTorch tensors.

**Returns:** A NumPy array or PyTorch tensor containing the scores, depending on configuration.

| Value | Type | Description |
|---|---|---|
| `scores` | `np.ndarray` or `torch.Tensor` | Relevance scores in the same order as the input pairs. |
| `scores[0]` | `float` or scalar tensor | Score for the first query-document pair. |
| `scores[1]` | `float` or scalar tensor | Score for the second query-document pair. |

For a single-output reranking model, each pair receives one score. Higher scores indicate greater relevance.

**When to use:** When you need relevance scores but want to handle sorting yourself.

### `rank()`

**Purpose:** Compare one query against multiple documents, score them, and sort by relevance.

**Parameters:**

- `query`: User prompt as a string.
- `documents`: List of document strings.
- `top_k`: Maximum number of ranked documents returned; `None` returns all.
- `return_documents`: Include original document text in the results.
- `batch_size`: Number of query-document pairs processed per batch.
- `show_progress_bar`: Display ranking progress.
- `activation_fn`: Function applied to output scores.
- `apply_softmax`: Whether to apply softmax to multi-label outputs.

**Returns:** A list of dictionaries sorted by relevance, highest score first.

Each dictionary contains:

| Key | Type | Description |
|---|---|---|
| `corpus_id` | `int` | Original index of the document in the input list. |
| `score` | `float` | Relevance score assigned by the CrossEncoder. |
| `text` | `str` | Original document content, only when `return_documents=True`. |

**Example return value:**

    [
        {
            "corpus_id": 2,
            "score": 8.92,
            "text": "A pointer stores a memory address."
        },
        {
            "corpus_id": 0,
            "score": 6.35,
            "text": "Pointers allow indirect memory access."
        }
    ]

**Accessing results:**

- `ranks[0]` — Highest-ranked result.
- `ranks[0]["corpus_id"]` — Original index of the highest-ranked document.
- `ranks[0]["score"]` — Relevance score.
- `ranks[0]["text"]` — Document text, if requested.

**When to use:** For RAG reranking after Chroma retrieval.

**Important:** `rank()` internally calculates the scores, so calling `predict()` beforehand is unnecessary.

### `save_pretrained()`

**Purpose:** Save the CrossEncoder model locally.

**Main parameters:**

- `save_directory`: Directory where the model is saved.
- `safe_serialization`: Whether to use the safer `safetensors` format.

**Returns:** `None`. The model files are written to the specified directory.

**When to use:** When you want to preserve a downloaded or fine-tuned model locally.

### `push_to_hub()`

**Purpose:** Upload the model to Hugging Face Hub.

**Main parameters:**

- `repo_id`: Destination repository.
- `private`: Whether the repository should be private.
- `commit_message`: Description of the upload.
- `token`: Authentication token, when required.

**Returns:** `str` — URL of the uploaded model repository or commit.

**When to use:** When publishing or sharing a model.

## 4. Important Concepts

| Concept | Explanation |
|---|---|
| Reranking | Reordering retrieved documents by relevance. |
| Relevance score | Numerical estimate of query-document relevance. |
| Query-document pair | Two texts evaluated together. |
| Batch size | Number of pairs processed simultaneously. |
| Truncation | Cutting inputs that exceed the model's token limit. |
| Top K | Number of highest-ranked documents retained. |
| `corpus_id` | Original index of a document in the input list. |

## 5. CrossEncoder vs. Embeddings

| Embedding Model | CrossEncoder |
|---|---|
| Processes texts separately. | Processes query and document together. |
| Produces vectors. | Produces relevance scores. |
| Fast for large-scale retrieval. | Slower but generally more accurate for reranking. |
| Used for semantic search. | Used for reranking search results. |

## 6. Documentation

**CrossEncoder Usage:**

https://sbert.net/docs/cross_encoder/usage/usage.html

**CrossEncoder API Reference:**

https://sbert.net/docs/package_reference/cross_encoder/cross_encoder.html

**SentenceTransformers Documentation:**

https://sbert.net/
