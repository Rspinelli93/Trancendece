import logging
import retrieval
import api
import llm
import chroma
import schemas

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='info.log', level=logging.DEBUG, filemode='w', format='%(asctime)s - %(message)s')
