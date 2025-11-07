# Session Handoff: Client API Integration Plan

**Date:** 2025-11-06  
**Session Focus:** Client-Server Integration Planning  
**Time:** ~2 hours  
**Status:** ✅ Planning Complete

---

## Executive Summary

Created a comprehensive implementation plan for integrating the **BabylonJS/Next.js client** with the **Python FastAPI server**. The plan covers API client architecture, state management, data flow patterns, error handling, and a phased implementation roadmap.

**Key Deliverable:** `CLIENT_API_INTEGRATION_PLAN.md` (comprehensive 1000+ line technical specification)

---

## What Was Completed

### 1. Technical Analysis ✅

**Server Capabilities Reviewed:**
- ✅ 17 REST API endpoints across 3 routers
- ✅ Document management (7 endpoints)
- ✅ Repository management (5 endpoints)
- ✅ Statistics & status (5 endpoints)
- ✅ WebSocket support (planned for real-time updates)
- ✅ Event bus integration (Redis pub/sub)

**Client Stack Analyzed:**
- ✅ Next.js 14.2.32 (React 18)
- ✅ BabylonJS 8.33.2 (3D/VR engine)
- ✅ TypeScript 5.8.3
- ✅ Tailwind CSS
- ✅ WebXR support

### 2. Architecture Design ✅

**Layered Architecture Defined:**
```
React Components → State Management → API Client → HTTP/WebSocket → FastAPI Server
```

**Technology Decisions Made:**
- **HTTP Client:** Axios (with interceptors)
- **State Management:** React Query (TanStack Query) + React Context
- **Type Safety:** TypeScript types generated from OpenAPI schema
- **Real-time:** Native WebSocket API
- **Validation:** Zod for runtime validation

### 3. Implementation Plan Created ✅

**6 Implementation Phases Defined:**

1. **Phase 1: Foundation** (Week 1)
   - API client infrastructure
   - TypeScript types
   - React Query setup

2. **Phase 2: Document API** (Week 2)
   - CRUD operations
   - Document viewer
   - Upload functionality

3. **Phase 3: Search Integration** (Week 3)
   - Semantic search
   - Keyword search
   - Result highlighting

4. **Phase 4: Real-time Updates** (Week 4)
   - WebSocket integration
   - Live notifications
   - Progress updates

5. **Phase 5: 3D Visualization** (Week 5-6)
   - Timeline corridor
   - Document meshes
   - VR interactions

6. **Phase 6: Admin Features** (Week 7)
   - Statistics dashboard
   - Repository management
   - Health monitoring

### 4. Code Examples Provided ✅

**Complete Working Examples:**
- ✅ Base API client with interceptors
- ✅ TypeScript type definitions
- ✅ Document API methods
- ✅ React Query hooks
- ✅ WebSocket manager
- ✅ Error handling utilities
- ✅ Component examples (DocumentList, SearchBar, etc.)

### 5. Directory Structure Defined ✅

```
client/src/
├── lib/
│   ├── api/          # API client & methods
│   ├── hooks/        # React Query hooks
│   ├── stores/       # State stores (optional)
│   └── utils/        # Error handling, formatting
├── components/
│   ├── documents/    # Document components
│   ├── search/       # Search components
│   ├── babylon/      # BabylonJS 3D components
│   ├── stats/        # Statistics components
│   └── common/       # Shared components
└── app/
    ├── providers.tsx # React Query provider
    └── ...
```

---

## Current State

### Server (Backend) ✅
- **Status:** 85% Complete
- **API Endpoints:** 17 endpoints fully implemented
- **Documentation:** OpenAPI/Swagger at `/docs`
- **Testing:** 60 tests, 84% coverage
- **Event Bus:** Redis pub/sub implemented
- **Next:** Complete agent implementation (#10)

### Client (Frontend) 🟡
- **Status:** Scaffolded (BabylonJS Editor template)
- **Current:** Basic Next.js + BabylonJS scene
- **Next:** Implement API integration (Phase 1-6)

### Integration ❌
- **Status:** Not started
- **Blocker:** Client API layer needs implementation
- **Plan:** Follow CLIENT_API_INTEGRATION_PLAN.md

---

## Key Technical Decisions

### 1. API Client: Axios + React Query ✅

**Why?**
- Axios: Mature, interceptor support, good TypeScript support
- React Query: Built-in caching, automatic refetching, optimistic updates
- Alternative considered: SWR (lighter but fewer features)

### 2. State Management: Hybrid Approach ✅

**Server State:** React Query (API data, caching)
**UI State:** React Context (modals, selections, filters)
**Alternative:** Zustand (code examples provided if needed)

### 3. Type Safety: OpenAPI → TypeScript ✅

**Approach:** Generate TypeScript types from server's OpenAPI schema
**Tools:** `openapi-typescript` or manual definitions
**Benefit:** End-to-end type safety, catch errors at compile time

### 4. Real-time: Native WebSocket ✅

**Protocol:** WebSocket (ws://)
**Events:** Task updates, document indexing, search completion
**Fallback:** HTTP polling if WebSocket unavailable

---

## Next Actions (Priority Order)

### Immediate (This Week)

1. **Set up client dependencies** (2 hours)
   ```bash
   cd client
   npm install axios @tanstack/react-query zod
   npm install -D @types/node
   ```

2. **Create `.env.local`** (15 min)
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Implement Phase 1: Foundation** (4-6 hours)
   - Create `lib/api/client.ts`
   - Create `lib/api/types.ts`
   - Set up React Query provider
   - Test server connectivity

4. **Test basic API calls** (1 hour)
   - List documents
   - Get system stats
   - Verify CORS configuration

### Short-term (Next 2 Weeks)

5. **Phase 2: Document API Integration** (8-12 hours)
   - Document CRUD operations
   - Upload functionality
   - Search integration

6. **Phase 3: Search Integration** (6-8 hours)
   - Search UI components
   - Result display
   - Filters

7. **Phase 4: WebSocket Integration** (4-6 hours)
   - Real-time event handling
   - Progress notifications
   - Task updates

### Medium-term (Weeks 3-4)

8. **Phase 5: 3D Visualization** (12-16 hours)
   - Integrate API data with BabylonJS
   - Timeline corridor generation
   - Document mesh rendering
   - VR interactions

9. **Phase 6: Admin Features** (6-8 hours)
   - Statistics dashboard
   - Repository management
   - Health monitoring

---

## Files Created

### Documentation
- ✅ `CLIENT_API_INTEGRATION_PLAN.md` - Comprehensive integration plan (1000+ lines)
- ✅ `HANDOFF_2025-11-06_CLIENT_API.md` - This handoff document

### Code (To Be Created - See Plan)
- [ ] `client/src/lib/api/client.ts`
- [ ] `client/src/lib/api/types.ts`
- [ ] `client/src/lib/api/documents.ts`
- [ ] `client/src/lib/hooks/useDocuments.ts`
- [ ] `client/src/app/providers.tsx`
- [ ] (30+ more files - see plan)

---

## GitHub Issues (To Create)

Based on the implementation plan, the following issues should be created:

### Phase 1 Issues

**Issue #30: Client API Infrastructure Setup**
- **Priority:** P0 (Critical Path)
- **Time:** 4-6 hours
- **Tasks:**
  - Install dependencies (axios, react-query, zod)
  - Create base API client with interceptors
  - Define TypeScript types
  - Set up React Query provider
  - Configure environment variables
  - Test server connectivity

**Issue #31: TypeScript Type Definitions**
- **Priority:** P1 (High)
- **Time:** 2-3 hours
- **Tasks:**
  - Generate types from OpenAPI schema OR
  - Create manual type definitions
  - Validate types against server responses
  - Document type usage

### Phase 2 Issues

**Issue #32: Document API Integration**
- **Priority:** P0 (Critical Path)
- **Time:** 8-12 hours
- **Depends on:** #30
- **Tasks:**
  - Create `documents.ts` API methods
  - Create React Query hooks
  - Build DocumentList component
  - Build DocumentViewer component
  - Build DocumentUploader component
  - Test CRUD operations

**Issue #33: Search Integration**
- **Priority:** P1 (High)
- **Time:** 6-8 hours
- **Depends on:** #32
- **Tasks:**
  - Create search API methods
  - Create useSearch hook
  - Build SearchBar component
  - Build SearchResults component
  - Add filters (year, source)
  - Test semantic & keyword search

### Phase 3 Issues

**Issue #34: WebSocket Real-time Updates**
- **Priority:** P1 (High)
- **Time:** 4-6 hours
- **Depends on:** #30, Server Issue #21 (WebSocket Handler)
- **Tasks:**
  - Create WebSocket manager
  - Create useWebSocket hook
  - Handle connection/reconnection
  - Subscribe to events
  - Update UI on events
  - Test event flow

### Phase 4 Issues

**Issue #35: 3D Timeline Visualization**
- **Priority:** P2 (Medium)
- **Time:** 12-16 hours
- **Depends on:** #32
- **Tasks:**
  - Create Timeline3D component
  - Generate document meshes from API data
  - Sort documents by year
  - Add interactive selection
  - Implement search result highlighting
  - Optimize for VR

**Issue #36: Statistics Dashboard**
- **Priority:** P2 (Medium)
- **Time:** 6-8 hours
- **Depends on:** #30
- **Tasks:**
  - Create stats API methods
  - Create useStats hook
  - Build StatsPanel component
  - Build charts (document counts, trends)
  - Real-time updates

**Issue #37: Repository Management UI**
- **Priority:** P2 (Medium)
- **Time:** 4-6 hours
- **Depends on:** #30
- **Tasks:**
  - Create repository API methods
  - Build RepositoryManager component
  - Add sync functionality
  - Show connection status
  - Test repository operations

---

## Technical Debt & Considerations

### CORS Configuration ⚠️

**Current Server Config:**
```python
cors_origins: list[str] = Field(
    default=["http://localhost:3000", "http://localhost:8000"],
    alias="CORS_ORIGINS",
)
```

**Action Required:** Verify CORS settings work with client requests

### Authentication 🔒

**Current State:** No authentication implemented
**Impact:** All endpoints are public
**Next Step:** Implement in server Issue #23, then update client

### Error Handling 🚨

**Plan Includes:**
- Axios interceptors for global error handling
- React Error Boundaries for component errors
- User-friendly error messages
- Retry logic for transient failures

### Performance 🚀

**Optimization Strategies:**
- React Query caching (5-30 min TTL)
- Request deduplication
- Pagination for large datasets
- Optimistic updates for better UX
- WebSocket for real-time (avoid polling)

---

## Testing Strategy

### Unit Tests
- API client methods
- React hooks
- Utility functions

### Integration Tests
- Component + API interaction
- End-to-end workflows
- WebSocket event handling

### E2E Tests (Future)
- Full user journeys
- VR interactions
- Cross-browser compatibility

---

## Dependencies & Blockers

### Server Dependencies (Must Complete First)
- ✅ REST API endpoints (COMPLETE)
- ✅ Event Bus (COMPLETE)
- 🟡 WebSocket handler (Issue #21) - For real-time updates
- 🟡 Authentication (Issue #23) - For production security

### Client Dependencies (Can Start Now)
- None - Phase 1 can begin immediately

### External Dependencies
- Server must be running (`localhost:8000`)
- Redis must be running (for event bus)
- Browser must support WebSocket & WebXR

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| CORS issues | Medium | Medium | Test early, document configuration |
| Type mismatches | Medium | Low | Generate types from OpenAPI schema |
| WebSocket instability | Low | Medium | Implement reconnection logic, fallback to polling |
| Performance in VR | Medium | High | Profile early, optimize 3D rendering |
| API breaking changes | Low | High | Version API, use semantic versioning |

---

## Success Metrics

### Phase 1 Success Criteria
- ✅ Client can connect to server
- ✅ Can fetch and display documents
- ✅ Types are validated
- ✅ Error handling works

### Overall Success Criteria
- ✅ All CRUD operations work
- ✅ Search returns accurate results
- ✅ Real-time updates function
- ✅ 3D scene renders API data
- ✅ VR mode fully functional
- ✅ No critical bugs
- ✅ Good performance (60 FPS in VR)

---

## Resources & References

### Documentation
- **Integration Plan:** `CLIENT_API_INTEGRATION_PLAN.md`
- **Server API Docs:** http://localhost:8000/docs
- **Project Status:** `specs/PROJECT_STATUS.md`
- **Tasks:** `specs/TASKS.md`

### External Resources
- **React Query:** https://tanstack.com/query/latest
- **Axios:** https://axios-http.com/
- **BabylonJS:** https://doc.babylonjs.com/
- **Next.js:** https://nextjs.org/docs
- **TypeScript:** https://www.typescriptlang.org/docs

### Code Examples
- All code examples in `CLIENT_API_INTEGRATION_PLAN.md`
- Server API examples: `server/scripts/test_api.py`

---

## Questions for Next Session

1. **State Management:** Confirm React Query + Context approach vs Zustand?
2. **Type Generation:** Auto-generate from OpenAPI or manual definitions?
3. **WebSocket Priority:** Implement in Phase 4 or defer to later?
4. **3D Performance:** What's the target document count for timeline (100? 1000? 10k)?
5. **Authentication:** When to implement (before or after basic integration)?

---

## Handoff Checklist

- ✅ Implementation plan documented
- ✅ Architecture designed
- ✅ Technology decisions made
- ✅ Phases defined with timelines
- ✅ Code examples provided
- ✅ File structure outlined
- ✅ Dependencies identified
- ✅ Risks assessed
- ✅ Next actions prioritized
- 🟡 GitHub issues ready to create (see list above)
- 🟡 TASKS.md needs updating
- 🟡 PROJECT_STATUS.md needs updating

---

## Summary for Quick Handoff

**What we did:** Created comprehensive plan for BabylonJS client to call Python server API

**What we decided:** Axios + React Query + TypeScript, 6-phase implementation

**What's next:** Install dependencies, implement Phase 1 (API foundation), create GitHub issues

**Time estimate:** 6-8 weeks for full implementation (40-60 hours)

**Blocker:** None - can start Phase 1 immediately

**Critical path:** Phase 1 → Phase 2 → Phase 4 (Real-time) → Phase 5 (3D)

---

**Session Complete** ✅  
**Ready for Implementation** ✅  
**Documentation Status:** Complete  
**Next Session:** Begin Phase 1 implementation

