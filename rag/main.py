import logging
import chunking
import chromadb
import chroma
import reranker
import llm

logger = logging.getLogger(__name__)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def main():
	user_prompt = "What is a pointer?"				#User prompt recieved in HTTP
	tips = ["memory lost", "seg_fault", "pointer"]	#Pre set excersise tips
	forbidden_functions = ["printf"]				#Pre set forbidden functions
	excersise_subject = "Make a function that swaps two pointers"
	code = """
			int main(void)
			{
				char *ptr1 = "hola";
				
			}
			"""									#User code

	#Try to log to ChromaDB
	logging.basicConfig(filename='info.log', level=logging.DEBUG, filemode='w', format='%(asctime)s - %(message)s')

	#Check if ChromaDB was loaded
	collection = chroma_client.get_or_create_collection(name="trancendence_rag")

	#If not loaded, load, chunck, vectorize, store
	if not chroma.chroma_is_init(collection):
		chunked_doc = chunking.chunker()
		chroma.init_chroma_db(collection, chunked_doc)

	#Get matched from ChromaDB + User prompt + tips
	matches = chroma.get_querry_matches(collection, user_prompt, tips, 5)

	#Rerank the retireved chunks with SentenceTransformers
	ranks = reranker.re_ranker(user_prompt, matches)

	#Send context to the LLM
	message = llm.get_llm_answer(ranks, user_prompt, tips, code, excersise_subject, forbidden_functions)

	print(message)
	
main()
