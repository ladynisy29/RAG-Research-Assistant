#!/usr/bin/env python3
"""Test script to verify vector store loading."""

import os
from dotenv import load_dotenv

load_dotenv()

print('Testing vector store loading...')
print()

# Check environment
token = os.getenv('GITHUB_TOKEN')
token_status = 'Set' if token else 'Not set'
print(f'GitHub Token: {token_status}')

# Check files
print(f'Vector store dir exists: {os.path.isdir("vector_store")}')
print(f'index.faiss exists: {os.path.isfile("vector_store/index.faiss")}')
print(f'index.pkl exists: {os.path.isfile("vector_store/index.pkl")}')
print()

# Try to load retriever
try:
    from app.services.retriever import get_retriever
    print('Loading retriever...')
    retriever = get_retriever()
    print('✅ Retriever loaded successfully!')
    print()
    
    # Test a query
    print('Testing retrieval with a sample query...')
    # Try both methods for compatibility
    try:
        docs = retriever.invoke('What is the main topic?')
    except:
        docs = retriever.get_relevant_documents('What is the main topic?')
    
    print(f'✅ Retrieved {len(docs)} documents')
    if docs:
        print(f'First result preview: {docs[0].page_content[:100]}...')
except Exception as e:
    print(f'❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()
