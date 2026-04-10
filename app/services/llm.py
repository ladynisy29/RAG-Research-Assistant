# app/services/llm.py

import os
import logging
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

def generate_answer(query, docs):
    """Generate an answer using GPT-4 Mini from GitHub Marketplace Models."""
    if not docs:
        return "No relevant documents found to answer the question."
    
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}"""
    
    # Get API key from GitHub Marketplace Models
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set. Get it from GitHub Marketplace Models.")
    
    try:
        # Use GitHub Marketplace Models endpoint with GPT-4.1 Mini
        llm = ChatOpenAI(
            api_key=github_token,
            model="gpt-4.1-mini",
            base_url="https://models.inference.ai.azure.com",
            timeout=30,
            max_retries=2
        )
        logger.info(f"Calling LLM with query: {query[:50]}...")
        response = llm.invoke(prompt)
        logger.info(f"LLM response received: {response.content[:50]}...")
        return response.content
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}", exc_info=True)
        raise