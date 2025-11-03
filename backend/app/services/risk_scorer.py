"""
Risk Scorer Service
Calculates client health scores and risk factors
"""

import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class RiskScorerService:
    """Service for calculating client health scores and risk analysis"""
    
    def __init__(self):
        """Initialize risk scorer"""
        self.feature_weights = {
            'communication_sentiment': 0.28,
            'payment_timeliness': 0.28,
            'service_utilization': 0.15,
            'response_satisfaction': 0.12,
            'ticket_frequency_trend': 0.07,
            'contract_value_trend': 0.04,
            'escalation_frequency': 0.03,
            'contact_engagement': 0.03
        }
    
    async def calculate_health_score(self, client: Dict) -> Dict:
        """
        Calculate comprehensive health score for a client
        
        Args:
            client: Client data dictionary
            
        Returns:
            Health score and analysis
        """
        try:
            # Normalize features
            normalized_features = self._normalize_features(client)
            
            # Calculate risk score (0-1, higher = more risk)
            risk_score = self._calculate_risk_score(normalized_features)
            
            # Convert to health score (0-100, higher = healthier)
            health_score = int((1 - risk_score) * 100)
            
            # Determine risk level
            risk_level = self._get_risk_level(health_score)
            
            # Analyze risk factors
            risk_factors = self._analyze_risk_factors(client, normalized_features)
            
            return {
                'client_id': client.get('id'),
                'name': client.get('name'),
                'health_score': health_score,
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'contract_value': client.get('contract_value', 0),
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating health score: {str(e)}")
            raise
    
    def _normalize_features(self, client: Dict) -> Dict:
        """Normalize all features to 0-1 scale"""
        
        # Get raw values with defaults
        sentiment = client.get('sentiment', 0.0)  # -1 to 1
        payment_delay = client.get('payment_delay', 0)  # days
        satisfaction = client.get('satisfaction', 3.0)  # 1-5
        utilization = client.get('utilization', 0.7)  # 0-1
        tickets = client.get('tickets', 10)  # count
        
        # Normalize to 0-1 where 1 = high risk
        normalized = {
            'communication_sentiment': (1 - sentiment) / 2,  # -1,1 to 0,1 inverted
            'payment_timeliness': min(payment_delay / 30.0, 1.0),  # 0-30+ days
            'service_utilization': 1 - utilization,  # Invert (low util = high risk)
            'response_satisfaction': 1 - (satisfaction / 5.0),  # Invert
            'ticket_frequency_trend': min(tickets / 50.0, 1.0),  # 0-50+ tickets
            'contract_value_trend': 0.5,  # Default neutral
            'escalation_frequency': 0.3,  # Default low
            'contact_engagement': 0.3  # Default medium
        }
        
        return normalized
    
    def _calculate_risk_score(self, normalized_features: Dict) -> float:
        """Calculate weighted risk score"""
        
        risk_score = sum(
            normalized_features.get(feature, 0.5) * weight
            for feature, weight in self.feature_weights.items()
        )
        
        return min(max(risk_score, 0), 1)  # Clamp between 0 and 1
    
    def _get_risk_level(self, health_score: int) -> str:
        """Determine risk level from health score"""
        
        if health_score >= 80:
            return "healthy"
        elif health_score >= 70:
            return "low"
        elif health_score >= 50:
            return "medium"
        elif health_score >= 40:
            return "high"
        else:
            return "critical"
    
    def _analyze_risk_factors(self, client: Dict, normalized: Dict) -> List[Dict]:
        """Identify and prioritize risk factors"""
        
        risk_factors = []
        
        # Payment delays
        payment_delay = client.get('payment_delay', 0)
        if payment_delay > 10:
            risk_factors.append({
                'factor': 'Payment Delays',
                'score': int((1 - normalized['payment_timeliness']) * 100),
                'impact': 'HIGH' if payment_delay > 20 else 'MEDIUM',
                'description': f'Average {payment_delay} days late on payments',
                'trend': 'declining'
            })
        
        # Low satisfaction
        satisfaction = client.get('satisfaction', 3.0)
        if satisfaction < 3.5:
            risk_factors.append({
                'factor': 'Low Satisfaction',
                'score': int((1 - normalized['response_satisfaction']) * 100),
                'impact': 'HIGH' if satisfaction < 2.5 else 'MEDIUM',
                'description': f'CSAT score: {satisfaction:.1f}/5.0',
                'trend': 'declining'
            })
        
        # Poor service utilization
        utilization = client.get('utilization', 0.7)
        if utilization < 0.6:
            risk_factors.append({
                'factor': 'Underutilized Services',
                'score': int((1 - normalized['service_utilization']) * 100),
                'impact': 'MEDIUM',
                'description': f'Only {int(utilization * 100)}% of services used',
                'trend': 'stable'
            })
        
        # Negative sentiment
        sentiment = client.get('sentiment', 0.0)
        if sentiment < -0.2:
            risk_factors.append({
                'factor': 'Negative Communication Sentiment',
                'score': int((1 - normalized['communication_sentiment']) * 100),
                'impact': 'HIGH' if sentiment < -0.5 else 'MEDIUM',
                'description': f'Sentiment score: {sentiment:.2f}',
                'trend': 'declining'
            })
        
        # High ticket volume
        tickets = client.get('tickets', 10)
        if tickets > 20:
            risk_factors.append({
                'factor': 'High Support Ticket Volume',
                'score': int(normalized['ticket_frequency_trend'] * 100),
                'impact': 'MEDIUM',
                'description': f'{tickets} tickets in last 30 days',
                'trend': 'increasing'
            })
        
        # Sort by impact and score
        risk_factors.sort(key=lambda x: (
            0 if x['impact'] == 'HIGH' else 1,
            -x['score']
        ))
        
        return risk_factors[:5]  # Top 5 risk factors
    
    async def analyze_risk_factors(self, client: Dict) -> Dict:
        """
        Detailed risk factor analysis
        
        Args:
            client: Client data
            
        Returns:
            Detailed risk analysis
        """
        result = await self.calculate_health_score(client)
        
        return {
            'health_score': result['health_score'],
            'risk_level': result['risk_level'],
            'risk_factors': result['risk_factors'],
            'payment_delay_score': self._score_payment_delay(client),
            'satisfaction_score': self._score_satisfaction(client),
            'utilization_score': self._score_utilization(client),
            'sentiment_score': self._score_sentiment(client)
        }
    
    def _score_payment_delay(self, client: Dict) -> int:
        """Score payment timeliness (0-100, higher is better)"""
        delay = client.get('payment_delay', 0)
        return max(0, 100 - int(delay * 3))
    
    def _score_satisfaction(self, client: Dict) -> int:
        """Score customer satisfaction (0-100)"""
        satisfaction = client.get('satisfaction', 3.0)
        return int(satisfaction * 20)
    
    def _score_utilization(self, client: Dict) -> int:
        """Score service utilization (0-100)"""
        utilization = client.get('utilization', 0.7)
        return int(utilization * 100)
    
    def _score_sentiment(self, client: Dict) -> int:
        """Score communication sentiment (0-100)"""
        sentiment = client.get('sentiment', 0.0)  # -1 to 1
        return int((sentiment + 1) * 50)  # Convert to 0-100