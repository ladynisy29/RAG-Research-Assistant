@echo off
REM Installation script for RAG Research Assistant

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Installation completed successfully!
    echo.
    echo Next steps:
    echo 1. Edit .env and add your OPENAI_API_KEY
    echo 2. Place PDF files in data/papers/
    echo 3. Run: python setup_vector_store.py
    echo 4. Run: uvicorn app.main:app --reload
    echo 5. In another terminal: streamlit run app/streamlit_app.py
) else (
    echo Installation failed. Please check the error messages above.
)

pause
