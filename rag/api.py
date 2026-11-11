import logging
from fastapi import FastAPI, HTTPException
import schemas
import chromadb
import chroma
import reranker
import llm
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
app = FastAPI()
#+ Load the CrossEncoder model selected
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

@app.get("/")
async def root():
    return {"status": "OK"}

@app.post("/ask")
def retrieve_message(prompt: schemas.Prompt):
    # Load ChromaDB
    collection = chroma_client.get_collection(name="trancendence_rag")

    # Vector Searching and retrieval
    matches = chroma.get_querry_matches(collection, prompt.question, 5)

    # Rerank the retireved chunks with SentenceTransformers
    ranks = reranker.re_ranker(reranker_model, prompt.question, matches)

    # Send context to the LLM
    message = llm.get_llm_answer(ranks, prompt)

    return(message)