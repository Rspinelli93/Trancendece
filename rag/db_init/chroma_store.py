import hashlib
import logging

logger = logging.getLogger(__name__)

def chroma_is_init(collection):
	return collection.count() > 0

def add_data_to_chroma_db(collection, chunks:list):
    """
    Function to init the DB
    Args:
        collection: the DB collection retrieved (or not) in main
        chunks: the chunked documents
        Each Document element:
                .page_content -> Chunk text
                .metadata -> Original document metadata
    """

    #+	Init the DB
    # Prepare data to store
    texts = [doc.page_content for doc in chunks]

    # Use deterministic IDs (meaning same id if the same value, no repetiton)
    ids = [hashlib.sha256(text.encode("utf-8")).hexdigest() for text in texts] 
    metadata = []
    metadata = [
        {
            "source": doc.metadata.get("source", "")
        }
        for doc in chunks
    ]

    #+	Add chunks to the DB (embedding done by chroma)
    #+  Upsert with deterministic IDs will not create extra records on double init
    collection.upsert(
        documents=texts,	# A list of strings
        ids=ids,			# A list of IDS
        metadatas=metadata	# A list of {} metadata
    )
    logger.debug("chroma.py - DB collection created: Success")
