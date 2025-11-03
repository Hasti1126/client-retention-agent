import React, { useState, useMemo } from 'react';
import { AlertCircle, TrendingDown, TrendingUp, Users, DollarSign, Target, ArrowRight, CheckCircle, Clock, Phone, Mail, Calendar } from 'lucide-react';
import { recommendationEngine } from './services/recommendationEngine';
import { sentimentService } from './services/sentimentService';

// Simulated client data with realistic MSP scenarios
const generateClientData = () => {
  const clients = [
    {
      id: 1, name: "TechCorp Solutions", healthScore: 25, risk: "critical",
      contractValue: 8500, paymentDelay: 18, satisfaction: 2.3, utilization: 0.40,
      sentiment: -0.6, tickets: 28, lastContact: "12 days ago",
      churnProb: 0.78, industry: "Healthcare",
      communication_sentiment: -0.6,
      payment_timeliness: 18,
      service_utilization: 0.40,
      response_satisfaction: 2.3,
      ticket_frequency_trend: 28,
      contract_value_trend: -0.2,
      contact_engagement: 0.2,
      escalation_frequency: 0.6,
      client_id: 'CLT_001'
    },
    {
      id: 2, name: "DataFlow Systems", healthScore: 35, risk: "high",
      contractValue: 6200, paymentDelay: 8, satisfaction: 3.1, utilization: 0.55,
      sentiment: -0.3, tickets: 22, lastContact: "8 days ago",
      churnProb: 0.65, industry: "Finance",
      communication_sentiment: -0.3,
      payment_timeliness: 8,
      service_utilization: 0.55,
      response_satisfaction: 3.1,
      ticket_frequency_trend: 22,
      contract_value_trend: -0.1,
      contact_engagement: 0.4,
      escalation_frequency: 0.4,
      client_id: 'CLT_002'
    },
    {
      id: 3, name: "NetSys Enterprises", healthScore: 42, risk: "high",
      contractValue: 7800, paymentDelay: 5, satisfaction: 3.4, utilization: 0.62,
      sentiment: -0.1, tickets: 18, lastContact: "5 days ago",
      churnProb: 0.58, industry: "Retail",
      communication_sentiment: -0.1,
      payment_timeliness: 5,
      service_utilization: 0.62,
      response_satisfaction: 3.4,
      ticket_frequency_trend: 18,
      contract_value_trend: 0.05,
      contact_engagement: 0.5,
      escalation_frequency: 0.3,
      client_id: 'CLT_003'
    },
    {
      id: 4, name: "CloudFirst Inc", healthScore: 58, risk: "medium",
      contractValue: 5400, paymentDelay: 2, satisfaction: 3.8, utilization: 0.68,
      sentiment: 0.2, tickets: 12, lastContact: "3 days ago",
      churnProb: 0.42, industry: "Technology",
      communication_sentiment: 0.2,
      payment_timeliness: 2,
      service_utilization: 0.68,
      response_satisfaction: 3.8,
      ticket_frequency_trend: 12,
      contract_value_trend: 0.1,
      contact_engagement: 0.65,
      escalation_frequency: 0.2,
      client_id: 'CLT_004'
    },
    {
      id: 5, name: "SecureNet Corp", healthScore: 72, risk: "low",
      contractValue: 9200, paymentDelay: 0, satisfaction: 4.2, utilization: 0.78,
      sentiment: 0.5, tickets: 8, lastContact: "1 day ago",
      churnProb: 0.28, industry: "Legal",
      communication_sentiment: 0.5,
      payment_timeliness: 0,
      service_utilization: 0.78,
      response_satisfaction: 4.2,
      ticket_frequency_trend: 8,
      contract_value_trend: 0.15,
      contact_engagement: 0.8,
      escalation_frequency: 0.1,
      client_id: 'CLT_005'
    },
    {
      id: 6, name: "FastTrack Media", healthScore: 85, risk: "healthy",
      contractValue: 4800, paymentDelay: 0, satisfaction: 4.6, utilization: 0.85,
      sentiment: 0.7, tickets: 5, lastContact: "Today",
      churnProb: 0.15, industry: "Media",
      communication_sentiment: 0.7,
      payment_timeliness: 0,
      service_utilization: 0.85,
      response_satisfaction: 4.6,
      ticket_frequency_trend: 5,
      contract_value_trend: 0.2,
      contact_engagement: 0.9,
      escalation_frequency: 0.05,
      client_id: 'CLT_006'
    },
    {
      id: 7, name: "BuildRight Construction", healthScore: 91, risk: "healthy",
      contractValue: 6700, paymentDelay: 0, satisfaction: 4.8, utilization: 0.92,
      sentiment: 0.8, tickets: 3, lastContact: "Today",
      churnProb: 0.09, industry: "Construction",
      communication_sentiment: 0.8,
      payment_timeliness: 0,
      service_utilization: 0.92,
      response_satisfaction: 4.8,
      ticket_frequency_trend: 3,
      contract_value_trend: 0.25,
      contact_engagement: 0.95,
      escalation_frequency: 0.02,
      client_id: 'CLT_007'
    }
  ];
  return clients;
};

// Enhanced AI recommendation generator with LLM integration
const generateRecommendationsWithLLM = (client: any) => {
  const recs = recommendationEngine.generateRecommendations(
    client,
    client.risk,
    client.sentiment
  );
  
  return recs.map(rec => ({
    action: rec.action,
    priority: rec.priority === 'high' ? 'HIGH' : rec.priority === 'medium' ? 'MEDIUM' : 'LOW',
    successRate: rec.success_rate,
    timeline: rec.timeframe,
    reason: rec.description,
    roi: rec.roi
  }));
};

const App = () => {
  const [selectedClient, setSelectedClient] = useState<any>(null);
  const [view, setView] = useState('dashboard');
  const clients = useMemo(() => generateClientData(), []);
  
  const stats = useMemo(() => {
    const healthy = clients.filter(c => c.healthScore >= 70).length;
    const atRisk = clients.filter(c => c.healthScore >= 40 && c.healthScore < 70).length;
    const critical = clients.filter(c => c.healthScore < 40).length;
    const totalRevenue = clients.reduce((sum, c) => sum + c.contractValue, 0);
    const atRiskRevenue = clients.filter(c => c.healthScore < 70).reduce((sum, c) => sum + c.contractValue, 0);
    
    return { healthy, atRisk, critical, totalRevenue, atRiskRevenue };
  }, [clients]);
  
  const getRiskColor = (risk: string) => {
    switch(risk) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-green-500';
    }
  };
  
  const getRiskTextColor = (risk: string) => {
    switch(risk) {
      case 'critical': return 'text-red-600';
      case 'high': return 'text-orange-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-blue-600';
      default: return 'text-green-600';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                <span className="text-2xl">🧠</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold">NeuroNova</h1>
                <p className="text-sm text-indigo-100">AI-Powered Client Intelligence</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-indigo-100">SuperHack 2025 Prototype</p>
              <p className="text-xs text-indigo-200">Live Demo</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {view === 'dashboard' ? (
          <>
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Healthy Clients</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.healthy}</p>
                    <p className="text-xs text-green-600 mt-1">
                      {((stats.healthy / clients.length) * 100).toFixed(0)}% of portfolio
                    </p>
                  </div>
                  <CheckCircle className="text-green-500" size={32} />
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-yellow-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">At Risk</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.atRisk}</p>
                    <p className="text-xs text-yellow-600 mt-1">
                      {((stats.atRisk / clients.length) * 100).toFixed(0)}% needs attention
                    </p>
                  </div>
                  <AlertCircle className="text-yellow-500" size={32} />
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-red-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Critical</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.critical}</p>
                    <p className="text-xs text-red-600 mt-1">
                      Immediate action required
                    </p>
                  </div>
                  <TrendingDown className="text-red-500" size={32} />
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-indigo-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Revenue at Risk</p>
                    <p className="text-3xl font-bold text-gray-900">${(stats.atRiskRevenue / 1000).toFixed(0)}K</p>
                    <p className="text-xs text-indigo-600 mt-1">
                      Monthly recurring revenue
                    </p>
                  </div>
                  <DollarSign className="text-indigo-500" size={32} />
                </div>
              </div>
            </div>

            {/* Critical Alerts */}
            <div className="bg-white rounded-xl shadow-md p-6 mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <AlertCircle className="text-red-500" size={24} />
                  Critical Alerts
                </h2>
                <span className="text-sm text-gray-500">Powered by AI + LLM</span>
              </div>
              
              <div className="space-y-4">
                {clients.filter(c => c.healthScore < 40).map(client => {
                  const topRec = generateRecommendationsWithLLM(client)[0];
                  return (
                    <div key={client.id} className="border border-red-200 rounded-lg p-4 bg-red-50 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="font-semibold text-lg text-gray-900">{client.name}</h3>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getRiskColor(client.risk)} text-white`}>
                              {client.risk.toUpperCase()}
                            </span>
                            <span className="text-sm text-gray-600">Health Score: {client.healthScore}/100</span>
                          </div>
                          <div className="flex flex-wrap gap-4 text-sm text-gray-700 mb-3">
                            <span>💰 ${client.contractValue.toLocaleString()}/mo</span>
                            <span>📊 {(client.churnProb * 100).toFixed(0)}% churn risk</span>
                            <span>⏱️ Last contact: {client.lastContact}</span>
                          </div>
                          <div className="text-sm text-gray-600 mb-3">
                            <strong>Risk Factors:</strong> Payment delays ({client.paymentDelay} days), 
                            Low satisfaction ({client.satisfaction}/5.0), 
                            Underutilization ({(client.utilization * 100).toFixed(0)}%)
                          </div>
                          <div className="bg-white p-3 rounded border border-indigo-200">
                            <p className="text-sm font-medium text-indigo-900 mb-1">
                              🤖 AI Recommendation (LLM Generated):
                            </p>
                            <p className="text-sm text-gray-700">
                              {topRec?.action} - {topRec?.timeline}
                              <span className="text-green-600 font-medium ml-2">
                                ({(topRec?.successRate * 100).toFixed(0)}% success rate)
                              </span>
                            </p>
                          </div>
                        </div>
                        <button
                          onClick={() => {
                            setSelectedClient(client);
                            setView('detail');
                          }}
                          className="ml-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
                        >
                          View Details
                          <ArrowRight size={16} />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* All Clients Table */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Users size={24} />
                All Clients
              </h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Client</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Health Score</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Risk Level</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">MRR</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Satisfaction</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {clients.map(client => (
                      <tr key={client.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3">
                          <div>
                            <p className="font-medium text-gray-900">{client.name}</p>
                            <p className="text-xs text-gray-500">{client.industry}</p>
                          </div>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            <div className="w-full bg-gray-200 rounded-full h-2 max-w-[100px]">
                              <div
                                className={`h-2 rounded-full ${
                                  client.healthScore >= 70 ? 'bg-green-500' :
                                  client.healthScore >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                                }`}
                                style={{ width: `${client.healthScore}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium text-gray-700">{client.healthScore}</span>
                          </div>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getRiskColor(client.risk)} text-white`}>
                            {client.risk}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-700">
                          ${client.contractValue.toLocaleString()}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-700">
                          {client.satisfaction.toFixed(1)}/5.0
                        </td>
                        <td className="px-4 py-3">
                          <button
                            onClick={() => {
                              setSelectedClient(client);
                              setView('detail');
                            }}
                            className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                          >
                            View →
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        ) : (
          /* Client Detail View */
          <div>
            <button
              onClick={() => setView('dashboard')}
              className="mb-6 text-indigo-600 hover:text-indigo-800 flex items-center gap-2"
            >
              ← Back to Dashboard
            </button>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Client Info */}
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-white rounded-xl shadow-md p-6">
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">{selectedClient.name}</h2>
                      <div className="flex flex-wrap gap-3 text-sm text-gray-600">
                        <span>💼 {selectedClient.industry}</span>
                        <span>💰 ${selectedClient.contractValue.toLocaleString()}/month</span>
                        <span>📅 Client since 2019</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600 mb-1">Health Score</p>
                      <p className={`text-4xl font-bold ${getRiskTextColor(selectedClient.risk)}`}>
                        {selectedClient.healthScore}
                      </p>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskColor(selectedClient.risk)} text-white mt-2 inline-block`}>
                        {selectedClient.risk.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  {/* Risk Factors */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">🎯 Risk Factor Breakdown</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="border border-red-200 rounded-lg p-4 bg-red-50">
                        <p className="text-sm font-semibold text-gray-900 mb-1">Payment Delays</p>
                        <p className="text-2xl font-bold text-red-600 mb-2">-15pts</p>
                        <p className="text-xs text-gray-600 mb-2">HIGH IMPACT</p>
                        <p className="text-sm text-gray-700">Avg: {selectedClient.paymentDelay} days late</p>
                        <p className="text-xs text-gray-500 mt-1">Trend: ⬆️ Getting worse</p>
                      </div>
                      
                      <div className="border border-orange-200 rounded-lg p-4 bg-orange-50">
                        <p className="text-sm font-semibold text-gray-900 mb-1">Low Satisfaction</p>
                        <p className="text-2xl font-bold text-orange-600 mb-2">-12pts</p>
                        <p className="text-xs text-gray-600 mb-2">HIGH IMPACT</p>
                        <p className="text-sm text-gray-700">CSAT: {selectedClient.satisfaction}/5.0</p>
                        <p className="text-xs text-gray-500 mt-1">Trend: ⬇️ Declining</p>
                      </div>
                      
                      <div className="border border-yellow-200 rounded-lg p-4 bg-yellow-50">
                        <p className="text-sm font-semibold text-gray-900 mb-1">Underutilized Services</p>
                        <p className="text-2xl font-bold text-yellow-600 mb-2">-8pts</p>
                        <p className="text-xs text-gray-600 mb-2">MEDIUM IMPACT</p>
                        <p className="text-sm text-gray-700">Only {(selectedClient.utilization * 100).toFixed(0)}% used</p>
                        <p className="text-xs text-gray-500 mt-1">Trend: ➡️ Stable</p>
                      </div>
                    </div>
                  </div>

                  {/* AI Recommendations with LLM */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">🤖 AI Recommendations (LLM + ML)</h3>
                    <div className="space-y-3">
                      {generateRecommendationsWithLLM(selectedClient).map((rec, idx) => (
                        <div key={idx} className="border border-indigo-200 rounded-lg p-4 bg-indigo-50">
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <span className="font-semibold text-gray-900">{idx + 1}. {rec.action}</span>
                                <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                                  rec.priority === 'HIGH' ? 'bg-red-100 text-red-700' : rec.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                                }`}>
                                  {rec.priority}
                                </span>
                              </div>
                              <p className="text-sm text-gray-600 mb-2">{rec.reason}</p>
                              <div className="flex gap-4 text-xs text-gray-500">
                                <span>⏱️ {rec.timeline}</span>
                                {rec.roi && <span>💰 ROI: {rec.roi}</span>}
                              </div>
                            </div>
                            <div className="text-right ml-4">
                              <p className="text-sm text-gray-600 mb-1">Success Rate</p>
                              <p className="text-2xl font-bold text-green-600">{(rec.successRate * 100).toFixed(0)}%</p>
                            </div>
                          </div>
                          <div className="mt-3 flex gap-2">
                            <button className="px-3 py-1.5 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
                              Execute Plan
                            </button>
                            <button className="px-3 py-1.5 bg-gray-200 text-gray-700 rounded text-sm hover:bg-gray-300">
                              Customize
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Key Metrics</h3>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Churn Probability</span>
                        <span className="font-semibold text-red-600">{(selectedClient.churnProb * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-red-500 h-2 rounded-full" style={{ width: `${selectedClient.churnProb * 100}%` }} />
                      </div>
                    </div>
                    
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Service Utilization</span>
                        <span className="font-semibold text-yellow-600">{(selectedClient.utilization * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${selectedClient.utilization * 100}%` }} />
                      </div>
                    </div>
                    
                    <div className="pt-4 border-t">
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-600">Support Tickets (30d)</span>
                        <span className="font-semibold">{selectedClient.tickets}</span>
                      </div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-600">Sentiment Score</span>
                        <span className={`font-semibold ${selectedClient.sentiment > 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {selectedClient.sentiment > 0 ? '+' : ''}{selectedClient.sentiment.toFixed(1)}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Last Contact</span>
                        <span className="font-semibold">{selectedClient.lastContact}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">⚡ Quick Actions</h3>
                  <div className="space-y-2">
                    <button className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2">
                      <Phone size={16} />
                      Call Client
                    </button>
                    <button className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 flex items-center gap-2">
                      <Mail size={16} />
                      Send Email
                    </button>
                    <button className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 flex items-center gap-2">
                      <Calendar size={16} />
                      Schedule Meeting
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-gray-800 text-white py-6 mt-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-sm">NeuroNova - SuperHack 2025 Prototype</p>
          <p className="text-xs text-gray-400 mt-1">Igniting the Future of AI for a Sustainable World</p>
        </div>
      </div>
    </div>
  );
};

export default App;
