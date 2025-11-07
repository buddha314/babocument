---
name: WebSocket Real-time Updates (Client)
about: Implement WebSocket connection for real-time agent updates
title: 'WebSocket Real-time Updates (Client)'
labels: 'client, websocket, realtime, P1, phase-2'
assignees: ''
---

## Summary

Implement WebSocket connection in the BabylonJS client to receive real-time updates from the server for agent tasks, document processing, and search completion events.

## Background

The server will emit events via WebSocket for:
- Task started/progress/completed/failed
- Document indexed
- Search completed
- Agent activity

The client needs to subscribe to these events and update the UI in real-time.

## Tasks

### 1. Create WebSocket Manager
- [ ] Create `client/src/lib/api/websocket.ts`
  - Connect to WebSocket endpoint (`ws://localhost:8000/ws/agents`)
  - Auto-reconnect on disconnect (exponential backoff)
  - Subscribe to event types
  - Emit events to subscribers
  - Handle connection lifecycle (open, close, error)
  - Graceful shutdown on page unload

### 2. Create WebSocket Hook
- [ ] Create `client/src/lib/hooks/useWebSocket.ts`
  - `useWebSocket(url)` - Connect and return events
  - `useWebSocketEvent(eventType, callback)` - Subscribe to specific event
  - Track connection status
  - Return latest events
  - Clean up on unmount

### 3. Create Notification System
- [ ] Create `client/src/components/common/Notification.tsx`
  - Toast notifications for events
  - Different styles for success/error/info
  - Auto-dismiss after timeout
  - Stack multiple notifications

### 4. Integrate with Components
- [ ] Update DocumentUploader
  - Show upload progress from WebSocket events
  - Show success notification when indexed
- [ ] Update SearchResults
  - Show notification when search completes
- [ ] Create AgentActivity component
  - Display current agent tasks
  - Show progress bars
  - List active operations

### 5. Handle Events
- [ ] Subscribe to `task.started` events
- [ ] Subscribe to `task.progress` events
- [ ] Subscribe to `task.completed` events
- [ ] Subscribe to `task.failed` events
- [ ] Subscribe to `document.indexed` events
- [ ] Subscribe to `search.completed` events

### 6. Test Event Flow
- [ ] Test connection on page load
- [ ] Test reconnection after disconnect
- [ ] Test receiving events
- [ ] Test multiple subscribers
- [ ] Test cleanup on unmount
- [ ] Test error handling

## Files to Create

```
client/src/
├── lib/
│   ├── api/
│   │   └── websocket.ts           # WebSocket manager
│   └── hooks/
│       └── useWebSocket.ts        # WebSocket hook
└── components/
    ├── common/
    │   └── Notification.tsx       # Toast notifications
    └── agents/
        └── AgentActivity.tsx      # Agent task display
```

## Acceptance Criteria

- [ ] WebSocket connects on page load
- [ ] Auto-reconnects on disconnect (up to 5 attempts)
- [ ] Receives and parses events correctly
- [ ] UI updates in real-time when events arrive
- [ ] Notifications show for important events
- [ ] Connection status is visible
- [ ] Multiple components can subscribe to events
- [ ] Proper cleanup on unmount
- [ ] Error handling for connection failures
- [ ] Works in development and production

## Code Example

**WebSocket Manager:**
```typescript
// lib/api/websocket.ts
export class WebSocketManager {
  private ws: WebSocket | null = null;
  private subscribers: Map<string, Set<(event: any) => void>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(url: string) {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('[WebSocket] Connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.emit(data.type, data);
    };

    this.ws.onclose = () => {
      console.log('[WebSocket] Disconnected');
      this.reconnect(url);
    };

    this.ws.onerror = (error) => {
      console.error('[WebSocket] Error:', error);
    };
  }

  subscribe(eventType: string, callback: (event: any) => void) {
    if (!this.subscribers.has(eventType)) {
      this.subscribers.set(eventType, new Set());
    }
    this.subscribers.get(eventType)!.add(callback);
  }

  private emit(eventType: string, event: any) {
    this.subscribers.get(eventType)?.forEach(callback => callback(event));
  }

  private reconnect(url: string) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.reconnectAttempts++;
        this.connect(url);
      }, 1000 * this.reconnectAttempts);
    }
  }
}
```

**useWebSocket Hook:**
```typescript
export function useWebSocket(url: string) {
  const [events, setEvents] = useState<WebSocketEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEvents(prev => [...prev, data]);
    };
    ws.onclose = () => setIsConnected(false);

    return () => ws.close();
  }, [url]);

  return { events, isConnected };
}
```

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)
- **Depends on:** Server Issue #21 (WebSocket Handler - must be implemented first)

## Estimated Time

4-6 hours

## Phase

Phase 2 - Client Development

## Related Issues

- Issue #30 - Client API Infrastructure (dependency)
- Server Issue #21 - WebSocket Handler (dependency - must be done first)
- Server Issue #19 - Event Bus (completed - enables WebSocket)

## Testing

- [ ] Test connection on mount
- [ ] Test reconnection after server restart
- [ ] Test receiving different event types
- [ ] Test multiple subscribers to same event
- [ ] Test cleanup on unmount
- [ ] Test error handling when server is down
- [ ] Test in VR mode

## Notes

**Important:** Server Issue #21 (WebSocket Handler) must be completed before this can be fully tested. However, the client-side infrastructure can be built and tested with mock data.

## Documentation

- Server WebSocket will be at: `ws://localhost:8000/ws/agents`
- Event types defined in `client/src/lib/api/types.ts`
- See `CLIENT_API_INTEGRATION_PLAN.md` for WebSocket architecture
