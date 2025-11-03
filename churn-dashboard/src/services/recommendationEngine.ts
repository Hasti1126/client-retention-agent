import { ClientData } from '../types';

interface Recommendation {
  action: string;
  priority: 'high' | 'medium' | 'low';
  success_rate: number;
  roi: string;
  timeframe: string;
  description: string;
}

export const recommendationEngine = {
  generateRecommendations: (clientData: ClientData, riskLevel: string, sentiment: number): Recommendation[] => {
    const recommendations: Recommendation[] = [];

    // Risk-based recommendations
    if (riskLevel === 'critical') {
      recommendations.push({
        action: '🚨 Schedule Emergency QBR',
        priority: 'high',
        success_rate: 0.87,
        roi: '$42,500',
        timeframe: 'Within 7 days',
        description: 'Immediate executive business review to address critical concerns and demonstrate value'
      });

      recommendations.push({
        action: '🎁 Offer Service Credit or Discount',
        priority: 'high',
        success_rate: 0.84,
        roi: '$38,000',
        timeframe: 'Immediate',
        description: 'Goodwill gesture to restore confidence and show commitment to partnership'
      });

      recommendations.push({
        action: '👥 Assign Dedicated Success Manager',
        priority: 'high',
        success_rate: 0.81,
        roi: '$35,500',
        timeframe: 'Within 3 days',
        description: 'Personal account management to rebuild relationship and ensure satisfaction'
      });
    }

    if (riskLevel === 'high') {
      recommendations.push({
        action: '📅 Schedule Business Review',
        priority: 'high',
        success_rate: 0.78,
        roi: '$32,000',
        timeframe: 'Within 14 days',
        description: 'Formal QBR to understand needs and demonstrate strategic value'
      });

      recommendations.push({
        action: '📊 Showcase ROI & Usage Analytics',
        priority: 'medium',
        success_rate: 0.72,
        roi: '$28,000',
        timeframe: 'This week',
        description: 'Provide concrete data on service value and utilization improvements'
      });

      recommendations.push({
        action: '🎯 Service Utilization Training',
        priority: 'medium',
        success_rate: 0.68,
        roi: '$24,000',
        timeframe: 'Within 10 days',
        description: 'Help client maximize current service adoption and ROI'
      });
    }

    if (riskLevel === 'medium') {
      recommendations.push({
        action: '💬 Regular Check-in Call',
        priority: 'medium',
        success_rate: 0.65,
        roi: '$18,000',
        timeframe: 'This month',
        description: 'Stay connected and proactively address emerging concerns'
      });

      recommendations.push({
        action: '📚 Share Best Practice Resources',
        priority: 'low',
        success_rate: 0.60,
        roi: '$14,000',
        timeframe: 'This week',
        description: 'Provide educational content to increase engagement and value perception'
      });
    }

    if (riskLevel === 'low' || riskLevel === 'healthy') {
      recommendations.push({
        action: '🚀 Identify Upsell Opportunities',
        priority: 'medium',
        success_rate: 0.75,
        roi: '$45,000',
        timeframe: 'This month',
        description: 'Analyze usage patterns to recommend complementary services for growth'
      });

      recommendations.push({
        action: '🎉 Recognize & Celebrate Success',
        priority: 'low',
        success_rate: 0.62,
        roi: '$12,000',
        timeframe: 'Ongoing',
        description: 'Share success stories and metrics to strengthen relationship'
      });
    }

    // Sentiment-based recommendations
    if (sentiment < 0.4) {
      recommendations.push({
        action: '🤝 Personal Outreach from Leadership',
        priority: 'high',
        success_rate: 0.82,
        roi: '$40,000',
        timeframe: 'Within 5 days',
        description: 'CEO/VP outreach to signal importance of relationship and address issues'
      });
    }

    // Engagement-based recommendations
    if (clientData.contact_engagement < 0.3) {
      recommendations.push({
        action: '📞 Increase Touchpoint Frequency',
        priority: 'medium',
        success_rate: 0.70,
        roi: '$25,000',
        timeframe: 'Starting immediately',
        description: 'Establish regular weekly/bi-weekly communication cadence'
      });
    }

    // Utilization-based recommendations
    if (clientData.service_utilization < 0.5) {
      recommendations.push({
        action: '🔍 Comprehensive Service Audit',
        priority: 'medium',
        success_rate: 0.76,
        roi: '$35,000',
        timeframe: 'Within 2 weeks',
        description: 'Identify underutilized services and create adoption plan'
      });

      recommendations.push({
        action: '📈 Cross-sell Complementary Services',
        priority: 'medium',
        success_rate: 0.68,
        roi: '$42,000',
        timeframe: 'This month',
        description: 'Bundle services to increase value and stickiness'
      });
    }

    // Sort by priority and success rate
    return recommendations.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      }
      return b.success_rate - a.success_rate;
    });
  },

  calculateSuccessProbability: (recommendation: Recommendation): number => {
    return recommendation.success_rate;
  },

  getActionTemplate: (action: string): string => {
    const templates: { [key: string]: string } = {
      'Schedule Emergency QBR': 'Send calendar invite for 1-hour executive business review. Agenda: Current challenges, value delivered, strategic alignment.',
      'Assign Dedicated Success Manager': 'Introduce dedicated account manager with direct contact. Schedule monthly check-ins.',
      'Service Utilization Training': 'Offer 90-minute training session covering advanced features and best practices.',
      'Increase Touchpoint Frequency': 'Establish weekly 15-min sync calls and monthly strategy sessions.'
    };
    return templates[action] || 'Execute recommended action based on client needs and preferences.';
  }
};
