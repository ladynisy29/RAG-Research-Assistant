# Quick Start Guide - GitHub Marketplace Models

## 5-Minute Setup

### 1. Get GitHub Token
Visit [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) and create a new token.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure GitHub Token
Edit `.env`:
```
GITHUB_TOKEN=ghp_your_actual_token_here
```

### 4. Add Your PDFs
Copy PDF files to `data/papers/`

### 5. Create Vector Store
```bash
python setup_vector_store.py
```

Expected output:
```
INFO - Found 2 PDF file(s)
INFO - Processing paper1.pdf...
INFO - Loaded 45 chunks from paper1.pdf
INFO - Creating vector store with 90 total chunks...
INFO - Vector store created successfully!
```

### 6. Start the API
```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs (interactive API docs)

### 7. Start the UI (in another terminal)
```bash
streamlit run app/streamlit_app.py
```

Visit: http://localhost:8501

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test:
```bash
pytest tests/test_routes.py::test_health_check -v
```

## API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

Response:
```json
{
  "answer": "The main topic is...",
  "sources": [
    {"source": "paper1.pdf", "page": 1}
  ]
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GITHUB_TOKEN not set` | Add token to `.env` file |
| `Vector store not found` | Run `python setup_vector_store.py` |
| `Cannot connect to API` | Ensure FastAPI is running on port 8000 |
| `No PDFs found` | Add PDF files to `data/papers/` |
| `Invalid token` | Check token hasn't expired, generate new one |

## Next Steps

- Modify chunk size in `app/utils/parser.py` for different document types
- Adjust retrieval count in `app/services/retriever.py` (currently returns top 3)
- Customize prompts in `app/services/llm.py`
- Add authentication to API endpoints
- Deploy with Docker: `docker build -t rag-app . && docker run -p 8000:8000 rag-app`

## Models Used

- **LLM**: `gpt-4-mini` from GitHub Marketplace Models
- **Embeddings**: `text-embedding-3-small` from GitHub Marketplace Models

See [GITHUB_MARKETPLACE_SETUP.md](GITHUB_MARKETPLACE_SETUP.md) for more details.
