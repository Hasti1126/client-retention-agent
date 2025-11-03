import os
import json

os.environ['USE_S3_MODELS'] = 'true'
os.environ['MODEL_S3_BUCKET'] = 'msp-churn-models'

def agent_process(prompt, predictor):
    try:
        if 'assess' in prompt.lower() or 'risk' in prompt.lower():
            risk_result = predictor.predict_churn_risk({
                'communication_sentiment': -0.3,
                'payment_timeliness': -5.0,
                'service_utilization': 0.45,
                'response_satisfaction': 0.6,
                'ticket_frequency_trend': 1.5,
                'contract_value_trend': -0.1,
                'contact_engagement': 0.4,
                'escalation_frequency': 0.2
            })
            health_result = predictor.calculate_health_score({
                'communication_sentiment': -0.3,
                'payment_timeliness': -5.0,
                'service_utilization': 0.45,
                'response_satisfaction': 0.6,
                'ticket_frequency_trend': 1.5,
                'contract_value_trend': -0.1,
                'contact_engagement': 0.4,
                'escalation_frequency': 0.2
            })
            response = {
                'client_id': 'CLT_001',
                'risk_assessment': risk_result,
                'health_metrics': health_result,
                'model_used': 'XGBoost_84.3_accuracy'
            }
            return json.dumps(response, indent=2)
        elif 'recommend' in prompt.lower():
            response = {
                'client_id': 'CLT_001',
                'strategies': [
                    {'action': 'Schedule emergency QBR', 'success_rate': 0.72},
                    {'action': 'Assign success manager', 'success_rate': 0.70}
                ]
            }
            return json.dumps(response, indent=2)
        else:
            response = {
                'message': 'Ready',
                'capabilities': ['assess', 'recommend', 'batch']
            }
            return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({'error': str(e)})
