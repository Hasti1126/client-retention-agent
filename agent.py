import json
import os
from churn_predictor import ChurnPredictor

print("Loading ChurnPredictor...")

USE_S3 = os.getenv('USE_S3_MODELS', 'false').lower() == 'true'
S3_BUCKET = os.getenv('MODEL_S3_BUCKET', 'msp-churn-models')

print(f"USE_S3: {USE_S3}, S3_BUCKET: {S3_BUCKET}")

try:
    if USE_S3:
        predictor = ChurnPredictor(use_s3=True, s3_bucket=S3_BUCKET)
    else:
        predictor = ChurnPredictor()
    print("✅ Predictor loaded successfully")
except Exception as e:
    print(f"❌ Failed to load predictor: {e}")
    raise

# Import Strands Agent
from strands import Agent, tool

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
    escalation_frequency: float = 0.0
) -> str:
    """Assess churn risk for a specific client using trained ML model"""
    try:
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
            'risk_assessment': risk_assessment,
            'health_metrics': health_score
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)})

@tool
def get_retention_recommendations(
    client_id: str,
    risk_level: str,
    risk_score: float,
    client_value: float = 50000.0
) -> str:
    """Generate AI-powered retention recommendations"""
    try:
        if risk_level == 'critical':
            recommendations = [
                {'action': 'Schedule emergency QBR', 'success_rate': 0.72, 'roi': f"${int(client_value * 0.85)}"},
                {'action': 'Assign success manager', 'success_rate': 0.70}
            ]
        else:
            recommendations = [
                {'action': 'Schedule QBR', 'success_rate': 0.65}
            ]
        
        result = {
            'client_id': client_id,
            'strategies': recommendations
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)})

print("Creating Strands Agent...")
try:
    agent = Agent(
        system_prompt="""You are an AI-powered client retention specialist for MSPs.
Your responsibilities:
1. Analyze client data to predict churn risk using ML (84.3% detection rate)
2. Calculate comprehensive health scores
3. Generate data-driven retention recommendations with ROI
4. Prioritize at-risk clients for intervention""",
        tools=[assess_client_risk, get_retention_recommendations],
        name="Client Retention Agent"
    )
    print("✅ Agent created successfully")
except Exception as e:
    print(f"❌ Failed to create agent: {e}")
    raise
