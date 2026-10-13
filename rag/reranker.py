from sentence_transformers import CrossEncoder

def re_ranker(user_prompt, docs):
	#+ Load the CrossEncoder model selected
	model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

	#+ Turn the list of lists from Chroma into a list of "pre selected" strings
	documents = [doc for group in docs["documents"] for doc in group]

	#+ Rank the prompt agains each of the documents selected by Chroma
	ranks = model.rank(user_prompt, documents)

	print(ranks)