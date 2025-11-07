"""
Tests for Event Bus (Redis Pub/Sub).

Tests event publishing, subscribing, and event types.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.utils.event_bus import (
    EventBus,
    Event,
    EventType,
    get_event_bus,
    init_event_bus,
    shutdown_event_bus,
)


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch("app.utils.event_bus.redis") as mock:
        # Create async mock for Redis client
        redis_client = AsyncMock()
        redis_client.ping = AsyncMock(return_value=True)
        redis_client.publish = AsyncMock(return_value=1)
        redis_client.close = AsyncMock()
        
        # Mock pubsub
        pubsub_mock = AsyncMock()
        pubsub_mock.subscribe = AsyncMock()
        pubsub_mock.unsubscribe = AsyncMock()
        pubsub_mock.close = AsyncMock()
        
        async def mock_listen():
            # Yield a test message
            yield {"type": "message", "data": '{"event_type": "task_started", "task_id": "test_123", "timestamp": "2025-11-06T12:00:00", "data": {"agent_type": "research", "query": "test"}}'}
        
        pubsub_mock.listen = mock_listen
        redis_client.pubsub = MagicMock(return_value=pubsub_mock)
        
        mock.from_url = AsyncMock(return_value=redis_client)
        yield mock


@pytest.mark.asyncio
async def test_event_creation():
    """Test Event dataclass creation and serialization."""
    event = Event(
        event_type=EventType.TASK_STARTED,
        task_id="task_123",
        timestamp="2025-11-06T12:00:00",
        data={"agent_type": "research", "query": "diabetes"}
    )
    
    # Test to_dict
    event_dict = event.to_dict()
    assert event_dict["event_type"] == "task_started"
    assert event_dict["task_id"] == "task_123"
    assert event_dict["data"]["agent_type"] == "research"
    
    # Test to_json
    json_str = event.to_json()
    assert "task_started" in json_str
    assert "task_123" in json_str
    
    # Test from_json
    reconstructed = Event.from_json(json_str)
    assert reconstructed.event_type == EventType.TASK_STARTED
    assert reconstructed.task_id == "task_123"
    assert reconstructed.data["agent_type"] == "research"


@pytest.mark.asyncio
async def test_event_bus_connect(mock_redis):
    """Test Event Bus connection."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    
    assert not event_bus.is_connected()
    
    await event_bus.connect()
    
    assert event_bus.is_connected()
    mock_redis.from_url.assert_called_once()


@pytest.mark.asyncio
async def test_event_bus_disconnect(mock_redis):
    """Test Event Bus disconnection."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    await event_bus.connect()
    
    assert event_bus.is_connected()
    
    await event_bus.disconnect()
    
    assert not event_bus.is_connected()


@pytest.mark.asyncio
async def test_publish_event(mock_redis):
    """Test publishing events."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    await event_bus.connect()
    
    await event_bus.publish(
        event_type=EventType.TASK_STARTED,
        task_id="task_123",
        data={"agent_type": "research", "query": "diabetes"}
    )
    
    # Verify publish was called
    redis_client = mock_redis.from_url.return_value
    redis_client.publish.assert_called_once()
    
    # Check the channel and message
    call_args = redis_client.publish.call_args
    assert call_args[0][0] == "task_events"  # Default channel
    assert "task_123" in call_args[0][1]


@pytest.mark.asyncio
async def test_publish_without_connection():
    """Test publishing without connection (should log warning)."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    
    # Should not raise error, just log warning
    await event_bus.publish(
        event_type=EventType.TASK_STARTED,
        task_id="task_123",
        data={"test": "data"}
    )


@pytest.mark.asyncio
async def test_convenience_methods(mock_redis):
    """Test convenience methods for task lifecycle events."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    await event_bus.connect()
    
    redis_client = mock_redis.from_url.return_value
    
    # Test task_started
    await event_bus.publish_task_started(
        task_id="task_1",
        agent_type="research",
        query="test query"
    )
    assert redis_client.publish.call_count == 1
    
    # Test task_progress
    await event_bus.publish_task_progress(
        task_id="task_1",
        progress=50.0,
        message="Halfway done"
    )
    assert redis_client.publish.call_count == 2
    
    # Test task_completed
    await event_bus.publish_task_completed(
        task_id="task_1",
        result={"findings": "test results"}
    )
    assert redis_client.publish.call_count == 3
    
    # Test task_error
    await event_bus.publish_task_error(
        task_id="task_1",
        error="Something went wrong"
    )
    assert redis_client.publish.call_count == 4


@pytest.mark.asyncio
async def test_subscribe_and_handle(mock_redis):
    """Test subscribing to events and handling them."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    await event_bus.connect()
    
    received_events = []
    
    async def test_handler(event: Event):
        received_events.append(event)
    
    # Subscribe (will receive one test message from mock)
    subscribe_task = asyncio.create_task(
        event_bus.subscribe("task_events", test_handler)
    )
    
    # Give it time to process
    await asyncio.sleep(0.1)
    
    # Cancel subscription
    subscribe_task.cancel()
    try:
        await subscribe_task
    except asyncio.CancelledError:
        pass
    
    # Verify handler was called with the mock message
    assert len(received_events) > 0
    assert received_events[0].task_id == "test_123"
    assert received_events[0].event_type == EventType.TASK_STARTED


@pytest.mark.asyncio
async def test_global_event_bus():
    """Test global event bus singleton."""
    with patch("app.utils.event_bus.redis"):
        # Reset global
        import app.utils.event_bus as eb
        eb._event_bus = None
        
        bus1 = get_event_bus()
        bus2 = get_event_bus()
        
        # Should return same instance
        assert bus1 is bus2


@pytest.mark.asyncio
async def test_init_event_bus(mock_redis):
    """Test initialization helper."""
    import app.utils.event_bus as eb
    eb._event_bus = None
    
    bus = await init_event_bus("redis://localhost:6379")
    
    assert bus.is_connected()
    mock_redis.from_url.assert_called_once()


@pytest.mark.asyncio
async def test_shutdown_event_bus(mock_redis):
    """Test shutdown helper."""
    import app.utils.event_bus as eb
    
    bus = await init_event_bus("redis://localhost:6379")
    assert bus.is_connected()
    
    await shutdown_event_bus()
    
    assert eb._event_bus is None


@pytest.mark.asyncio
async def test_event_types():
    """Test all event types are defined."""
    assert EventType.TASK_STARTED == "task_started"
    assert EventType.TASK_PROGRESS == "task_progress"
    assert EventType.TASK_COMPLETED == "task_completed"
    assert EventType.TASK_ERROR == "task_error"
    assert EventType.DOCUMENT_INDEXED == "document_indexed"
    assert EventType.SEARCH_COMPLETED == "search_completed"


@pytest.mark.asyncio
async def test_publish_custom_channel(mock_redis):
    """Test publishing to custom channel."""
    event_bus = EventBus(redis_url="redis://localhost:6379")
    await event_bus.connect()
    
    await event_bus.publish(
        event_type=EventType.DOCUMENT_INDEXED,
        task_id="doc_123",
        data={"document_id": "123", "title": "Test Paper"},
        channel="document_events"
    )
    
    redis_client = mock_redis.from_url.return_value
    call_args = redis_client.publish.call_args
    assert call_args[0][0] == "document_events"
