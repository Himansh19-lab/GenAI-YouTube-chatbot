from langchain_core.documents import Document

from src.logger import Logger
from src.interface.component_interface import ComponentInterface



class Retriever(ComponentInterface):
    def __init__(self, vector_store: object):
        """
        Initializes the Retriever with the provided vector store.
        Arguments:
            vector_store (object): The vector store to be used for retrieving relevant chunks.
        """
        self.logger = Logger(__name__, log_file="retriever.log", level="DEBUG").logger
        self.vector_store = vector_store

    def retrieve_relevant_chunks(self, query: str, k: int = 5) -> list[Document]:
        """
        Retrieves the most relevant chunks from the vector store based on the provided query.
        Arguments:
            query (str): The query text for which to retrieve relevant chunks.
            k (int): The number of top relevant chunks to retrieve. Default is 5.
        Returns:
            List[str]: A list of the most relevant transcript chunks.
        """         
        try:
            retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k, "fetch_k": 20 })
            relevant_chunks = retriever.invoke(query)
            self.logger.info(f"Successfully retrieved {len(relevant_chunks)} relevant chunks for the query.")
            return relevant_chunks
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving relevant chunks: {e}")
            raise
    
    def invoke(self, *args, **kwargs):
        """
        Invokes the retrieval process using the provided arguments.
        Arguments:
            *args: Positional arguments for the retrieval process.
            **kwargs: Keyword arguments for the retrieval process.
        Returns:
            List[str]: A list of the most relevant transcript chunks.
        """
        return self.retrieve_relevant_chunks(*args, **kwargs)

