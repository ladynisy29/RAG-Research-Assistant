@echo off
REM Start FastAPI server

echo Starting RAG Research Assistant API...
echo.
echo API will be available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload

pause
