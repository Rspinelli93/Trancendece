from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
#* DirectoryLoader: Loads multiple files from a directory.
#* PyPDFLoader: Loads PDF files and extracts their content into Document objects.
#* RecursiveCharacterTextSplitter: Splits documents into smaller chunks, trying to preserve text structure (paragraphs, sentences, words).

logger = logging.getLogger(__name__)

def chunker():
	"""
    Function to chunk documentation
	Document:
		An object defined by PyPDFLoader
		Each Document element:
			.page_content -> Chunk text
			.metadata -> Original document metadata
    Return:
		A list of Document instances
    """

	#- INIT THE FILE LOADER
	#(Check the documentation of PyPDFLoader, many values are set to default in this __init__ call)
	loader = PyMuPDFLoader(
		file_path="./docs/C_Book_2nd.pdf",
		mode="page",
		extract_images=False
	)
	logger.debug("chunking.py - Loader Created")
	# Call the function load() to load the text and init the instance Document
	docs = loader.load()
	logger.debug("chunking.py - Document Loaded")
	
	# Skip intro and outro
	docs = docs[8:]

	#- INIT THE TEXT SPLITTER
	# decide here how small you want to chunk, its set to max at 1000/200
	splitter = RecursiveCharacterTextSplitter(
		chunk_size=1000,
		chunk_overlap=200
	)
	logger.debug("chunking.py - Splitter Created")
	# Call the function split_documents() to split the docs and init the list of Documents
	# Each document in the list is a chunck of the original
	chunks = splitter.split_documents(docs)
	logger.debug("chunking.py - Docs Splitted")
	return (chunks)

chunker()