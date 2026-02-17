"""TOON formatter module for token-efficient data representation.

This module provides utilities to format document context using TOON
(Token-Oriented Object Notation) format, reducing token usage by 30-60%
compared to standard JSON/text formatting when sending to LLM APIs.

Uses the 'toons' library - a high-performance Rust-based TOON implementation.
"""

import toons


class ToonFormatter:
    """Handles TOON formatting for RAG context and responses."""
    
    def __init__(self, enabled: bool = True):
        """
        Initialize TOON formatter.
        
        Args:
            enabled: Whether to use TOON formatting (default: True)
        """
        self.enabled = enabled
    
    def format_documents_as_toon(self, documents: list) -> str:
        """
        Format retrieved documents as TOON for efficient token usage.
        
        Args:
            documents: List of Document objects from vector store
            
        Returns:
            TOON-formatted string representation
        """
        if not self.enabled or not documents:
            # Fallback to standard formatting
            return "\\n\\n".join(doc.page_content for doc in documents)
        
        try:
            # Create structured data for TOON
            doc_data = {
                "chunks": [
                    {
                        "id": i + 1,
                        "text": doc.page_content,
                        "src": doc.metadata.get("source", "")[:20]  # Abbreviated source
                    }
                    for i, doc in enumerate(documents)
                ]
            }
            
            # Convert to TOON format using toons library
            toon_str = toons.dumps(doc_data)
            return toon_str
            
        except Exception as e:
            # Fallback to standard format if TOON fails
            print(f"TOON formatting failed: {e}. Using standard format.")
            return "\\n\\n".join(doc.page_content for doc in documents)
    
    def format_simple_context(self, documents: list) -> str:
        """
        Format documents with a simpler TOON structure for maximum token savings.
        
        Uses toons library to encode list of document contents.
        TOON format is more compact than JSON for arrays.
        
        Args:
            documents: List of Document objects
            
        Returns:
            TOON-formatted string
        """
        if not self.enabled or not documents:
            return "\\n\\n".join(doc.page_content for doc in documents)
        
        try:
            # Extract just the content as a list
            content_list = [doc.page_content for doc in documents]
            
            # Use toons library to encode
            # TOON format for arrays: [n]: item1,item2,item3
            toon_str = toons.dumps(content_list)
            return toon_str
            
        except Exception as e:
            print(f"TOON formatting failed: {e}. Using standard format.")
            return "\\n\\n".join(doc.page_content for doc in documents)
    
    def calculate_token_savings(self, standard_text: str, toon_text: str) -> dict:
        """
        Calculate approximate token savings between standard and TOON formats.
        
        Args:
            standard_text: Original text format
            toon_text: TOON-formatted text
            
        Returns:
            Dictionary with token counts and savings percentage
        """
        # Approximate token count (1 token ≈ 4 characters for English)
        standard_tokens = len(standard_text) / 4
        toon_tokens = len(toon_text) / 4
        
        savings = standard_tokens - toon_tokens
        savings_pct = (savings / standard_tokens * 100) if standard_tokens > 0 else 0
        
        return {
            "standard_tokens": int(standard_tokens),
            "toon_tokens": int(toon_tokens),
            "tokens_saved": int(savings),
            "savings_percentage": round(savings_pct, 1)
        }
    
    def toggle(self, enabled: bool):
        """
        Toggle TOON formatting on/off.
        
        Args:
            enabled: True to enable TOON, False to disable
        """
        self.enabled = enabled
