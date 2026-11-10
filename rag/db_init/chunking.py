from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
#* DirectoryLoader: Loads multiple files from a directory.
#* PyPDFLoader: Loads PDF files and extracts their content into Document objects.
#* RecursiveCharacterTextSplitter: Splits documents into smaller chunks, trying to preserve text structure (paragraphs, sentences, words).

logger = logging.getLogger(__name__)

def chunker(doc, start, end):
	"""
    Chunk the desired pdf document
	Document:
		An object defined by PyPDFLoader
		Each Document element:
			.page_content -> Chunk text
			.metadata -> Original document metadata
	Args: 
		- doc: path to pdf to be chunked
		- start: page to begin chunking
		- end: last page to chunk
    Return:
		A list of Document instances
    """

	#- INIT THE FILE LOADER
	loader = PyMuPDFLoader(
		file_path=doc,
		mode="page",
		extract_images=False
	)
	logger.debug("chunking.py - Loader Created")
	# Call the function load() to load the text and init the instance Document
	docs = loader.load()
	logger.debug("chunking.py - Document Loaded")
	
	# Skip intro and outro
	docs = docs[start:end]

	#- INIT THE TEXT SPLITTER
	# decide here how small you want to chunk, its set to max at 1000/200
	splitter = RecursiveCharacterTextSplitter(
		chunk_size=700,
		chunk_overlap=150
	)
	logger.debug("chunking.py - Splitter Created")
	# Call the function split_documents() to split the docs and init the list of Documents
	# Each document in the list is a chunck of the original
	chunks = splitter.split_documents(docs)
	logger.info(f"chunking.py - {doc} Splitted")
	return (chunks)