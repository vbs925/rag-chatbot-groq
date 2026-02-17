import os
import sys
from src.document_processor import DocumentProcessor
import nltk

# Ensure NLTK data path includes user's home directory
nltk.data.path.append(os.path.expanduser("~/nltk_data"))

def debug_file(file_path):
    print(f"--- Debugging: {file_path} ---")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    
    print("1. Loading document...")
    try:
        docs = processor.load_document(file_path)
        print(f"   Loaded {len(docs)} raw document objects.")
        total_len = sum(len(d.page_content) for d in docs)
        print(f"   Total raw text length: {total_len} characters.")
        
        if total_len == 0:
            print("   WARNING: Loaded text is empty!")
        else:
            print(f"   First 500 chars start: {docs[0].page_content[:500]!r}")
            print(f"   Last 500 chars end: {docs[-1].page_content[-500:]!r}")

    except Exception as e:
        print(f"   ERROR loading document: {e}")
        return

    print("\n2. Chunking document...")
    try:
        chunks = processor.chunk_documents(docs)
        print(f"   Created {len(chunks)} chunks.")
        
        if not chunks:
            print("   WARNING: No chunks created.")
            return

        print("\n   --- Chunk Statistics ---")
        sizes = [len(c.page_content) for c in chunks]
        if sizes:
            print(f"   Min chunk size: {min(sizes)}")
            print(f"   Max chunk size: {max(sizes)}")
            print(f"   Avg chunk size: {sum(sizes)/len(sizes):.2f}")

        print("\n   --- Sample Chunks ---")
        print(f"   Chunk 1: {chunks[0].page_content[:200]!r}...")
        if len(chunks) > 1:
            print(f"   Chunk {len(chunks)}: {chunks[-1].page_content[:200]!r}...")

    except Exception as e:
        print(f"   ERROR chunking document: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = "default_document.txt"
    
    debug_file(target_file)
