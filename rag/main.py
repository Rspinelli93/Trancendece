import logging
import chunking
import chromadb
import chroma

logger = logging.getLogger(__name__)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def main():
	logging.basicConfig(filename='info.log', level=logging.DEBUG, filemode='w', format='%(asctime)s - %(message)s')

	collection = chroma_client.get_or_create_collection(name="trancendence_rag")
	if not chroma.chroma_is_init(collection):
		chunked_doc = chunking.chunker()
		chroma.init_chroma_db(collection, chunked_doc)
	matches = chroma.get_querry_matches(collection, "What is a pointer?", ["memory", "seg_fault", "pointer"], 5)
	print(matches)

main()