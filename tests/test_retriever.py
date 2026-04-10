import pytest
import os
from unittest.mock import Mock, patch
from app.services.retriever import evaluate_retrieval


def test_get_retriever_vector_store_not_found():
    """Test that FileNotFoundError is raised when vector store doesn't exist."""
    with patch("os.path.exists", return_value=False):
        from app.services.retriever import get_retriever
        with pytest.raises(FileNotFoundError, match="Vector store not found"):
            get_retriever()


def test_evaluate_retrieval_found():
    """Test evaluation when expected document is found."""
    mock_doc = Mock()
    mock_doc.page_content = "Expected content"
    
    mock_retriever = Mock()
    mock_retriever.invoke.return_value = [mock_doc]
    
    result = evaluate_retrieval("test query", "Expected content", mock_retriever)
    assert result is True


def test_evaluate_retrieval_not_found():
    """Test evaluation when expected document is not found."""
    mock_doc = Mock()
    mock_doc.page_content = "Different content"
    
    mock_retriever = Mock()
    mock_retriever.invoke.return_value = [mock_doc]
    
    result = evaluate_retrieval("test query", "Expected content", mock_retriever)
    assert result is False


def test_evaluate_retrieval_error():
    """Test evaluation handles errors gracefully."""
    mock_retriever = Mock()
    mock_retriever.invoke.side_effect = Exception("Test error")
    
    result = evaluate_retrieval("test query", "Expected content", mock_retriever)
    assert result is False
