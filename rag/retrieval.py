import chromadb
import logging
import chroma
import reranker
import llm
import schemas

logger = logging.getLogger(__name__)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def retrieve_message(prompt: schemas.Prompt):
    # Load ChromaDB
    collection = chroma_client.get_collection(name="trancendence_rag")

    # Vector Searching and retrieval
    matches = chroma.get_querry_matches(collection, prompt.question + prompt.description, 5)

    # Rerank the retireved chunks with SentenceTransformers
    ranks = reranker.re_ranker(prompt.question, matches)

    # Send context to the LLM
    message = llm.get_llm_answer(ranks, prompt)

    return(message)