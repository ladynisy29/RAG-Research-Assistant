# app/services/retriever.py

import os
import logging

logger = logging.getLogger(__name__)

# Global cache for retriever to avoid reloading
_retriever_cache = None

def get_retriever():
    """Load and return a retriever from the vector store using GitHub Marketplace Models."""
    global _retriever_cache
    
    # Return cached retriever if available
    if _retriever_cache is not None:
        logger.debug("Returning cached retriever")
        return _retriever_cache
    
    # Import here to avoid hanging on module load
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    
    vector_store_path = "vector_store"
    
    if not os.path.exists(vector_store_path):
        raise FileNotFoundError(
            f"Vector store not found at {vector_store_path}. "
            "Please create it first using: python setup_vector_store.py"
        )
    
    # Check if vector store files exist
    index_file = os.path.join(vector_store_path, "index.faiss")
    pkl_file = os.path.join(vector_store_path, "index.pkl")
    
    if not os.path.exists(index_file) or not os.path.exists(pkl_file):
        raise FileNotFoundError(
            f"Vector store files not found. Expected {index_file} and {pkl_file}. "
            "Please run: python setup_vector_store.py"
        )
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set. Get it from GitHub Marketplace Models.")
    
    try:
        logger.info(f"Loading vector store from {vector_store_path}")
        
        # Use GitHub Marketplace Models endpoint for embeddings
        embeddings = OpenAIEmbeddings(
            api_key=github_token,
            model="text-embedding-3-small",
            base_url="https://models.inference.ai.azure.com"
        )
        
        # Load FAISS index
        db = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
        logger.info(f"Vector store loaded successfully with {db.index.ntotal} vectors")
        
        # Cache the retriever
        _retriever_cache = db.as_retriever(search_kwargs={"k": 3})
        return _retriever_cache
        
    except Exception as e:
        logger.error(f"Error loading retriever: {str(e)}")
        raise FileNotFoundError(
            f"Failed to load vector store: {str(e)}. "
            "Try recreating it with: python setup_vector_store.py"
        )

def evaluate_retrieval(query, expected_doc, retriever=None):
    """Evaluate if retrieval returns expected document."""
    if retriever is None:
        retriever = get_retriever()
    
    try:
        # Use invoke() method for LangChain retriever
        docs = retriever.invoke(query)
        return expected_doc in [d.page_content for d in docs]
    except Exception as e:
        logger.error(f"Error evaluating retrieval: {str(e)}")
        return False