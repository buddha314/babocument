---
name: Agent-Assisted Paper Discovery
about: Implement natural language queries for finding scientific papers
title: 'Agent-Assisted Paper Discovery'
labels: 'agent', 'search', 'nlp', 'P1', 'feature'
assignees: ''
---

## User Story

> **As Beabadoo**, I want to ask the agent to find scientific papers for me using natural language, so I can quickly discover relevant research without manually searching through databases.

## Background

Beabadoo needs to discover relevant research papers quickly without manually constructing complex search queries. By leveraging the Research Agent with LLM capabilities, users can ask questions in natural language and receive ranked, relevant results with AI-generated explanations.

## Requirements

### Natural Language Query Interface

**Example Queries:**
- "Find papers about bioink formulation for 3D printing"
- "Show me recent advances in CRISPR gene editing"
- "Papers by George Church about synthetic biology"
- "Compare different methods for tissue scaffolding"
- "What's new in biomanufacturing since 2023?"
- "Papers about CAR-T cell therapy with clinical trial data"

### Agent Capabilities

- [ ] Process natural language queries using LLM
- [ ] Extract search intent (keywords, authors, topics, time ranges)
- [ ] Perform semantic search across local corpus
- [ ] Query external repositories (PubMed, arXiv, bioRxiv via MCP)
- [ ] Rank results by relevance
- [ ] Generate brief summaries for each result
- [ ] Explain why each paper matches the query

### Query Types

- [x] Keyword-based: "papers about CRISPR"
- [ ] Author-based: "papers by Jennifer Doudna"
- [ ] Topic-based: "recent advances in synthetic biology"
- [ ] Comparative: "compare bioink materials"
- [ ] Time-ranged: "papers from last 5 years"
- [ ] Citation-based: "papers citing [DOI]"

### Response Format

- [ ] Ranked list of papers with scores
- [ ] AI-generated summary for each result
- [ ] Highlighted relevant sections
- [ ] "Why this matches" explanation
- [ ] Options to view/download/add to workspace
- [ ] Export as bibliography (BibTeX, RIS)

## Technical Implementation

### Backend (Server)

**Files to Create/Update:**
- [ ] `server/app/agents/research.py` - Enhance Research Agent
  - Add natural language query parsing
  - Add query intent extraction
  - Add result ranking and explanation generation
- [ ] `server/app/api/agents.py` - New agent API endpoints
  - `POST /api/v1/agents/search` - Natural language search
  - `GET /api/v1/agents/search/{task_id}` - Search progress
  - `POST /api/v1/agents/search/{task_id}/refine` - Refine results

**API Endpoint:**
```python
@router.post("/api/v1/agents/search")
async def agent_search(query: AgentSearchQuery):
    """
    Natural language search using Research Agent
    
    Args:
        query: Natural language query string
        filters: Optional filters (year, author, etc.)
        limit: Max results (default 20)
    
    Returns:
        task_id: Background task ID
        status: "processing"
    """
```

**Event Bus Integration:**
- Emit `search.started` event
- Emit `search.progress` events with partial results
- Emit `search.completed` event with final results

### Frontend (Client)

**Files to Create:**
- [ ] `client/src/lib/api/agents.ts` - Agent API methods
- [ ] `client/src/lib/hooks/useAgentSearch.ts` - React Query hook
- [ ] `client/src/components/agents/AgentSearchBar.tsx` - NL query input
- [ ] `client/src/components/agents/AgentSearchResults.tsx` - Results with explanations
- [ ] `client/src/components/agents/AgentThinking.tsx` - Loading animation

**UI Components:**
```typescript
<AgentSearchBar 
  onSearch={(query) => handleAgentSearch(query)}
  placeholder="Ask me to find papers..."
/>

<AgentSearchResults 
  results={results}
  onSelectPaper={(id) => viewPaper(id)}
  onAddToWorkspace={(id) => addToWorkspace(id)}
/>
```

### Integration Points

- [ ] Integrate with existing search functionality
- [ ] Add "Ask Agent" button to search interface
- [ ] Show agent avatar with "thinking" animation
- [ ] Display results in timeline visualization
- [ ] Support voice input in VR mode

## Acceptance Criteria

- [ ] Can input natural language queries
- [ ] Agent processes query and returns ranked results
- [ ] Results show relevance scores
- [ ] Each result has AI-generated summary
- [ ] Results include "why this matches" explanation
- [ ] Can click to view full paper
- [ ] Can add results to workspace
- [ ] Can export as bibliography
- [ ] Voice input works in VR mode
- [ ] Real-time progress updates via WebSocket
- [ ] Query history is saved
- [ ] Follow-up questions refine results

## Example User Flow

1. Beabadoo enters: "Find recent papers about bioink formulation"
2. Agent avatar shows "thinking" animation
3. Research Agent:
   - Parses query → keywords: ["bioink", "formulation"], time: "recent"
   - Searches local corpus + PubMed via MCP
   - Ranks results by relevance
   - Generates summaries
4. Results display:
   - "Alginate-based bioink for 3D bioprinting" (score: 0.95)
     - Summary: "This paper presents a novel alginate formulation..."
     - Why: "Directly discusses bioink formulation for 3D printing"
   - [More results...]
5. Beabadoo clicks a result to view full paper
6. Beabadoo asks follow-up: "Which one has the best mechanical properties?"
7. Agent re-ranks and highlights relevant sections

## Dependencies

- **Depends on:** Issue #10 (Complete Agents - Research Agent)
- **Depends on:** Server Issue #15 (REST API - completed)
- **Depends on:** Client Issue #30 (API Infrastructure)
- **Depends on:** Client Issue #32 (Document API)
- **Related to:** Issue #5 (MCP Integration - for external sources)

## Estimated Time

**Backend:** 8-12 hours
- Natural language processing: 3-4 hours
- Intent extraction: 2-3 hours
- Result ranking & explanation: 2-3 hours
- API endpoints: 1-2 hours

**Frontend:** 6-8 hours
- UI components: 3-4 hours
- Agent API integration: 2-3 hours
- Voice input (VR): 1-1 hour

**Total:** 14-20 hours

## Priority

**P1 (High)** - Core feature for user experience

## Phase

Phase 2 - Client Development / Agent Enhancement

## Testing

- [ ] Test simple keyword queries
- [ ] Test complex multi-criteria queries
- [ ] Test author-specific queries
- [ ] Test time-ranged queries
- [ ] Test follow-up question refinement
- [ ] Test with empty corpus
- [ ] Test with large result sets (100+)
- [ ] Test real-time progress updates
- [ ] Test voice input in VR
- [ ] Test error handling (network, LLM failures)

## Future Enhancements

- [ ] Multi-language support
- [ ] Query suggestions based on workspace
- [ ] Smart query auto-complete
- [ ] Conversational refinement (chat interface)
- [ ] Learning user preferences
- [ ] Collaborative search (share queries with team)

## Documentation

- See `specs/VISUALIZATION_REQUIREMENTS.md` - Section 3 (Agent-Assisted Paper Discovery)
- See `CLIENT_API_INTEGRATION_PLAN.md` - User Story section
- See `specs/MULTI_AGENT_ARCHITECTURE.md` - Research Agent capabilities

## Notes

This feature combines:
- Semantic search (existing)
- LLM natural language understanding (new)
- Multi-source federation (MCP integration)
- Real-time agent communication (WebSocket)

It transforms Babocument from a document viewer into an intelligent research assistant.
