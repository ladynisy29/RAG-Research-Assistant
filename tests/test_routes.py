import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_empty_question():
    """Test query endpoint with empty question."""
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 400


def test_query_vector_store_not_found():
    """Test query endpoint when vector store doesn't exist."""
    with patch("app.services.retriever.get_retriever") as mock_retriever:
        mock_retriever.side_effect = FileNotFoundError("Vector store not found")
        response = client.post("/query", json={"question": "test question"})
        assert response.status_code == 503


def test_query_success():
    """Test successful query."""
    mock_doc = Mock()
    mock_doc.page_content = "Test content"
    mock_doc.metadata = {"source": "test.pdf"}
    
    mock_retriever = Mock()
    # Use invoke() instead of get_relevant_documents()
    mock_retriever.invoke.return_value = [mock_doc]
    
    with patch("app.services.retriever.get_retriever", return_value=mock_retriever):
        with patch("app.services.llm.generate_answer", return_value="Test answer"):
            response = client.post("/query", json={"question": "test question"})
            assert response.status_code == 200
            data = response.json()
            assert data["answer"] == "Test answer"
            assert len(data["sources"]) == 1
