#!/usr/bin/env python3
"""Test the API with the vector store."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('Testing API endpoints...')
print()

# Test 1: Health check
print('1. Health Check')
response = client.get('/health')
print(f'   Status: {response.status_code}')
print(f'   Response: {response.json()}')
print()

# Test 2: Query with valid question
print('2. Query with Valid Question')
response = client.post('/query', json={'question': 'What is the main topic?'})
print(f'   Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'   Answer: {data["answer"][:100]}...')
    print(f'   Sources: {len(data["sources"])} document(s)')
else:
    print(f'   Error: {response.json()}')
print()

# Test 3: Query with empty question
print('3. Query with Empty Question')
response = client.post('/query', json={'question': ''})
print(f'   Status: {response.status_code}')
print(f'   Response: {response.json()}')
print()

print('All tests completed!')
