
# CrossEncoder Cheatsheet — SentenceTransformers

## 1. What is a CrossEncoder?

A CrossEncoder evaluates two texts together and assigns a relevance score.
We use this after the retireval done with Chroma, once we have the user prompt
and a series of documents retrieved, the re ranker uses a more accurate matching
algorithm, so we get a better solution.
This is mostly useful for large amounts of documents, since the vector comparison
with chroma in those cases can be innacurate, this is a good thing to use.

There are other re-ranking systems by SentenceTransformers, see: **SentenceTransformer, SparseEncoder and MultiVectorEncoder**

## 2. Initialization

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
# There are other cheaper models in terms of memory usage
```

### Common Initialization Parameters

| Parameter | Purpose |
|---|---|
| `model_name_or_path` | Model to load from Hugging Face or local storage. |
| `device` | Execution device (`cpu`, `cuda`, `mps`). |
| `max_length` | Maximum input token length; longer inputs are truncated. |
| `num_labels` | Number of output labels. |
| `trust_remote_code` | Allow custom model code; use only with trusted models. |

## 3. Main Methods

| Method | Purpose |
|---|---|
| `predict()` | Calculate scores for query-document pairs. |
| `rank()` | Score and rank documents for a query. |
| `save_pretrained()` | Save the model locally. |
| `push_to_hub()` | Upload the model to Hugging Face Hub. |

## 4. predict()

Receives pairs of texts and returns their scores.

```python
pairs = [
    ("What is a pointer?", "A pointer stores a memory address."),
    ("What is a pointer?", "A loop repeats instructions.")
]

scores = model.predict(pairs)
```

- Input: List of text pairs.
- Output: Scores for each pair.
- Higher scores generally indicate greater relevance.

## 5. rank()

Receives a query and a list of documents, then scores and sorts them.

```python
documents = [
    "A pointer stores a memory address.",
    "A loop repeats instructions.",
    "Pointers allow indirect memory access."
]

results = model.rank(
    query="What is a pointer?",
    documents=documents,
    top_k=2,
    return_documents=True
)
```

- `query`: User's question.
- `documents`: List of candidate texts.
- `top_k`: Maximum number of results to return.
- `return_documents`: Include document text in results.

### Result Structure

Each ranked result contains:

- `corpus_id`: Original document index.
- `score`: Relevance score.
- `text`: Document text, when `return_documents=True`.

## 6. Important Concepts

| Concept | Explanation |
|---|---|
| Reranking | Reordering documents by relevance. |
| Relevance score | Numerical estimate of how well a document matches the query. |
| Query-document pair | Two texts evaluated together. |
| Batch size | Number of pairs processed per batch. |
| Truncation | Cutting off text exceeding the model's token limit. |
| Top K | Number of highest-ranked documents retained. |

## 7. CrossEncoder vs. Embeddings

| Embedding Model | CrossEncoder |
|---|---|
| Processes texts separately. | Processes query and document together. |
| Produces vectors. | Produces relevance scores. |
| Fast for large-scale retrieval. | Slower but generally more accurate for reranking. |
| Used for semantic search. | Used for reranking search results. |

## 8. Documentation

CrossEncoder Usage:
https://sbert.net/docs/cross_encoder/usage/usage.html

CrossEncoder API Reference:
https://sbert.net/docs/package_reference/cross_encoder/cross_encoder.html

SentenceTransformers Documentation:
https://sbert.net/
