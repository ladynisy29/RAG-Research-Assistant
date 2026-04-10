@echo off
REM Start Streamlit UI

echo Starting RAG Research Assistant UI...
echo.
echo UI will be available at: http://localhost:8501
echo.

python -m streamlit run app/streamlit_app.py

pause
