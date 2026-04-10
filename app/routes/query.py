from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import Body
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_rag(request: QueryRequest = Body(...)):
    """Process a RAG query and return answer with sources."""
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        logger.info(f"Processing query: {request.question}")
        
        # Import here to avoid hanging on module load
        from app.services.retriever import get_retriever
        from app.services.llm import generate_answer
        
        logger.info("Getting retriever...")
        retriever = get_retriever()
        logger.info("Retriever obtained, invoking with question...")
        
        # Use invoke() method for LangChain retriever
        docs = retriever.invoke(request.question)
        logger.info(f"Retrieved {len(docs)} documents")
        
        logger.info("Generating answer...")
        answer = generate_answer(request.question, docs)
        logger.info(f"Answer generated: {answer[:50]}...")
        
        return {
            "answer": answer,
            "sources": [doc.metadata for doc in docs]
        }
    except FileNotFoundError as e:
        logger.error(f"Vector store not found: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail="Vector store not initialized. Please load documents first.")
    except ValueError as e:
        if "GITHUB_TOKEN" in str(e):
            logger.error(f"GitHub token not configured: {str(e)}", exc_info=True)
            raise HTTPException(status_code=503, detail="GitHub token not configured. Please set GITHUB_TOKEN in .env")
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
