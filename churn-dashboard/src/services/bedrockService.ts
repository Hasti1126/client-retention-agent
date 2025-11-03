import axios from 'axios';
import { ClientData, AnalysisResult, Recommendation } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

export const bedrockService = {
  // Analyze churn risk via backend
  async analyzeChurnRisk(clientData: ClientData): Promise<AnalysisResult> {
    try {
      const response = await axios.post(`${API_URL}/invocations`, {
        prompt: `Analyze churn risk for client ${clientData.client_id}`,
        data: clientData
      });
      
      // Parse response from Bedrock AgentCore
      const output = response.data?.output?.message;
      if (typeof output === 'string') {
        return JSON.parse(output);
      }
      return response.data;
    } catch (error) {
      console.error('Backend error:', error);
      throw error;
    }
  },

  // Get AI recommendations from backend
  async getRecommendations(clientId: string, riskLevel: string): Promise<Recommendation[]> {
    try {
      const response = await axios.post(`${API_URL}/invocations`, {
        prompt: `Get retention recommendations for ${clientId} with ${riskLevel} risk`
      });
      
      const output = response.data?.output?.message;
      if (typeof output === 'string') {
        const parsed = JSON.parse(output);
        return parsed.strategies || [];
      }
      return response.data.strategies || [];
    } catch (error) {
      console.error('Backend error:', error);
      throw error;
    }
  },

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await axios.get(`${API_URL}/health`, { timeout: 5000 });
      return response.status === 200;
    } catch {
      return false;
    }
  }
};
