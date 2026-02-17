"""Streamlit app for RAG Chatbot with Groq API."""

import streamlit as st
import os
import shutil
import tempfile
import time
from pathlib import Path
import base64
import base64
from dotenv import load_dotenv
import nltk

# Add backend to path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

# Ensure NLTK data path includes user's home directory
nltk.data.path.append(os.path.expanduser("~/nltk_data"))

# Download required NLTK data if missing
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChain
from styles import get_custom_css


# Load environment variables
load_dotenv(dotenv_path="../backend/.env")

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
    default_doc_path = Path("../backend/default_document.txt")
    
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
    upload_dir = Path("../backend/uploads")
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
    # --------------------------------------------------------------------------
    
    # --------------------------------------------------------------------------
    
    # Custom Header with Logo
    logo_path = Path("assets/logo.png")
    logo_html = ""
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{encoded_string}" class="header-logo" alt="Logo">'
        except:
            pass
            
    st.markdown(f"""
        <div class="custom-header">
            <div class="header-content">
                <span style="font-size: 2.5rem;">🤖</span>
                <div class="header-title">RAG Chatbot with Groq</div>
            </div>
            {logo_html}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)


    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Enter your Groq API key. It is used only for this session."
        )
        
        if not groq_api_key:
            st.warning("Please enter your Groq API key to continue.")
            st.markdown("[Get your Groq API key](https://console.groq.com/)")
            st.stop()
        
        # Auto-load default document on first run
        if not st.session_state.vector_store_ready and groq_api_key:
            with st.spinner("Loading default template document..."):
                if load_default_document(groq_api_key):
                    st.success("Default template loaded and indexed!")
        
        st.divider()
        
        # File upload
        st.subheader("Documents")
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=['pdf', 'txt', 'docx', 'pptx'],
            accept_multiple_files=True,
            help="Upload one or more PDF, TXT, DOCX, or PPTX files to index into the vector store."
        )
        
        if uploaded_files:
            st.write(f"Selected: {len(uploaded_files)} files")

        can_process = bool(uploaded_files)
        if st.button(
            "Index documents",
            type="primary",
            disabled=not can_process,
        ):
            st.session_state.using_default = False
            process_uploaded_files(uploaded_files, groq_api_key)
        
        st.divider()
        
        # Status & Debug
        st.subheader("Status")
        if st.session_state.vector_store_ready:
            st.success("System Ready")
            if st.session_state.using_default:
                st.info("Using default template.")
        else:
            st.info("Waiting for documents.")
            
        # Clear chat button
        if st.button("Clear chat history"):
            st.session_state.messages = []
            st.rerun()
    
    # --------------------------------------------------------------------------
    # Chat Interface
    # --------------------------------------------------------------------------
    
    # Custom Container for Chat
    chat_container_placeholder = st.empty()
    
    with chat_container_placeholder.container():
        st.markdown(
            """
            <div class="chat-container">
                <div class="chat-header">
                    <div>AI Chat Assistant</div>
                    <div style="font-size: 0.8rem; font-weight: normal; color: #64748B;">Ready to help</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

    # Main chat interface
    if not st.session_state.vector_store_ready:
        st.info("Upload a document to start chatting.")
    else:
        # Show info banner and buttons if using default template
        if st.session_state.using_default and len(st.session_state.messages) == 0:
            st.info("Using Default Template Document. process a document to override.")
            
            # Sample question buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("What is RAG?", use_container_width=True):
                    st.session_state.pending_query = "What is RAG?"
                    st.rerun()
            
            with col2:
                if st.button("How does TOON save tokens?", use_container_width=True):
                    st.session_state.pending_query = "How does TOON save tokens?"
                    st.rerun()
            
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
        if not st.session_state.messages:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 50vh; color: #6B7280; font-size: 1.2rem; text-align: center;">
                    Upload a document and ask questions to get started
                </div>
                """, 
                unsafe_allow_html=True
            )
            
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

        # Close chat container
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
