from sentence_transformers import CrossEncoder

def re_ranker(model:CrossEncoder, user_prompt:str, docs:list[str]):
	"""
	Re ranker, will recieve the pre selected chunks and make
	a second filtering with SentenceTransforemes CrossEncoder model.
	Args:
		model: model init in FastAPI initialization
		user_prompt: User prompt string
		docs: A list of pre selected chunks of string texts
	Return:
    	A sorted list with the "corpus_id", "score", and optionally "text" of the documents.
	"""

	#+ Turn the list of lists from Chroma into a list of "pre selected" strings
	documents = [doc for group in docs["documents"] for doc in group]

	#+ Rank the prompt agains each of the documents selected by Chroma
	ranks = model.rank(user_prompt, documents, return_documents=True)

	return(ranks)