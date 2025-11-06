"""
Statistics and Status API Endpoints

REST API for system statistics, metrics, and processing status.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import structlog
import time
from pathlib import Path

from app.services.vector_db import VectorDatabase, get_vector_db
from app.config import settings

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["stats"])

# Track server start time for uptime calculation
_server_start_time = time.time()


# Pydantic Models
class SystemStats(BaseModel):
    """System-wide statistics"""
    total_documents: int = Field(0, description="Total documents in system")
    indexed_documents: int = Field(0, description="Documents with embeddings")
    repositories_count: int = Field(0, description="Configured repositories")
    total_embeddings: int = Field(0, description="Total embedding vectors")
    storage_used_mb: float = Field(0.0, description="Storage used in MB")
    last_updated: datetime
    uptime_seconds: float = Field(0.0, description="Server uptime in seconds")


class RepositoryStats(BaseModel):
    """Statistics per repository"""
    repository_id: str
    repository_name: str
    document_count: int
    indexed_count: int
    last_sync: Optional[datetime] = None
    avg_document_size_kb: float = 0.0


class DocumentStats(BaseModel):
    """Document-level statistics"""
    by_year: dict = Field(default_factory=dict, description="Document count by year")
    by_source: dict = Field(default_factory=dict, description="Document count by source")
    by_type: dict = Field(default_factory=dict, description="Document count by type")
    top_authors: List[dict] = Field(default_factory=list, description="Most frequent authors")
    top_journals: List[dict] = Field(default_factory=list, description="Most frequent journals")


class ProcessingTask(BaseModel):
    """Background processing task status"""
    task_id: str
    type: str = Field(..., description="Task type: 'upload', 'sync', 'embedding', etc.")
    status: str = Field(..., description="'pending', 'running', 'completed', 'failed'")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Progress percentage")
    message: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: dict = Field(default_factory=dict, description="Task-specific metadata")


class ProcessingStatus(BaseModel):
    """Processing queue status"""
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    tasks: List[ProcessingTask]


class AgentStats(BaseModel):
    """Agent performance statistics"""
    agent_name: str
    agent_type: str
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    avg_execution_time_ms: float
    last_active: Optional[datetime] = None


class AllStats(BaseModel):
    """Comprehensive system statistics"""
    system: SystemStats
    repositories: List[RepositoryStats]
    documents: DocumentStats
    agents: List[AgentStats]


# Endpoints

@router.get("/stats", response_model=SystemStats)
async def get_system_stats(
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Get high-level system statistics.
    
    Returns document counts, storage usage, and basic system metrics.
    """
    logger.info("get_system_stats")
    
    try:
        # Get vector DB stats
        db_stats = vector_db.get_stats()
        total_documents = db_stats.get("total_papers", 0)
        
        # Calculate storage usage
        storage_used_mb = 0.0
        storage_path = Path(settings.document_storage_path)
        if storage_path.exists():
            storage_used_mb = sum(
                f.stat().st_size for f in storage_path.rglob("*") if f.is_file()
            ) / (1024 * 1024)
        
        # Calculate server uptime
        uptime_seconds = time.time() - _server_start_time
        
        return SystemStats(
            total_documents=total_documents,
            indexed_documents=total_documents,  # All documents in ChromaDB are indexed
            repositories_count=1,  # Currently just "local" repository
            total_embeddings=total_documents,
            storage_used_mb=round(storage_used_mb, 2),
            last_updated=datetime.now(),
            uptime_seconds=round(uptime_seconds, 2)
        )
    except Exception as e:
        logger.error("get_system_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get system stats: {str(e)}")


@router.get("/stats/all", response_model=AllStats)
async def get_all_stats(
    vector_db: VectorDatabase = Depends(get_vector_db)
):
    """
    Get comprehensive statistics for all system components.
    
    Returns detailed metrics for documents, repositories, and agents.
    """
    logger.info("get_all_stats")
    
    try:
        # Get system stats
        db_stats = vector_db.get_stats()
        total_documents = db_stats.get("total_papers", 0)
        
        storage_used_mb = 0.0
        storage_path = Path(settings.document_storage_path)
        if storage_path.exists():
            storage_used_mb = sum(
                f.stat().st_size for f in storage_path.rglob("*") if f.is_file()
            ) / (1024 * 1024)
        
        uptime_seconds = time.time() - _server_start_time
        
        system_stats = SystemStats(
            total_documents=total_documents,
            indexed_documents=total_documents,
            repositories_count=1,
            total_embeddings=total_documents,
            storage_used_mb=round(storage_used_mb, 2),
            last_updated=datetime.now(),
            uptime_seconds=round(uptime_seconds, 2)
        )
        
        # Get all papers and calculate document stats
        papers, _ = vector_db.get_all_papers(limit=1000)
        
        doc_stats = DocumentStats()
        by_year = {}
        by_source = {}
        author_counts = {}
        
        for paper in papers:
            metadata = paper.get("metadata", {})
            
            # Count by year
            year = metadata.get("year")
            if year:
                by_year[str(year)] = by_year.get(str(year), 0) + 1
            
            # Count by source
            source = metadata.get("source", "unknown")
            by_source[source] = by_source.get(source, 0) + 1
            
            # Count authors
            authors = metadata.get("authors", "")
            if authors:
                for author in authors.split(", "):
                    author = author.strip()
                    if author:
                        author_counts[author] = author_counts.get(author, 0) + 1
        
        doc_stats.by_year = by_year
        doc_stats.by_source = by_source
        
        # Get top 10 authors
        top_authors = sorted(
            [{"name": k, "count": v} for k, v in author_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]
        doc_stats.top_authors = top_authors
        
        # Repository stats (currently just local)
        repo_stats = [
            RepositoryStats(
                repository_id="local",
                repository_name="Local Documents",
                document_count=total_documents,
                indexed_count=total_documents,
                last_sync=None,
                avg_document_size_kb=storage_used_mb * 1024 / total_documents if total_documents > 0 else 0
            )
        ]
        
        return AllStats(
            system=system_stats,
            repositories=repo_stats,
            documents=doc_stats,
            agents=[]  # Agent stats will be populated when agents are active
        )
    except Exception as e:
        logger.error("get_all_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get all stats: {str(e)}")


@router.get("/status/processing", response_model=ProcessingStatus)
async def get_processing_status(
    limit: int = 20,
    status: Optional[str] = None
):
    """
    Get status of background processing tasks.
    
    Returns information about upload processing, sync tasks, and embedding generation.
    """
    logger.info("get_processing_status", limit=limit, status=status)
    
    try:
        # TODO: Implement task tracking
        # Query task queue or database for task status
        
        return ProcessingStatus(
            pending_tasks=0,
            running_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            tasks=[]
        )
    except Exception as e:
        logger.error("get_processing_status_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get processing status: {str(e)}")


@router.get("/status/processing/{task_id}", response_model=ProcessingTask)
async def get_task_status(task_id: str):
    """
    Get status of a specific processing task.
    
    Returns detailed information about a background task.
    """
    logger.info("get_task_status", task_id=task_id)
    
    try:
        # TODO: Implement task lookup
        # Query task database for specific task
        
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_task_status_error", task_id=task_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")


@router.get("/stats/agents", response_model=List[AgentStats])
async def get_agent_stats():
    """
    Get performance statistics for all agents.
    
    Returns metrics about agent task execution and success rates.
    """
    logger.info("get_agent_stats")
    
    try:
        # TODO: Implement agent stats collection
        # Query agent coordinator for performance metrics
        
        return []
    except Exception as e:
        logger.error("get_agent_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get agent stats: {str(e)}")
