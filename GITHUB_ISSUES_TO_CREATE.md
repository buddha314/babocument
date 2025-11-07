# GitHub Issues - Ready to Create

These are the GitHub issues ready to be created. Copy each section into GitHub's "New Issue" form.

---

## Issue #30: Client API Infrastructure Setup

**Labels:** `client`, `api`, `P0`, `phase-2`

**Title:** Client API Infrastructure Setup

**Description:**

## Summary

Set up API client infrastructure for the BabylonJS/Next.js client to communicate with the FastAPI server. This is the foundation for all client-server communication.

## Background

The server exposes 17 REST API endpoints for document management, search, and statistics. The client needs a type-safe, robust API client to consume these endpoints.

**Server API:** http://localhost:8000/docs (OpenAPI documentation)

## Tasks

- [ ] Install dependencies (axios, @tanstack/react-query, zod)
- [ ] Create base API client with interceptors
- [ ] Define TypeScript types (from OpenAPI or manual)
- [ ] Set up React Query provider
- [ ] Configure environment variables
- [ ] Test server connectivity

## Files to Create

- `client/src/lib/api/client.ts`
- `client/src/lib/api/types.ts`
- `client/src/app/providers.tsx`
- `client/.env.local`

## Acceptance Criteria

- [ ] API client can successfully connect to server
- [ ] Types are defined for all server responses
- [ ] React Query is set up and working
- [ ] Environment variables are configured
- [ ] Error handling works
- [ ] CORS allows client requests

## Dependencies

None - can start immediately

## Estimated Time

4-6 hours

## Documentation

- See `CLIENT_API_INTEGRATION_PLAN.md` for full architecture
- See `HANDOFF_2025-11-06_CLIENT_API.md` for implementation details

---

## Issue #32: Document API Integration (Client)

**Labels:** `client`, `api`, `documents`, `P0`, `phase-2`

**Title:** Document API Integration (Client)

**Description:**

## Summary

Implement document management features in the BabylonJS client using the server's REST API. This includes listing, viewing, uploading, deleting, and searching documents.

## Tasks

- [ ] Create `lib/api/documents.ts` with all document API methods
- [ ] Create `lib/hooks/useDocuments.ts` with React Query hooks
- [ ] Build DocumentList component
- [ ] Build DocumentViewer component
- [ ] Build DocumentUploader component
- [ ] Test all CRUD operations

## Files to Create

- `client/src/lib/api/documents.ts`
- `client/src/lib/hooks/useDocuments.ts`
- `client/src/components/documents/DocumentList.tsx`
- `client/src/components/documents/DocumentViewer.tsx`
- `client/src/components/documents/DocumentUploader.tsx`

## Acceptance Criteria

- [ ] Can list all documents with pagination
- [ ] Can view document details
- [ ] Can upload new PDF documents
- [ ] Can delete documents
- [ ] Can search documents (semantic & keyword)
- [ ] Can generate AI summaries
- [ ] Loading states show during API calls
- [ ] Errors are handled gracefully

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)

## Estimated Time

8-12 hours

## Documentation

- Server API: http://localhost:8000/docs
- See `CLIENT_API_INTEGRATION_PLAN.md` for code examples

---

## Issue #33: Search Integration (Client)

**Labels:** `client`, `search`, `P1`, `phase-2`

**Title:** Search Integration (Client)

**Description:**

## Summary

Implement semantic and keyword search functionality in the BabylonJS client with UI components for search input, results display, and filtering.

## Tasks

- [ ] Create `lib/hooks/useSearch.ts` with debounced search
- [ ] Build SearchBar component
- [ ] Build SearchResults component
- [ ] Build SearchFilters component (year, source)
- [ ] Integrate with 3D scene (highlight results - optional)

## Files to Create

- `client/src/lib/hooks/useSearch.ts`
- `client/src/components/search/SearchBar.tsx`
- `client/src/components/search/SearchResults.tsx`
- `client/src/components/search/SearchFilters.tsx`

## Acceptance Criteria

- [ ] Can search documents using text input
- [ ] Can toggle between semantic and keyword search
- [ ] Search is debounced
- [ ] Results show relevance scores
- [ ] Can filter by year and source
- [ ] Loading states work
- [ ] Error handling works

## Dependencies

- **Depends on:** Issue #32 (Document API Integration)

## Estimated Time

6-8 hours

---

## Issue #34: WebSocket Real-time Updates (Client)

**Labels:** `client`, `websocket`, `realtime`, `P1`, `phase-2`

**Title:** WebSocket Real-time Updates (Client)

**Description:**

## Summary

Implement WebSocket connection in the BabylonJS client to receive real-time updates from the server for agent tasks, document processing, and search completion events.

## Tasks

- [ ] Create `lib/api/websocket.ts` with auto-reconnect
- [ ] Create `lib/hooks/useWebSocket.ts`
- [ ] Create Notification component
- [ ] Integrate with DocumentUploader (show upload progress)
- [ ] Subscribe to all event types
- [ ] Test event flow

## Files to Create

- `client/src/lib/api/websocket.ts`
- `client/src/lib/hooks/useWebSocket.ts`
- `client/src/components/common/Notification.tsx`
- `client/src/components/agents/AgentActivity.tsx`

## Acceptance Criteria

- [ ] WebSocket connects on page load
- [ ] Auto-reconnects on disconnect
- [ ] Receives and parses events correctly
- [ ] UI updates in real-time
- [ ] Notifications show for events
- [ ] Connection status visible
- [ ] Proper cleanup on unmount

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)
- **Depends on:** Server Issue #21 (WebSocket Handler - must be implemented first)

## Estimated Time

4-6 hours

**Note:** Server Issue #21 must be completed before this can be fully tested.

---

## Issue #38: Agent-Assisted Paper Discovery

**Labels:** `agent`, `search`, `nlp`, `P1`, `feature`

**Title:** Agent-Assisted Paper Discovery

**Description:**

## User Story

> **As Beabadoo**, I want to ask the agent to find scientific papers for me using natural language, so I can quickly discover relevant research without manually searching through databases.

## Summary

Enable natural language queries for finding scientific papers using the Research Agent with LLM capabilities. Users can ask questions like "Find papers about bioink formulation" and receive ranked, relevant results with AI-generated explanations.

## Example Queries

- "Find papers about bioink formulation for 3D printing"
- "Show me recent advances in CRISPR gene editing"
- "Papers by George Church about synthetic biology"
- "Compare different methods for tissue scaffolding"
- "What's new in biomanufacturing since 2023?"

## Tasks

**Backend (8-12 hours):**
- [ ] Enhance Research Agent with NLP query processing
- [ ] Add query intent extraction (keywords, authors, time ranges)
- [ ] Create `/api/v1/agents/search` endpoint
- [ ] Generate AI explanations for results ("why this matches")
- [ ] Integrate with existing semantic search
- [ ] Add result ranking algorithm

**Frontend (6-8 hours):**
- [ ] Create `lib/api/agents.ts` API methods
- [ ] Create `lib/hooks/useAgentSearch.ts` hook
- [ ] Build AgentSearchBar component
- [ ] Build AgentSearchResults component with explanations
- [ ] Add agent avatar with "thinking" animation
- [ ] Support voice input in VR mode

## Acceptance Criteria

- [ ] Can input natural language queries
- [ ] Agent processes query and returns ranked results
- [ ] Results show relevance scores and AI summaries
- [ ] Each result has "why this matches" explanation
- [ ] Can view full paper or add to workspace
- [ ] Voice input works in VR mode
- [ ] Real-time progress updates via WebSocket

## Dependencies

- **Depends on:** Issue #10 (Complete Agents)
- **Depends on:** Client Issue #32 (Document API)
- **Related to:** Issue #5 (MCP Integration - for external sources)

## Estimated Time

14-20 hours (Backend: 8-12, Frontend: 6-8)

## Documentation

- See `specs/VISUALIZATION_REQUIREMENTS.md` - Section 3
- See `.github/ISSUE_TEMPLATE/agent-paper-discovery.md` for full details

---

## Issue #35: 3D Timeline Visualization (Client)

**Labels:** `client`, `babylonjs`, `3d`, `visualization`, `P2`, `phase-3`

**Title:** 3D Timeline Visualization (Client)

**Description:**

## Summary

Create an immersive 3D timeline corridor in BabylonJS that visualizes documents from the API sorted by year, with interactive selection and search result highlighting.

## Tasks

- [ ] Create Timeline3D component
- [ ] Generate document meshes from API data
- [ ] Position documents by year
- [ ] Add interactive selection (click/hover)
- [ ] Integrate search result highlighting
- [ ] Add VR/XR controller support
- [ ] Optimize performance (60+ FPS)

## Files to Create

- `client/src/components/babylon/Timeline3D.tsx`
- `client/src/components/babylon/DocumentMesh.tsx`
- `client/src/components/babylon/YearPartition.tsx`
- `client/src/components/babylon/utils/meshGeneration.ts`
- `client/src/components/babylon/utils/positioning.ts`

## Acceptance Criteria

- [ ] Documents load from API and render in 3D
- [ ] Documents sorted by year along timeline
- [ ] Can navigate through timeline
- [ ] Can select documents
- [ ] Search results are highlighted
- [ ] Works in desktop and VR modes
- [ ] Maintains 60+ FPS with 100+ documents

## Dependencies

- **Depends on:** Issue #32 (Document API Integration)
- **Related to:** Issue #33 (Search - for highlighting)

## Estimated Time

12-16 hours

---

## Issue #36: Statistics Dashboard (Client)

**Labels:** `client`, `stats`, `dashboard`, `P2`, `phase-3`

**Title:** Statistics Dashboard (Client)

**Description:**

## Summary

Create statistics dashboard showing system metrics and document analytics.

## Tasks

- [ ] Create `lib/api/stats.ts` API methods
- [ ] Create `lib/hooks/useStats.ts`
- [ ] Build StatsPanel component
- [ ] Build charts (documents by year, source trends)
- [ ] Add real-time updates via WebSocket

## Files to Create

- `client/src/lib/api/stats.ts`
- `client/src/lib/hooks/useStats.ts`
- `client/src/components/stats/StatsPanel.tsx`
- `client/src/components/stats/StatsChart.tsx`

## Acceptance Criteria

- [ ] Shows system statistics
- [ ] Shows document analytics
- [ ] Charts are interactive
- [ ] Real-time updates work

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)

## Estimated Time

6-8 hours

---

## Issue #37: Repository Management UI (Client)

**Labels:** `client`, `repository`, `admin`, `P2`, `phase-3`

**Title:** Repository Management UI (Client)

**Description:**

## Summary

Create UI for managing document repositories and MCP server connections.

## Tasks

- [ ] Create `lib/api/repositories.ts` API methods
- [ ] Create `lib/hooks/useRepositories.ts`
- [ ] Build RepositoryManager component
- [ ] Show connection status and health
- [ ] Add sync functionality

## Files to Create

- `client/src/lib/api/repositories.ts`
- `client/src/lib/hooks/useRepositories.ts`
- `client/src/components/repositories/RepositoryManager.tsx`
- `client/src/components/repositories/RepositoryCard.tsx`

## Acceptance Criteria

- [ ] Shows all repositories
- [ ] Shows connection status
- [ ] Can trigger sync
- [ ] Shows document counts

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)

## Estimated Time

4-6 hours

---

## How to Create These Issues

1. Go to: https://github.com/buddha314/babocument/issues/new
2. Copy the content from each issue above
3. Set labels as indicated
4. Assign to yourself if needed
5. Create issue

**Note:** The issue templates are also available in `.github/ISSUE_TEMPLATE/` for reference.
