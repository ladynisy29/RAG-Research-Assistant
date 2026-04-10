# GitHub Marketplace Models Setup Guide

## Overview

This RAG Research Assistant now uses **GPT-4 Mini** from GitHub Marketplace Models instead of OpenAI's direct API. This provides:

- ✅ Better pricing
- ✅ Integrated with GitHub
- ✅ Easy token management
- ✅ Access to multiple models

## Models Used

- **LLM**: `gpt-4-mini` - For generating answers
- **Embeddings**: `text-embedding-3-small` - For document embeddings

## Setup Steps

### 1. Get Your GitHub Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `read:packages` (read packages)
4. Copy the token (you won't see it again!)

### 2. Configure Environment

Edit `.env` file:
```
GITHUB_TOKEN=ghp_your_token_here
```

Replace `ghp_your_token_here` with your actual GitHub token.

### 3. Verify Setup

Test the configuration:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token set:', bool(os.getenv('GITHUB_TOKEN')))"
```

Expected output:
```
Token set: True
```

## API Endpoints

The application uses GitHub's inference API:
- **Base URL**: `https://models.inference.ai.azure.com`
- **Authentication**: GitHub token in `api_key` parameter

## Usage

### Initialize Vector Store

```bash
python setup_vector_store.py
```

This will:
1. Load PDFs from `data/papers/`
2. Create embeddings using `text-embedding-3-small`
3. Save to `vector_store/`

### Run the Application

**Terminal 1 - API Server:**
```bash
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Streamlit UI:**
```bash
python -m streamlit run app/streamlit_app.py
```

### Query the API

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

## Troubleshooting

### "GITHUB_TOKEN not set"
- Make sure `.env` file exists in the project root
- Verify the token is correctly set: `GITHUB_TOKEN=ghp_...`
- Restart the application after updating `.env`

### "Invalid token"
- Check that the token hasn't expired
- Verify you copied the entire token correctly
- Generate a new token if needed

### "Model not found"
- Ensure you're using the correct model names:
  - LLM: `gpt-4-mini`
  - Embeddings: `text-embedding-3-small`
- Check GitHub Marketplace Models for available models

### "Rate limit exceeded"
- GitHub Marketplace Models has rate limits
- Wait a few minutes before retrying
- Check your usage in GitHub settings

## Available Models

You can use other models from GitHub Marketplace Models by updating the model names in:

- `app/services/llm.py` - Change `gpt-4-mini` to another model
- `app/services/embeddings.py` - Change `text-embedding-3-small` to another embedding model

Common alternatives:
- **LLM**: `gpt-4`, `gpt-3.5-turbo`, `claude-3-5-sonnet`
- **Embeddings**: `text-embedding-3-large`

## Code Changes

### LLM Service
```python
llm = ChatOpenAI(
    api_key=github_token,
    model="gpt-4-mini",
    base_url="https://models.inference.ai.azure.com"
)
```

### Embeddings Service
```python
embeddings = OpenAIEmbeddings(
    api_key=github_token,
    model="text-embedding-3-small",
    base_url="https://models.inference.ai.azure.com"
)
```

## Security Notes

- ✅ Never commit `.env` file to git
- ✅ Keep your GitHub token private
- ✅ Use environment variables for secrets
- ✅ Rotate tokens periodically
- ✅ Use `.gitignore` to exclude `.env`

## Pricing

GitHub Marketplace Models pricing varies by model. Check the [GitHub Marketplace](https://github.com/marketplace/models) for current rates.

## Support

For issues with GitHub Marketplace Models:
- Check [GitHub Marketplace Models Documentation](https://docs.github.com/en/github-models)
- Visit [GitHub Community Discussions](https://github.com/orgs/community/discussions)
- Check your GitHub token permissions

## Next Steps

1. ✅ Get GitHub token
2. ✅ Update `.env` with token
3. ✅ Run `python setup_vector_store.py`
4. ✅ Start API and UI
5. ✅ Begin using the application

---

**Note**: The application is now fully integrated with GitHub Marketplace Models. All API calls use your GitHub token for authentication.
