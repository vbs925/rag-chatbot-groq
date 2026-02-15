"""RAG chain module for integrating Groq API with retrieval."""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.toon_formatter import ToonFormatter


class RAGChain:
    """Manages the RAG (Retrieval Augmented Generation) chain."""
    
    def __init__(self, groq_api_key: str, model_name: str = "llama-3.3-70b-versatile", use_toon: bool = True):
        """
        Initialize the RAG chain.
        
        Args:
            groq_api_key: Groq API key
            model_name: Name of the Groq model to use
            use_toon: Whether to use TOON formatting for token optimization (default: True)
        """
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        self.use_toon = use_toon
        self.llm = None
        self.qa_chain = None
        self.retriever = None
        self.toon_formatter = ToonFormatter(enabled=use_toon)
        
        # Custom prompt template optimized for TOON format
        if use_toon:
            self.prompt_template = """Use the following TOON-formatted context to answer the question at the end.
The context is in TOON (Token-Oriented Object Notation) format for efficiency.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always provide a detailed and helpful response based on the context.

Context (TOON format):
{context}

Question: {question}

Helpful Answer:"""
        else:
            self.prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always provide a detailed and helpful response based on the context.

Context:
{context}

Question: {question}

Helpful Answer:"""
    
    def initialize_llm(self):
        """Initialize the Groq LLM."""
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name,
            temperature=0.2,
            max_tokens=1024
        )
    
    def format_docs(self, docs):
        """
        Format retrieved documents - uses TOON if enabled, otherwise standard.
        
        Args:
            docs: List of Document objects
            
        Returns:
            Formatted string (TOON or standard)
        """
        if self.use_toon:
            return self.toon_formatter.format_simple_context(docs)
        else:
            return "\n\n".join(doc.page_content for doc in docs)
    
    def create_qa_chain(self, retriever):
        """
        Create a question-answering chain with retrieval.
        
        Args:
            retriever: Retriever instance from vector store
            
        Returns:
            Chain instance
        """
        if self.llm is None:
            self.initialize_llm()
        
        self.retriever = retriever
        
        # Create custom prompt
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        
        # Create QA chain using LCEL (LangChain Expression Language)
        self.qa_chain = (
            {
                "context": retriever | self.format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return self.qa_chain
    
    def query(self, question: str) -> dict:
        """
        Query the RAG chain with a question.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with 'result', 'source_documents', and optional 'token_info'
        """
        if self.qa_chain is None:
            raise ValueError("QA chain not initialized. Create chain first.")
        
        # Get source documents for token analysis
        source_docs = self.retriever.invoke(question)
        
        # Get the answer
        answer = self.qa_chain.invoke(question)
        
        # Calculate token savings if TOON is enabled
        token_info = None
        if self.use_toon:
            # Calculate what standard format would have used
            standard_format = "\n\n".join(doc.page_content for doc in source_docs)
            toon_format = self.toon_formatter.format_simple_context(source_docs)
            token_info = self.toon_formatter.calculate_token_savings(standard_format, toon_format)
        
        result = {
            "result": answer,
            "source_documents": source_docs
        }
        
        if token_info:
            result["token_info"] = token_info
        
        return result
