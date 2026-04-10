# app/services/embeddings.py

import logging
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

def create_vector_store(documents):
    """Create and save a FAISS vector store from documents using GitHub Marketplace Models."""
    if not documents:
        raise ValueError("No documents provided to create vector store")
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set. Get it from GitHub Marketplace Models.")
    
    try:
        # Use GitHub Marketplace Models endpoint for embeddings
        embeddings = OpenAIEmbeddings(
            api_key=github_token,
            model="text-embedding-3-small",
            base_url="https://models.inference.ai.azure.com"
        )
        db = FAISS.from_documents(documents, embeddings)
        db.save_local("vector_store")
        logger.info(f"Vector store created with {len(documents)} documents")
        return db
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        raise