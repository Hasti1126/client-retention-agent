"""
NeuroNova AI Engine - FastAPI Backend
SuperHack 2025 - Team NeuroNova
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import List, Optional

from app.config import settings
from app.models.client import Client, ClientHealthResponse
from app.models.recommendation import RecommendationResponse
from app.services.bedrock_agent import BedrockAgentService
from app.services.ml_engine import MLEngineService
from app.services.risk_scorer import RiskScorerService
from app.services.recommendation_engine import RecommendationEngine
from app.database.connection import get_db, init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
bedrock_service = None
ml_service = None
risk_scorer = None
recommendation_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global bedrock_service, ml_service, risk_scorer, recommendation_engine
    
    logger.info("Initializing NeuroNova AI Engine...")
    
    # Initialize database
    await init_db()
    
    # Initialize AI services
    bedrock_service = BedrockAgentService(
        model_id=settings.BEDROCK_MODEL_ID,
        region=settings.AWS_REGION
    )
    
    ml_service = MLEngineService()
    await ml_service.load_models()
    
    risk_scorer = RiskScorerService()
    recommendation_engine = RecommendationEngine(bedrock_service)
    
    logger.info("NeuroNova AI Engine initialized successfully!")
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down NeuroNova AI Engine...")

# Create FastAPI app
app = FastAPI(
    title="NeuroNova AI Engine",
    description="AI-Powered Client Retention & Growth Engine for MSPs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "service": "NeuroNova AI Engine",
        "version": "1.0.0",
        "status": "operational",
        "team": "NeuroNova - SuperHack 2025"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "bedrock": bedrock_service is not None,
            "ml_engine": ml_service is not None,
            "risk_scorer": risk_scorer is not None,
            "recommendation_engine": recommendation_engine is not None
        }
    }

# Client endpoints
@app.get("/api/clients", response_model=List[ClientHealthResponse])
async def get_all_clients(db=Depends(get_db)):
    """Get all clients with health scores"""
    try:
        # Get clients from database
        clients = await db.get_all_clients()
        
        # Calculate health scores for each client
        client_responses = []
        for client in clients:
            health_data = await risk_scorer.calculate_health_score(client)
            client_responses.append(ClientHealthResponse(**health_data))
        
        return client_responses
    except Exception as e:
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clients/{client_id}", response_model=ClientHealthResponse)
async def get_client(client_id: int, db=Depends(get_db)):
    """Get detailed client information with AI analysis"""
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
        
        # Get sentiment analysis
        sentiment = await ml_service.analyze_sentiment(client.communications)
        health_data['sentiment_score'] = sentiment
        
        return ClientHealthResponse(**health_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clients/{client_id}/recommendations", 
         response_model=RecommendationResponse)
async def get_recommendations(client_id: int, db=Depends(get_db)):
    """Get AI-generated recommendations for a client"""
    try:
        # Get client data
        client = await db.get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Calculate risk factors
        risk_analysis = await risk_scorer.analyze_risk_factors(client)
        
        # Generate AI recommendations using Bedrock
        recommendations = await recommendation_engine.generate_recommendations(
            client=client,
            risk_analysis=risk_analysis
        )
        
        return RecommendationResponse(
            client_id=client_id,
            client_name=client.name,
            health_score=risk_analysis['health_score'],
            recommendations=recommendations
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations for client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/portfolio")
async def get_portfolio_analytics(db=Depends(get_db)):
    """Get portfolio-wide analytics"""
    try:
        clients = await db.get_all_clients()
        
        analytics = {
            "total_clients": len(clients),
            "healthy": 0,
            "at_risk": 0,
            "critical": 0,
            "total_revenue": 0,
            "at_risk_revenue": 0
        }
        
        for client in clients:
            health_data = await risk_scorer.calculate_health_score(client)
            score = health_data['health_score']
            
            analytics['total_revenue'] += client.contract_value
            
            if score >= 70:
                analytics['healthy'] += 1
            elif score >= 40:
                analytics['at_risk'] += 1
                analytics['at_risk_revenue'] += client.contract_value
            else:
                analytics['critical'] += 1
                analytics['at_risk_revenue'] += client.contract_value
        
        return analytics
    except Exception as e:
        logger.error(f"Error calculating portfolio analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ml/predict-churn")
async def predict_churn_batch(client_ids: List[int], db=Depends(get_db)):
    """Batch predict churn for multiple clients"""
    try:
        predictions = []
        
        for client_id in client_ids:
            client = await db.get_client(client_id)
            if client:
                churn_prob = await ml_service.predict_churn(client)
                predictions.append({
                    "client_id": client_id,
                    "client_name": client.name,
                    "churn_probability": churn_prob,
                    "risk_level": "critical" if churn_prob > 0.7 else 
                                 "high" if churn_prob > 0.5 else
                                 "medium" if churn_prob > 0.3 else "low"
                })
        
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Error in batch churn prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )