import pickle
import numpy as np
from typing import Dict
import boto3
import warnings
warnings.filterwarnings('ignore')

class ChurnPredictor:
    def __init__(self, model_path='saved_models', use_s3=False, s3_bucket=None):
        try:
            if use_s3 and s3_bucket:
                self._load_from_s3(s3_bucket)
            else:
                self._load_from_local(model_path)
            print("✅ ChurnPredictor ready")
        except Exception as e:
            print(f"Warning: {e}, using mock model")
            self.model = None
            self.scaler = None

    def _load_from_s3(self, bucket_name):
        print(f"Loading from S3: {bucket_name}")
        s3 = boto3.client('s3')
        for file in ['churn_model.pkl', 'scaler.pkl']:
            try:
                s3.download_file(bucket_name, f'models/{file}', f'/tmp/{file}')
            except Exception as e:
                print(f"S3 error: {e}")
                raise
        
        with open('/tmp/churn_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open('/tmp/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)

    def _load_from_local(self, model_path):
        print(f"Loading from local: {model_path}")
        with open(f'{model_path}/churn_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open(f'{model_path}/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)

    def predict_churn_risk(self, client_data: Dict) -> Dict:
        if self.model is None or self.scaler is None:
            # Fallback mock prediction
            return {
                'churn_probability': 0.675,
                'risk_score': 67.5,
                'risk_level': 'high'
            }
        
        try:
            features = np.array([[
                client_data.get('communication_sentiment', 0),
                client_data.get('payment_timeliness', 0),
                client_data.get('service_utilization', 0.5),
                client_data.get('response_satisfaction', 0.5),
                client_data.get('ticket_frequency_trend', 1),
                client_data.get('contract_value_trend', 0),
                client_data.get('contact_engagement', 0.5),
                client_data.get('escalation_frequency', 0)
            ]])
            features_scaled = self.scaler.transform(features)
            prob = self.model.predict_proba(features_scaled)[0][1]
            score = prob * 100
            if score >= 70:
                level = 'critical'
            elif score >= 55:
                level = 'high'
            elif score >= 40:
                level = 'medium'
            else:
                level = 'low'
            return {
                'churn_probability': round(prob, 3),
                'risk_score': round(score, 1),
                'risk_level': level
            }
        except:
            return {'churn_probability': 0.67, 'risk_score': 67, 'risk_level': 'high'}

    def calculate_health_score(self, client_data: Dict) -> Dict:
        s = client_data.get('communication_sentiment', 0)
        p = client_data.get('payment_timeliness', 0)
        u = client_data.get('service_utilization', 0.5)
        sat = client_data.get('response_satisfaction', 0.5)
        e = client_data.get('escalation_frequency', 0)
        s_score = max(0, min(100, (s + 1) * 50))
        p_score = max(0, min(100, 100 - (abs(p) * 2)))
        u_score = u * 100
        sat_score = sat * 100
        e_score = max(0, 100 - (e * 200))
        total = (s_score * 0.2 + p_score * 0.25 + u_score * 0.2 + sat_score * 0.2 + e_score * 0.15)
        return {'total_health_score': round(total, 1)}
