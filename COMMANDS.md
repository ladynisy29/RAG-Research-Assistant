# All Commands Reference

## Quick Start (Windows)

Use the provided batch scripts - they handle Python PATH issues automatically:

```
install.bat          # Install all dependencies
setup_docs.bat       # Initialize vector store from PDFs
run_api.bat          # Start FastAPI server
run_ui.bat           # Start Streamlit UI
run_tests.bat        # Run test suite
```

## Manual Commands (if needed)

### Installation
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Setup Vector Store
```bash
python setup_vector_store.py
```

### Run API Server
```bash
python -m uvicorn app.main:app --reload
```

API endpoints:
- `GET http://localhost:8000/health` - Health check
- `POST http://localhost:8000/query` - Submit query
- `GET http://localhost:8000/docs` - Interactive API documentation

### Run Streamlit UI
```bash
python -m streamlit run app/streamlit_app.py
```

UI available at: http://localhost:8501

### Run Tests
```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_routes.py -v

# Specific test
python -m pytest tests/test_routes.py::test_health_check -v

# With coverage
python -m pytest tests/ --cov=app --cov-report=html
```

## API Usage Examples

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### Query Endpoint
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

## Docker Commands

### Build Image
```bash
docker build -t rag-assistant .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  rag-assistant
```

### Run with Volume Mount
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data/papers:/app/data/papers \
  -v $(pwd)/vector_store:/app/vector_store \
  rag-assistant
```

## Development Commands

### Format Code
```bash
# Install formatter
python -m pip install black

# Format all Python files
black app/ tests/
```

### Lint Code
```bash
# Install linter
python -m pip install flake8

# Check code
flake8 app/ tests/
```

### Type Checking
```bash
# Install type checker
python -m pip install mypy

# Check types
mypy app/
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
python -m pip list
```

### Verify OpenAI API Key
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key set:', bool(os.getenv('OPENAI_API_KEY')))"
```

### Check Vector Store
```bash
python -c "import os; print('Vector store exists:', os.path.exists('vector_store'))"
```

### View Logs
```bash
# API logs are printed to console when running with --reload
# Streamlit logs are in ~/.streamlit/logs/
```

## Environment Setup

### Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Update Requirements
```bash
# After installing new packages
python -m pip freeze > requirements.txt
```

## File Structure Commands

### Create Project Structure
```bash
mkdir -p data/papers vector_store tests notebooks
```

### List Project Files
```bash
# Windows
dir /s /b

# Linux/Mac
find . -type f -name "*.py" | head -20
```

## Useful Aliases (add to .bashrc or .zshrc)

```bash
alias rag-api="python -m uvicorn app.main:app --reload"
alias rag-ui="python -m streamlit run app/streamlit_app.py"
alias rag-test="python -m pytest tests/ -v"
alias rag-setup="python setup_vector_store.py"
```

Then use:
```bash
rag-api
rag-ui
rag-test
rag-setup
```
