import os
import json

# Set environment variables
os.environ['USE_S3_MODELS'] = 'true'
os.environ['MODEL_S3_BUCKET'] = 'msp-churn-models'

print("🚀 Initializing agent_entry...")

# Import the agent (this loads models from S3)
from agent import agent

print("✅ Agent loaded successfully")

def handler(event, context):
    """
    Lambda/AgentCore handler function
    """
    try:
        # Handle health check
        if event.get('path') == '/ping' or event.get('routeKey') == 'GET /ping':
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'healthy', 'agent': 'client-retention-agent'})
            }
        
        # Extract prompt from event
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        prompt = body.get('prompt', body.get('input', {}).get('prompt', 'Hello'))
        
        print(f"Processing prompt: {prompt[:100]}...")
        
        # Invoke agent
        response = agent(prompt)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': str(response.message),
                'status': 'success'
            })
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'status': 'error'
            })
        }

# For local testing
if __name__ == "__main__":
    test_event = {'body': json.dumps({'prompt': 'Test'})}
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
