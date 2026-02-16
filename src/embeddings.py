"""Embeddings module for generating text embeddings."""

import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings


@st.cache_resource
def get_huggingface_embeddings(model_name: str):
    """
    Get or create cached embeddings instance.
    
    Args:
        model_name: Name of the sentence transformer model to use
        
    Returns:
        HuggingFaceEmbeddings instance
    """
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


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
            self.embeddings = get_huggingface_embeddings(self.model_name)
        return self.embeddings
