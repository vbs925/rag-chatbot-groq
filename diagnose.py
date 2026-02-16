"""
Quick diagnostic test to verify RAG chatbot components are working.
Run this to test if the issue is with your setup or the chatbot itself.
"""

import sys
import os

print("=" * 60)
print("RAG Chatbot Diagnostic Test")
print("=" * 60)

# Test 1: Check imports
print("\n Testing imports...")
try:
    import streamlit
    from langchain_groq import ChatGroq
    from langchain.chains import RetrievalQA
    from src.document_processor import DocumentProcessor
    from src.embeddings import EmbeddingManager
    from src.vector_store import VectorStoreManager
    from src.rag_chain import RAGChain
    from dotenv import load_dotenv
    print("All imports successful!")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Test 2: Check API key
print("\n Testing API key...")
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key and groq_api_key.startswith("gsk_"):
    print(f"API key found (starts with: {groq_api_key[:10]}...)")
else:
    print("API key not found or invalid!")
    sys.exit(1)

# Test 3: Initialize components
print("\n Testing component initialization...")
try:
    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.get_embeddings()
    print("Embeddings initialized!")
    
    vector_store_manager = VectorStoreManager(embeddings)
    print("Vector store manager initialized!")
    
    rag_chain = RAGChain(groq_api_key)
    print("RAG chain initialized!")
except Exception as e:
    print(f"Initialization error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test with sample text
print("\n Testing with sample document...")
try:
    from langchain.schema import Document
    
    # Create sample documents
    sample_docs = [
        Document(page_content="Python is a high-level programming language.", metadata={"source": "test"}),
        Document(page_content="Machine learning is a subset of artificial intelligence.", metadata={"source": "test"}),
        Document(page_content="RAG combines retrieval with generation for better AI responses.", metadata={"source": "test"})
    ]
    
    print("  Creating vector store...")
    vector_store_manager.create_vector_store(sample_docs)
    print("Vector store created!")
    
    print("  Setting up retriever...")
    retriever = vector_store_manager.get_retriever(k=2)
    print("Retriever ready!")
    
    print("  Creating QA chain...")
    rag_chain.create_qa_chain(retriever)
    print("QA chain ready!")
    
except Exception as e:
    print(f"Document processing error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test query
print("\n Testing query with Groq API...")
try:
    test_question = "What is Python?"
    print(f"  Question: {test_question}")
    response = rag_chain.query(test_question)
    
    print("Query successful!")
    print(f"\n  Answer: {response['result'][:200]}...")
    print(f"  Sources: {len(response['source_documents'])} documents")
    
except Exception as e:
    print(f"Query error: {e}")
    print("\nPossible issues:")
    print("  1. Check your Groq API key is valid")
    print("  2. Check internet connection")
    print("  3. Groq API might be temporarily down")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nYour RAG chatbot is working correctly!")
print("If the Streamlit app still has issues, try:")
print("  1. Restart Streamlit (Ctrl+C and run again)")
print("  2. Clear browser cache")
print("  3. Check browser console for errors (F12)")
