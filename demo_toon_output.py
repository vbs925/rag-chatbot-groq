"""
Demonstration: Show actual TOON output sent to Groq API
This shows the difference between standard and TOON-formatted context.
"""

import os
from dotenv import load_dotenv
from langchain_core.documents import Document

from src.embeddings import EmbeddingManager
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain

# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

print("=" * 80)
print("TOON FORMAT DEMONSTRATION - What Your Chatbot Sends to Groq")
print("=" * 80)

# Sample documents (simulating what comes from vector store)
sample_docs = [
    Document(
        page_content="Python is a high-level programming language known for simplicity and readability.",
        metadata={"source": "python_intro.txt"}
    ),
    Document(
        page_content="Machine learning is a subset of AI that focuses on algorithms learning from data.",
        metadata={"source": "ml_basics.txt"}
    ),
    Document(
        page_content="RAG combines retrieval and generation for context-aware AI responses.",
        metadata={"source": "rag_explained.txt"}
    )
]

print("\nSample Documents (3 chunks):")
for i, doc in enumerate(sample_docs, 1):
    print(f"  {i}. {doc.page_content[:60]}...")

# Create RAG chains - with and without TOON
print("\n" + "=" * 80)
print("COMPARISON: Standard vs TOON Format")
print("=" * 80)

# Standard format (TOON disabled)
rag_standard = RAGChain(groq_api_key, use_toon=False)
standard_context = rag_standard.format_docs(sample_docs)

print("\nSTANDARD FORMAT (use_toon=False):")
print("-" * 80)
print(standard_context)
print("-" * 80)
print(f"Length: {len(standard_context)} characters (~{len(standard_context)//4} tokens)")

# TOON format (TOON enabled)
rag_toon = RAGChain(groq_api_key, use_toon=True)
toon_context = rag_toon.format_docs(sample_docs)

print("\nTOON FORMAT (use_toon=True) ← THIS IS WHAT GROQ RECEIVES:")
print("-" * 80)
print(toon_context)
print("-" * 80)
print(f"Length: {len(toon_context)} characters (~{len(toon_context)//4} tokens)")

# Show savings
char_saved = len(standard_context) - len(toon_context)
token_saved = char_saved // 4
savings_pct = (char_saved / len(standard_context)) * 100

print("\nTOKEN SAVINGS:")
print(f"  Characters saved: {char_saved}")
print(f"  Tokens saved:     ~{token_saved}")
print(f"  Savings:          {savings_pct:.1f}%")

# Show the actual prompt sent to Groq
print("\n" + "=" * 80)
print("COMPLETE PROMPT SENT TO GROQ API (with TOON)")
print("=" * 80)

question = "What is machine learning?"
full_prompt = rag_toon.prompt_template.format(context=toon_context, question=question)

print(full_prompt)
print("=" * 80)

print("\nThis is exactly what Groq receives when you ask a question!")
print("   The TOON format makes it more compact, saving you tokens and money.")
