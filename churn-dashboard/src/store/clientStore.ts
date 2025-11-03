import { create } from 'zustand';
import { ClientData, AnalysisResult } from '../types';

interface ClientStore {
  currentClient: ClientData;
  analysisResult: AnalysisResult | null;
  loading: boolean;
  error: string | null;
  setClientData: (data: Partial<ClientData>) => void;
  setAnalysisResult: (result: AnalysisResult) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  resetClient: () => void;
}

const defaultClient: ClientData = {
  client_id: 'CLT_001',
  communication_sentiment: -0.3,
  payment_timeliness: -5,
  service_utilization: 0.45,
  response_satisfaction: 0.6,
  ticket_frequency_trend: 1.5,
  contract_value_trend: -0.1,
  contact_engagement: 0.4,
  escalation_frequency: 0.2,
};

export const useClientStore = create<ClientStore>((set) => ({
  currentClient: defaultClient,
  analysisResult: null,
  loading: false,
  error: null,
  setClientData: (data) => set((state) => ({
    currentClient: { ...state.currentClient, ...data }
  })),
  setAnalysisResult: (result) => set({ analysisResult: result }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  resetClient: () => set({
    currentClient: defaultClient,
    analysisResult: null,
    error: null
  })
}));
