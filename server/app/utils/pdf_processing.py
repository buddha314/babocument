"""
PDF Processing Utilities

Functions for extracting text and metadata from PDF files.
"""

import structlog
from pathlib import Path
from typing import Any

logger = structlog.get_logger(__name__)


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """
    Extract full text from a PDF file.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Extracted text content
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If text extraction fails
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    logger.info("extracting_text_from_pdf", file=str(pdf_path))
    
    try:
        # Use pypdf (modern replacement for PyPDF2)
        try:
            from pypdf import PdfReader
            
            text = ""
            with open(pdf_path, "rb") as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            logger.info("text_extracted_pypdf", char_count=len(text))
            return text.strip()
            
        except ImportError:
            # Fall back to pdfplumber if pypdf not available
            import pdfplumber
            
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            logger.info("text_extracted_pdfplumber", char_count=len(text))
            return text.strip()
            
    except Exception as e:
        logger.error("pdf_extraction_error", file=str(pdf_path), error=str(e))
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_pdf_metadata(pdf_path: str | Path) -> dict[str, Any]:
    """
    Extract metadata from PDF file.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Dictionary with metadata (title, author, creation date, etc.)
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    logger.info("extracting_pdf_metadata", file=str(pdf_path))
    
    try:
        from pypdf import PdfReader
        
        with open(pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)
            metadata = pdf_reader.metadata or {}
            
            # Extract common fields
            extracted = {
                "title": metadata.get("/Title", ""),
                "author": metadata.get("/Author", ""),
                "subject": metadata.get("/Subject", ""),
                "creator": metadata.get("/Creator", ""),
                "producer": metadata.get("/Producer", ""),
                "creation_date": metadata.get("/CreationDate", ""),
                "modification_date": metadata.get("/ModDate", ""),
                "page_count": len(pdf_reader.pages),
            }
            
            logger.info("pdf_metadata_extracted", title=extracted["title"])
            return extracted
            
    except ImportError:
        logger.warning("pypdf_not_available", fallback="basic_metadata")
        # Return basic metadata without PDF parsing
        return {
            "title": pdf_path.stem,
            "page_count": 0,
        }
    except Exception as e:
        logger.error("pdf_metadata_error", file=str(pdf_path), error=str(e))
        return {"title": pdf_path.stem}


def parse_research_paper_metadata(text: str, pdf_metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Parse research paper metadata from extracted text.
    
    Uses heuristics to extract title, abstract, authors from paper text.
    
    Args:
        text: Extracted PDF text
        pdf_metadata: PDF file metadata
    
    Returns:
        Dictionary with parsed metadata
    """
    # TODO: Implement smarter parsing
    # For now, use PDF metadata as fallback
    
    metadata = {
        "title": pdf_metadata.get("title", "Untitled"),
        "authors": [],
        "abstract": "",
        "year": None,
    }
    
    # Try to extract year from text (simple regex)
    import re
    year_match = re.search(r'\b(19|20)\d{2}\b', text[:1000])
    if year_match:
        metadata["year"] = int(year_match.group())
    
    # Try to find abstract
    abstract_match = re.search(
        r'abstract\s*[:\-]?\s*(.{100,1000}?)\s*(?:introduction|keywords|1\.|i\.)',
        text[:5000],
        re.IGNORECASE | re.DOTALL
    )
    if abstract_match:
        metadata["abstract"] = abstract_match.group(1).strip()
    
    return metadata
