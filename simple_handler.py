import json
from datetime import datetime

def main(event, context):
    """Simple handler for testing"""
    try:
        # Parse event
        if isinstance(event, str):
            data = json.loads(event)
        else:
            data = event.get('body', {}) if 'body' in event else event
        
        result = {
            "status": "success",
            "message": "Autonomous team function is working!",
            "timestamp": datetime.now().isoformat(),
            "received_data": data
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {"Content-Type": "application/json"}
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
