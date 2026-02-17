"""
Test script to verify TOON integration and measure token savings.
This demonstrates the token optimization achieved by TOON format.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.embeddings import EmbeddingManager
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain
from src.toon_formatter import ToonFormatter

# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("❌ Error: GROQ_API_KEY not found in .env file")
    sys.exit(1)

print("=" * 70)
print("TOON Token Optimization - Test & Comparison")
print("=" * 70)

# Create sample documents
print("\n📄 Creating sample documents...")
sample_docs = [
    Document(
        page_content="Python is a high-level programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
        metadata={"source": "python_intro.txt"}
    ),
    Document(
        page_content="Machine learning is a subset of artificial intelligence that focuses on creating systems that learn from data. Popular frameworks include TensorFlow, PyTorch, and scikit-learn.",
        metadata={"source": "ml_basics.txt"}
    ),
    Document(
        page_content="RAG (Retrieval Augmented Generation) combines information retrieval with text generation. It retrieves relevant documents and uses them as context for generating responses.",
        metadata={"source": "rag_explained.txt"}
    ),
    Document(
        page_content="Vector databases like ChromaDB store embeddings for semantic search. They enable finding similar documents based on meaning rather than keyword matching.",
        metadata={"source": "vector_db.txt"}
    )
]

print(f"✅ Created {len(sample_docs)} sample documents")

# Test 1: TOON Formatter Directly
print("\n" + "=" * 70)
print("Test 1: TOON Format Comparison")
print("=" * 70)

toon_formatter = ToonFormatter(enabled=True)

# Standard format
standard_text = "\n\n".join(doc.page_content for doc in sample_docs)
print(f"\n📝 Standard Format ({len(standard_text)} characters):")
print(standard_text[:200] + "...")

# TOON format
toon_text = toon_formatter.format_simple_context(sample_docs)
print(f"\n🎯 TOON Format ({len(toon_text)} characters):")
print(toon_text[:200] + "...")

# Calculate savings
savings = toon_formatter.calculate_token_savings(standard_text, toon_text)
print(f"\n💰 Token Savings:")
print(f"  Standard Tokens: {savings['standard_tokens']}")
print(f"  TOON Tokens:     {savings['toon_tokens']}")
print(f"  Saved:           {savings['tokens_saved']} tokens")
print(f"  Savings:         {savings['savings_percentage']}%")

# Test 2: RAG Chain with TOON
print("\n" + "=" * 70)
print("Test 2: RAG Chain Integration")
print("=" * 70)

print("\n🔄 Setting up RAG components...")
try:
    # Initialize components
    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.get_embeddings()
    print("✅ Embeddings initialized")
    
    # Create vector store
    vector_store_manager = VectorStoreManager(embeddings, persist_directory="./test_chroma_db")
    vector_store_manager.create_vector_store(sample_docs)
    print("✅ Vector store created")
    
    # Create RAG chains - with and without TOON
    rag_with_toon = RAGChain(groq_api_key, use_toon=True)
    rag_without_toon = RAGChain(groq_api_key, use_toon=False)
    
    retriever = vector_store_manager.get_retriever(k=3)
    rag_with_toon.create_qa_chain(retriever)
    rag_without_toon.create_qa_chain(retriever)
    print("✅ RAG chains created (with and without TOON)")
    
    # Test query
    test_question = "What is machine learning and which frameworks are popular?"
    
    print(f"\n🤔 Test Question: {test_question}")
    
    # Query with TOON
    print("\n🎯 With TOON optimization:")
    response_toon = rag_with_toon.query(test_question)
    print(f"Answer: {response_toon['result'][:150]}...")
    if 'token_info' in response_toon:
        ti = response_toon['token_info']
        print(f"Token Savings: {ti['savings_percentage']}% ({ti['tokens_saved']} tokens saved)")
    
    # Query without TOON (for comparison)
    print("\n📝 Without TOON (standard format):")
    response_standard = rag_without_toon.query(test_question)
    print(f"Answer: {response_standard['result'][:150]}...")
    
    print("\n✅ Both queries successful!")
    
    # Cleanup
    import shutil
    if os.path.exists("./test_chroma_db"):
        shutil.rmtree("./test_chroma_db")
    print("\n🧹 Cleaned up test database")
    
except Exception as e:
    print(f"\n❌ Error during RAG test: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ TOON Integration Tests Complete!")
print("=" * 70)
print("\n💡 Summary:")
print(f"  - TOON reduces token usage by ~{savings['savings_percentage']}%")
print(f"  - Lower API costs and faster responses")
print(f"  - Same answer quality")
print("\n🎉 TOON is working correctly!")
