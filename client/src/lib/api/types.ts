/**
 * TypeScript types for Babocument API
 * 
 * Generated from FastAPI server OpenAPI schema
 */

// Document Types
export interface Document {
  id: string;
  title: string;
  authors: string[];
  year: number;
  source: string;
  abstract?: string;
  doi?: string;
  indexed_at?: string;
  metadata?: Record<string, any>;
}

export interface DocumentList {
  documents: Document[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

export interface DocumentContent {
  document_id: string;
  full_text: string;
  sections: {
    title: string;
    content: string;
  }[];
  metadata: Record<string, any>;
}

export interface DocumentUploadResponse {
  document_id: string;
  title: string;
  authors: string[];
  year: number;
  source: string;
  message: string;
  indexed: boolean;
}

// Search Types
export interface SearchResult {
  document_id: string;
  title: string;
  authors: string[];
  year: number;
  source: string;
  abstract?: string;
  score: number;
  highlights?: string[];
}

export interface SearchResults {
  query: string;
  search_type: 'semantic' | 'keyword';
  results: SearchResult[];
  total_found: number;
  search_time_ms: number;
}

export interface SearchRequest {
  query: string;
  search_type?: 'semantic' | 'keyword';
  limit?: number;
  filters?: {
    year_min?: number;
    year_max?: number;
    sources?: string[];
  };
}

// Summary Types
export interface DocumentSummary {
  document_id: string;
  summary: string;
  generated_at: string;
  max_length?: number;
}

// Stats Types
export interface SystemStats {
  total_documents: number;
  indexed_documents: number;
  total_size_mb: number;
  uptime_seconds: number;
  environment: string;
}

export interface AllStats {
  system: SystemStats;
  documents_by_year: Record<string, number>;
  documents_by_source: Record<string, number>;
  recent_uploads: Document[];
}

// Repository Types
export interface Repository {
  id: string;
  name: string;
  type: 'mcp' | 'local' | 'external';
  status: 'active' | 'inactive' | 'error';
  url?: string;
  last_sync?: string;
  document_count: number;
}

export interface RepositoryList {
  repositories: Repository[];
  total: number;
}

// Agent Types
export interface AgentTask {
  task_id: string;
  agent_type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: number;
  message?: string;
  result?: any;
  created_at: string;
  updated_at: string;
}

// Error Types
export interface ApiError {
  detail: string;
  status_code?: number;
}

// Pagination
export interface PaginationParams {
  page?: number;
  page_size?: number;
}

// Filters
export interface DocumentFilters {
  year_min?: number;
  year_max?: number;
  sources?: string[];
  indexed_only?: boolean;
}
