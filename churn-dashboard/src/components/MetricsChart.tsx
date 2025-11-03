import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ClientData } from '../types';

interface MetricsChartProps {
  clientData: ClientData;
}

export const MetricsChart: React.FC<MetricsChartProps> = ({ clientData }) => {
  const data = [
    { name: 'Communication', value: (clientData.communication_sentiment + 1) * 50 },
    { name: 'Payment', value: Math.max(0, Math.min(100, 100 - Math.abs(clientData.payment_timeliness) * 2)) },
    { name: 'Service Util.', value: clientData.service_utilization * 100 },
    { name: 'Satisfaction', value: clientData.response_satisfaction * 100 },
    { name: 'Engagement', value: clientData.contact_engagement * 100 }
  ];

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <h3 className="text-xl font-bold text-white mb-6">📊 Client Metrics</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis dataKey="name" stroke="#999" />
          <YAxis domain={[0, 100]} stroke="#999" />
          <Tooltip contentStyle={{ backgroundColor: '#333', border: '1px solid #666' }} />
          <Bar dataKey="value" fill="#3B82F6" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
