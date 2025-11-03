"""
Client API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from app.models.client import ClientHealthResponse, ChurnPrediction
from app.database.connection import get_db, DatabaseService
from app.services.ml_engine import MLEngineService
from app.services.risk_scorer import RiskScorerService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/clients", tags=["clients"])

# Services will be injected
ml_service: MLEngineService = None
risk_scorer: RiskScorerService = None

def set_services(ml: MLEngineService, scorer: RiskScorerService):
    """Set service instances"""
    global ml_service, risk_scorer
    ml_service = ml
    risk_scorer = scorer

@router.get("/", response_model=List[ClientHealthResponse])
async def get_all_clients(db: DatabaseService = Depends(get_db)):
    """
    Get all clients with health scores
    
    Returns list of clients with calculated health scores
    """
    try:
        # Get all clients from database
        clients = await db.get_all_clients()
        
        # Calculate health scores for each
        client_responses = []
        for client in clients:
            health_data = await risk_scorer.calculate_health_score(client)
            
            # Add churn probability from ML model
            churn_prob = await ml_service.predict_churn(client)
            health_data['churn_probability'] = churn_prob
            health_data['confidence'] = 0.85  # Model confidence
            
            client_responses.append(ClientHealthResponse(**health_data))
        
        return client_responses
        
    except Exception as e:
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{client_id}", response_model=ClientHealthResponse)
async def get_client(client_id: int, db: DatabaseService = Depends(get_db)):
    """
    Get detailed client information with AI analysis
    
    Args:
        client_id: Client ID
        
    Returns:
        Client with health score, risk factors, and predictions
    """
    try:
        # Get client from database
        client = await db.get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Calculate comprehensive health score
        health_data = await risk_scorer.calculate_health_score(client)
        
        # Get ML-based churn prediction
        churn_prob = await ml_service.predict_churn(client)
        health_data['churn_probability'] = churn_prob
        health_data['confidence'] = 0.85
        
        return ClientHealthResponse(**health_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{client_id}/predict", response_model=ChurnPrediction)
async def predict_client_churn(client_id: int, db: DatabaseService = Depends(get_db)):
    """
    Predict churn probability for a specific client
    
    Args:
        client_id: Client ID
        
    Returns:
        Churn prediction with explanation
    """
    try:
        # Get client
        client = await db.get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Predict churn
        churn_prob = await ml_service.predict_churn(client)
        
        # Get risk level
        if churn_prob >= 0.7:
            risk_level = "critical"
        elif churn_prob >= 0.5:
            risk_level = "high"
        elif churn_prob >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Get explanation
        explanation = await ml_service.explain_prediction(client, churn_prob)
        
        return ChurnPrediction(
            client_id=client_id,
            client_name=client['name'],
            churn_probability=churn_prob,
            risk_level=risk_level,
            confidence=0.85,
            top_factors=explanation.get('top_factors', []),
            predicted_at=None  # Will be set by Pydantic default
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting churn for client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))