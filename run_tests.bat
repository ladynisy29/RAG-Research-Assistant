@echo off
REM Run test suite

echo Running test suite...
echo.

python -m pytest tests/ -v

pause
