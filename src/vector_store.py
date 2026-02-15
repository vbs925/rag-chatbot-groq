"""Vector store module for ChromaDB operations."""

from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStoreManager:
    """Manages ChromaDB vector store operations."""
    
    def __init__(self, embeddings: HuggingFaceEmbeddings, persist_directory: str = "./chroma_db"):
        """
        Initialize the vector store manager.
        
        Args:
            embeddings: Embeddings instance for vectorization
            persist_directory: Directory to persist the vector database
        """
        self.embeddings = embeddings
        self.persist_directory = persist_directory
        self.vector_store = None
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create a new vector store from documents.
        
        Args:
            documents: List of Document objects to store
            
        Returns:
            Chroma vector store instance
        """
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return self.vector_store
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to existing vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if self.vector_store is None:
            self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)
    
    def get_retriever(self, k: int = 4):
        """
        Get a retriever for similarity search.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever instance
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Add documents first.")
        
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar Document objects
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Add documents first.")
        
        return self.vector_store.similarity_search(query, k=k)
