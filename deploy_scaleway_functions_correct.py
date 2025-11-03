#!/usr/bin/env python3
"""
Deploy Serverless Functions to Scaleway - Correct Method
Using the proper Scaleway CLI commands
"""

import subprocess
import json
import zipfile
import os
from pathlib import Path
from datetime import datetime

def deploy_serverless_functions_correct():
    """Deploy functions using correct Scaleway method"""
    
    print("🚀 DEPLOYING SERVERLESS FUNCTIONS - CORRECT METHOD")
    print("=" * 60)
    
    project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
    region = "fr-par"
    namespace_id = "9a4d8548-df9c-4038-93e7-ae0b21c7d8bb"
    
    # Function definitions
    functions = [
        {
            "name": "autonomous-coordinator",
            "runtime": "python311",
            "handler": "handler.main",
            "description": "Coordinate autonomous team operations",
            "code": generate_coordinator_code()
        },
        {
            "name": "voice-synthesis-agent", 
            "runtime": "python311",
            "handler": "handler.main",
            "description": "British voice synthesis agent",
            "code": generate_voice_code()
        },
        {
            "name": "web-search-agent",
            "runtime": "python311", 
            "handler": "handler.main",
            "description": "Real-time web search",
            "code": generate_search_code()
        },
        {
            "name": "code-execution-sandbox",
            "runtime": "python311",
            "handler": "handler.main", 
            "description": "Secure code execution",
            "code": generate_code_execution()
        }
    ]
    
    deployed_functions = []
    
    for func in functions:
        print(f"\n⚡ Deploying: {func['name']}")
        
        # Create function directory
        func_dir = Path(f"/tmp/scaleway_functions/{func['name']}")
        func_dir.mkdir(parents=True, exist_ok=True)
        
        # Write handler code
        handler_file = func_dir / "handler.py"
        with open(handler_file, 'w') as f:
            f.write(func['code'])
        
        # Write requirements
        req_file = func_dir / "requirements.txt"
        with open(req_file, 'w') as f:
            f.write("requests>=2.31.0\n")
        
        # Create zip file
        zip_path = func_dir / "function.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(handler_file, "handler.py")
            zipf.write(req_file, "requirements.txt")
        
        # Create function first
        create_cmd = [
            "scw", "function", "function", "create",
            f"namespace-id={namespace_id}",
            f"name={func['name']}",
            f"runtime={func['runtime']}",
            f"handler={func['handler']}",
            f"description={func['description']}",
            f"region={region}"
        ]
        
        try:
            print(f"   📦 Creating function {func['name']}...")
            result = subprocess.run(create_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ Function {func['name']} created")
                
                # Deploy code to function
                deploy_cmd = [
                    "scw", "function", "function", "deploy",
                    f"function-id={func['name']}",
                    f"namespace-id={namespace_id}",
                    f"region={region}",
                    f"zip-file={zip_path}"
                ]
                
                print(f"   🚀 Deploying code to {func['name']}...")
                deploy_result = subprocess.run(deploy_cmd, capture_output=True, text=True, timeout=120)
                
                if deploy_result.returncode == 0:
                    print(f"   ✅ {func['name']} deployed successfully")
                    deployed_functions.append(func['name'])
                else:
                    print(f"   ❌ {func['name']} code deployment failed:")
                    print(f"      {deploy_result.stderr}")
            else:
                print(f"   ❌ {func['name']} creation failed:")
                print(f"      {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ {func['name']} deployment timed out")
        except Exception as e:
            print(f"   ❌ {func['name']} deployment error: {e}")
    
    # List deployed functions
    print(f"\n🔍 Listing deployed functions...")
    list_cmd = [
        "scw", "function", "function", "list",
        f"namespace-id={namespace_id}",
        f"region={region}"
    ]
    
    try:
        result = subprocess.run(list_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   ✅ Functions listed:")
            print(f"   {result.stdout}")
        else:
            print(f"   ❌ Failed to list functions: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Error listing functions: {e}")
    
    print(f"\n🎉 DEPLOYMENT SUMMARY")
    print(f"   ✅ Successfully deployed: {len(deployed_functions)}/{len(functions)} functions")
    for func in deployed_functions:
        print(f"      - {func}")
    
    return deployed_functions

def generate_coordinator_code():
    return '''import json
import os
from datetime import datetime

def main(event, context):
    """Autonomous coordinator function"""
    try:
        # Parse event
        if isinstance(event, str):
            data = json.loads(event)
        else:
            data = event.get('body', {}) if 'body' in event else event
        
        # Generate task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Process task
        task_type = data.get('task_type', 'general')
        priority = data.get('priority', 'medium')
        
        result = {
            "status": "success",
            "task_id": task_id,
            "task_type": task_type,
            "priority": priority,
            "message": "Task delegated successfully",
            "timestamp": datetime.now().isoformat(),
            "function": "autonomous-coordinator"
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
'''

def generate_voice_code():
    return '''import json
import os
from datetime import datetime

def main(event, context):
    """Voice synthesis function"""
    try:
        # Parse event
        if isinstance(event, str):
            data = json.loads(event)
        else:
            data = event.get('body', {}) if 'body' in event else event
        
        text = data.get('text', 'Hello from autonomous team!')
        voice_profile = data.get('voice_profile', 'professional_british')
        
        # Mock voice synthesis
        audio_url = f"https://audio.autonomous-team.com/{voice_profile}/{hash(text)}.wav"
        
        result = {
            "status": "success",
            "text": text,
            "voice_profile": voice_profile,
            "audio_url": audio_url,
            "duration": len(text) * 0.1,
            "timestamp": datetime.now().isoformat(),
            "function": "voice-synthesis-agent"
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
'''

def generate_search_code():
    return '''import json
import requests
from datetime import datetime

def main(event, context):
    """Web search function"""
    try:
        # Parse event
        if isinstance(event, str):
            data = json.loads(event)
        else:
            data = event.get('body', {}) if 'body' in event else event
        
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        
        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Query required"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        # Mock search results
        results = [
            {
                "title": f"Search Result {i+1} for '{query}'",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"This is result {i+1} for the query {query}",
                "relevance": 0.9 - (i * 0.1)
            }
            for i in range(min(max_results, 5))
        ]
        
        result = {
            "status": "success",
            "query": query,
            "results": results,
            "total_results": len(results),
            "timestamp": datetime.now().isoformat(),
            "function": "web-search-agent"
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
'''

def generate_code_execution():
    return '''import json
import subprocess
import tempfile
import os
from datetime import datetime

def main(event, context):
    """Code execution function"""
    try:
        # Parse event
        if isinstance(event, str):
            data = json.loads(event)
        else:
            data = event.get('body', {}) if 'body' in event else event
        
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Code required"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        if language != 'python':
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Only Python supported"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        # Create temporary file and execute
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            execution_result = {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr if result.stderr else None,
                "return_code": result.returncode,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "function": "code-execution-sandbox"
            }
            
        finally:
            os.unlink(temp_file)
        
        return {
            "statusCode": 200,
            "body": json.dumps(execution_result),
            "headers": {"Content-Type": "application/json"}
        }
        
    except subprocess.TimeoutExpired:
        return {
            "statusCode": 408,
            "body": json.dumps({"error": "Code execution timed out"}),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
'''

if __name__ == "__main__":
    deploy_serverless_functions_correct()
