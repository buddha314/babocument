---
name: Document API Integration (Client)
about: Implement document management features in BabylonJS client
title: 'Document API Integration (Client)'
labels: 'client, api, documents, P0, phase-2'
assignees: ''
---

## Summary

Implement document management features in the BabylonJS client using the server's REST API. This includes listing, viewing, uploading, deleting, and searching documents.

## Background

The server provides 7 document endpoints:
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document metadata
- `GET /api/v1/documents/{id}/content` - Get full content
- `POST /api/v1/documents` - Upload document
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/documents/search` - Search documents
- `GET /api/v1/documents/{id}/summary` - Generate AI summary

## Tasks

### 1. Create Document API Methods
- [ ] Create `client/src/lib/api/documents.ts`
  - `documentsApi.list(params)` - List documents with pagination
  - `documentsApi.get(id)` - Get document metadata
  - `documentsApi.getContent(id)` - Get full content
  - `documentsApi.upload(file, metadata)` - Upload PDF
  - `documentsApi.delete(id)` - Delete document
  - `documentsApi.search(query)` - Search documents
  - `documentsApi.getSummary(id, maxLength)` - Get AI summary

### 2. Create React Query Hooks
- [ ] Create `client/src/lib/hooks/useDocuments.ts`
  - `useDocuments(params)` - List documents
  - `useDocument(id)` - Get single document
  - `useDocumentContent(id)` - Get document content
  - `useSearch(query)` - Search documents
  - `useUploadDocument()` - Upload mutation
  - `useDeleteDocument()` - Delete mutation
  - Define query keys for cache invalidation

### 3. Build DocumentList Component
- [ ] Create `client/src/components/documents/DocumentList.tsx`
  - Display paginated list of documents
  - Show title, authors, year, source
  - Add pagination controls
  - Add loading states
  - Handle errors gracefully
  - Click to view document details

### 4. Build DocumentViewer Component
- [ ] Create `client/src/components/documents/DocumentViewer.tsx`
  - Display document metadata
  - Show document content
  - Add "Generate Summary" button
  - Display AI summary when generated
  - Add "Delete" button with confirmation
  - Handle loading and error states

### 5. Build DocumentUploader Component
- [ ] Create `client/src/components/documents/DocumentUploader.tsx`
  - File input for PDF files
  - Optional metadata fields (title, authors, year)
  - Upload progress indicator
  - Success/error notifications
  - Validate file type (PDF only)
  - Handle upload errors

### 6. Test All Operations
- [ ] Test listing documents
- [ ] Test viewing document details
- [ ] Test document search (semantic & keyword)
- [ ] Test uploading PDFs
- [ ] Test deleting documents
- [ ] Test error cases (404, 500, network errors)
- [ ] Test cache invalidation after mutations

## Files to Create

```
client/src/
├── lib/
│   ├── api/
│   │   └── documents.ts           # Document API methods
│   └── hooks/
│       └── useDocuments.ts        # React Query hooks
└── components/
    └── documents/
        ├── DocumentList.tsx       # List view
        ├── DocumentViewer.tsx     # Detail view
        ├── DocumentUploader.tsx   # Upload form
        └── DocumentCard.tsx       # List item (optional)
```

## Acceptance Criteria

- [ ] Can list all documents with pagination
- [ ] Can view document details
- [ ] Can view full document content
- [ ] Can upload new PDF documents
- [ ] Can delete documents
- [ ] Can search documents (semantic & keyword)
- [ ] Can generate AI summaries
- [ ] Loading states show during API calls
- [ ] Errors are handled and displayed to user
- [ ] React Query cache is properly invalidated
- [ ] UI updates optimistically where appropriate

## Code Example

**useDocuments Hook:**
```typescript
export function useDocuments(params?: { limit?: number; offset?: number }) {
  return useQuery({
    queryKey: ['documents', 'list', params],
    queryFn: () => documentsApi.list(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ file, metadata }) => documentsApi.upload(file, metadata),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents', 'list'] });
    },
  });
}
```

## Dependencies

- **Depends on:** Issue #30 (Client API Infrastructure)
- **Blocks:** Issue #35 (3D Timeline Visualization)

## Estimated Time

8-12 hours

## Phase

Phase 2 - Client Development

## Related Issues

- Issue #30 - Client API Infrastructure (dependency)
- Issue #33 - Search Integration (related)
- Issue #35 - 3D Timeline Visualization (blocked by this)

## Documentation

- Server API: http://localhost:8000/docs
- See `CLIENT_API_INTEGRATION_PLAN.md` for full examples
