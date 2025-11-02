from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime, timezone
from agent import agent
import json

app = FastAPI(
    title="Client Retention Agent Server",
    version="1.0.0",
    description="AI-Powered Client Retention & Growth Engine"
)

class InvocationRequest(BaseModel):
    input: Dict[str, Any]

class InvocationResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    """Main invocation endpoint for the agent"""
    try:
        user_message = request.input.get("prompt", "")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No prompt found")
        
        result = agent(user_message)
        
        response = {
            "message": result.message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": "client-retention-agent"
        }
        
        return InvocationResponse(output=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "client-retention-agent"}

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Client Retention Agent API",
        "version": "1.0.0",
        "endpoints": {
            "invocations": "POST /invocations",
            "health": "GET /ping"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
