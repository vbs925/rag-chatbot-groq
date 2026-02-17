"""
Example script to test RAG chatbot components.
This script verifies that all components work correctly together.
"""

import os
from pathlib import Path

# Create a sample text file for testing
sample_text = """
Artificial Intelligence and Machine Learning

Artificial Intelligence (AI) is the simulation of human intelligence processes by machines,
especially computer systems. These processes include learning, reasoning, and self-correction.

Machine Learning (ML) is a subset of AI that provides systems the ability to automatically
learn and improve from experience without being explicitly programmed. ML focuses on the
development of computer programs that can access data and use it to learn for themselves.

Deep Learning is a subset of machine learning that uses neural networks with multiple layers.
These neural networks attempt to simulate the behavior of the human brain to "learn" from
large amounts of data.

Applications of AI include:
1. Natural Language Processing (NLP)
2. Computer Vision
3. Robotics
4. Expert Systems
5. Speech Recognition

The future of AI holds tremendous potential for transforming various industries including
healthcare, finance, transportation, and education.
"""

# Create test document
def create_test_document():
    """Create a test document for RAG chatbot."""
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "sample_ai_document.txt"
    with open(test_file, "w") as f:
        f.write(sample_text)
    
    print(f"✅ Created test document: {test_file}")
    return test_file


def test_document_processor():
    """Test document processing."""
    from src.document_processor import DocumentProcessor
    
    print("\n🧪 Testing Document Processor...")
    test_file = create_test_document()
    
    processor = DocumentProcessor(chunk_size=200, chunk_overlap=50)
    chunks = processor.process_document(str(test_file))
    
    print(f"✅ Document processed into {len(chunks)} chunks")
    print(f"   First chunk preview: {chunks[0].page_content[:100]}...")
    
    return chunks


def test_embeddings():
    """Test embedding generation."""
    from src.embeddings import EmbeddingManager
    
    print("\n🧪 Testing Embeddings...")
    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.get_embeddings()
    
    # Test embedding
    test_text = "This is a test sentence for embedding."
    embedding = embeddings.embed_query(test_text)
    
    print(f"✅ Embedding generated with dimension: {len(embedding)}")
    
    return embeddings


def test_vector_store(chunks, embeddings):
    """Test vector store operations."""
    from src.vector_store import VectorStoreManager
    
    print("\n🧪 Testing Vector Store...")
    vector_store_manager = VectorStoreManager(embeddings, persist_directory="./test_chroma_db")
    vector_store_manager.create_vector_store(chunks)
    
    # Test similarity search
    query = "What is machine learning?"
    results = vector_store_manager.similarity_search(query, k=2)
    
    print(f"✅ Vector store created and tested")
    print(f"   Query: '{query}'")
    print(f"   Found {len(results)} similar chunks")
    print(f"   Top result preview: {results[0].page_content[:100]}...")
    
    return vector_store_manager


def test_rag_chain(vector_store_manager):
    """Test RAG chain (requires Groq API key)."""
    from src.rag_chain import RAGChain
    from dotenv import load_dotenv
    
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("\n⚠️  Skipping RAG chain test - GROQ_API_KEY not found in .env")
        print("   To test RAG chain, add your Groq API key to .env file")
        return
    
    print("\n🧪 Testing RAG Chain with Groq API...")
    rag_chain = RAGChain(groq_api_key)
    retriever = vector_store_manager.get_retriever(k=3)
    rag_chain.create_qa_chain(retriever)
    
    # Test query
    question = "What is the difference between AI and Machine Learning?"
    response = rag_chain.query(question)
    
    print(f"✅ RAG chain tested successfully")
    print(f"   Question: {question}")
    print(f"   Answer: {response['result'][:200]}...")
    print(f"   Used {len(response['source_documents'])} source documents")


def cleanup():
    """Clean up test files."""
    import shutil
    
    print("\n🧹 Cleaning up test files...")
    
    # Remove test data
    if Path("test_data").exists():
        shutil.rmtree("test_data")
    
    # Remove test ChromaDB
    if Path("test_chroma_db").exists():
        shutil.rmtree("test_chroma_db")
    
    print("✅ Cleanup complete")


def main():
    """Run all tests."""
    print("=" * 60)
    print("RAG Chatbot Component Tests")
    print("=" * 60)
    
    try:
        # Test components
        chunks = test_document_processor()
        embeddings = test_embeddings()
        vector_store_manager = test_vector_store(chunks, embeddings)
        test_rag_chain(vector_store_manager)
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup()


if __name__ == "__main__":
    main()
