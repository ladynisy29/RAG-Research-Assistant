#!/usr/bin/env python3
"""
Script to initialize the vector store from PDF documents.
Usage: python setup_vector_store.py
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from app.utils.parser import load_and_split
from app.services.embeddings import create_vector_store


def main():
    """Initialize vector store from PDFs in data/papers directory."""
    
    # Check GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        logger.error("GITHUB_TOKEN not set in .env file. Please add your GitHub token.")
        logger.error("Get your token from: https://github.com/settings/tokens")
        sys.exit(1)
    
    papers_dir = Path("data/papers")
    if not papers_dir.exists():
        logger.error(f"Directory {papers_dir} does not exist")
        sys.exit(1)
    
    # Find all PDF files
    pdf_files = list(papers_dir.glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDF files found in {papers_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF file(s)")
    
    all_docs = []
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing {pdf_file.name}...")
            docs = load_and_split(str(pdf_file))
            all_docs.extend(docs)
            logger.info(f"  Loaded {len(docs)} chunks from {pdf_file.name}")
        except Exception as e:
            logger.error(f"  Error processing {pdf_file.name}: {str(e)}")
            continue
    
    if not all_docs:
        logger.error("No documents were successfully loaded")
        sys.exit(1)
    
    try:
        logger.info(f"Creating vector store with {len(all_docs)} total chunks...")
        create_vector_store(all_docs)
        logger.info("Vector store created successfully!")
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
