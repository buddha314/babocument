"""
Event Bus implementation using Redis Pub/Sub for agent coordination and real-time updates.

This module provides a centralized event bus for:
- Agent task lifecycle events (started, progress, completed, error)
- Real-time updates to connected clients via WebSocket
- Decoupling between API endpoints and WebSocket handlers
"""

import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass, asdict

try:
    import redis.asyncio as redis
except ImportError:
    # Fallback for older redis versions
    import redis
    redis.asyncio = redis  # type: ignore

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Event types for agent task lifecycle."""
    TASK_STARTED = "task_started"
    TASK_PROGRESS = "task_progress"
    TASK_COMPLETED = "task_completed"
    TASK_ERROR = "task_error"
    DOCUMENT_INDEXED = "document_indexed"
    SEARCH_COMPLETED = "search_completed"


@dataclass
class Event:
    """Event data structure."""
    event_type: EventType
    task_id: str
    timestamp: str
    data: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "task_id": self.task_id,
            "timestamp": self.timestamp,
            "data": self.data
        }
    
    def to_json(self) -> str:
        """Convert event to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "Event":
        """Create event from JSON string."""
        data = json.loads(json_str)
        return cls(
            event_type=EventType(data["event_type"]),
            task_id=data["task_id"],
            timestamp=data["timestamp"],
            data=data["data"]
        )


class EventBus:
    """
    Redis-based event bus for pub/sub messaging.
    
    Example usage:
        # Initialize
        event_bus = EventBus(redis_url="redis://localhost:6379")
        await event_bus.connect()
        
        # Publish event
        await event_bus.publish(
            event_type=EventType.TASK_STARTED,
            task_id="task_123",
            data={"agent": "research", "query": "diabetes"}
        )
        
        # Subscribe to events
        async def handle_event(event: Event):
            print(f"Received: {event.event_type} for {event.task_id}")
        
        await event_bus.subscribe("task_events", handle_event)
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize Event Bus.
        
        Args:
            redis_url: Redis connection URL (default: redis://localhost:6379)
        """
        self.redis_url = redis_url
        self.redis_client: Any = None  # Type: redis.Redis
        self.pubsub: Any = None  # Type: redis.client.PubSub
        self._connected = False
        
    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            self._connected = True
            logger.info(f"Event Bus connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()
        self._connected = False
        logger.info("Event Bus disconnected from Redis")
    
    def is_connected(self) -> bool:
        """Check if connected to Redis."""
        return self._connected
    
    async def publish(
        self,
        event_type: EventType,
        task_id: str,
        data: Dict[str, Any],
        channel: str = "task_events"
    ) -> None:
        """
        Publish an event to a channel.
        
        Args:
            event_type: Type of event (from EventType enum)
            task_id: Unique task identifier
            data: Event payload data
            channel: Redis channel name (default: task_events)
        """
        if not self._connected:
            logger.warning("Event Bus not connected. Call connect() first.")
            return
        
        event = Event(
            event_type=event_type,
            task_id=task_id,
            timestamp=datetime.utcnow().isoformat(),
            data=data
        )
        
        try:
            await self.redis_client.publish(channel, event.to_json())
            logger.debug(f"Published {event_type.value} for task {task_id} to {channel}")
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            raise
    
    async def subscribe(
        self,
        channel: str,
        handler: Callable[[Event], Any]
    ) -> None:
        """
        Subscribe to a channel and handle events.
        
        Args:
            channel: Redis channel name
            handler: Async callback function to handle events
        
        Example:
            async def my_handler(event: Event):
                print(f"Got event: {event.event_type}")
            
            await event_bus.subscribe("task_events", my_handler)
        """
        if not self._connected:
            logger.warning("Event Bus not connected. Call connect() first.")
            return
        
        try:
            self.pubsub = self.redis_client.pubsub()
            await self.pubsub.subscribe(channel)
            logger.info(f"Subscribed to channel: {channel}")
            
            # Listen for messages
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        event = Event.from_json(message["data"])
                        await handler(event)
                    except Exception as e:
                        logger.error(f"Error handling event: {e}")
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            raise
    
    async def publish_task_started(
        self,
        task_id: str,
        agent_type: str,
        query: str,
        **kwargs
    ) -> None:
        """
        Convenience method to publish task started event.
        
        Args:
            task_id: Unique task identifier
            agent_type: Type of agent (research, analysis, summary, recommendation)
            query: Task query/prompt
            **kwargs: Additional data
        """
        await self.publish(
            event_type=EventType.TASK_STARTED,
            task_id=task_id,
            data={
                "agent_type": agent_type,
                "query": query,
                "status": "started",
                **kwargs
            }
        )
    
    async def publish_task_progress(
        self,
        task_id: str,
        progress: float,
        message: str,
        **kwargs
    ) -> None:
        """
        Convenience method to publish task progress event.
        
        Args:
            task_id: Unique task identifier
            progress: Progress percentage (0-100)
            message: Progress message
            **kwargs: Additional data
        """
        await self.publish(
            event_type=EventType.TASK_PROGRESS,
            task_id=task_id,
            data={
                "progress": progress,
                "message": message,
                "status": "in_progress",
                **kwargs
            }
        )
    
    async def publish_task_completed(
        self,
        task_id: str,
        result: Any,
        **kwargs
    ) -> None:
        """
        Convenience method to publish task completed event.
        
        Args:
            task_id: Unique task identifier
            result: Task result/output
            **kwargs: Additional data
        """
        await self.publish(
            event_type=EventType.TASK_COMPLETED,
            task_id=task_id,
            data={
                "result": result,
                "status": "completed",
                **kwargs
            }
        )
    
    async def publish_task_error(
        self,
        task_id: str,
        error: str,
        **kwargs
    ) -> None:
        """
        Convenience method to publish task error event.
        
        Args:
            task_id: Unique task identifier
            error: Error message
            **kwargs: Additional data
        """
        await self.publish(
            event_type=EventType.TASK_ERROR,
            task_id=task_id,
            data={
                "error": error,
                "status": "error",
                **kwargs
            }
        )


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Get the global event bus instance.
    
    Returns:
        EventBus: Global event bus instance
    """
    global _event_bus
    if _event_bus is None:
        from app.config import settings
        _event_bus = EventBus(redis_url=settings.redis_url)
    return _event_bus


async def init_event_bus(redis_url: Optional[str] = None) -> EventBus:
    """
    Initialize and connect the global event bus.
    
    Args:
        redis_url: Optional Redis URL override
    
    Returns:
        EventBus: Connected event bus instance
    """
    global _event_bus
    if redis_url:
        _event_bus = EventBus(redis_url=redis_url)
    else:
        _event_bus = get_event_bus()
    
    if not _event_bus.is_connected():
        await _event_bus.connect()
    
    return _event_bus


async def shutdown_event_bus() -> None:
    """Shutdown the global event bus."""
    global _event_bus
    if _event_bus:
        await _event_bus.disconnect()
        _event_bus = None
