"""
Document Management API Endpoints

REST API for document CRUD operations, search, and metadata management.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
import structlog
import uuid
import shutil

from app.services.vector_db import VectorDatabase, get_vector_db
from app.services.llm_client import LLMClient, get_llm_client
from app.config import settings
from app.utils.pdf_processing import extract_text_from_pdf, extract_pdf_metadata, parse_research_paper_metadata

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


# Pydantic Models
class DocumentMetadata(BaseModel):
    """Metadata for a document"""
    id: str
    title: str
    authors: Optional[List[str]] = None
    abstract: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = Field(None, description="Repository source (e.g., 'local', 'pubmed', 'arxiv')")
    created_at: datetime
    updated_at: datetime
    file_path: Optional[str] = None
    indexed: bool = Field(False, description="Whether document is in vector DB")


class DocumentList(BaseModel):
    """Paginated list of documents"""
    documents: List[DocumentMetadata]
    total: int
    limit: int
    offset: int
    has_next: bool


class DocumentContent(BaseModel):
    """Full document content"""
    metadata: DocumentMetadata
    content: str
    sections: Optional[List[dict]] = Field(None, description="Parsed sections if available")


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    id: str
    status: str
    message: str
    processing_task_id: Optional[str] = None


class SearchQuery(BaseModel):
    """Search query parameters"""
    query: str
    limit: int = Field(10, ge=1, le=100)
    search_type: str = Field("semantic", description="'semantic' or 'keyword'")
    filters: Optional[dict] = Field(None, description="Metadata filters (year, author, etc.)")


class SearchResult(BaseModel):
    """Search result with relevance score"""
    document: DocumentMetadata
    score: float
    highlights: Optional[List[str]] = None


class SearchResults(BaseModel):
    """Search results response"""
    results: List[SearchResult]
    query: str
    search_type: str
    total: int
    execution_time_ms: float


class DocumentSummary(BaseModel):
    """AI-generated document summary"""
    document_id: str
    summary: str
    key_points: List[str]
    generated_at: datetime


# Endpoints

@router.get("", response_model=DocumentList)
async def list_documents(
    limit: int = Query(20, ge=1, le=100, description="Number of documents per page"),
    offset: int = Query(0, ge=0, description="Number of documents to skip"),
    source: Optional[str] = Query(None, description="Filter by source"),
    year: Optional[int] = Query(None, description="Filter by year"),
    indexed_only: bool = Query(False, description="Only show indexed documents"),
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    List all documents with pagination and filtering.
    
    Returns metadata for documents in the system with optional filters.
    """
    logger.info("list_documents", limit=limit, offset=offset, source=source, year=year)
    
    try:
        # Build filters
        filters = {}
        if source:
            filters["source"] = source
        if year:
            filters["year"] = year
        
        # Get papers from vector DB
        papers, total = vector_db.get_all_papers(
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
        
        # Convert to API response format
        documents = []
        for paper in papers:
            metadata = paper.get("metadata", {})
            doc = DocumentMetadata(
                id=paper["id"],
                title=metadata.get("title", "Untitled"),
                authors=metadata.get("authors", "").split(", ") if metadata.get("authors") else None,
                abstract=None,
                year=metadata.get("year"),
                journal=None,
                doi=metadata.get("doi"),
                url=None,
                source=metadata.get("source", "unknown"),
                created_at=datetime.now(),  # TODO: Store creation time in metadata
                updated_at=datetime.now(),
                file_path=metadata.get("file_path"),
                indexed=True
            )
            documents.append(doc)
        
        return DocumentList(
            documents=documents,
            total=total,
            limit=limit,
            offset=offset,
            has_next=(offset + limit) < total
        )
    except Exception as e:
        logger.error("list_documents_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")


@router.get("/{document_id}", response_model=DocumentMetadata)
async def get_document(
    document_id: str,
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Get document metadata by ID.
    
    Returns detailed metadata for a specific document.
    """
    logger.info("get_document", document_id=document_id)
    
    try:
        paper = vector_db.get_paper(document_id)
        
        if not paper:
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        metadata = paper.get("metadata", {})
        return DocumentMetadata(
            id=paper["id"],
            title=metadata.get("title", "Untitled"),
            authors=metadata.get("authors", "").split(", ") if metadata.get("authors") else None,
            abstract=None,
            year=metadata.get("year"),
            journal=None,
            doi=metadata.get("doi"),
            url=None,
            source=metadata.get("source", "unknown"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            file_path=metadata.get("file_path"),
            indexed=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_document_error", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get document: {str(e)}")


@router.get("/{document_id}/content", response_model=DocumentContent)
async def get_document_content(
    document_id: str,
    vector_db: VectorDatabase = Depends(get_vector_db),
    llm_client: LLMClient = Depends(get_llm_client)
):
    """
    Get full document content including text.
    
    Returns complete document with metadata and full text content.
    """
    logger.info("get_document_content", document_id=document_id)
    
    try:
        paper = vector_db.get_paper(document_id)
        
        if not paper:
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        metadata = paper.get("metadata", {})
        doc_metadata = DocumentMetadata(
            id=paper["id"],
            title=metadata.get("title", "Untitled"),
            authors=metadata.get("authors", "").split(", ") if metadata.get("authors") else None,
            abstract=None,
            year=metadata.get("year"),
            journal=None,
            doi=metadata.get("doi"),
            url=None,
            source=metadata.get("source", "unknown"),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            file_path=metadata.get("file_path"),
            indexed=True
        )
        
        return DocumentContent(
            metadata=doc_metadata,
            content=paper.get("document", ""),
            sections=None  # TODO: Parse document structure
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_document_content_error", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get document content: {str(e)}")


@router.post("", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = None,
    authors: Optional[str] = None,
    year: Optional[int] = None,
    source: str = "upload",
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Upload a new document to the system.
    
    Accepts PDF files and schedules background processing for text extraction
    and embedding generation.
    """
    logger.info("upload_document", filename=file.filename, content_type=file.content_type)
    
    # Validate file type
    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Create storage directory
        storage_path = Path(settings.document_storage_path)
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Save file to disk
        file_path = storage_path / f"{document_id}.pdf"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        logger.info("pdf_saved", document_id=document_id, path=str(file_path))
        
        # Extract text and metadata from PDF
        try:
            pdf_text = extract_text_from_pdf(file_path)
            pdf_metadata = extract_pdf_metadata(file_path)
            parsed_metadata = parse_research_paper_metadata(pdf_text, pdf_metadata)
            
            # Use provided metadata or fall back to extracted
            final_title = title or parsed_metadata.get("title") or file.filename
            final_authors = authors.split(",") if authors else parsed_metadata.get("authors", [])
            final_year = year or parsed_metadata.get("year")
            
            # Prepare paper data for vector DB
            paper_data = {
                "id": document_id,
                "title": final_title,
                "abstract": parsed_metadata.get("abstract", ""),
                "full_text": pdf_text,
                "authors": final_authors,
                "year": final_year,
                "source": source,
                "file_path": str(file_path),
            }
            
            # Add to vector database
            vector_db.add_papers([paper_data])
            
            logger.info("document_indexed", document_id=document_id, title=final_title)
            
            return DocumentUploadResponse(
                id=document_id,
                status="completed",
                message="Document uploaded and indexed successfully",
                processing_task_id=None
            )
            
        except Exception as e:
            logger.error("pdf_processing_error", document_id=document_id, error=str(e))
            # Clean up file if processing failed
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process PDF: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("upload_document_error", filename=file.filename, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Delete a document from the system.
    
    Removes document metadata, files, and embeddings.
    """
    logger.info("delete_document", document_id=document_id)
    
    try:
        # Get paper info to find file path
        paper = vector_db.get_paper(document_id)
        
        if not paper:
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        # Delete file from disk if it exists
        metadata = paper.get("metadata", {})
        file_path_str = metadata.get("file_path")
        if file_path_str:
            file_path = Path(file_path_str)
            if file_path.exists():
                file_path.unlink()
                logger.info("document_file_deleted", path=str(file_path))
        
        # Remove from vector DB
        vector_db.delete_paper(document_id)
        
        logger.info("document_deleted", document_id=document_id)
        
        return {
            "status": "success",
            "message": f"Document {document_id} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("delete_document_error", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")


@router.post("/search", response_model=SearchResults)
async def search_documents(
    query: SearchQuery,
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Search documents using keyword or semantic search.
    
    Supports two search types:
    - 'semantic': Vector similarity search using embeddings
    - 'keyword': Traditional text matching
    """
    logger.info("search_documents", query=query.query, search_type=query.search_type)
    
    import time
    start_time = time.time()
    
    try:
        if query.search_type == "semantic":
            # Perform semantic search using vector DB
            raw_results = vector_db.search(
                query=query.query,
                n_results=query.limit,
                filters=query.filters
            )
            
            # Convert to API response format
            results = []
            for result in raw_results:
                metadata = result.get("metadata", {})
                document = DocumentMetadata(
                    id=result["id"],
                    title=metadata.get("title", "Untitled"),
                    authors=metadata.get("authors", "").split(", ") if metadata.get("authors") else None,
                    abstract=None,  # Not stored in metadata
                    year=metadata.get("year"),
                    journal=None,
                    doi=metadata.get("doi"),
                    url=None,
                    source=metadata.get("source", "unknown"),
                    created_at=datetime.now(),  # TODO: Store in metadata
                    updated_at=datetime.now(),
                    file_path=metadata.get("file_path"),
                    indexed=True
                )
                
                search_result = SearchResult(
                    document=document,
                    score=result["similarity"],
                    highlights=None  # TODO: Add text highlighting
                )
                results.append(search_result)
        else:
            # TODO: Implement keyword search
            logger.warning("keyword_search_not_implemented")
            results = []
        
        execution_time = (time.time() - start_time) * 1000
        
        return SearchResults(
            results=results,
            query=query.query,
            search_type=query.search_type,
            total=len(results),
            execution_time_ms=execution_time
        )
    except Exception as e:
        logger.error("search_documents_error", query=query.query, error=str(e))
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/{document_id}/summary", response_model=DocumentSummary)
async def generate_document_summary(
    document_id: str,
    max_length: int = Query(500, ge=100, le=2000, description="Maximum summary length in words"),
    vector_db: VectorDatabase = Depends(get_vector_db),
    llm_client: LLMClient = Depends(get_llm_client)
):
    """
    Generate an AI summary of a document.
    
    Uses LLM to create a concise summary and extract key points.
    """
    logger.info("generate_summary", document_id=document_id, max_length=max_length)
    
    try:
        # Get document content
        paper = vector_db.get_paper(document_id)
        
        if not paper:
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        content = paper.get("document", "")
        if not content:
            raise HTTPException(status_code=400, detail="Document has no content to summarize")
        
        # Truncate content if too long (avoid token limits)
        max_chars = max_length * 10  # Rough estimate
        if len(content) > max_chars:
            content = content[:max_chars]
        
        # Generate summary using LLM
        summary_prompt = f"""Please provide a concise summary of the following research paper in approximately {max_length} words.
Also extract 3-5 key points as bullet points.

Paper content:
{content}

Format your response as:
SUMMARY: [your summary here]

KEY POINTS:
- [point 1]
- [point 2]
- [point 3]
"""
        
        try:
            response = llm_client.generate(
                prompt=summary_prompt,
                max_tokens=max_length * 2,  # Allow extra tokens for key points
                temperature=0.3  # Lower temperature for more focused summaries
            )
            
            # Parse response
            response_text = response.get("text", "")
            
            # Extract summary and key points
            summary = ""
            key_points = []
            
            if "SUMMARY:" in response_text and "KEY POINTS:" in response_text:
                parts = response_text.split("KEY POINTS:")
                summary = parts[0].replace("SUMMARY:", "").strip()
                
                # Parse key points
                key_points_text = parts[1].strip()
                for line in key_points_text.split("\n"):
                    line = line.strip()
                    if line.startswith("-") or line.startswith("•"):
                        key_points.append(line.lstrip("-•").strip())
            else:
                summary = response_text
            
            return DocumentSummary(
                document_id=document_id,
                summary=summary,
                key_points=key_points,
                generated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error("llm_generation_error", error=str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate summary: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("generate_summary_error", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")
