import React from 'react';
import { useClientStore } from '../store/clientStore';

interface SidebarProps {
  onAnalyze: () => void;
  loading: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({ onAnalyze, loading }) => {
  const { currentClient, setClientData, resetClient } = useClientStore();

  return (
    <aside className="w-80 bg-gray-900 text-white p-6 overflow-y-auto border-r border-gray-700">
      <h2 className="text-2xl font-bold mb-6">⚙️ Client Config</h2>
      
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Client ID</label>
        <input
          type="text"
          value={currentClient.client_id}
          onChange={(e) => setClientData({ client_id: e.target.value })}
          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white focus:outline-none focus:border-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Communication Sentiment: <span className="text-blue-400">{currentClient.communication_sentiment.toFixed(2)}</span>
        </label>
        <input
          type="range"
          min="-1"
          max="1"
          step="0.1"
          value={currentClient.communication_sentiment}
          onChange={(e) => setClientData({ communication_sentiment: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Payment Timeliness: <span className="text-blue-400">{currentClient.payment_timeliness.toFixed(1)}</span>
        </label>
        <input
          type="range"
          min="-10"
          max="10"
          step="1"
          value={currentClient.payment_timeliness}
          onChange={(e) => setClientData({ payment_timeliness: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Service Utilization: <span className="text-blue-400">{(currentClient.service_utilization * 100).toFixed(0)}%</span>
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={currentClient.service_utilization}
          onChange={(e) => setClientData({ service_utilization: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Response Satisfaction: <span className="text-blue-400">{(currentClient.response_satisfaction * 100).toFixed(0)}%</span>
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={currentClient.response_satisfaction}
          onChange={(e) => setClientData({ response_satisfaction: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Ticket Frequency: <span className="text-blue-400">{currentClient.ticket_frequency_trend.toFixed(1)}</span>
        </label>
        <input
          type="range"
          min="0"
          max="5"
          step="0.5"
          value={currentClient.ticket_frequency_trend}
          onChange={(e) => setClientData({ ticket_frequency_trend: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Contract Value Trend: <span className="text-blue-400">{currentClient.contract_value_trend.toFixed(2)}</span>
        </label>
        <input
          type="range"
          min="-1"
          max="1"
          step="0.1"
          value={currentClient.contract_value_trend}
          onChange={(e) => setClientData({ contract_value_trend: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Contact Engagement: <span className="text-blue-400">{(currentClient.contact_engagement * 100).toFixed(0)}%</span>
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={currentClient.contact_engagement}
          onChange={(e) => setClientData({ contact_engagement: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="mb-8">
        <label className="block text-sm font-medium mb-2">
          Escalation Frequency: <span className="text-blue-400">{(currentClient.escalation_frequency * 100).toFixed(0)}%</span>
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={currentClient.escalation_frequency}
          onChange={(e) => setClientData({ escalation_frequency: parseFloat(e.target.value) })}
          className="w-full h-2 bg-gray-700 rounded cursor-pointer accent-blue-500"
        />
      </div>

      <div className="space-y-3 mt-8 border-t border-gray-700 pt-6">
        <button
          onClick={onAnalyze}
          disabled={loading}
          className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded transition"
        >
          {loading ? '⏳ Analyzing...' : '🚀 Analyze Client'}
        </button>
        <button
          onClick={resetClient}
          className="w-full px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded transition"
        >
          ↺ Reset Defaults
        </button>
      </div>
    </aside>
  );
};
