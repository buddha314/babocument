/**
 * Document API Client
 * 
 * Methods for interacting with document endpoints
 */

import apiClient from './client';
import type {
  Document,
  DocumentList,
  DocumentContent,
  DocumentUploadResponse,
  SearchRequest,
  SearchResults,
  DocumentSummary,
  PaginationParams,
  DocumentFilters,
} from './types';

export const documentsApi = {
  /**
   * List all documents with optional pagination and filters
   */
  async list(params?: PaginationParams & DocumentFilters): Promise<DocumentList> {
    const response = await apiClient.get<DocumentList>('/documents', { params });
    return response.data;
  },

  /**
   * Get a single document by ID
   */
  async get(documentId: string): Promise<Document> {
    const response = await apiClient.get<Document>(`/documents/${documentId}`);
    return response.data;
  },

  /**
   * Get document full text content
   */
  async getContent(documentId: string): Promise<DocumentContent> {
    const response = await apiClient.get<DocumentContent>(`/documents/${documentId}/content`);
    return response.data;
  },

  /**
   * Search documents
   */
  async search(request: SearchRequest): Promise<SearchResults> {
    const response = await apiClient.post<SearchResults>('/documents/search', request);
    return response.data;
  },

  /**
   * Upload a PDF document
   */
  async upload(
    file: File,
    metadata?: {
      title?: string;
      authors?: string[];
      year?: number;
      source?: string;
    }
  ): Promise<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    if (metadata) {
      Object.entries(metadata).forEach(([key, value]) => {
        if (value !== undefined) {
          formData.append(key, typeof value === 'object' ? JSON.stringify(value) : String(value));
        }
      });
    }

    const response = await apiClient.post<DocumentUploadResponse>('/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Delete a document
   */
  async delete(documentId: string): Promise<void> {
    await apiClient.delete(`/documents/${documentId}`);
  },

  /**
   * Generate or get document summary
   */
  async getSummary(documentId: string, maxLength?: number): Promise<DocumentSummary> {
    const response = await apiClient.get<DocumentSummary>(
      `/documents/${documentId}/summary`,
      { params: { max_length: maxLength } }
    );
    return response.data;
  },
};
