# Commands Reference

## Setup Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get GitHub Token
Visit: https://github.com/settings/tokens

### 3. Configure Environment
Edit `.env` file:
```
GITHUB_TOKEN=ghp_your_token_here
```

### 4. Create Vector Store
```bash
python setup_vector_store.py
```

## Running the Application

### Start API Server
```bash
uvicorn app.main:app --reload
```
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Start Streamlit UI
```bash
streamlit run app/streamlit_app.py
```
- UI: http://localhost:8501

### Run Both (Recommended)
```bash
# Terminal 1
uvicorn app.main:app --reload

# Terminal 2
streamlit run app/streamlit_app.py
```

## Testing Commands

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_llm.py -v
pytest tests/test_retriever.py -v
pytest tests/test_routes.py -v
pytest tests/test_parser.py -v
```

### Run Specific Test
```bash
pytest tests/test_routes.py::test_health_check -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## API Commands

### Health Check
```bash
curl http://localhost:8000/health
```

### Query the API
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

### View API Documentation
```
http://localhost:8000/docs
```

## Docker Commands

### Build Docker Image
```bash
docker build -t rag-assistant .
```

### Run Docker Container
```bash
docker run -p 8000:8000 \
  -e GITHUB_TOKEN=your_token \
  rag-assistant
```

## Development Commands

### Format Code
```bash
black app/ tests/
```

### Lint Code
```bash
flake8 app/ tests/
```

### Type Check
```bash
mypy app/
```

## Utility Commands

### Check Python Version
```bash
python --version
```

### List Installed Packages
```bash
pip list
```

### Update pip
```bash
pip install --upgrade pip
```

### Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Windows Batch Scripts

### Install Dependencies
```bash
install.bat
```

### Setup Vector Store
```bash
setup_docs.bat
```

### Run API
```bash
run_api.bat
```

### Run UI
```bash
run_ui.bat
```

### Run Tests
```bash
run_tests.bat
```

## Debugging Commands

### Check Environment Variables
```bash
# Linux/Mac
echo $GITHUB_TOKEN

# Windows PowerShell
$env:GITHUB_TOKEN
```

### View Application Logs
```bash
# API logs appear in terminal where uvicorn is running
# UI logs appear in terminal where streamlit is running
```

### Test Vector Store
```bash
python -c "from app.services.retriever import get_retriever; r = get_retriever(); print('Vector store loaded successfully')"
```

### Test LLM Connection
```bash
python -c "from app.services.llm import generate_answer; print(generate_answer('test', []))"
```

## Cleanup Commands

### Remove Vector Store
```bash
# Linux/Mac
rm -rf vector_store/

# Windows PowerShell
Remove-Item -Recurse -Force vector_store
```

### Remove Python Cache
```bash
# Linux/Mac
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Windows PowerShell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
```

### Remove Virtual Environment
```bash
# Linux/Mac
rm -rf .venv

# Windows PowerShell
Remove-Item -Recurse -Force .venv
```

## Troubleshooting Commands

### Verify GitHub Token
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token set:', bool(os.getenv('GITHUB_TOKEN')))"
```

### Check Vector Store Exists
```bash
# Linux/Mac
ls -la vector_store/

# Windows PowerShell
Get-ChildItem vector_store/
```

### Test API Connection
```bash
curl -v http://localhost:8000/health
```

### View Streamlit Logs
```bash
streamlit run app/streamlit_app.py --logger.level=debug
```

## Quick Reference

| Task | Command |
|------|---------|
| Install | `pip install -r requirements.txt` |
| Setup | `python setup_vector_store.py` |
| API | `uvicorn app.main:app --reload` |
| UI | `streamlit run app/streamlit_app.py` |
| Test | `pytest tests/ -v` |
| Query | `curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question": "..."}' ` |

## Environment Variables

```bash
# Required
GITHUB_TOKEN=ghp_your_token_here

# Optional (for development)
DEBUG=true
LOG_LEVEL=INFO
```

## File Locations

```
.env                          # Environment variables
requirements.txt              # Python dependencies
app/main.py                   # FastAPI application
app/streamlit_app.py          # Streamlit UI
app/services/llm.py           # LLM service
app/services/embeddings.py    # Embeddings service
app/services/retriever.py     # Retriever service
app/utils/parser.py           # PDF parser
data/papers/                  # PDF documents
vector_store/                 # FAISS vector store
tests/                        # Test suite
```

---

**For more information, see:**
- README.md - Project overview
- GITHUB_MARKETPLACE_SETUP.md - Detailed setup guide
- QUICKSTART.md - 5-minute quick start
- MIGRATION_GUIDE.md - Migration from OpenAI
