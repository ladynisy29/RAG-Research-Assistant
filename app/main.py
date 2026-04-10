# FastAPI main app entry point

import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Research Assistant", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes here
from app.routes import query

app.include_router(query.router)

@app.on_event("startup")
async def startup_event():
    """Preload retriever on startup to avoid hanging on first request."""
    try:
        logger.info("Preloading vector store retriever...")
        from app.services.retriever import get_retriever
        retriever = get_retriever()
        logger.info("Vector store retriever loaded successfully!")
    except Exception as e:
        logger.warning(f"Could not preload retriever: {str(e)}")
        logger.warning("Vector store will be loaded on first query")

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
