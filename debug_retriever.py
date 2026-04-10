#!/usr/bin/env python3
"""Debug script to check retriever loading."""

import os
from dotenv import load_dotenv

load_dotenv()

print('Debugging vector store loading...')
print()

# Check files
print('1. Vector store files:')
print(f'   vector_store dir exists: {os.path.isdir("vector_store")}')
print(f'   index.faiss exists: {os.path.isfile("vector_store/index.faiss")}')
print(f'   index.pkl exists: {os.path.isfile("vector_store/index.pkl")}')
print()

# Check token
print('2. GitHub token:')
token = os.getenv('GITHUB_TOKEN')
print(f'   Token set: {bool(token)}')
if token:
    print(f'   Token starts with: {token[:20]}...')
print()

# Try to load with detailed error
print('3. Attempting to load retriever:')
try:
    from app.services.retriever import get_retriever
    print('   Calling get_retriever()...')
    retriever = get_retriever()
    print('   SUCCESS: Retriever loaded!')
    print(f'   Retriever type: {type(retriever)}')
except FileNotFoundError as e:
    print(f'   FileNotFoundError: {e}')
except ValueError as e:
    print(f'   ValueError: {e}')
except Exception as e:
    print(f'   Exception ({type(e).__name__}): {e}')
    import traceback
    traceback.print_exc()
