# Windows Setup Guide

## Issue with Python PATH

Your system has Python installed but the `python` command is redirecting to the Microsoft Store. This is a known Windows issue. We've created batch scripts to work around this.

## Installation Steps

### 1. Run the Installation Script

Double-click `install.bat` in the project folder. This will:
- Upgrade pip
- Install all dependencies from requirements.txt
- Show you the next steps

**Expected output:**
```
Installing dependencies...
...
Installation completed successfully!
```

### 2. Configure Environment

Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Add Your Documents

Copy your PDF files to the `data/papers/` folder.

### 4. Initialize Vector Store

Double-click `setup_docs.bat` to process your PDFs and create the vector store.

**Expected output:**
```
Setting up vector store from PDFs...
Found 2 PDF file(s)
Processing paper1.pdf...
Loaded 45 chunks from paper1.pdf
Creating vector store with 90 total chunks...
Vector store created successfully!
```

## Running the Application

### Option 1: API Only

Double-click `run_api.bat`

The API will be available at:
- Main: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs

### Option 2: UI Only

Double-click `run_ui.bat`

The UI will be available at: http://localhost:8501

### Option 3: Both (Recommended)

1. Double-click `run_api.bat` (keep it running)
2. Open another command prompt and double-click `run_ui.bat`

## Testing

Double-click `run_tests.bat` to run the test suite.

## Troubleshooting

### "Python was not found" error

This is the Microsoft Store redirect issue. The batch scripts handle this automatically. If you still get errors:

1. Open Settings → Apps → Advanced app settings
2. Search for "python"
3. Click on "python.exe" and disable the app execution alias
4. Repeat for "python3.exe"

Then try the batch scripts again.

### "OPENAI_API_KEY not set"

Make sure you've edited `.env` and added your actual API key (not the placeholder).

### "Vector store not found"

Run `setup_docs.bat` first to create the vector store from your PDFs.

### "Cannot connect to API"

Make sure `run_api.bat` is running in another terminal before starting the UI.

## Manual Commands (if batch scripts don't work)

If the batch scripts fail, you can run commands manually in PowerShell:

```powershell
# Install dependencies
&"C:\Users\empre\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt

# Setup vector store
&"C:\Users\empre\AppData\Local\Programs\Python\Python313\python.exe" setup_vector_store.py

# Run API
&"C:\Users\empre\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn app.main:app --reload

# Run UI
&"C:\Users\empre\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app/streamlit_app.py

# Run tests
&"C:\Users\empre\AppData\Local\Programs\Python\Python313\python.exe" -m pytest tests/ -v
```

## Next Steps

1. ✅ Run `install.bat`
2. ✅ Edit `.env` with your API key
3. ✅ Add PDFs to `data/papers/`
4. ✅ Run `setup_docs.bat`
5. ✅ Run `run_api.bat` and `run_ui.bat`
6. ✅ Open http://localhost:8501 in your browser

That's it! You're ready to use the RAG Research Assistant.
