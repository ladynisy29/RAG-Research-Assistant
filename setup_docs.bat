@echo off
REM Initialize vector store from PDFs

echo Setting up vector store from PDFs...
echo.
echo Make sure you have:
echo 1. Added OPENAI_API_KEY to .env
echo 2. Placed PDF files in data/papers/
echo.

python setup_vector_store.py

pause
