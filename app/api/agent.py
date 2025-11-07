"""
Agent Chat API Endpoints

REST API for conversational AI agent interaction.
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import structlog
import uuid

from app.agents.coordinator import AgentCoordinator
from app.services.vector_db import VectorDatabase, get_vector_db
from app.services.llm_client import LLMClient, get_llm_client

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


# Pydantic Models
class ChatSource(BaseModel):
    """Source citation from agent"""
    title: str
    url: Optional[str] = None
    relevance: Optional[float] = None


class ChatRequest(BaseModel):
    """Request to chat with agent"""
    message: str
    conversation_id: Optional[str] = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    """Response from agent"""
    message: str
    conversation_id: str
    sources: Optional[List[ChatSource]] = None
    metadata: Optional[dict] = None


# Endpoints

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    vector_db: VectorDatabase = Depends(get_vector_db),
    llm_client: LLMClient = Depends(get_llm_client)
):
    """
    Send message to AI agent and receive response.
    
    Uses the AgentCoordinator to handle conversational requests
    with context-aware responses, document search, and citations.
    """
    logger.info("agent_chat_request", 
                message=request.message[:100],
                conversation_id=request.conversation_id)
    
    try:
        # Initialize coordinator
        coordinator = AgentCoordinator(
            event_bus=None,
            vector_db=vector_db,
            llm_client=llm_client
        )
        
        # Handle conversation through coordinator
        context = request.context or {}
        result = await coordinator.handle_conversation(
            message=request.message,
            context=context
        )
        
        # Generate or retrieve conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Format response
        response = ChatResponse(
            message=result.get("response", "I apologize, I couldn''t process that request."),
            conversation_id=conversation_id,
            sources=[
                ChatSource(
                    title=src.get("title", ""),
                    url=src.get("url"),
                    relevance=src.get("relevance")
                )
                for src in result.get("sources", [])
            ],
            metadata=result.get("metadata")
        )
        
        logger.info("agent_chat_response", 
                    conversation_id=conversation_id,
                    response_length=len(response.message))
        
        return response
        
    except Exception as e:
        logger.error("agent_chat_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history (to be implemented with persistence).
    """
    # TODO: Implement conversation storage and retrieval
    raise HTTPException(
        status_code=501,
        detail="Conversation history not yet implemented"
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete conversation (to be implemented with persistence).
    """
    # TODO: Implement conversation deletion
    raise HTTPException(
        status_code=501,
        detail="Conversation deletion not yet implemented"
    )
