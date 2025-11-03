import React from 'react';
import { Recommendation } from '../types';
import { TrendingUp } from 'lucide-react';

interface RecommendationsPanelProps {
  recommendations: Recommendation[];
  loading: boolean;
}

export const RecommendationsPanel: React.FC<RecommendationsPanelProps> = ({ recommendations, loading }) => {
  if (loading) {
    return <div className="text-white">Loading recommendations...</div>;
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <h3 className="text-xl font-bold text-white mb-6">💡 Retention Recommendations</h3>
      <div className="space-y-4">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="bg-gray-700 p-4 rounded-lg hover:bg-gray-600 transition">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="font-semibold text-white flex items-center gap-2">
                  <TrendingUp size={18} className="text-green-400" />
                  {rec.action}
                </p>
                <p className="text-gray-400 text-sm mt-1">Success Rate: {(rec.success_rate * 100).toFixed(0)}%</p>
              </div>
              {rec.roi && (
                <div className="text-right">
                  <p className="font-bold text-green-400">{rec.roi}</p>
                  <p className="text-gray-400 text-xs">Estimated ROI</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
