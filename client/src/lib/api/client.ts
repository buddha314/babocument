/**
 * API Client for Babocument Backend
 * 
 * Base client with axios configuration and error handling
 */

import axios, { AxiosError, AxiosInstance } from 'axios';
import type { ApiError } from './types';

// Force network IP for VR headset access
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://192.168.1.200:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds
    });

    // Request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        console.log(`[API] ${response.status} ${response.config.url}`);
        return response;
      },
      (error: AxiosError<ApiError>) => {
        if (error.response) {
          // Server responded with error
          console.error(`[API Error] ${error.response.status}:`, error.response.data);
        } else if (error.request) {
          // Request made but no response
          console.error('[API Error] No response received:', error.message);
        } else {
          // Error setting up request
          console.error('[API Error] Request setup failed:', error.message);
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Get the axios instance for custom requests
   */
  getClient(): AxiosInstance {
    return this.client;
  }

  /**
   * Check if backend is reachable
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await axios.get(`${API_URL}/health`, { timeout: 5000 });
      return response.status === 200;
    } catch (error) {
      console.error('[API] Health check failed:', error);
      return false;
    }
  }
}

// Singleton instance
export const apiClient = new ApiClient();
export default apiClient.getClient();
