import pickle
import numpy as np
from typing import Dict, List, Tuple
import json
import boto3
import os

class ChurnPredictor:
    def __init__(self, model_path='saved_models', use_s3=False, s3_bucket=None):
        """Load the trained churn prediction model from local or S3"""
        if use_s3 and s3_bucket:
            self._load_from_s3(s3_bucket)
        else:
            self._load_from_local(model_path)
        
        self.threshold = 0.42  # Optimized threshold
    
    def _load_from_s3(self, bucket_name):
        """Load models from S3 bucket"""
        s3 = boto3.client('s3')
        model_files = ['churn_model.pkl', 'scaler.pkl', 'feature_names.pkl']
        
        for file in model_files:
            s3.download_file(bucket_name, f'models/{file}', f'/tmp/{file}')
        
        with open('/tmp/churn_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open('/tmp/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        with open('/tmp/feature_names.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)
        
        print(f"✅ Models loaded from S3: {bucket_name}")
    
    def _load_from_local(self, model_path):
        """Load models from local directory"""
        with open(f'{model_path}/churn_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open(f'{model_path}/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        with open(f'{model_path}/feature_names.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)
    
    def predict_churn_risk(self, client_data: Dict) -> Dict:
        """Predict churn risk for a client"""
        features = np.array([[
            client_data.get('communication_sentiment', 0.0),
            client_data.get('payment_timeliness', 0.0),
            client_data.get('service_utilization', 0.0),
            client_data.get('response_satisfaction', 0.0),
            client_data.get('ticket_frequency_trend', 0.0),
            client_data.get('contract_value_trend', 0.0),
            client_data.get('contact_engagement', 0.0),
            client_data.get('escalation_frequency', 0.0)
        ]])
        
        features_scaled = self.scaler.transform(features)
        churn_probability = self.model.predict_proba(features_scaled)[0][1]
        risk_score = churn_probability * 100
        
        if risk_score >= 60:
            risk_level = 'critical'
        elif risk_score >= 40:
            risk_level = 'high'
        elif risk_score >= 25:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        feature_importance = self._get_feature_importance(client_data)
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'churn_probability': round(churn_probability, 4),
            'is_at_risk': churn_probability >= self.threshold,
            'key_risk_factors': feature_importance[:3],
            'confidence': 0.84
        }
    
    def _get_feature_importance(self, client_data: Dict) -> List[Tuple[str, float]]:
        """Rank features by their contribution to risk"""
        importance_weights = {
            'communication_sentiment': 0.3234,
            'payment_timeliness': 0.2763,
            'service_utilization': 0.0864,
            'response_satisfaction': 0.0856,
            'ticket_frequency_trend': 0.0667,
            'contract_value_trend': 0.0613,
            'contact_engagement': 0.0507,
            'escalation_frequency': 0.0496
        }
        
        feature_scores = []
        for feature, weight in importance_weights.items():
            value = abs(client_data.get(feature, 0.0))
            score = value * weight
            feature_scores.append((feature, score))
        
        feature_scores.sort(key=lambda x: x[1], reverse=True)
        return feature_scores
    
    def calculate_health_score(self, client_data: Dict) -> Dict:
        """Calculate overall client health score (0-100)"""
        payment_score = max(0, min(10, (client_data.get('payment_timeliness', 0) + 5) * 2))
        contract_score = max(0, min(10, (client_data.get('contract_value_trend', 0) + 0.5) * 10))
        financial_health = payment_score + contract_score
        
        sentiment_score = max(0, min(15, (client_data.get('communication_sentiment', 0) + 1) * 7.5))
        satisfaction_score = max(0, min(10, client_data.get('response_satisfaction', 0) * 10))
        engagement_quality = sentiment_score + satisfaction_score
        
        utilization_score = max(0, min(10, client_data.get('service_utilization', 0) * 10))
        adoption_score = max(0, min(10, (1 - client_data.get('escalation_frequency', 1)) * 10))
        service_utilization = utilization_score + adoption_score
        
        ticket_score = max(0, min(8, (2 - client_data.get('ticket_frequency_trend', 1)) * 4))
        resolution_score = max(0, min(7, client_data.get('response_satisfaction', 0) * 7))
        support_patterns = ticket_score + resolution_score
        
        contact_score = max(0, min(5, client_data.get('contact_engagement', 0) * 5))
        relationship_stability = contact_score + 5
        
        total_health = (financial_health + engagement_quality + service_utilization + 
                       support_patterns + relationship_stability)
        
        return {
            'total_health_score': round(total_health, 1),
            'components': {
                'financial_health': round(financial_health, 1),
                'engagement_quality': round(engagement_quality, 1),
                'service_utilization': round(service_utilization, 1),
                'support_patterns': round(support_patterns, 1),
                'relationship_stability': round(relationship_stability, 1)
            }
        }
