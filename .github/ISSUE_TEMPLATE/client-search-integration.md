---
name: Search Integration (Client)
about: Implement semantic and keyword search in BabylonJS client
title: 'Search Integration (Client)'
labels: 'client, search, P1, phase-2'
assignees: ''
---

## Summary

Implement semantic and keyword search functionality in the BabylonJS client with UI components for search input, results display, and filtering.

## Background

The server provides powerful search capabilities:
- **Semantic search:** Uses vector embeddings for similarity-based search
- **Keyword search:** Traditional text matching
- **Filters:** Year, source, document type

This issue focuses on building the client-side search experience.

## Tasks

### 1. Create Search API Methods
- [ ] Add to `client/src/lib/api/documents.ts`:
  - `documentsApi.search(query)` - Already created in #32
  - Ensure support for both search types
  - Support filter parameters

### 2. Create Search Hook
- [ ] Create `client/src/lib/hooks/useSearch.ts`
  - `useSearch(query)` - Search documents
  - Debounce search queries (wait 300ms after typing stops)
  - Cache results
  - Handle empty queries

### 3. Build SearchBar Component
- [ ] Create `client/src/components/search/SearchBar.tsx`
  - Text input for search query
  - Search type selector (semantic/keyword toggle)
  - Clear button
  - Search on Enter key
  - Show loading indicator while searching
  - Handle focus/blur states

### 4. Build SearchResults Component
- [ ] Create `client/src/components/search/SearchResults.tsx`
  - Display search results with scores
  - Show execution time
  - Highlight matched terms (if available)
  - Click result to view document
  - Show "No results" state
  - Show result count

### 5. Build SearchFilters Component
- [ ] Create `client/src/components/search/SearchFilters.tsx`
  - Year range filter
  - Source filter (local, pubmed, arxiv, etc.)
  - Document type filter (optional)
  - Clear filters button
  - Apply filters to search query

### 6. Integrate with 3D Scene (Optional)
- [ ] Highlight search results in Timeline3D
  - Color matching documents differently
  - Add glow effect to matches
  - Camera animation to focus on results

## Files to Create

```
client/src/
├── lib/
│   └── hooks/
│       └── useSearch.ts           # Search hook with debounce
└── components/
    └── search/
        ├── SearchBar.tsx          # Search input
        ├── SearchResults.tsx      # Results display
        └── SearchFilters.tsx      # Filter controls
```

## Acceptance Criteria

- [ ] Can search documents using text input
- [ ] Can toggle between semantic and keyword search
- [ ] Search is debounced (doesn't fire on every keystroke)
- [ ] Results show relevance scores
- [ ] Results show execution time
- [ ] Can filter by year
- [ ] Can filter by source
- [ ] Can clear filters
- [ ] Empty query shows no results
- [ ] Loading state during search
- [ ] Error handling for failed searches
- [ ] Results are clickable (navigate to document)
- [ ] Search works in both desktop and VR modes

## Code Example

**useSearch Hook with Debounce:**
```typescript
import { useQuery } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import { documentsApi } from '../api/documents';

export function useSearch(query: string, searchType: 'semantic' | 'keyword' = 'semantic') {
  const [debouncedQuery, setDebouncedQuery] = useState(query);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(query), 300);
    return () => clearTimeout(timer);
  }, [query]);

  return useQuery({
    queryKey: ['documents', 'search', debouncedQuery, searchType],
    queryFn: () => documentsApi.search({
      query: debouncedQuery,
      search_type: searchType,
      limit: 20,
    }),
    enabled: debouncedQuery.length > 0,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}
```

**SearchBar Component:**
```typescript
export function SearchBar() {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState<'semantic' | 'keyword'>('semantic');
  const { data, isLoading } = useSearch(query, searchType);

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search documents..."
      />
      <select value={searchType} onChange={(e) => setSearchType(e.target.value as any)}>
        <option value="semantic">Semantic</option>
        <option value="keyword">Keyword</option>
      </select>
      {isLoading && <LoadingSpinner />}
    </div>
  );
}
```

## Dependencies

- **Depends on:** Issue #32 (Document API Integration)
- **Related to:** Issue #35 (3D Timeline - for result highlighting)

## Estimated Time

6-8 hours

## Phase

Phase 2 - Client Development

## Related Issues

- Issue #32 - Document API Integration (dependency)
- Issue #35 - 3D Timeline Visualization (can integrate search highlighting)
- Server Issue #15 - REST API (completed)

## Testing

- [ ] Test semantic search returns relevant results
- [ ] Test keyword search returns exact matches
- [ ] Test search with filters
- [ ] Test empty query behavior
- [ ] Test search with no results
- [ ] Test network error handling
- [ ] Test debounce (verify doesn't search on every keystroke)

## Documentation

- Server API: http://localhost:8000/docs#/documents/search_documents_api_v1_documents_search_post
- See `CLIENT_API_INTEGRATION_PLAN.md` for architecture
