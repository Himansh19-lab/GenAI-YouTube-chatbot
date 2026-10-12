

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path



from src.logger import Logger
from src.interface.component_interface import ComponentInterface    


class Indexer(ComponentInterface):
    def __init__(self, embedding_model: object):
        """
        Initializes the Indexer with the provided embedding model.
        Arguments:
            embedding_model (object): The embedding model to be used for creating the FAISS index.
            text_splitter (RecursiveCharacterTextSplitter): The text splitter to be used for splitting the transcript.              
        """
        self.logger = Logger(__name__, log_file="indexer.log", level="DEBUG").logger
        self.embeddings = embedding_model
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.index_file_path = Path(__file__).resolve().parents[1] / "VectorStore" / "faiss_index"
    

    def split_transcript(self, transcript: str):
        """
        Splits the provided transcript into smaller chunks using the text splitter.
        Arguments:
            transcript (str): The transcript text to be split.
        Returns:
            List[str]: A list of transcript chunks.
        """
        if not isinstance(transcript, str) or not transcript.strip():
            self.logger.error(
                "Transcript must be a non-empty string. "
                "Received: %s",
                type(transcript).__name__
            )
            return []
        try:
            chunks = self.text_splitter.create_documents([transcript])
            self.logger.info(f"Successfully split transcript into {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            self.logger.error(f"An error occurred while splitting the transcript: {e}")
            return [] 
    
    def create_vector_index(self, chunks):
        """
        Creates a FAISS index from the provided transcript by first splitting it into chunks and then creating embeddings.
        Arguments:
            transcript (str): The transcript text to be indexed.
        Returns:
            FAISS: The created FAISS index.
        """
        try:
            vector_store = FAISS.from_documents(chunks, self.embeddings)
            self.logger.info("Successfully created FAISS index from transcript chunks.")
            return vector_store
        except Exception as e:
            self.logger.error(f"An error occurred while creating the FAISS index: {e}")
            return None

    def store_vector_index(self, vector_store, index_file_path):
        """
        Stores the provided FAISS index to a file.
        Arguments:
            vector_store (FAISS): The FAISS index to be stored.
            index_file_path (str): The file path where the index should be stored.
        """
        try:
            Path(index_file_path).parent.mkdir(parents=True, exist_ok=True)
            vector_store.save_local(index_file_path)
            self.logger.info(f"Successfully stored FAISS index at: {index_file_path}")
        except Exception as e:
            self.logger.error(f"An error occurred while storing the FAISS index: {e}")

    def invoke(self, transcript):
        """
        Invokes the indexing process: splits the transcript, creates a FAISS index, and stores it.
        Arguments:
            transcript (str): The transcript text to be indexed.
            index_file_path (str): The file path where the index should be stored.
        """
        try:
            chunks = self.split_transcript(transcript)
            if not chunks:
                self.logger.error("No chunks were created from the transcript. Aborting indexing process.")
                return None
            
            vector_store = self.create_vector_index(chunks)
            if vector_store is None:
                self.logger.error("FAISS index creation failed. Aborting indexing process.")
                return None
            
            self.store_vector_index(vector_store, self.index_file_path)
            return vector_store
        except Exception as e:
            self.logger.error(f"An error occurred during the indexing process: {e}")
            raise
        
