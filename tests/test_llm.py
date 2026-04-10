import pytest
import os
from unittest.mock import Mock, patch
from app.services.llm import generate_answer


def test_generate_answer_no_docs():
    """Test that empty docs returns appropriate message."""
    result = generate_answer("test question", [])
    assert "No relevant documents" in result


def test_generate_answer_missing_github_token():
    """Test that missing GitHub token raises ValueError."""
    mock_doc = Mock()
    mock_doc.page_content = "Test content"
    
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GITHUB_TOKEN"):
            generate_answer("test question", [mock_doc])


def test_generate_answer_with_docs():
    """Test successful answer generation with mocked LLM."""
    mock_doc = Mock()
    mock_doc.page_content = "Test document content"
    
    mock_response = Mock()
    mock_response.content = "Test answer"
    
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"}):
        with patch("app.services.llm.ChatOpenAI") as mock_llm_class:
            mock_instance = Mock()
            mock_instance.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_instance
            result = generate_answer("test question", [mock_doc])
            assert result == "Test answer"
