# RAG Research Assistant

A FastAPI-based research assistant using retrieval-augmented generation (RAG) to answer questions about research papers using **GPT-4 Mini from GitHub Marketplace Models**.

## Features

- PDF document loading and processing
- Vector embeddings using GitHub Marketplace Models
- FAISS vector store for efficient retrieval
- FastAPI REST API for queries
- Streamlit web interface
- Comprehensive error handling and logging
- GitHub Marketplace Models integration

## Prerequisites

- Python 3.10+
- GitHub account with access to Marketplace Models
- GitHub personal access token
- pip or conda

## Quick Start

1. **Get GitHub Token**: [Create a personal access token](https://github.com/settings/tokens)
2. **Install**: `pip install -r requirements.txt`
3. **Configure**: Edit `.env` and add `GITHUB_TOKEN=your_token`
4. **Add PDFs**: Place files in `data/papers/`
5. **Setup**: `python setup_vector_store.py`
6. **Run**: 
   - API: `uvicorn app.main:app --reload`
   - UI: `streamlit run app/streamlit_app.py`

See [GITHUB_MARKETPLACE_SETUP.md](GITHUB_MARKETPLACE_SETUP.md) for detailed setup instructions.

## Setup

### 1. Prepare Your Documents

Place your PDF files in the `data/papers/` directory.

### 2. Initialize Vector Store

Run the setup script to process PDFs and create the vector store:
```bash
python setup_vector_store.py
```

This will:
- Load all PDFs from `data/papers/`
- Split documents into chunks
- Create embeddings using OpenAI
- Save the vector store to `vector_store/`

## Running the Application

### Option 1: FastAPI Server Only

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API endpoints:
- `GET /health` - Health check
- `POST /query` - Submit a question

Example query:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

### Option 2: Streamlit UI

In a separate terminal:
```bash
streamlit run app/streamlit_app.py
```

The UI will be available at `http://localhost:8501`

### Option 3: Both (Recommended)

Terminal 1 - Start FastAPI:
```bash
uvicorn app.main:app --reload
```

Terminal 2 - Start Streamlit:
```bash
streamlit run app/streamlit_app.py
```

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── streamlit_app.py     # Streamlit UI
│   ├── routes/
│   │   └── query.py         # Query endpoint
│   ├── services/
│   │   ├── embeddings.py    # Vector store creation
│   │   ├── llm.py           # LLM integration
│   │   └── retriever.py     # Document retrieval
│   └── utils/
│       └── parser.py        # PDF parsing
├── data/
│   └── papers/              # Place PDF files here
├── vector_store/            # FAISS vector store (auto-created)
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── Dockerfile               # Docker configuration
└── README.md               # This file
```

## Configuration

### Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

### Vector Store Path

The vector store is saved to `vector_store/` by default. To change this, modify the path in:
- `app/services/embeddings.py` - `create_vector_store()`
- `app/services/retriever.py` - `get_retriever()`

## Docker

Build and run with Docker:
```bash
docker build -t rag-assistant .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key rag-assistant
```

## Troubleshooting

### Vector store not found
- Run `python setup_vector_store.py` to create it
- Ensure PDFs are in `data/papers/`

### API connection error in Streamlit
- Ensure FastAPI server is running on `http://localhost:8000`
- Check firewall settings

### OpenAI API errors
- Verify `OPENAI_API_KEY` is set correctly in `.env`
- Check your OpenAI account has available credits

## Performance Notes

- Chunk size: 500 tokens with 50 token overlap
- Retrieval: Returns top 3 most relevant documents
- Model: GPT-3.5-turbo for answer generation

## License

MIT

