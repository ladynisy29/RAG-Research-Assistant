# Migration Guide: OpenAI → GitHub Marketplace Models

This guide helps you migrate from using OpenAI's API directly to GitHub Marketplace Models.

## What Changed

### Before (OpenAI)
```python
# Used OPENAI_API_KEY
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
embeddings = OpenAIEmbeddings()
```

### After (GitHub Marketplace Models)
```python
# Uses GITHUB_TOKEN
llm = ChatOpenAI(
    api_key=github_token,
    model="gpt-4-mini",
    base_url="https://models.inference.ai.azure.com"
)
embeddings = OpenAIEmbeddings(
    api_key=github_token,
    model="text-embedding-3-small",
    base_url="https://models.inference.ai.azure.com"
)
```

## Migration Steps

### 1. Update Environment Variables

**Old `.env`:**
```
OPENAI_API_KEY=sk-...
```

**New `.env`:**
```
GITHUB_TOKEN=ghp_...
```

### 2. Get GitHub Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select required scopes
4. Copy and save the token

### 3. Update Code (Already Done!)

The following files have been updated:
- ✅ `app/services/llm.py` - Uses GitHub token and gpt-4-mini
- ✅ `app/services/embeddings.py` - Uses GitHub token and text-embedding-3-small
- ✅ `app/services/retriever.py` - Uses GitHub token for embeddings
- ✅ `tests/test_llm.py` - Updated tests for GitHub token
- ✅ `tests/test_retriever.py` - Updated tests for GitHub token

### 4. Reinitialize Vector Store

Since embeddings model changed, recreate the vector store:

```bash
# Remove old vector store
rm -rf vector_store/  # On Windows: rmdir /s /q vector_store

# Create new one with GitHub Marketplace embeddings
python setup_vector_store.py
```

### 5. Test the Setup

```bash
# Run tests
pytest tests/ -v

# Start API
uvicorn app.main:app --reload

# In another terminal, start UI
streamlit run app/streamlit_app.py
```

## Benefits of GitHub Marketplace Models

| Aspect | OpenAI | GitHub Marketplace |
|--------|--------|-------------------|
| **Authentication** | API Key | GitHub Token |
| **Integration** | Standalone | GitHub-native |
| **Models** | Limited | Multiple options |
| **Pricing** | Per-token | Competitive |
| **Management** | Separate account | GitHub account |

## Troubleshooting

### "GITHUB_TOKEN not set"
- Ensure `.env` file exists in project root
- Verify token format: `GITHUB_TOKEN=ghp_...`
- Restart application after updating `.env`

### "Vector store not found"
- Old vector store is incompatible with new embeddings model
- Run: `python setup_vector_store.py`

### "Model not found"
- Verify model names are correct:
  - LLM: `gpt-4-mini`
  - Embeddings: `text-embedding-3-small`

### "Invalid token"
- Token may have expired
- Generate a new token from GitHub settings
- Ensure token has required scopes

## Reverting to OpenAI (If Needed)

If you need to revert to OpenAI:

1. Update `.env`:
```
OPENAI_API_KEY=sk_...
```

2. Update `app/services/llm.py`:
```python
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
```

3. Update `app/services/embeddings.py`:
```python
embeddings = OpenAIEmbeddings()
```

4. Update `app/services/retriever.py`:
```python
embeddings = OpenAIEmbeddings()
```

5. Recreate vector store:
```bash
python setup_vector_store.py
```

## Model Comparison

### GPT-4 Mini (GitHub Marketplace)
- ✅ Latest model
- ✅ Better reasoning
- ✅ Competitive pricing
- ✅ GitHub integration

### GPT-3.5-Turbo (OpenAI)
- ✅ Proven performance
- ✅ Lower latency
- ✅ Established pricing
- ✅ Direct OpenAI support

## Performance Notes

- **Latency**: GitHub Marketplace may have slightly higher latency
- **Accuracy**: GPT-4 Mini provides better reasoning
- **Cost**: Generally more cost-effective
- **Rate Limits**: Check GitHub Marketplace for limits

## Support

For issues:
- [GitHub Marketplace Models Docs](https://docs.github.com/en/github-models)
- [GitHub Community Discussions](https://github.com/orgs/community/discussions)
- Check your GitHub token permissions

## Summary

✅ All code has been updated to use GitHub Marketplace Models
✅ Tests have been updated and pass successfully
✅ Documentation has been updated
✅ Ready to use with your GitHub token

**Next Step**: Update `.env` with your GitHub token and run `python setup_vector_store.py`
