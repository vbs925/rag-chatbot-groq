"""Streamlit app for RAG Chatbot with Groq API."""

import streamlit as st
import os
import shutil
import tempfile
import time
from pathlib import Path
import base64
from dotenv import load_dotenv

from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain
from src.styles import get_custom_css

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot with Groq",
    page_icon=None,
    layout="wide"
)

# Apply custom styles
st.markdown(get_custom_css(), unsafe_allow_html=True)

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



def process_uploaded_files(uploaded_files, groq_api_key: str):
    """Process uploaded files and create vector store."""
    if not uploaded_files:
        return
        
    # Save uploaded files temporarily
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    all_chunks = []
    processed_files = []
    
    progress_text = "Operation in progress. Please wait..."
    my_bar = st.progress(0, text=progress_text)
    
    try:
        total_files = len(uploaded_files)
        
        for i, uploaded_file in enumerate(uploaded_files):
            # Update progress
            progress_percent = int((i / total_files) * 50)
            my_bar.progress(progress_percent, text=f"Processing {uploaded_file.name}...")
            
            file_path = upload_dir / uploaded_file.name
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process document
            try:
                doc_processor = DocumentProcessor()
                chunks = doc_processor.process_document(str(file_path))
                all_chunks.extend(chunks)
                processed_files.append(file_path)
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
            
        if not all_chunks:
            st.error("No valid documents were processed.")
            return

        # Create vector store
        my_bar.progress(60, text="Creating vector store...")
        
        # Use a temporary directory for the vector store
        persist_dir = tempfile.mkdtemp()
        st.session_state.persist_dir = persist_dir
            
        vector_store_manager, rag_chain = initialize_components(groq_api_key, persist_dir)
        vector_store_manager.create_vector_store(all_chunks)
        
        my_bar.progress(80, text="Initializing QA chain...")
        
        # Create QA chain
        retriever = vector_store_manager.get_retriever(k=4)
        rag_chain.create_qa_chain(retriever)
        
        # Store in session state
        st.session_state.vector_store_manager = vector_store_manager
        st.session_state.rag_chain = rag_chain
        st.session_state.vector_store_ready = True
        
        my_bar.progress(100, text="Complete!")
        time.sleep(0.5)
        my_bar.empty()
        
        st.success(f"Successfully processed {len(processed_files)} documents into {len(all_chunks)} chunks!")
        st.success("Vector store created! You can now ask questions across all your documents.")
        
    finally:
        # Clean up temporary files
        for file_path in processed_files:
            try:
                os.remove(file_path)
            except:
                pass
        try:
            # Try to remove empty directory
            os.rmdir(upload_dir)
        except:
            pass


def main():
    """Main application with Dashboard Layout."""
    
    # --------------------------------------------------------------------------
    # Top Navigation Bar
    # --------------------------------------------------------------------------
    
    # Logo Logic
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            navbar_right = f'<img src="data:image/png;base64,{encoded_string}" class="navbar-logo-img" alt="Logo">'
        except Exception:
            navbar_right = '<div class="user-profile">VB</div>'
    else:
        navbar_right = '<div class="user-profile">VB</div>'

    st.markdown(f"""
        <div class="navbar">
            <div class="navbar-brand">
                <div class="navbar-icon">
                    🤖
                </div>
                <span>RAG Chatbot</span>
            </div>
            {navbar_right}
        </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Metrics Row
    # --------------------------------------------------------------------------
    
    # Calculate real metrics
    doc_count = 0
    if st.session_state.vector_store_manager and st.session_state.vector_store_manager.vector_store:
        try:
            doc_count = st.session_state.vector_store_manager.vector_store._collection.count()
        except:
            pass
            
    status_class = "status-active" if st.session_state.vector_store_ready else "status-waiting"
    status_text = "Active" if st.session_state.vector_store_ready else "Waiting"

    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <div class="metric-title">System Status</div>
                        <div class="metric-value">Online</div>
                    </div>
                    <div class="metric-status {status_class}">{status_text}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Documents Indexed</div>
                <div class="metric-value">{doc_count}</div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Est. Cost Savings</div>
                <div class="metric-value">~28%</div>
            </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">Active Model</div>
                <div class="metric-value" style="font-size: 1.25rem;">Llama3-70b</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Main Content Area
    # --------------------------------------------------------------------------
    
    st.markdown("""
        <div class="chat-header">
            <div class="chat-title">AI Chat Interface</div>
            <div style="font-size: 0.8rem; color: #6B7280; background: #F3F4F6; padding: 2px 8px; border-radius: 4px;">
                Session Active
            </div>
        </div>
    """, unsafe_allow_html=True)

    # The actual chat history logic follows...

    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
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
                    st.success("Default template loaded!")
        
        st.divider()
        
        # File upload
        st.header("Upload Document(s)")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload one or more PDF or TXT files to chat with"
        )
        
        if uploaded_files:
            if st.button("Process Documents", type="primary"):
                st.session_state.using_default = False
                process_uploaded_files(uploaded_files, groq_api_key)
        
        st.divider()
        
        # Debug Information
        with st.expander("Debug Information"):
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
                st.success("Using default template document")
                st.info("Upload your own document to replace it")
                
                # Explain what's in the default template
                with st.expander("What's in the default template?"):
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
                st.success("Document loaded and ready!")
        else:
            st.info("Upload and process a document to start chatting")
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    if not st.session_state.vector_store_ready:
        st.info("Upload documents from the sidebar to get started!")
        
        # Display example questions
        st.subheader("Example Questions You Can Ask:")
        st.markdown("""
        - What are these documents about?
        - Summarize the main points across all files
        - Compare [topic] between the documents
        - Can you explain [concept] from the documents?
        """)
    else:
        # Show info banner and buttons if using default template
        if st.session_state.using_default and len(st.session_state.messages) == 0:
            st.info("""
            **Using Default Template Document**
            
            This template contains information about RAG, AI chatbots, Groq API, ChromaDB, 
            and TOON optimization. Ask questions to learn how this chatbot works!
            
            **Upload your own PDF or TXT file to chat with your documents.**
            """)
            
            # Sample question buttons
            st.markdown("### Try These Sample Questions:")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("What is RAG?", use_container_width=True):
                    st.session_state.pending_query = "What is RAG?"
                    st.rerun()
            
            with col2:
                if st.button("How does TOON save tokens?", use_container_width=True):
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
                        with st.expander("View Source Context"):
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
