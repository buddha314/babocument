---
name: Client API Infrastructure Setup
about: Set up API client infrastructure for BabylonJS client
title: 'Client API Infrastructure Setup'
labels: 'client, api, P0, phase-2'
assignees: ''
---

## Summary

Set up API client infrastructure for the BabylonJS/Next.js client to communicate with the FastAPI server. This is the foundation for all client-server communication.

## Background

The server exposes 17 REST API endpoints for document management, search, and statistics. The client needs a type-safe, robust API client to consume these endpoints.

**Server API:** http://localhost:8000/docs (OpenAPI documentation)

## Tasks

### 1. Install Dependencies
- [ ] Install `axios` for HTTP requests
- [ ] Install `@tanstack/react-query` for data fetching & caching
- [ ] Install `zod` for runtime type validation
- [ ] Install dev dependencies: `@types/node`

```bash
cd client
npm install axios @tanstack/react-query zod
npm install -D @types/node
```

### 2. Create Base API Client
- [ ] Create `client/src/lib/api/client.ts`
  - Configure axios instance with base URL
  - Add request interceptor (auth, logging)
  - Add response interceptor (error handling)
  - Handle status codes (401, 404, 500)

### 3. Define TypeScript Types
- [ ] Create `client/src/lib/api/types.ts`
  - Define all API request/response types
  - Match server Pydantic models
  - Option: Generate from OpenAPI schema using `openapi-typescript`
  - Define WebSocket event types

### 4. Set up React Query Provider
- [ ] Create `client/src/app/providers.tsx`
  - Configure QueryClient
  - Set cache times (5-30 min)
  - Set retry logic
  - Add DevTools in development

### 5. Configure Environment Variables
- [ ] Create `client/.env.local`
  - Add `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - Document all env vars in README

### 6. Test Server Connectivity
- [ ] Test GET `/` (health check)
- [ ] Test GET `/api/v1/stats` (system stats)
- [ ] Test GET `/api/v1/documents` (list documents)
- [ ] Verify CORS configuration works
- [ ] Test error handling (network errors, 404, 500)

## Files to Create

```
client/
├── .env.local                    # Environment variables
├── src/
│   ├── lib/
│   │   └── api/
│   │       ├── client.ts         # Base API client (axios config)
│   │       └── types.ts          # TypeScript type definitions
│   └── app/
│       └── providers.tsx         # React Query provider
```

## Acceptance Criteria

- [ ] API client can successfully connect to server
- [ ] Types are defined for all server responses
- [ ] React Query is set up and working
- [ ] Environment variables are configured
- [ ] Error handling works (shows meaningful errors)
- [ ] CORS allows client requests
- [ ] DevTools show queries in development
- [ ] Basic API calls work (health check, stats, documents)

## Code Example

**client/src/lib/api/client.ts:**
```typescript
import axios from 'axios';

export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
};

export const apiClient = axios.create(API_CONFIG);

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.response?.status, error.message);
    return Promise.reject(error);
  }
);
```

## Dependencies

- None - can start immediately

## Estimated Time

4-6 hours

## Phase

Phase 2 - Client Development

## Related Issues

- Blocks #32 (Document API Integration)
- Blocks #33 (Search Integration)
- Blocks #34 (WebSocket Real-time Updates)
- Related to server API (Issue #15 - completed)

## Documentation

- See `CLIENT_API_INTEGRATION_PLAN.md` for full architecture
- See `HANDOFF_2025-11-06_CLIENT_API.md` for implementation details
