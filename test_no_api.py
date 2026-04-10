#!/usr/bin/env python3
"""Test without making API calls."""

import os
from dotenv import load_dotenv
from unittest.mock import Mock, patch

load_dotenv()

print('Testing without API calls...')
print()

# Test 1: Check files
print('1. Checking vector store files...')
print(f'   index.faiss: {os.path.isfile("vector_store/index.faiss")}')
print(f'   index.pkl: {os.path.isfile("vector_store/index.pkl")}')
print()

# Test 2: Mock the embeddings and test retriever
print('2. Testing retriever with mocked embeddings...')
try:
    with patch('app.services.retriever.OpenAIEmbeddings') as mock_embeddings:
        with patch('app.services.retriever.FAISS.load_local') as mock_load:
            # Setup mocks
            mock_db = Mock()
            mock_retriever = Mock()
            mock_db.as_retriever.return_value = mock_retriever
            mock_load.return_value = mock_db
            
            from app.services.retriever import get_retriever
            retriever = get_retriever()
            print('   ✅ Retriever loaded with mocked embeddings')
except Exception as e:
    print(f'   ❌ Error: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
print()

print('✅ All tests passed!')
