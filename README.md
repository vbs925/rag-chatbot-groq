# RAG Chatbot with Groq API

A powerful document-based chatbot using **Retrieval Augmented Generation (RAG)** that allows you to upload documents and have intelligent conversations about their content using **Groq's lightning-fast LLM API**.

## Features

- **Document Upload**: Support for PDF and TXT files
- **Semantic Search**: ChromaDB vector database for intelligent context retrieval
- **Fast Responses**: Powered by Groq's optimized LLM infrastructure
- **Chat Interface**: Clean Streamlit-based UI with chat history
- **Context-Aware**: Answers questions based on your document content
- **Source Citations**: View the exact document sections used for each answer

## Technology Stack

- **Streamlit** - Web interface
- **LangChain** - RAG orchestration framework
- **Groq API** - Fast LLM inference (Mixtral, Llama models)
- **ChromaDB** - Vector database for embeddings
- **Sentence Transformers** - Text embeddings
- **PyPDF2** - PDF document processing

## Prerequisites

- Python 3.8 or higher
- Groq API key ([Get it here](https://console.groq.com/))

## Installation

### Step 1: Clone or Download the Project

```bash
cd /Users/varunbharadwaj/.gemini/antigravity/scratch/rag-chatbot-groq
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

## Usage

### Step 1: Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 2: Upload a Document

1. Enter your **Groq API key** in the sidebar (or it will use the one from `.env`)
2. Click **"Choose a file"** to upload a PDF or TXT document
3. Click **"Process Document"** to analyze and index the document

### Step 3: Start Chatting!

Ask questions about your document in the chat interface:

- "What is this document about?"
- "Summarize the main points"
- "What does it say about [specific topic]?"
- "Explain [concept] in detail"

## Project Structure

```
rag-chatbot-groq/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   ├── document_processor.py  # Document loading and chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB operations
│   └── rag_chain.py           # RAG pipeline with Groq
└── uploads/                   # Temporary file storage (auto-created)
```

## Configuration Options

### Available Groq Models

You can change the model in `src/rag_chain.py`:

- `mixtral-8x7b-32768` (default) - Best for general tasks
- `llama2-70b-4096` - Good balance of speed and quality
- `gemma-7b-it` - Lightweight and fast

### Adjust Chunk Size

Modify chunking parameters in `src/document_processor.py`:

```python
chunk_size=1000,      # Size of each text chunk
chunk_overlap=200     # Overlap between chunks
```

### Change Retrieval Count

Adjust how many relevant chunks to retrieve in `app.py`:

```python
retriever = vector_store_manager.get_retriever(k=4)  # Retrieve top 4 chunks
```

## Troubleshooting

### "No API key provided" Error

- Make sure you've created a `.env` file with your Groq API key
- Or enter the API key directly in the sidebar

### Document Processing Fails

- Ensure your PDF is not password-protected
- Check that the file is not corrupted
- Try a different document format (TXT instead of PDF)

### Slow Response Times

- Try using a smaller model like `gemma-7b-it`
- Reduce the number of retrieved chunks (lower `k` value)
- Check your internet connection (Groq API is cloud-based)

### Import Errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment before running

## Security Notes

- Never commit your `.env` file or expose your API key
- The `.gitignore` file is configured to exclude sensitive files
- API keys entered in the sidebar are stored only in session state

## How It Works

1. **Document Upload**: User uploads a PDF or TXT file
2. **Text Extraction**: Content is extracted from the document
3. **Chunking**: Text is split into manageable chunks with overlap
4. **Embedding**: Each chunk is converted to a vector embedding
5. **Vector Storage**: Embeddings are stored in ChromaDB
6. **Query Processing**: User asks a question
7. **Retrieval**: Relevant chunks are found using similarity search
8. **Generation**: Groq LLM generates an answer using the retrieved context
9. **Display**: Answer is shown with source citations

## Next Steps

Want to enhance this chatbot? Try:

- Add support for more file types (DOCX, CSV, etc.)
- Implement conversation memory for multi-turn dialogues
- Add user authentication and document management
- Deploy to cloud platforms (Streamlit Cloud, Heroku, etc.)
- Add conversation export functionality

## License

This project is open source and available for educational and commercial use.

## Acknowledgments

- **Groq** for providing blazing-fast LLM inference
- **LangChain** for the RAG framework
- **Streamlit** for the easy-to-use web framework

---

**Built with RAG and Groq API**
