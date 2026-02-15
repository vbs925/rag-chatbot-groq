"""Embeddings module for generating text embeddings."""

from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingManager:
    """Manages text embedding generation."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding manager.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.embeddings = None
    
    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Get or create embeddings instance.
        
        Returns:
            HuggingFaceEmbeddings instance
        """
        if self.embeddings is None:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        return self.embeddings
