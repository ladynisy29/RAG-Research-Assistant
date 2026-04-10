import pytest
import os
from app.utils.parser import load_and_split


def test_load_and_split_file_not_found():
    """Test that FileNotFoundError is raised for non-existent PDF."""
    with pytest.raises(FileNotFoundError):
        load_and_split("nonexistent.pdf")


def test_load_and_split_invalid_file():
    """Test that error is raised for invalid PDF."""
    # Create a temporary invalid PDF file
    test_file = "test_invalid.pdf"
    with open(test_file, "w") as f:
        f.write("This is not a PDF")
    
    try:
        # Invalid PDF will raise an error during parsing
        with pytest.raises((FileNotFoundError, Exception)):
            load_and_split(test_file)
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
