"""
Repository Management API Endpoints

REST API for managing external data sources (MCP servers) and repository operations.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import structlog

from app.services.vector_db import VectorDatabase, get_vector_db

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/repositories", tags=["repositories"])


# Pydantic Models
class RepositoryInfo(BaseModel):
    """Information about a repository/data source"""
    id: str
    name: str
    type: str = Field(..., description="Repository type: 'pubmed', 'arxiv', 'biorxiv', 'local', etc.")
    status: str = Field(..., description="'connected', 'disconnected', 'error', 'syncing'")
    url: Optional[str] = None
    description: Optional[str] = None
    document_count: int = Field(0, description="Number of documents from this repository")
    last_sync: Optional[datetime] = None
    last_error: Optional[str] = None
    config: Optional[dict] = Field(None, description="Repository-specific configuration")


class RepositoryList(BaseModel):
    """List of configured repositories"""
    repositories: List[RepositoryInfo]
    total: int


class RepositoryStatus(BaseModel):
    """Detailed repository status"""
    repository: RepositoryInfo
    connection_status: str
    available_documents: Optional[int] = None
    indexed_documents: int
    last_check: datetime
    health: dict = Field(default_factory=dict, description="Health check details")


class SyncRequest(BaseModel):
    """Request to sync a repository"""
    repository_id: Optional[str] = Field(None, description="Specific repository to sync, or all if None")
    full_sync: bool = Field(False, description="Full re-sync vs incremental")
    filters: Optional[dict] = Field(None, description="Filters for selective sync (date range, keywords, etc.)")


class SyncResponse(BaseModel):
    """Response after initiating sync"""
    task_id: str
    status: str
    message: str
    repositories: List[str]
    started_at: datetime


class RepositoryDocuments(BaseModel):
    """Documents from a specific repository"""
    repository_id: str
    documents: List[dict]  # Using dict for now, should reference DocumentMetadata
    total: int
    limit: int
    offset: int


# Endpoints

@router.get("", response_model=RepositoryList)
async def list_repositories(
    status: Optional[str] = Query(None, description="Filter by status"),
    type: Optional[str] = Query(None, description="Filter by repository type"),
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    List all configured repositories (MCP servers and local sources).
    
    Returns information about all data sources configured in the system.
    """
    logger.info("list_repositories", status=status, type=type)
    
    try:
        # Get vector DB stats for local repository
        db_stats = vector_db.get_stats()
        total_papers = db_stats.get("total_papers", 0)
        
        # Create local repository entry
        local_repo = RepositoryInfo(
            id="local",
            name="Local Documents",
            type="local",
            status="connected",
            description="Locally uploaded and managed documents",
            document_count=total_papers,
            last_sync=None,
            config={"storage_path": db_stats.get("storage_path")}
        )
        
        repositories = [local_repo]
        
        # Apply filters
        if type and type != "local":
            repositories = []
        if status and status != "connected":
            repositories = []
        
        # TODO: Add MCP repositories when Phase 2 is implemented
        # - BioMCP (PubMed, ClinicalTrials)
        # - arXiv MCP
        # - bioRxiv/medRxiv MCP
        
        return RepositoryList(
            repositories=repositories,
            total=len(repositories)
        )
    except Exception as e:
        logger.error("list_repositories_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to list repositories: {str(e)}")


@router.get("/{repository_id}/status", response_model=RepositoryStatus)
async def get_repository_status(
    repository_id: str,
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Get detailed status for a specific repository.
    
    Checks connection health, document counts, and last sync information.
    """
    logger.info("get_repository_status", repository_id=repository_id)
    
    try:
        if repository_id == "local":
            # Get local repository status
            db_stats = vector_db.get_stats()
            total_papers = db_stats.get("total_papers", 0)
            
            repo_info = RepositoryInfo(
                id="local",
                name="Local Documents",
                type="local",
                status="connected",
                description="Locally uploaded and managed documents",
                document_count=total_papers,
                last_sync=None,
                config={"storage_path": db_stats.get("storage_path")}
            )
            
            return RepositoryStatus(
                repository=repo_info,
                connection_status="healthy",
                available_documents=None,  # Not applicable for local
                indexed_documents=total_papers,
                last_check=datetime.now(),
                health={
                    "vector_db": "connected",
                    "embedding_model": db_stats.get("embedding_model"),
                    "storage_accessible": True
                }
            )
        else:
            # TODO: Check MCP server repositories (Phase 2)
            raise HTTPException(status_code=404, detail=f"Repository {repository_id} not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_repository_status_error", repository_id=repository_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get repository status: {str(e)}")


@router.post("/sync", response_model=SyncResponse)
async def sync_repositories(request: SyncRequest):
    """
    Trigger synchronization of repositories.
    
    Initiates background task to fetch new/updated documents from repositories
    and index them in the vector database.
    """
    logger.info("sync_repositories", repository_id=request.repository_id, full_sync=request.full_sync)
    
    try:
        # TODO: Implement sync
        # 1. Identify repositories to sync
        # 2. Create background task
        # 3. For each repository:
        #    - Query for new/updated documents
        #    - Download and process
        #    - Add to vector DB
        # 4. Return task ID for status tracking
        
        return SyncResponse(
            task_id="temp_task_id",
            status="queued",
            message="Sync task queued",
            repositories=[request.repository_id] if request.repository_id else [],
            started_at=datetime.now()
        )
    except Exception as e:
        logger.error("sync_repositories_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to start sync: {str(e)}")


@router.get("/{repository_id}/documents", response_model=RepositoryDocuments)
async def list_repository_documents(
    repository_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    List documents from a specific repository.
    
    Returns documents that originated from the specified repository.
    """
    logger.info("list_repository_documents", repository_id=repository_id, limit=limit, offset=offset)
    
    try:
        # Query vector DB for documents from this repository
        # Use source filter to match repository_id
        filters = {"source": repository_id} if repository_id != "all" else None
        
        papers, total = vector_db.get_all_papers(
            limit=limit,
            offset=offset,
            filters=filters
        )
        
        # Convert to dict format
        documents = []
        for paper in papers:
            metadata = paper.get("metadata", {})
            documents.append({
                "id": paper["id"],
                "title": metadata.get("title", "Untitled"),
                "authors": metadata.get("authors"),
                "year": metadata.get("year"),
                "source": metadata.get("source", "unknown")
            })
        
        return RepositoryDocuments(
            repository_id=repository_id,
            documents=documents,
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error("list_repository_documents_error", repository_id=repository_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to list repository documents: {str(e)}")


@router.post("/{repository_id}/test", response_model=dict)
async def test_repository_connection(
    repository_id: str,
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Test connection to a repository.
    
    Verifies that the repository is accessible and properly configured.
    """
    logger.info("test_repository_connection", repository_id=repository_id)
    
    try:
        if repository_id == "local":
            # Test local repository
            try:
                db_stats = vector_db.get_stats()
                return {
                    "repository_id": repository_id,
                    "status": "connected",
                    "message": f"Local repository is healthy with {db_stats.get('total_papers', 0)} documents",
                    "timestamp": datetime.now().isoformat(),
                    "details": db_stats
                }
            except Exception as e:
                return {
                    "repository_id": repository_id,
                    "status": "error",
                    "message": f"Failed to connect to local repository: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # TODO: Test MCP server connections (Phase 2)
            # For now, return not implemented for MCP repositories
            return {
                "repository_id": repository_id,
                "status": "not_configured",
                "message": "MCP repository testing will be implemented in Phase 2",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error("test_repository_connection_error", repository_id=repository_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")
