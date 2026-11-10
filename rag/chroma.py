import logging

logger = logging.getLogger(__name__)

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