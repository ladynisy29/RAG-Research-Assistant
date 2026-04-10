"""Integration tests for the RAG Research Assistant."""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app


class TestProjectStructure:
    """Test project structure and configuration."""
    
    def test_project_directories_exist(self):
        """Test that all required directories exist."""
        required_dirs = [
            'app', 'app/services', 'app/routes', 'app/utils',
            'data', 'data/papers', 'vector_store', 'tests'
        ]
        for dir_name in required_dirs:
            assert os.path.isdir(dir_name), f"Directory {dir_name} not found"
    
    def test_required_files_exist(self):
        """Test that all required files exist."""
        required_files = [
            'app/main.py', 'app/streamlit_app.py',
            'app/services/llm.py', 'app/services/embeddings.py',
            'app/services/retriever.py', 'app/routes/query.py',
            'app/utils/parser.py', 'requirements.txt', '.env',
            'setup_vector_store.py'
        ]
        for file_name in required_files:
            assert os.path.isfile(file_name), f"File {file_name} not found"
    
    def test_package_init_files_exist(self):
        """Test that all __init__.py files exist."""
        init_files = [
            'app/__init__.py', 'app/services/__init__.py',
            'app/routes/__init__.py', 'app/utils/__init__.py'
        ]
        for file_name in init_files:
            assert os.path.isfile(file_name), f"Init file {file_name} not found"


class TestAPIEndpoints:
    """Test FastAPI endpoints."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
    
    def test_query_empty_question(self):
        """Test query endpoint with empty question."""
        response = self.client.post('/query', json={'question': ''})
        assert response.status_code == 400
        assert 'empty' in response.json()['detail'].lower()
    
    def test_query_whitespace_question(self):
        """Test query endpoint with whitespace-only question."""
        response = self.client.post('/query', json={'question': '   '})
        assert response.status_code == 400
    
    def test_query_missing_github_token(self):
        """Test query endpoint without GitHub token."""
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post('/query', json={'question': 'test'})
            assert response.status_code == 503
            assert 'GitHub token' in response.json()['detail']
    
    def test_query_vector_store_not_found(self):
        """Test query endpoint when vector store doesn't exist."""
        with patch('app.services.retriever.get_retriever') as mock_retriever:
            mock_retriever.side_effect = FileNotFoundError("Vector store not found")
            response = self.client.post('/query', json={'question': 'test'})
            assert response.status_code == 503
            assert 'Vector store' in response.json()['detail']


class TestServices:
    """Test service layer."""
    
    def test_llm_empty_docs(self):
        """Test LLM service with empty docs."""
        from app.services.llm import generate_answer
        result = generate_answer('test', [])
        assert 'No relevant documents' in result
    
    def test_llm_missing_token(self):
        """Test LLM service without GitHub token."""
        from app.services.llm import generate_answer
        mock_doc = Mock()
        mock_doc.page_content = 'test'
        
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match='GITHUB_TOKEN'):
                generate_answer('test', [mock_doc])
    
    def test_parser_missing_file(self):
        """Test parser with missing file."""
        from app.utils.parser import load_and_split
        with pytest.raises(FileNotFoundError):
            load_and_split('nonexistent.pdf')
    
    def test_retriever_missing_vector_store(self):
        """Test retriever without vector store."""
        from app.services.retriever import get_retriever
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileNotFoundError, match='Vector store'):
                get_retriever()
    
    def test_retriever_missing_token(self):
        """Test retriever without GitHub token."""
        from app.services.retriever import get_retriever
        with patch('os.path.exists', return_value=True):
            with patch.dict(os.environ, {}, clear=True):
                with pytest.raises(ValueError, match='GITHUB_TOKEN'):
                    get_retriever()


class TestErrorHandling:
    """Test error handling across the application."""
    
    def test_llm_error_handling(self):
        """Test LLM service error handling."""
        from app.services.llm import generate_answer
        mock_doc = Mock()
        mock_doc.page_content = 'test'
        
        with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}):
            with patch('app.services.llm.ChatOpenAI') as mock_llm:
                mock_llm.side_effect = Exception('API Error')
                with pytest.raises(Exception):
                    generate_answer('test', [mock_doc])
    
    def test_embeddings_error_handling(self):
        """Test embeddings service error handling."""
        from app.services.embeddings import create_vector_store
        with pytest.raises(ValueError, match='No documents'):
            create_vector_store([])
    
    def test_parser_error_handling(self):
        """Test parser error handling."""
        from app.utils.parser import load_and_split
        with pytest.raises(FileNotFoundError):
            load_and_split('invalid.pdf')


class TestConfiguration:
    """Test configuration and environment."""
    
    def test_env_file_exists(self):
        """Test that .env file exists."""
        assert os.path.isfile('.env')
    
    def test_requirements_file_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.isfile('requirements.txt')
    
    def test_requirements_has_versions(self):
        """Test that requirements have version pinning."""
        with open('requirements.txt', 'r') as f:
            content = f.read()
            # Check for version pinning (==)
            assert '==' in content, "Requirements should have pinned versions"
    
    def test_github_token_in_env(self):
        """Test that GITHUB_TOKEN is in .env."""
        with open('.env', 'r') as f:
            content = f.read()
            assert 'GITHUB_TOKEN' in content


class TestDocumentation:
    """Test documentation files."""
    
    def test_readme_exists(self):
        """Test that README exists."""
        assert os.path.isfile('README.md')
    
    def test_quickstart_exists(self):
        """Test that QUICKSTART guide exists."""
        assert os.path.isfile('QUICKSTART.md')
    
    def test_github_marketplace_setup_exists(self):
        """Test that GitHub Marketplace setup guide exists."""
        assert os.path.isfile('GITHUB_MARKETPLACE_SETUP.md')
    
    def test_migration_guide_exists(self):
        """Test that migration guide exists."""
        assert os.path.isfile('MIGRATION_GUIDE.md')


class TestDataDirectories:
    """Test data directories."""
    
    def test_papers_directory_exists(self):
        """Test that papers directory exists."""
        assert os.path.isdir('data/papers')
    
    def test_vector_store_directory_exists(self):
        """Test that vector store directory exists."""
        assert os.path.isdir('vector_store')
