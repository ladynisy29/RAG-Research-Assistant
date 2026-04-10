"""
Syntax and import validation tests - no external dependencies required
"""
import sys
import ast
from pathlib import Path


def test_all_python_files_have_valid_syntax():
    """Test that all Python files have valid syntax."""
    app_dir = Path("app")
    python_files = list(app_dir.rglob("*.py"))
    
    assert len(python_files) > 0, "No Python files found in app directory"
    
    for py_file in python_files:
        with open(py_file, 'r') as f:
            code = f.read()
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise AssertionError(f"Syntax error in {py_file}: {e}")


def test_main_py_exists():
    """Test that main.py exists."""
    assert Path("app/main.py").exists(), "app/main.py not found"


def test_services_exist():
    """Test that all service files exist."""
    services = [
        "app/services/llm.py",
        "app/services/embeddings.py",
        "app/services/retriever.py"
    ]
    for service in services:
        assert Path(service).exists(), f"{service} not found"


def test_routes_exist():
    """Test that route files exist."""
    assert Path("app/routes/query.py").exists(), "app/routes/query.py not found"


def test_utils_exist():
    """Test that utility files exist."""
    assert Path("app/utils/parser.py").exists(), "app/utils/parser.py not found"


def test_init_files_exist():
    """Test that all __init__.py files exist."""
    init_files = [
        "app/__init__.py",
        "app/services/__init__.py",
        "app/routes/__init__.py",
        "app/utils/__init__.py"
    ]
    for init_file in init_files:
        assert Path(init_file).exists(), f"{init_file} not found"


def test_config_files_exist():
    """Test that configuration files exist."""
    config_files = [
        ".env",
        "requirements.txt",
        "pytest.ini",
        "Dockerfile"
    ]
    for config_file in config_files:
        assert Path(config_file).exists(), f"{config_file} not found"


def test_documentation_exists():
    """Test that documentation files exist."""
    docs = [
        "README.md",
        "QUICKSTART.md",
        "FIXES_APPLIED.md"
    ]
    for doc in docs:
        assert Path(doc).exists(), f"{doc} not found"


def test_setup_script_exists():
    """Test that setup script exists."""
    assert Path("setup_vector_store.py").exists(), "setup_vector_store.py not found"


def test_batch_scripts_exist():
    """Test that Windows batch scripts exist."""
    scripts = [
        "install.bat",
        "run_api.bat",
        "run_ui.bat",
        "run_tests.bat",
        "setup_docs.bat"
    ]
    for script in scripts:
        assert Path(script).exists(), f"{script} not found"


def test_main_py_has_fastapi_app():
    """Test that main.py defines FastAPI app."""
    with open("app/main.py", 'r') as f:
        content = f.read()
    
    assert "FastAPI" in content, "FastAPI not imported in main.py"
    assert "app = FastAPI" in content, "FastAPI app not instantiated in main.py"


def test_routes_has_router():
    """Test that routes define router."""
    with open("app/routes/query.py", 'r') as f:
        content = f.read()
    
    assert "APIRouter" in content, "APIRouter not imported in query.py"
    assert "router = APIRouter" in content, "Router not instantiated in query.py"


def test_services_have_functions():
    """Test that services define expected functions."""
    services = {
        "app/services/llm.py": "generate_answer",
        "app/services/embeddings.py": "create_vector_store",
        "app/services/retriever.py": "get_retriever",
        "app/utils/parser.py": "load_and_split"
    }
    
    for service_file, function_name in services.items():
        with open(service_file, 'r') as f:
            content = f.read()
        
        assert f"def {function_name}" in content, \
            f"Function {function_name} not found in {service_file}"


def test_error_handling_in_services():
    """Test that services have error handling."""
    services = [
        "app/services/llm.py",
        "app/services/embeddings.py",
        "app/services/retriever.py",
        "app/utils/parser.py"
    ]
    
    for service in services:
        with open(service, 'r') as f:
            content = f.read()
        
        assert "try:" in content or "except" in content or "raise" in content, \
            f"No error handling found in {service}"


def test_logging_configured():
    """Test that logging is configured."""
    with open("app/main.py", 'r') as f:
        content = f.read()
    
    assert "logging" in content, "Logging not imported in main.py"
    assert "basicConfig" in content, "Logging not configured in main.py"


def test_env_file_has_api_key():
    """Test that .env file has API key placeholder."""
    with open(".env", 'r') as f:
        content = f.read()
    
    assert "OPENAI_API_KEY" in content, "OPENAI_API_KEY not in .env"


def test_requirements_has_versions():
    """Test that requirements.txt has pinned versions."""
    with open("requirements.txt", 'r') as f:
        lines = f.readlines()
    
    versioned_packages = [line for line in lines if "==" in line]
    assert len(versioned_packages) > 5, "Not enough pinned versions in requirements.txt"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
