# Client API Integration Plan - BabylonJS Client to Python Server

**Date:** 2025-11-06  
**Status:** Planning  
**Phase:** Phase 2 - Client Development

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [API Client Service](#api-client-service)
5. [State Management](#state-management)
6. [Data Flow Patterns](#data-flow-patterns)
7. [Error Handling](#error-handling)
8. [Implementation Phases](#implementation-phases)
9. [File Structure](#file-structure)
10. [Usage Examples](#usage-examples)
11. [Testing Strategy](#testing-strategy)
12. [Performance Considerations](#performance-considerations)

---

## Overview

This document outlines the strategy for integrating the **BabylonJS client** (Next.js 14 + React 18 + TypeScript) with the **Python FastAPI server** to enable document management, search, and visualization capabilities in an immersive 3D/VR environment.

### Goals

- ✅ **Type-safe API communication** using TypeScript
- ✅ **Reactive state management** for real-time UI updates
- ✅ **Optimistic updates** for responsive UX
- ✅ **Error resilience** with retry logic and fallbacks
- ✅ **WebSocket support** for real-time agent updates
- ✅ **Caching strategy** to minimize server load
- ✅ **VR/XR compatibility** for immersive experiences

### User Story

> **As Beabadoo**, I want to ask the agent to find scientific papers for me using natural language, so I can quickly discover relevant research without manually searching through databases.

This integration enables Beabadoo to:
- Search documents using semantic and keyword queries
- Upload and manage PDF documents
- View AI-generated summaries
- Interact with research agents for paper discovery
- Visualize documents in an immersive 3D timeline
- Receive real-time updates on processing tasks

### Server API Overview

The Python server exposes **17 REST endpoints** across 3 routers:

**Documents API** (`/api/v1/documents`)
- `GET /documents` - List documents with pagination
- `GET /documents/{id}` - Get document metadata
- `GET /documents/{id}/content` - Get full document content
- `POST /documents` - Upload new document (PDF)
- `DELETE /documents/{id}` - Delete document
- `POST /documents/search` - Search documents (semantic/keyword)
- `GET /documents/{id}/summary` - Generate AI summary

**Repositories API** (`/api/v1/repositories`)
- `GET /repositories` - List repositories
- `GET /repositories/{id}/status` - Get repository status
- `POST /repositories/sync` - Sync repositories
- `GET /repositories/{id}/documents` - List repo documents
- `POST /repositories/{id}/test` - Test repository connection

**Statistics API** (`/api/v1`)
- `GET /stats` - System statistics
- `GET /stats/all` - Comprehensive statistics
- `GET /status/processing` - Processing queue status
- `GET /status/processing/{task_id}` - Task status
- `GET /stats/agents` - Agent performance stats

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BabylonJS Client (Next.js)               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              React Components Layer                    │  │
│  │  • DocumentList  • SearchBar  • DocumentViewer       │  │
│  │  • Timeline3D    • Librarian  • StatsPanel           │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │            State Management Layer                      │  │
│  │  • React Context + Hooks (Recommended)                │  │
│  │  • Zustand (Alternative - Lightweight)                │  │
│  │  • Document Store  • Search Store  • UI Store        │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │              API Client Service                        │  │
│  │  • TypeScript API Client (Fetch/Axios)                │  │
│  │  • Type Definitions (Generated from OpenAPI)          │  │
│  │  • Request Interceptors (Auth, Logging)               │  │
│  │  • Response Interceptors (Error Handling)             │  │
│  │  • Caching Layer (React Query / SWR)                  │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │            WebSocket Manager                           │  │
│  │  • Real-time agent updates                            │  │
│  │  • Task progress notifications                        │  │
│  │  • Auto-reconnect logic                               │  │
│  └────────────────────┬──────────────────────────────────┘  │
└────────────────────────┼──────────────────────────────────┘
                         │ HTTP/HTTPS (REST)
                         │ WebSocket (ws://)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Python FastAPI Server (localhost:8000)         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                       │  │
│  │  • /api/v1/documents  • /api/v1/repositories          │  │
│  │  • /api/v1/stats      • /ws/agents (WebSocket)        │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │              Service Layer                             │  │
│  │  • VectorDB  • LLM Client  • Event Bus                │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │              Data Layer                                │  │
│  │  • ChromaDB  • Redis  • File Storage                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Communication Patterns

1. **REST API** - Primary communication (CRUD operations)
2. **WebSocket** - Real-time updates (agent tasks, processing status)
3. **Server-Sent Events (SSE)** - Alternative to WebSocket (optional)

---

## Technology Stack

### Client Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Next.js 14.2.32 | React framework with SSR/SSG |
| **UI Library** | React 18 | Component-based UI |
| **Language** | TypeScript 5.8.3 | Type-safe development |
| **3D Engine** | BabylonJS 8.33.2 | Immersive 3D/VR scenes |
| **HTTP Client** | Fetch API / Axios | REST API calls |
| **State Management** | React Context + Hooks | Global state (recommended) |
| **State Management (Alt)** | Zustand | Lightweight alternative |
| **Data Fetching** | React Query / SWR | Caching & synchronization |
| **WebSocket** | native WebSocket API | Real-time updates |
| **Validation** | Zod | Runtime type validation |
| **Styling** | Tailwind CSS 3.3.0 | Utility-first CSS |

### API Client Options

**Option A: React Query + Fetch (Recommended)**
- ✅ Built-in caching and cache invalidation
- ✅ Automatic background refetching
- ✅ Optimistic updates
- ✅ Request deduplication
- ✅ TypeScript support
- ✅ DevTools for debugging

**Option B: SWR + Fetch (Alternative)**
- ✅ Lightweight (~5KB)
- ✅ Stale-while-revalidate pattern
- ✅ Focus caching
- ✅ Simple API

**Option C: Axios + Custom Hooks (Manual)**
- ✅ Full control
- ✅ Interceptor support
- ❌ No built-in caching
- ❌ More boilerplate

**Decision: Use React Query (TanStack Query)** - Best balance of features, DX, and community support

---

## API Client Service

### Directory Structure

```
client/src/
├── lib/
│   ├── api/
│   │   ├── client.ts              # Base API client configuration
│   │   ├── types.ts               # TypeScript types (from OpenAPI)
│   │   ├── documents.ts           # Document API methods
│   │   ├── repositories.ts        # Repository API methods
│   │   ├── stats.ts               # Statistics API methods
│   │   └── websocket.ts           # WebSocket manager
│   ├── hooks/
│   │   ├── useDocuments.ts        # Document data hooks
│   │   ├── useSearch.ts           # Search hooks
│   │   ├── useRepositories.ts     # Repository hooks
│   │   ├── useStats.ts            # Statistics hooks
│   │   └── useWebSocket.ts        # WebSocket hook
│   └── stores/
│       ├── documentStore.ts       # Document state
│       ├── searchStore.ts         # Search state
│       └── uiStore.ts             # UI state (modals, loading)
```

### Implementation: Base API Client

**File: `client/src/lib/api/client.ts`**

```typescript
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

/**
 * API Client Configuration
 */
export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

/**
 * Create configured axios instance
 */
export const apiClient: AxiosInstance = axios.create(API_CONFIG);

/**
 * Request interceptor for auth, logging, etc.
 */
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Log requests in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }

    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

/**
 * Response interceptor for error handling
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API] Response from ${response.config.url}:`, response.data);
    }
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('[API] Server error:', {
        status: error.response.status,
        data: error.response.data,
        url: error.config?.url,
      });

      // Handle specific status codes
      switch (error.response.status) {
        case 401:
          // Unauthorized - clear auth and redirect
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
          break;
        case 404:
          console.warn('[API] Resource not found');
          break;
        case 500:
          console.error('[API] Server error - check logs');
          break;
      }
    } else if (error.request) {
      // Request made but no response
      console.error('[API] No response from server:', error.request);
    } else {
      // Error in request configuration
      console.error('[API] Request configuration error:', error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * Generic API error class
 */
export class ApiError extends Error {
  constructor(
    public status: number,
    public message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}
```

### Implementation: TypeScript Types

**File: `client/src/lib/api/types.ts`**

Generate types from OpenAPI schema or define manually:

```typescript
/**
 * API Response Types
 * 
 * Note: These should ideally be generated from the OpenAPI schema
 * using tools like openapi-typescript or swagger-typescript-api
 */

// Document Types
export interface DocumentMetadata {
  id: string;
  title: string;
  authors?: string[];
  abstract?: string;
  year?: number;
  journal?: string;
  doi?: string;
  url?: string;
  source?: string;
  created_at: string;
  updated_at: string;
  file_path?: string;
  indexed: boolean;
}

export interface DocumentContent {
  metadata: DocumentMetadata;
  content: string;
  sections?: Array<{
    title: string;
    content: string;
    level: number;
  }>;
}

export interface DocumentList {
  documents: DocumentMetadata[];
  total: number;
  limit: number;
  offset: number;
  has_next: boolean;
}

export interface DocumentUploadResponse {
  id: string;
  status: string;
  message: string;
  processing_task_id?: string;
}

// Search Types
export interface SearchQuery {
  query: string;
  limit?: number;
  search_type?: 'semantic' | 'keyword';
  filters?: Record<string, any>;
}

export interface SearchResult {
  document: DocumentMetadata;
  score: number;
  highlights?: string[];
}

export interface SearchResults {
  results: SearchResult[];
  query: string;
  search_type: string;
  total: number;
  execution_time_ms: number;
}

export interface DocumentSummary {
  document_id: string;
  summary: string;
  key_points: string[];
  generated_at: string;
}

// Repository Types
export interface RepositoryInfo {
  id: string;
  name: string;
  type: string;
  status: 'connected' | 'disconnected' | 'error' | 'syncing';
  url?: string;
  description?: string;
  document_count: number;
  last_sync?: string;
  last_error?: string;
  config?: Record<string, any>;
}

export interface RepositoryList {
  repositories: RepositoryInfo[];
  total: number;
}

export interface RepositoryStatus {
  repository: RepositoryInfo;
  connection_status: string;
  available_documents?: number;
  indexed_documents: number;
  last_check: string;
  health: Record<string, any>;
}

// Stats Types
export interface SystemStats {
  total_documents: number;
  indexed_documents: number;
  repositories_count: number;
  total_embeddings: number;
  storage_used_mb: number;
  last_updated: string;
  uptime_seconds: number;
}

export interface DocumentStats {
  by_year: Record<string, number>;
  by_source: Record<string, number>;
  by_type: Record<string, number>;
  top_authors: Array<{ name: string; count: number }>;
  top_journals: Array<{ name: string; count: number }>;
}

export interface AllStats {
  system: SystemStats;
  repositories: RepositoryInfo[];
  documents: DocumentStats;
  agents: any[];
}

// WebSocket Event Types
export enum EventType {
  TASK_STARTED = 'task.started',
  TASK_PROGRESS = 'task.progress',
  TASK_COMPLETED = 'task.completed',
  TASK_FAILED = 'task.failed',
  DOCUMENT_INDEXED = 'document.indexed',
  SEARCH_COMPLETED = 'search.completed',
}

export interface WebSocketEvent {
  type: EventType;
  task_id: string;
  timestamp: string;
  data: Record<string, any>;
}
```

### Implementation: Document API Methods

**File: `client/src/lib/api/documents.ts`**

```typescript
import { apiClient } from './client';
import type {
  DocumentMetadata,
  DocumentContent,
  DocumentList,
  DocumentUploadResponse,
  SearchQuery,
  SearchResults,
  DocumentSummary,
} from './types';

const BASE_PATH = '/api/v1/documents';

/**
 * Document API Methods
 */
export const documentsApi = {
  /**
   * List all documents with pagination
   */
  async list(params?: {
    limit?: number;
    offset?: number;
    source?: string;
    year?: number;
    indexed_only?: boolean;
  }): Promise<DocumentList> {
    const response = await apiClient.get<DocumentList>(BASE_PATH, { params });
    return response.data;
  },

  /**
   * Get document metadata by ID
   */
  async get(documentId: string): Promise<DocumentMetadata> {
    const response = await apiClient.get<DocumentMetadata>(`${BASE_PATH}/${documentId}`);
    return response.data;
  },

  /**
   * Get full document content
   */
  async getContent(documentId: string): Promise<DocumentContent> {
    const response = await apiClient.get<DocumentContent>(`${BASE_PATH}/${documentId}/content`);
    return response.data;
  },

  /**
   * Upload new document (PDF)
   */
  async upload(
    file: File,
    metadata?: {
      title?: string;
      authors?: string;
      year?: number;
      source?: string;
    }
  ): Promise<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    if (metadata) {
      Object.entries(metadata).forEach(([key, value]) => {
        if (value !== undefined) {
          formData.append(key, value.toString());
        }
      });
    }

    const response = await apiClient.post<DocumentUploadResponse>(BASE_PATH, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Delete document
   */
  async delete(documentId: string): Promise<{ status: string; message: string }> {
    const response = await apiClient.delete(`${BASE_PATH}/${documentId}`);
    return response.data;
  },

  /**
   * Search documents
   */
  async search(query: SearchQuery): Promise<SearchResults> {
    const response = await apiClient.post<SearchResults>(`${BASE_PATH}/search`, query);
    return response.data;
  },

  /**
   * Generate document summary
   */
  async getSummary(documentId: string, maxLength?: number): Promise<DocumentSummary> {
    const response = await apiClient.get<DocumentSummary>(
      `${BASE_PATH}/${documentId}/summary`,
      { params: { max_length: maxLength } }
    );
    return response.data;
  },
};
```

### Implementation: React Query Hooks

**File: `client/src/lib/hooks/useDocuments.ts`**

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { documentsApi } from '../api/documents';
import type { DocumentMetadata, SearchQuery } from '../api/types';

/**
 * Query keys for documents
 */
export const documentKeys = {
  all: ['documents'] as const,
  lists: () => [...documentKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...documentKeys.lists(), filters] as const,
  details: () => [...documentKeys.all, 'detail'] as const,
  detail: (id: string) => [...documentKeys.details(), id] as const,
  content: (id: string) => [...documentKeys.all, 'content', id] as const,
  summary: (id: string) => [...documentKeys.all, 'summary', id] as const,
  search: (query: SearchQuery) => [...documentKeys.all, 'search', query] as const,
};

/**
 * Hook: List documents
 */
export function useDocuments(params?: {
  limit?: number;
  offset?: number;
  source?: string;
  year?: number;
}) {
  return useQuery({
    queryKey: documentKeys.list(params || {}),
    queryFn: () => documentsApi.list(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook: Get document metadata
 */
export function useDocument(documentId: string) {
  return useQuery({
    queryKey: documentKeys.detail(documentId),
    queryFn: () => documentsApi.get(documentId),
    enabled: !!documentId,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

/**
 * Hook: Get document content
 */
export function useDocumentContent(documentId: string) {
  return useQuery({
    queryKey: documentKeys.content(documentId),
    queryFn: () => documentsApi.getContent(documentId),
    enabled: !!documentId,
    staleTime: 30 * 60 * 1000, // 30 minutes (content rarely changes)
  });
}

/**
 * Hook: Search documents
 */
export function useSearch(query: SearchQuery) {
  return useQuery({
    queryKey: documentKeys.search(query),
    queryFn: () => documentsApi.search(query),
    enabled: query.query.length > 0,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

/**
 * Hook: Upload document
 */
export function useUploadDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      file,
      metadata,
    }: {
      file: File;
      metadata?: { title?: string; authors?: string; year?: number; source?: string };
    }) => documentsApi.upload(file, metadata),
    onSuccess: () => {
      // Invalidate and refetch document lists
      queryClient.invalidateQueries({ queryKey: documentKeys.lists() });
    },
  });
}

/**
 * Hook: Delete document
 */
export function useDeleteDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (documentId: string) => documentsApi.delete(documentId),
    onSuccess: (_, documentId) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: documentKeys.detail(documentId) });
      queryClient.removeQueries({ queryKey: documentKeys.content(documentId) });
      // Invalidate lists
      queryClient.invalidateQueries({ queryKey: documentKeys.lists() });
    },
  });
}
```

---

## State Management

### Recommended Approach: React Query + Context

**Why React Query?**
- ✅ Server state management (caching, invalidation, refetching)
- ✅ Automatic background updates
- ✅ Request deduplication
- ✅ Optimistic updates
- ✅ Perfect for API-driven apps

**Why React Context?**
- ✅ UI state management (modals, selections, filters)
- ✅ Built-in to React (no extra dependencies)
- ✅ Simple and predictable

### Alternative: Zustand

If you prefer a single state management solution:

**File: `client/src/lib/stores/documentStore.ts`**

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type { DocumentMetadata, SearchResults } from '../api/types';

interface DocumentStore {
  // State
  selectedDocument: DocumentMetadata | null;
  searchResults: SearchResults | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setSelectedDocument: (doc: DocumentMetadata | null) => void;
  setSearchResults: (results: SearchResults | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useDocumentStore = create<DocumentStore>()(
  devtools(
    (set) => ({
      // Initial state
      selectedDocument: null,
      searchResults: null,
      isLoading: false,
      error: null,

      // Actions
      setSelectedDocument: (doc) => set({ selectedDocument: doc }),
      setSearchResults: (results) => set({ searchResults: results }),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),
      clearError: () => set({ error: null }),
    }),
    { name: 'DocumentStore' }
  )
);
```

---

## Data Flow Patterns

### Pattern 1: List Documents in 3D Timeline

```typescript
// Component: Timeline3D.tsx
import { useDocuments } from '@/lib/hooks/useDocuments';

export function Timeline3D() {
  const { data, isLoading, error } = useDocuments({ limit: 100 });

  useEffect(() => {
    if (!data) return;

    // Create 3D objects for each document
    data.documents.forEach((doc) => {
      createDocumentMesh(doc, scene);
    });
  }, [data]);

  // ... BabylonJS scene setup
}
```

### Pattern 2: Search and Highlight Results

```typescript
// Component: SearchBar.tsx
import { useState } from 'react';
import { useSearch } from '@/lib/hooks/useDocuments';

export function SearchBar() {
  const [query, setQuery] = useState('');
  const { data, isLoading } = useSearch({
    query,
    limit: 20,
    search_type: 'semantic',
  });

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search documents..."
      />
      {isLoading && <LoadingSpinner />}
      {data && <SearchResults results={data.results} />}
    </div>
  );
}
```

### Pattern 3: Upload with Progress

```typescript
// Component: DocumentUploader.tsx
import { useUploadDocument } from '@/lib/hooks/useDocuments';

export function DocumentUploader() {
  const uploadMutation = useUploadDocument();

  const handleUpload = async (file: File) => {
    try {
      const result = await uploadMutation.mutateAsync({
        file,
        metadata: { source: 'upload' },
      });
      
      console.log('Upload successful:', result);
      // Show success notification
    } catch (error) {
      console.error('Upload failed:', error);
      // Show error notification
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
      />
      {uploadMutation.isPending && <UploadProgress />}
    </div>
  );
}
```

---

## Error Handling

### Error Boundary Component

```typescript
// components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### API Error Handling

```typescript
// lib/utils/errorHandling.ts
export function handleApiError(error: any): string {
  if (error.response) {
    // Server responded with error
    const status = error.response.status;
    const message = error.response.data?.detail || error.response.data?.message;

    switch (status) {
      case 400:
        return `Bad request: ${message}`;
      case 404:
        return 'Resource not found';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return message || 'An error occurred';
    }
  } else if (error.request) {
    return 'No response from server. Check your connection.';
  } else {
    return error.message || 'An unexpected error occurred';
  }
}
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)

**Goal:** Set up API client infrastructure

- [ ] Install dependencies (axios, @tanstack/react-query, zod)
- [ ] Create base API client (`client.ts`)
- [ ] Define TypeScript types (`types.ts`)
- [ ] Set up React Query provider in `app/layout.tsx`
- [ ] Create environment variables (`.env.local`)
- [ ] Test basic connectivity to server

**Deliverables:**
- `lib/api/client.ts`
- `lib/api/types.ts`
- `app/providers.tsx` (React Query provider)

### Phase 2: Document API Integration (Week 2)

**Goal:** Implement document management features

- [ ] Create `documents.ts` API methods
- [ ] Create `useDocuments` hooks
- [ ] Build DocumentList component
- [ ] Build DocumentViewer component
- [ ] Build DocumentUploader component
- [ ] Test CRUD operations

**Deliverables:**
- `lib/api/documents.ts`
- `lib/hooks/useDocuments.ts`
- `components/DocumentList.tsx`
- `components/DocumentViewer.tsx`

### Phase 3: Search Integration (Week 3)

**Goal:** Implement semantic and keyword search

- [ ] Create search API methods
- [ ] Create `useSearch` hook
- [ ] Build SearchBar component
- [ ] Build SearchResults component
- [ ] Integrate with 3D scene (highlight results)
- [ ] Add filters (year, source, type)

**Deliverables:**
- `components/SearchBar.tsx`
- `components/SearchResults.tsx`
- Search integration in Timeline3D

### Phase 4: Real-time Updates (Week 4)

**Goal:** WebSocket integration for live updates

- [ ] Create WebSocket manager
- [ ] Create `useWebSocket` hook
- [ ] Subscribe to task events
- [ ] Update UI on document indexing
- [ ] Show upload progress
- [ ] Show agent activity

**Deliverables:**
- `lib/api/websocket.ts`
- `lib/hooks/useWebSocket.ts`
- Real-time notification system

### Phase 5: 3D Visualization (Week 5-6)

**Goal:** Integrate data with BabylonJS scenes

- [ ] Create document mesh generation
- [ ] Build timeline corridor (documents sorted by year)
- [ ] Add interactive document selection
- [ ] Implement search result highlighting
- [ ] Add VR controller support
- [ ] Optimize for performance

**Deliverables:**
- `components/babylon/Timeline3D.tsx`
- `components/babylon/DocumentMesh.tsx`
- VR-ready scene

### Phase 6: Statistics & Repository Management (Week 7)

**Goal:** Complete admin features

- [ ] Create stats API methods
- [ ] Create repository API methods
- [ ] Build StatsPanel component
- [ ] Build RepositoryManager component
- [ ] Add sync functionality
- [ ] Add health monitoring

**Deliverables:**
- `lib/api/stats.ts`
- `lib/api/repositories.ts`
- `components/StatsPanel.tsx`

---

## File Structure

```
client/
├── .env.local                      # Environment variables
├── src/
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts           # Base API client
│   │   │   ├── types.ts            # TypeScript types
│   │   │   ├── documents.ts        # Document API
│   │   │   ├── repositories.ts     # Repository API
│   │   │   ├── stats.ts            # Stats API
│   │   │   └── websocket.ts        # WebSocket manager
│   │   ├── hooks/
│   │   │   ├── useDocuments.ts     # Document hooks
│   │   │   ├── useSearch.ts        # Search hooks
│   │   │   ├── useRepositories.ts  # Repository hooks
│   │   │   ├── useStats.ts         # Stats hooks
│   │   │   └── useWebSocket.ts     # WebSocket hook
│   │   ├── stores/                 # Optional: Zustand stores
│   │   └── utils/
│   │       ├── errorHandling.ts    # Error utilities
│   │       └── formatting.ts       # Data formatting
│   ├── components/
│   │   ├── documents/
│   │   │   ├── DocumentList.tsx
│   │   │   ├── DocumentViewer.tsx
│   │   │   ├── DocumentUploader.tsx
│   │   │   └── DocumentCard.tsx
│   │   ├── search/
│   │   │   ├── SearchBar.tsx
│   │   │   ├── SearchResults.tsx
│   │   │   └── SearchFilters.tsx
│   │   ├── babylon/
│   │   │   ├── Timeline3D.tsx
│   │   │   ├── DocumentMesh.tsx
│   │   │   └── Librarian.tsx
│   │   ├── stats/
│   │   │   ├── StatsPanel.tsx
│   │   │   └── StatsChart.tsx
│   │   └── common/
│   │       ├── ErrorBoundary.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── Notification.tsx
│   └── app/
│       ├── providers.tsx           # React Query provider
│       ├── layout.tsx
│       └── page.tsx
```

---

## Usage Examples

### Example 1: Simple Document List

```typescript
// app/documents/page.tsx
'use client';

import { useDocuments } from '@/lib/hooks/useDocuments';

export default function DocumentsPage() {
  const { data, isLoading, error } = useDocuments({ limit: 20 });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>Documents ({data?.total})</h1>
      <ul>
        {data?.documents.map((doc) => (
          <li key={doc.id}>
            <h3>{doc.title}</h3>
            <p>{doc.authors?.join(', ')}</p>
            <p>{doc.year}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Example 2: Document Search

```typescript
// components/search/SearchBar.tsx
'use client';

import { useState } from 'react';
import { useSearch } from '@/lib/hooks/useDocuments';

export function SearchBar() {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState<'semantic' | 'keyword'>('semantic');

  const { data, isLoading } = useSearch({
    query,
    limit: 10,
    search_type: searchType,
  });

  return (
    <div className="search-container">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search documents..."
        className="search-input"
      />
      
      <select value={searchType} onChange={(e) => setSearchType(e.target.value as any)}>
        <option value="semantic">Semantic</option>
        <option value="keyword">Keyword</option>
      </select>

      {isLoading && <p>Searching...</p>}
      
      {data && (
        <div className="results">
          <p>Found {data.total} results in {data.execution_time_ms}ms</p>
          {data.results.map((result) => (
            <div key={result.document.id} className="result-card">
              <h3>{result.document.title}</h3>
              <p>Score: {result.score.toFixed(3)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### Example 3: WebSocket Real-time Updates

```typescript
// lib/hooks/useWebSocket.ts
import { useEffect, useState } from 'react';
import type { WebSocketEvent } from '../api/types';

export function useWebSocket(url: string) {
  const [events, setEvents] = useState<WebSocketEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      console.log('[WebSocket] Connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data) as WebSocketEvent;
      console.log('[WebSocket] Event:', data);
      setEvents((prev) => [...prev, data]);
    };

    ws.onerror = (error) => {
      console.error('[WebSocket] Error:', error);
    };

    ws.onclose = () => {
      console.log('[WebSocket] Disconnected');
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  return { events, isConnected };
}
```

---

## Testing Strategy

### Unit Tests

```typescript
// __tests__/api/documents.test.ts
import { documentsApi } from '@/lib/api/documents';
import { apiClient } from '@/lib/api/client';

jest.mock('@/lib/api/client');

describe('documentsApi', () => {
  it('should list documents', async () => {
    const mockResponse = {
      data: {
        documents: [],
        total: 0,
        limit: 20,
        offset: 0,
        has_next: false,
      },
    };

    (apiClient.get as jest.Mock).mockResolvedValue(mockResponse);

    const result = await documentsApi.list();
    expect(result).toEqual(mockResponse.data);
  });

  it('should handle errors', async () => {
    (apiClient.get as jest.Mock).mockRejectedValue(new Error('Network error'));

    await expect(documentsApi.list()).rejects.toThrow('Network error');
  });
});
```

### Integration Tests

```typescript
// __tests__/integration/documentFlow.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DocumentsPage from '@/app/documents/page';

describe('Document Flow', () => {
  it('should load and display documents', async () => {
    const queryClient = new QueryClient();
    
    render(
      <QueryClientProvider client={queryClient}>
        <DocumentsPage />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText(/Documents/i)).toBeInTheDocument();
    });
  });
});
```

---

## Performance Considerations

### 1. Caching Strategy

```typescript
// React Query configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});
```

### 2. Pagination

Always use pagination for large datasets:

```typescript
const { data } = useDocuments({
  limit: 20,
  offset: page * 20,
});
```

### 3. Request Deduplication

React Query automatically deduplicates identical requests.

### 4. Optimistic Updates

```typescript
const deleteMutation = useMutation({
  mutationFn: documentsApi.delete,
  onMutate: async (documentId) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: documentKeys.lists() });

    // Snapshot previous value
    const previous = queryClient.getQueryData(documentKeys.lists());

    // Optimistically update
    queryClient.setQueryData(documentKeys.lists(), (old: any) => ({
      ...old,
      documents: old.documents.filter((d: any) => d.id !== documentId),
    }));

    return { previous };
  },
  onError: (err, documentId, context) => {
    // Rollback on error
    queryClient.setQueryData(documentKeys.lists(), context?.previous);
  },
});
```

### 5. WebSocket Reconnection

```typescript
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

ws.onclose = () => {
  if (reconnectAttempts < maxReconnectAttempts) {
    setTimeout(() => {
      reconnectAttempts++;
      // Reconnect
    }, 1000 * reconnectAttempts);
  }
};
```

---

## Next Steps

1. **Review and approve this plan**
2. **Set up development environment**
   - Install dependencies
   - Configure environment variables
3. **Start Phase 1 implementation**
   - Create API client infrastructure
   - Test connectivity with server
4. **Iterate through phases**
   - Complete one phase before moving to next
   - Test thoroughly at each step

---

## References

- **Server API Documentation:** http://localhost:8000/docs (when server is running)
- **React Query Docs:** https://tanstack.com/query/latest
- **BabylonJS Docs:** https://doc.babylonjs.com/
- **Next.js Docs:** https://nextjs.org/docs
- **TypeScript Handbook:** https://www.typescriptlang.org/docs/

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-06  
**Status:** Ready for Implementation
