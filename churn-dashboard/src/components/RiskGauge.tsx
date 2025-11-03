import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface RiskGaugeProps {
  riskScore: number;
  riskLevel: string;
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({ riskScore, riskLevel }) => {
  const data = [{ name: 'Risk Score', value: riskScore }];
  
  const getRiskColor = (score: number) => {
    if (score >= 70) return '#EF4444';
    if (score >= 55) return '#F97316';
    if (score >= 40) return '#EAB308';
    return '#22C55E';
  };

  const getRiskBadge = (level: string) => {
    const badges = {
      critical: { emoji: '🔴', bg: 'bg-red-900', text: 'CRITICAL' },
      high: { emoji: '🟠', bg: 'bg-orange-900', text: 'HIGH' },
      medium: { emoji: '🟡', bg: 'bg-yellow-900', text: 'MEDIUM' },
      low: { emoji: '🟢', bg: 'bg-green-900', text: 'LOW' }
    };
    return badges[level as keyof typeof badges] || badges.medium;
  };

  const badge = getRiskBadge(riskLevel);

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-white">Risk Assessment</h3>
        <div className={`${badge.bg} px-4 py-2 rounded-full text-white font-bold`}>
          {badge.emoji} {badge.text}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis dataKey="name" stroke="#999" />
          <YAxis domain={[0, 100]} stroke="#999" />
          <Tooltip contentStyle={{ backgroundColor: '#333', border: '1px solid #666' }} />
          <Bar dataKey="value" fill={getRiskColor(riskScore)} radius={[8, 8, 0, 0]}>
            <Cell fill={getRiskColor(riskScore)} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-gray-700 p-4 rounded">
          <p className="text-gray-400 text-sm">Risk Score</p>
          <p className="text-3xl font-bold text-white">{riskScore}%</p>
        </div>
        <div className="bg-gray-700 p-4 rounded">
          <p className="text-gray-400 text-sm">Churn Probability</p>
          <p className="text-3xl font-bold text-blue-400">{(riskScore / 100).toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
};
