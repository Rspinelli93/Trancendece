import logging
from fastapi import FastAPI, HTTPException
import retrieval

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "OK"}

@app.post("/ask")
def retrieve_response():
    retrieval.retrieve_message()