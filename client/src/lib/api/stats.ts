/**
 * Stats API Client
 * 
 * Methods for getting system statistics
 */

import apiClient from './client';
import type { SystemStats, AllStats } from './types';

export const statsApi = {
  /**
   * Get system statistics
   */
  async getSystemStats(): Promise<SystemStats> {
    const response = await apiClient.get<SystemStats>('/stats');
    return response.data;
  },

  /**
   * Get all statistics (system + document analytics)
   */
  async getAllStats(): Promise<AllStats> {
    const response = await apiClient.get<AllStats>('/stats/all');
    return response.data;
  },
};
