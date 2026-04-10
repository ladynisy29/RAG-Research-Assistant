#!/usr/bin/env python3
"""Simple test to verify vector store works."""

import os
from dotenv import load_dotenv

load_dotenv()

print('Simple Vector Store Test')
print()

# Test 1: Check files
print('1. Checking vector store files...')
print(f'   index.faiss: {os.path.isfile("vector_store/index.faiss")}')
print(f'   index.pkl: {os.path.isfile("vector_store/index.pkl")}')
print()

# Test 2: Load retriever
print('2. Loading retriever...')
try:
    from app.services.retriever import get_retriever
    retriever = get_retriever()
    print('   ✅ Retriever loaded')
except Exception as e:
    print(f'   ❌ Error: {e}')
    exit(1)
print()

# Test 3: Test retrieval
print('3. Testing retrieval...')
try:
    docs = retriever.invoke('What is the main topic?')
    print(f'   ✅ Retrieved {len(docs)} documents')
    if docs:
        print(f'   First doc: {docs[0].page_content[:80]}...')
except Exception as e:
    print(f'   ❌ Error: {e}')
    exit(1)
print()

print('✅ All tests passed!')
