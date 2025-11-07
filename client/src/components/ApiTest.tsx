/**
 * API Test Component
 * 
 * Simple component to test backend connectivity and data flow
 */

'use client';

import { useEffect, useState } from 'react';
import { apiClient, documentsApi, statsApi } from '@/lib/api';
import type { Document, SystemStats } from '@/lib/api';

export default function ApiTest() {
  const [connectionStatus, setConnectionStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [apiUrl] = useState(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

  useEffect(() => {
    checkConnection();
  }, []);

  async function checkConnection() {
    setLoading(true);
    setError(null);

    try {
      // Check health
      const healthy = await apiClient.healthCheck();
      setConnectionStatus(healthy ? 'connected' : 'disconnected');

      if (!healthy) {
        setError(`Backend server is not responding. Make sure it's running on ${apiUrl}`);
        setLoading(false);
        return;
      }

      // Fetch stats
      const statsData = await statsApi.getSystemStats();
      setStats(statsData);

      // Fetch documents
      const docsData = await documentsApi.list({ page: 1, page_size: 10 });
      setDocuments(docsData.documents);

      setLoading(false);
    } catch (err) {
      console.error('Connection test failed:', err);
      setConnectionStatus('disconnected');
      setError(err instanceof Error ? err.message : 'Failed to connect to backend');
      setLoading(false);
    }
  }

  return (
    <div className="fixed top-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-6 max-w-md z-50 max-h-[80vh] overflow-y-auto">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-800">Backend API Test</h2>
          <button
            onClick={checkConnection}
            disabled={loading}
            className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? 'Testing...' : 'Refresh'}
          </button>
        </div>

        {/* Connection Status */}
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${
            connectionStatus === 'connected' ? 'bg-green-500' :
            connectionStatus === 'disconnected' ? 'bg-red-500' :
            'bg-yellow-500 animate-pulse'
          }`} />
          <span className="text-sm font-medium text-gray-700">
            {connectionStatus === 'connected' ? 'Connected' :
             connectionStatus === 'disconnected' ? 'Disconnected' :
             'Checking...'}
          </span>
        </div>

        {/* API URL Display */}
        <div className="text-xs text-gray-500 border-t pt-2">
          <div>API: {apiUrl}</div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Stats */}
        {stats && (
          <div className="border-t pt-4">
            <h3 className="font-semibold text-gray-700 mb-2">System Stats</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-gray-500">Documents:</span>
                <span className="ml-2 font-medium">{stats.total_documents ?? 0}</span>
              </div>
              <div>
                <span className="text-gray-500">Indexed:</span>
                <span className="ml-2 font-medium">{stats.indexed_documents ?? 0}</span>
              </div>
              <div>
                <span className="text-gray-500">Size:</span>
                <span className="ml-2 font-medium">{(stats.storage_used_mb ?? 0).toFixed(2)} MB</span>
              </div>
              <div>
                <span className="text-gray-500">Uptime:</span>
                <span className="ml-2 font-medium">{Math.floor((stats.uptime_seconds ?? 0) / 60)}m</span>
              </div>
            </div>
          </div>
        )}

        {/* Documents List */}
        {documents.length > 0 && (
          <div className="border-t pt-4">
            <h3 className="font-semibold text-gray-700 mb-2">Recent Documents ({documents.length})</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {documents.map((doc) => {
                const authors = doc.authors || [];
                const authorText = authors.length > 0 
                  ? authors.slice(0, 2).join(', ') + (authors.length > 2 ? ` +${authors.length - 2} more` : '')
                  : 'Unknown authors';
                
                return (
                  <div key={doc.id} className="p-2 bg-gray-50 rounded text-xs">
                    <div className="font-medium text-gray-800 truncate">{doc.title || 'Untitled'}</div>
                    <div className="text-gray-500 mt-1">
                      {authorText}
                    </div>
                    <div className="text-gray-400 mt-1">
                      {doc.year || 'N/A'} • {doc.source || 'Unknown'}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* No Documents */}
        {!loading && documents.length === 0 && connectionStatus === 'connected' && (
          <div className="border-t pt-4">
            <p className="text-sm text-gray-500 text-center py-4">
              No documents in database yet.
            </p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block w-8 h-8 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin" />
            <p className="mt-2 text-sm text-gray-500">Loading data...</p>
          </div>
        )}
      </div>
    </div>
  );
}
