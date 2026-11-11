import logging
import chromadb
import chroma_store
import chunking
import pathlib

logger = logging.getLogger(__name__)
chroma_client = chromadb.PersistentClient(path="../chroma_db")

def main():
    # Get the DB
    collection = chroma_client.get_or_create_collection(name="trancendence_rag")
    logger.info("ChromaDB get: Success")

    # Chunk all 3 docs
    if not chroma_store.chroma_is_init(collection):
        c_book_chunked = chunking.chunker("../docs/C_Book_2nd.pdf", 8, 217)
        libc_chunked = chunking.chunker("../docs/libc.pdf", 27, 1018)

        chroma_store.add_data_to_chroma_db(collection, c_book_chunked)
        chroma_store.add_data_to_chroma_db(collection, libc_chunked)
        logger.info("ChromaDB initialized successfully")
    else:
        logger.info("ChromaDB already initialized")

if __name__ == "__main__":
    main()