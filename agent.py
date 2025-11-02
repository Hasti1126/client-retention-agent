from strands import Agent, tool
from churn_predictor import ChurnPredictor
from typing import Dict, List
import json
from datetime import datetime
import os

# Initialize predictor with S3 support
USE_S3 = os.getenv('USE_S3_MODELS', 'false').lower() == 'true'
S3_BUCKET = os.getenv('MODEL_S3_BUCKET', 'msp-churn-models')

if USE_S3:
    predictor = ChurnPredictor(use_s3=True, s3_bucket=S3_BUCKET)
else:
    predictor = ChurnPredictor()

@tool
def assess_client_risk(
    client_id: str,
    communication_sentiment: float,
    payment_timeliness: float,
    service_utilization: float,
    response_satisfaction: float,
    ticket_frequency_trend: float = 1.0,
    contract_value_trend: float = 0.0,
    contact_engagement: float = 0.5,
    escalation_frequency: float = 0.1
) -> str:
    """Assess churn risk for a specific client using ML model."""
    client_data = {
        'communication_sentiment': communication_sentiment,
        'payment_timeliness': payment_timeliness,
        'service_utilization': service_utilization,
        'response_satisfaction': response_satisfaction,
        'ticket_frequency_trend': ticket_frequency_trend,
        'contract_value_trend': contract_value_trend,
        'contact_engagement': contact_engagement,
        'escalation_frequency': escalation_frequency
    }
    
    risk_assessment = predictor.predict_churn_risk(client_data)
    health_score = predictor.calculate_health_score(client_data)
    
    result = {
        'client_id': client_id,
        'timestamp': datetime.now().isoformat(),
        'risk_assessment': risk_assessment,
        'health_score': health_score,
        'raw_features': client_data
    }
    
    return json.dumps(result, indent=2)

@tool
def get_retention_recommendations(
    risk_level: str,
    key_risk_factors: str,
    client_value: float = 10000.0
) -> str:
    """Generate AI-powered retention strategies based on risk factors."""
    factors = [f.strip() for f in key_risk_factors.split(',')]
    recommendations = []
    
    action_map = {
        'communication_sentiment': {
            'action': 'Schedule immediate stakeholder QBR',
            'priority': 'critical',
            'timeframe': '7 days',
            'success_rate': 0.72,
            'effort': 'medium'
        },
        'payment_timeliness': {
            'action': 'Review billing and payment terms',
            'priority': 'high',
            'timeframe': '14 days',
            'success_rate': 0.68,
            'effort': 'low'
        },
        'service_utilization': {
            'action': 'Offer personalized training on underutilized services',
            'priority': 'medium',
            'timeframe': '30 days',
            'success_rate': 0.65,
            'effort': 'medium'
        },
        'response_satisfaction': {
            'action': 'Assign dedicated success manager',
            'priority': 'high',
            'timeframe': '7 days',
            'success_rate': 0.70,
            'effort': 'high'
        }
    }
    
    for factor in factors:
        if factor in action_map:
            rec = action_map[factor].copy()
            rec['factor'] = factor
            retention_value = client_value * 0.85
            rec['estimated_roi'] = f"${retention_value:,.0f}"
            recommendations.append(rec)
    
    if risk_level in ['critical', 'high']:
        recommendations.append({
            'action': 'Executive escalation - C-level engagement',
            'priority': 'critical',
            'timeframe': '3 days',
            'success_rate': 0.75,
            'effort': 'high',
            'factor': 'overall_risk',
            'estimated_roi': f"${client_value * 0.85:,.0f}"
        })
    
    result = {
        'risk_level': risk_level,
        'total_recommendations': len(recommendations),
        'estimated_retention_value': f"${client_value * 0.85:,.0f}",
        'recommendations': sorted(recommendations, key=lambda x: x['success_rate'], reverse=True)
    }
    
    return json.dumps(result, indent=2)

@tool
def batch_analyze_clients(clients_json: str) -> str:
    """Analyze multiple clients and prioritize by risk."""
    try:
        clients = json.loads(clients_json)
    except json.JSONDecodeError:
        return json.dumps({'error': 'Invalid JSON format'})
    
    results = []
    for client in clients:
        client_id = client.get('client_id', 'Unknown')
        risk = predictor.predict_churn_risk(client)
        health = predictor.calculate_health_score(client)
        
        results.append({
            'client_id': client_id,
            'company_name': client.get('company_name', 'N/A'),
            'risk_score': risk['risk_score'],
            'risk_level': risk['risk_level'],
            'health_score': health['total_health_score'],
            'is_at_risk': risk['is_at_risk'],
            'top_risk_factor': risk['key_risk_factors'][0][0] if risk['key_risk_factors'] else 'none'
        })
    
    results.sort(key=lambda x: x['risk_score'], reverse=True)
    
    summary = {
        'total_clients': len(results),
        'at_risk_count': len([c for c in results if c['is_at_risk']]),
        'risk_distribution': {
            'critical': len([c for c in results if c['risk_level'] == 'critical']),
            'high': len([c for c in results if c['risk_level'] == 'high']),
            'medium': len([c for c in results if c['risk_level'] == 'medium']),
            'low': len([c for c in results if c['risk_level'] == 'low'])
        },
        'top_10_at_risk': results[:10],
        'timestamp': datetime.now().isoformat()
    }
    
    return json.dumps(summary, indent=2)

# Create the agent
agent = Agent(
    system_prompt="""You are an AI-powered client retention specialist for MSPs.

Your responsibilities:
1. Analyze client data to predict churn risk using ML (84.3% detection rate)
2. Calculate comprehensive health scores
3. Generate data-driven retention recommendations
4. Prioritize at-risk clients for intervention

Always provide clear risk levels, actionable recommendations, and ROI estimates.""",
    tools=[assess_client_risk, get_retention_recommendations, batch_analyze_clients],
    name="Client Retention Agent"
)

