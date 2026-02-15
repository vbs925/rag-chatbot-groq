"""Streamlit app for RAG Chatbot with Groq API."""

import streamlit as st
import os
import shutil
import tempfile
from pathlib import Path
from dotenv import load_dotenv

from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot with Groq",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'vector_store_ready' not in st.session_state:
    st.session_state.vector_store_ready = False
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'vector_store_manager' not in st.session_state:
    st.session_state.vector_store_manager = None
if 'using_default' not in st.session_state:
    st.session_state.using_default = False
if 'pending_query' not in st.session_state:
    st.session_state.pending_query = None
if 'persist_dir' not in st.session_state:
    st.session_state.persist_dir = None


def initialize_components(groq_api_key: str, persist_directory: str = None):
    """Initialize RAG components."""
    # Initialize embedding manager
    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.get_embeddings()
    
    # Initialize vector store manager
    vector_store_manager = VectorStoreManager(embeddings, persist_directory=persist_directory)
    
    # Initialize RAG chain
    rag_chain = RAGChain(groq_api_key)
    
    return vector_store_manager, rag_chain


def load_default_document(groq_api_key: str):
    """Load default template document if no document is loaded."""
    default_doc_path = Path("default_document.txt")
    
    if not default_doc_path.exists():
        return False
    
    try:
        # Process default document
        doc_processor = DocumentProcessor()
        chunks = doc_processor.process_document(str(default_doc_path))
        
        # Use a temporary directory for the vector store
        # This prevents locking issues when multiple instances run
        persist_dir = tempfile.mkdtemp()
        st.session_state.persist_dir = persist_dir
        
        # Create vector store
        vector_store_manager, rag_chain = initialize_components(groq_api_key, persist_dir)
        vector_store_manager.create_vector_store(chunks)
        
        # Create QA chain
        retriever = vector_store_manager.get_retriever(k=4)
        rag_chain.create_qa_chain(retriever)
        
        # Store in session state
        st.session_state.vector_store_manager = vector_store_manager
        st.session_state.rag_chain = rag_chain
        st.session_state.vector_store_ready = True
        st.session_state.using_default = True
        
        return True
    except Exception as e:
        st.error(f"Failed to load default document: {e}")
        return False



def process_uploaded_file(uploaded_file, groq_api_key: str):
    """Process uploaded file and create vector store."""
    # Save uploaded file temporarily
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / uploaded_file.name
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process document
    with st.spinner("Processing document..."):
        doc_processor = DocumentProcessor()
        chunks = doc_processor.process_document(str(file_path))
        st.success(f"Document processed into {len(chunks)} chunks!")
    
    # Create vector store
    with st.spinner("Creating vector store..."):
        # Use a temporary directory for the vector store
        persist_dir = tempfile.mkdtemp()
        st.session_state.persist_dir = persist_dir
            
        vector_store_manager, rag_chain = initialize_components(groq_api_key, persist_dir)
        vector_store_manager.create_vector_store(chunks)
        
        # Create QA chain
        retriever = vector_store_manager.get_retriever(k=4)
        rag_chain.create_qa_chain(retriever)
        
        # Store in session state
        st.session_state.vector_store_manager = vector_store_manager
        st.session_state.rag_chain = rag_chain
        st.session_state.vector_store_ready = True
        
        st.success("Vector store created! You can now ask questions about your document.")
    
    # Clean up temporary file
    os.remove(file_path)


def main():
    """Main application."""
    st.title("🤖 RAG Chatbot with Groq API")
    st.markdown("Upload a document and chat with it using AI!")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Enter your Groq API key"
        )
        
        if not groq_api_key:
            st.warning("Please enter your Groq API key to continue.")
            st.markdown("[Get your Groq API key](https://console.groq.com/)")
            st.stop()
        
        # Auto-load default document on first run
        if not st.session_state.vector_store_ready and groq_api_key:
            with st.spinner("Loading default template document..."):
                if load_default_document(groq_api_key):
                    st.success("✅ Default template loaded!")
        
        st.divider()
        
        # File upload
        st.header("📁 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt'],
            help="Upload a PDF or TXT file to chat with"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document", type="primary"):
                st.session_state.using_default = False
                process_uploaded_file(uploaded_file, groq_api_key)
        
        st.divider()
        
        # Debug Information
        with st.expander("🛠️ Debug Information"):
            if st.session_state.persist_dir:
                st.markdown(f"**Database Path:**\n`{st.session_state.persist_dir}`")
                
                # Show document count if vector store is ready
                if st.session_state.vector_store_manager and st.session_state.vector_store_manager.vector_store:
                    try:
                        count = st.session_state.vector_store_manager.vector_store._collection.count()
                        st.markdown(f"**Document Count:** {count}")
                    except:
                        st.markdown("**Document Count:** Unknown")
            else:
                st.markdown("Database not initialized yet.")
        
        # Status indicator
        if st.session_state.vector_store_ready:
            if st.session_state.using_default:
                st.success("✅ Using default template document")
                st.info("💡 Upload your own document to replace it")
                
                # Explain what's in the default template
                with st.expander("ℹ️ What's in the default template?"):
                    st.markdown("""
                    **Sample Topics Included:**
                    - What is RAG (Retrieval-Augmented Generation)
                    - How this chatbot works
                    - Groq API explanation
                    - ChromaDB vector database
                    - TOON token optimization
                    - Technical architecture
                    - Best practices & tips
                    
                    **Try asking:**
                    - "What is RAG?"
                    - "How does TOON save tokens?"
                    - "Explain the vector database"
                    """)
            else:
                st.success("✅ Document loaded and ready!")
        else:
            st.info("📤 Upload and process a document to start chatting")
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    if not st.session_state.vector_store_ready:
        st.info("👈 Upload a document from the sidebar to get started!")
        
        # Display example questions
        st.subheader("Example Questions You Can Ask:")
        st.markdown("""
        - What is this document about?
        - Summarize the main points
        - What does it say about [specific topic]?
        - Can you explain [concept] from the document?
        """)
    else:
        # Show info banner and buttons if using default template
        if st.session_state.using_default and len(st.session_state.messages) == 0:
            st.info("""
            📘 **Using Default Template Document**
            
            This template contains information about RAG, AI chatbots, Groq API, ChromaDB, 
            and TOON optimization. Ask questions to learn how this chatbot works!
            
            **Upload your own PDF or TXT file to chat with your documents.**
            """)
            
            # Sample question buttons
            st.markdown("### 🚀 Try These Sample Questions:")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("❓ What is RAG?", use_container_width=True):
                    st.session_state.pending_query = "What is RAG?"
                    st.rerun()
            
            with col2:
                if st.button("💰 How does TOON save tokens?", use_container_width=True):
                    st.session_state.pending_query = "How does TOON save tokens?"
                    st.rerun()
            
            st.divider()
        
        # Process pending query from button click FIRST
        if st.session_state.pending_query:
            query = st.session_state.pending_query
            st.session_state.pending_query = None
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Generate response
            try:
                response = st.session_state.rag_chain.query(query)
                answer = response['result']
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            st.rerun()
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your document..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.rag_chain.query(prompt)
                        answer = response['result']
                        
                        # Display answer
                        st.markdown(answer)
                        
                        # Optionally display source documents
                        with st.expander("📚 View Source Context"):
                            for i, doc in enumerate(response['source_documents'], 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(doc.page_content)
                                st.divider()
                        
                        # Add assistant message to chat
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})


if __name__ == "__main__":
    main()
