# app/utils/parser.py

import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def load_and_split(pdf_path):
    """Load PDF and split into chunks."""
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        
        if not docs:
            raise ValueError(f"No documents found in {pdf_path}")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        split_docs = splitter.split_documents(docs)
        logger.info(f"Loaded {len(docs)} pages, split into {len(split_docs)} chunks")
        return split_docs
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Error loading PDF: {str(e)}")
        raise FileNotFoundError(f"Cannot load PDF from {pdf_path}: {str(e)}")
    except Exception as e:
        logger.error(f"Error loading PDF: {str(e)}")
        raise