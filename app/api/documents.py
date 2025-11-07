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
from app.utils.event_bus import get_event_bus, EventType

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
            
            # Parse timestamps
            created_at = datetime.now()
            updated_at = datetime.now()
            if metadata.get("created_at"):
                try:
                    created_at = datetime.fromisoformat(metadata["created_at"])
                except:
                    pass
            if metadata.get("updated_at"):
                try:
                    updated_at = datetime.fromisoformat(metadata["updated_at"])
                except:
                    pass
            
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
                created_at=created_at,
                updated_at=updated_at,
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
        
        # Parse timestamps
        created_at = datetime.now()
        updated_at = datetime.now()
        if metadata.get("created_at"):
            try:
                created_at = datetime.fromisoformat(metadata["created_at"])
            except:
                pass
        if metadata.get("updated_at"):
            try:
                updated_at = datetime.fromisoformat(metadata["updated_at"])
            except:
                pass
        
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
            created_at=created_at,
            updated_at=updated_at,
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
        
        # Parse timestamps
        created_at = datetime.now()
        updated_at = datetime.now()
        if metadata.get("created_at"):
            try:
                created_at = datetime.fromisoformat(metadata["created_at"])
            except:
                pass
        if metadata.get("updated_at"):
            try:
                updated_at = datetime.fromisoformat(metadata["updated_at"])
            except:
                pass
        
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
            created_at=created_at,
            updated_at=updated_at,
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
            now = datetime.now().isoformat()
            paper_data = {
                "id": document_id,
                "title": final_title,
                "abstract": parsed_metadata.get("abstract", ""),
                "full_text": pdf_text,
                "authors": final_authors,
                "year": final_year,
                "source": source,
                "file_path": str(file_path),
                "created_at": now,
                "updated_at": now,
            }
            
            # Add to vector database
            vector_db.add_papers([paper_data])
            
            logger.info("document_indexed", document_id=document_id, title=final_title)
            
            # Publish event
            try:
                event_bus = get_event_bus()
                if event_bus.is_connected():
                    await event_bus.publish(
                        event_type=EventType.DOCUMENT_INDEXED,
                        task_id=document_id,
                        data={
                            "document_id": document_id,
                            "title": final_title,
                            "authors": final_authors,
                            "year": final_year,
                            "source": source,
                        }
                    )
            except Exception as e:
                logger.warning("event_publish_failed", error=str(e))
            
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
                filters=query.filters,
                search_type="semantic"
            )
        elif query.search_type == "keyword":
            # Perform keyword search using vector DB
            raw_results = vector_db.search(
                query=query.query,
                n_results=query.limit,
                filters=query.filters,
                search_type="keyword"
            )
        else:
            logger.warning("unknown_search_type", search_type=query.search_type)
            raw_results = []
        
        # Convert to API response format
        results = []
        for result in raw_results:
            metadata = result.get("metadata", {})
            
            # Parse timestamps
            created_at = datetime.now()
            updated_at = datetime.now()
            if metadata.get("created_at"):
                try:
                    created_at = datetime.fromisoformat(metadata["created_at"])
                except:
                    pass
            if metadata.get("updated_at"):
                try:
                    updated_at = datetime.fromisoformat(metadata["updated_at"])
                except:
                    pass
            
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
                created_at=created_at,
                updated_at=updated_at,
                file_path=metadata.get("file_path"),
                indexed=True
            )
            
            search_result = SearchResult(
                document=document,
                score=result["similarity"],
                highlights=None  # TODO: Add text highlighting
            )
            results.append(search_result)
        
        execution_time = (time.time() - start_time) * 1000
        
        # Publish search event
        try:
            event_bus = get_event_bus()
            if event_bus.is_connected():
                search_id = str(uuid.uuid4())
                await event_bus.publish(
                    event_type=EventType.SEARCH_COMPLETED,
                    task_id=search_id,
                    data={
                        "query": query.query,
                        "search_type": query.search_type,
                        "results_count": len(results),
                        "execution_time_ms": execution_time,
                    }
                )
        except Exception as e:
            logger.warning("event_publish_failed", error=str(e))
        
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
        try:
            response = await llm_client.summarize(
                text=content,
                max_length=max_length,
                style="detailed"
            )
            
            if not response:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate summary - LLM returned no response"
                )
            
            # Parse response for key points (simple extraction)
            key_points = []
            lines = response.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("-") or line.startswith("•") or line.startswith("*"):
                    key_points.append(line.lstrip("-•*").strip())
            
            # If no bullet points found, use first 3 sentences as key points
            if not key_points:
                sentences = response.split(".")[:3]
                key_points = [s.strip() + "." for s in sentences if s.strip()]
            
            return DocumentSummary(
                document_id=document_id,
                summary=response,
                key_points=key_points[:5],  # Limit to 5 key points
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
