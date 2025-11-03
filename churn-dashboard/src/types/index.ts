export interface RiskAssessment {
  churn_probability: number;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
}

export interface HealthMetrics {
  total_health_score: number;
}

export interface ClientData {
  client_id: string;
  communication_sentiment: number;
  payment_timeliness: number;
  service_utilization: number;
  response_satisfaction: number;
  ticket_frequency_trend: number;
  contract_value_trend: number;
  contact_engagement: number;
  escalation_frequency: number;
}

export interface AnalysisResult {
  client_id: string;
  risk_assessment: RiskAssessment;
  health_metrics: HealthMetrics;
  model_used: string;
}

export interface Recommendation {
  action: string;
  success_rate: number;
  roi?: string;
}
