import chromadb
import uuid
import logging

logger = logging.getLogger(__name__)

def chroma_is_init(collection):
	"""
    Safecheck to see if the DB was init
	:collection: the DB collection retrieved (or not) in main
    :Return: bool to validate
    """
	if collection.count() == 0:
		return False
	else:
		return True

def init_chroma_db(collection, chunks):
	
	#+	Init the DB
	# Prepare data to store
	texts = [doc.page_content for doc in chunks]
	ids = [str(uuid.uuid4()) for _ in texts]
	metadata = []
	metadata = [
		{
			"source": doc.metadata.get("source", "")
		}
		for doc in chunks
	]

	#+	Add chunks to the DB (embedding done by chroma)
	collection.add(
		documents=texts,	# A list of strings
		ids=ids,			# A list of IDS
		metadatas=metadata	# A list of {} metadata
	)
	logger.debug("chroma.py - DB collection created: Success")



def	get_querry_matches(collection, user_prompt:str, tips:list[str], n_result:int):
	"""
    Function to find matching vectors in chromaDB using querry()
	Args:
		collection: DB retrieved from chromaDB
		user_prompt: the prompt string
		tips: an list of strings given by the excersise being evaluated
		n_result: number of returned chunks
    Return:
		A list of size n_result with the matching vectors
    """

	queries = [user_prompt] + tips
	
	results = collection.query(
	query_texts=queries,		# Chroma will embed this automatically
	n_results=n_result			# how many results to return
	)
	logger.debug("chroma.py - Querry matches found: Success")
	return(results)