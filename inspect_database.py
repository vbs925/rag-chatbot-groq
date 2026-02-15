"""
Script to access and inspect the ChromaDB backend database.
This shows you what documents are stored and allows querying.
"""

import sys
import os
import argparse
from pathlib import Path
from langchain_community.vectorstores import Chroma
from src.embeddings import EmbeddingManager

print("=" * 70)
print("ChromaDB Database Inspector")
print("=" * 70)

# Parse arguments
parser = argparse.ArgumentParser(description='Inspect ChromaDB contents')
parser.add_argument('path', nargs='?', default='./chroma_db', help='Path to the ChromaDB directory')
args = parser.parse_args()

db_path = args.path

# Check if database exists
if not os.path.exists(db_path):
    print(f"\n❌ No database found at: {db_path}")
    if db_path == './chroma_db':
        print(f"   Default location checked.")
    else:
        print(f"   Please check the path and try again.")
    print("\n💡 Tip: Check the 'Debug Information' in the Streamlit sidebar for the current database path.")
    exit(0)

print(f"\n✅ Database found at: {Path(db_path).absolute()}")

# Initialize embeddings
print("\n🔄 Loading database...")
embedding_manager = EmbeddingManager()
embeddings = embedding_manager.get_embeddings()

# Load existing vector store (Chroma automatically loads from persist_directory)
try:
    vector_store = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )
    print("✅ Database loaded successfully!")
    
    # Get the underlying ChromaDB collection
    collection = vector_store._collection
    
    # Show database stats
    count = collection.count()
    print(f"\n📊 Database Statistics:")
    print(f"   Total documents/chunks: {count}")
    
    if count > 0:
        # Get all documents
        results = collection.get(limit=min(count, 10), include=['documents', 'metadatas'])
        
        print(f"\n📄 Sample Documents (showing first {min(count, 10)}):")
        print("-" * 70)
        
        for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas']), 1):
            print(f"\n{i}. Source: {metadata.get('source', 'unknown')}")
            print(f"   Content preview: {doc[:100]}...")
        
        # Test search
        print("\n" + "=" * 70)
        print("🔍 Test Search")
        print("=" * 70)
        
        query = "What is this document about?"
        print(f"\nQuery: '{query}'")
        
        search_results = vector_store.similarity_search(query, k=3)
        print(f"\nTop {len(search_results)} results:")
        
        for i, doc in enumerate(search_results, 1):
            print(f"\n{i}. {doc.page_content[:150]}...")
            print(f"   Source: {doc.metadata.get('source', 'unknown')}")
    
    print("\n" + "=" * 70)
    print("✅ Database inspection complete!")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error loading database: {e}")
    exit(1)

print("\n💡 Database Operations:")
print("\n💡 Database Operations:")
print(f"   - Current location: {db_path}")
print("   - View contents: python inspect_database.py [path_to_db]")
print("   - Note: Streamlit app uses temporary directories, check debug info for path.")
