from fastapi import FastAPI
import os
import json
from datetime import datetime, timezone

os.environ['USE_S3_MODELS'] = 'true'
os.environ['MODEL_S3_BUCKET'] = 'msp-churn-models'

app = FastAPI()

predictor = None

def init_predictor():
    global predictor
    if predictor is None:
        try:
            from churn_predictor import ChurnPredictor
            predictor = ChurnPredictor(use_s3=True, s3_bucket='msp-churn-models')
            print("✅ Predictor loaded")
        except Exception as e:
            print(f"Predictor mock mode: {e}")
            predictor = 'mock'

init_predictor()

@app.post("/invocations")
async def invoke_agent(body: dict):
    try:
        # Extract prompt from various possible formats
        prompt = ""
        if "input" in body and isinstance(body["input"], dict):
            prompt = body["input"].get("prompt", "")
        elif "prompt" in body:
            prompt = body.get("prompt", "")
        
        if not prompt:
            prompt = "Hello"
        
        # Process with agent
        from agent_entry import agent_process
        result = agent_process(prompt, predictor)
        
        return {
            "output": {
                "message": result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
    except Exception as e:
        return {
            "output": {
                "error": str(e),
                "message": "Error processing request"
            }
        }

@app.get("/ping")
async def ping():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
