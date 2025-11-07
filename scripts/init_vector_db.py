"""
Initialize Vector Database with Local Papers

Scans data/papers directory for PDFs and populates ChromaDB
with embeddings for semantic search.

Usage:
    python scripts/init_vector_db.py [--reset]

Options:
    --reset: Clear existing database before initializing
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import structlog
from pypdf import PdfReader

from app.services.vector_db import get_vector_db
from app.config import settings

logger = structlog.get_logger(__name__)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Extracted text content
    """
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    except Exception as e:
        logger.error("pdf_extraction_error", file=str(pdf_path), error=str(e))
        raise


def extract_title_from_text(text: str) -> str:
    """
    Extract title from PDF text.
    
    Simple heuristic: Take first non-empty line, limit to 200 chars.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    if not lines:
        return "Untitled"
    
    title = lines[0]
    
    # Limit length
    if len(title) > 200:
        title = title[:200] + "..."
    
    return title


def extract_abstract_from_text(text: str) -> str:
    """
    Extract abstract from PDF text.
    
    Looks for "Abstract" section and extracts following text.
    Falls back to first paragraph if not found.
    """
    text_lower = text.lower()
    
    # Look for abstract section
    abstract_markers = ["abstract", "summary", "overview"]
    
    for marker in abstract_markers:
        marker_pos = text_lower.find(marker)
        if marker_pos != -1:
            # Find text after marker
            start = marker_pos + len(marker)
            
            # Look for next section or first 1000 chars
            next_section_markers = [
                "\nintroduction", "\nbackground", "\nmethods",
                "\n1.", "\n2.", "\ni."
            ]
            
            end = start + 1000
            for section_marker in next_section_markers:
                section_pos = text_lower.find(section_marker, start)
                if section_pos != -1 and section_pos < end:
                    end = section_pos
            
            abstract = text[start:end].strip()
            
            if len(abstract) > 100:  # Valid abstract
                return abstract
    
    # Fallback: Use first paragraph
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 100]
    
    if paragraphs:
        return paragraphs[0][:1000]
    
    return ""


def parse_paper(pdf_path: Path) -> dict:
    """
    Parse a PDF paper and extract metadata.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Dictionary with paper data
    """
    logger.info("parsing_paper", file=pdf_path.name)
    
    try:
        # Extract full text
        full_text = extract_text_from_pdf(pdf_path)
        
        # Extract title and abstract
        title = extract_title_from_text(full_text)
        abstract = extract_abstract_from_text(full_text)
        
        # Create paper dictionary
        paper = {
            "id": pdf_path.stem,  # Use filename without extension
            "title": title,
            "abstract": abstract,
            "full_text": full_text,
            "source": "local",
            "file_path": str(pdf_path.absolute()),
        }
        
        logger.info(
            "paper_parsed",
            file=pdf_path.name,
            title=title[:50] + "..." if len(title) > 50 else title,
            text_length=len(full_text),
        )
        
        return paper
    
    except Exception as e:
        logger.error("paper_parsing_error", file=pdf_path.name, error=str(e))
        raise


def initialize_from_papers(
    papers_dir: Path | None = None,
    reset: bool = False,
) -> None:
    """
    Initialize vector database with papers from directory.
    
    Args:
        papers_dir: Directory containing PDF files (default: data/papers)
        reset: Whether to reset database before initializing
    """
    # Default to data/papers relative to project root
    if papers_dir is None:
        project_root = Path(__file__).parent.parent.parent
        papers_dir = project_root / "data" / "papers"
    
    if not papers_dir.exists():
        logger.error("papers_directory_not_found", path=str(papers_dir))
        print(f"❌ Error: Papers directory not found: {papers_dir}")
        sys.exit(1)
    
    logger.info("initializing_vector_database", papers_dir=str(papers_dir))
    print(f"\n{'='*60}")
    print("Vector Database Initialization")
    print(f"{'='*60}")
    print(f"Papers directory: {papers_dir}")
    print(f"Storage path: {settings.chroma_persist_directory}")
    print(f"Embedding model: {settings.embedding_model}")
    print()
    
    # Get vector database instance
    vector_db = get_vector_db()
    
    # Reset if requested
    if reset:
        print("⚠️  Resetting existing database...")
        vector_db.reset()
        print("✅ Database reset complete\n")
    
    # Find all PDF files
    pdf_files = list(papers_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning("no_pdfs_found", path=str(papers_dir))
        print(f"⚠️  No PDF files found in {papers_dir}")
        sys.exit(0)
    
    print(f"Found {len(pdf_files)} PDF files\n")
    print(f"{'='*60}")
    print()
    
    # Parse all papers
    papers = []
    failed = []
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        
        try:
            paper = parse_paper(pdf_path)
            papers.append(paper)
            print(f"  ✅ Title: {paper['title'][:70]}")
            print(f"  📄 Text length: {len(paper['full_text']):,} characters")
            
        except Exception as e:
            failed.append((pdf_path.name, str(e)))
            print(f"  ❌ Failed: {e}")
        
        print()
    
    # Add papers to vector database
    if papers:
        print(f"{'='*60}")
        print(f"\nAdding {len(papers)} papers to vector database...")
        print("(This may take a few minutes for embedding generation)\n")
        
        try:
            count = vector_db.add_papers(papers)
            
            print(f"✅ Successfully added {count} papers!")
            
            # Show stats
            stats = vector_db.get_stats()
            print(f"\n{'='*60}")
            print("Database Statistics:")
            print(f"{'='*60}")
            print(f"Total papers: {stats['total_papers']}")
            print(f"Embedding model: {stats['embedding_model']}")
            print(f"Embedding dimension: {stats['embedding_dimension']}")
            print(f"Storage path: {stats['storage_path']}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            logger.error("database_initialization_error", error=str(e))
            print(f"\n❌ Error adding papers to database: {e}")
            sys.exit(1)
    
    # Report failures
    if failed:
        print(f"\n⚠️  Failed to process {len(failed)} files:")
        for filename, error in failed:
            print(f"  - {filename}: {error}")
    
    # Success!
    print("\n✅ Vector database initialization complete!")
    
    if papers:
        print("\nYou can now run semantic searches using the Research Agent.")
        print("\nExample test search:")
        print("  >>> from app.services.vector_db import get_vector_db")
        print("  >>> db = get_vector_db()")
        print('  >>> results = db.search("CRISPR gene editing", n_results=3)')
        print("  >>> for r in results: print(f'{r['similarity']:.2f} - {r['metadata']['title']}')")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize vector database with local papers"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database before initializing",
    )
    parser.add_argument(
        "--papers-dir",
        type=Path,
        help="Path to papers directory (default: data/papers)",
    )
    
    args = parser.parse_args()
    
    # Configure logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
    
    try:
        initialize_from_papers(
            papers_dir=args.papers_dir,
            reset=args.reset,
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Initialization cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error("initialization_failed", error=str(e))
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
