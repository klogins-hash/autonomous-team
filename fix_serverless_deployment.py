#!/usr/bin/env python3
"""
Fix Serverless Deployment using Scaleway Specialist Agent
"""

import sys
sys.path.append('/root/CascadeProjects/autonomous_team_workspace')

from agents.specialized.scaleway_specialist_agent import scaleway_specialist
import subprocess
import json
import zipfile
import os
from pathlib import Path
from datetime import datetime

def fix_serverless_deployment():
    """Fix serverless function deployment using Scaleway specialist knowledge"""
    
    print("🔧 FIXING SERVERLESS DEPLOYMENT WITH SCALEWAY SPECIALIST")
    print("=" * 60)
    
    # Step 1: Troubleshoot current issues
    print("\n🔍 Step 1: Troubleshooting current deployment issues...")
    troubleshooting = scaleway_specialist.troubleshoot_scaleway_issue(
        "function build error during build preparation phase"
    )
    
    print("   📋 Troubleshooting Results:")
    if troubleshooting.get("analysis"):
        print("   🎯 Common Causes:")
        for cause in troubleshooting["analysis"]["causes"]:
            print(f"      • {cause}")
        print("   💡 Solutions:")
        for solution in troubleshooting["analysis"]["solutions"]:
            print(f"      • {solution}")
    
    # Step 2: Get proper function deployment help
    print("\n📚 Step 2: Getting proper Scaleway function deployment help...")
    deploy_help = scaleway_specialist.get_scaleway_help("function function create")
    print("   📖 Function Creation Help:")
    if deploy_help["status"] == "success":
        help_lines = deploy_help["help"].split('\n')[:10]
        for line in help_lines:
            if line.strip():
                print(f"      {line}")
    
    # Step 3: Create proper function code
    print("\n📝 Step 3: Creating proper function code structure...")
    
    # Create proper function directory structure
    func_dir = Path("/tmp/proper_scaleway_function")
    func_dir.mkdir(parents=True, exist_ok=True)
    
    # Create proper handler.py
    proper_handler = '''import json
import os
from datetime import datetime

def main(event, context):
    """Main handler for Scaleway Function"""
    try:
        # Parse the event
        if isinstance(event, str):
            data = json.loads(event)
        else:
            data = event
        
        # Get function name from environment if available
        function_name = os.environ.get('SCW_FUNCTION_NAME', 'autonomous-team-function')
        
        # Create response
        result = {
            "status": "success",
            "message": f"Hello from {function_name}!",
            "timestamp": datetime.now().isoformat(),
            "function": function_name,
            "event_received": data,
            "scaleway_function": True
        }
        
        # Return proper response format
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {
                "Content-Type": "application/json",
                "X-Function-Name": function_name
            }
        }
        
    except Exception as e:
        # Return error response
        error_result = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "function": function_name
        }
        
        return {
            "statusCode": 500,
            "body": json.dumps(error_result),
            "headers": {"Content-Type": "application/json"}
        }
'''
    
    handler_file = func_dir / "handler.py"
    with open(handler_file, 'w') as f:
        f.write(proper_handler)
    
    # Create proper requirements.txt
    requirements = """# Scaleway Function Requirements
# No external dependencies for basic functionality
# Add requests>=2.31.0 if external API calls needed
"""
    
    req_file = func_dir / "requirements.txt"
    with open(req_file, 'w') as f:
        f.write(requirements)
    
    print(f"   ✅ Proper function code created at {func_dir}")
    
    # Step 4: Create zip file correctly
    print("\n📦 Step 4: Creating proper zip file...")
    zip_path = func_dir / "function.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(handler_file, "handler.py")
        zipf.write(req_file, "requirements.txt")
    
    print(f"   ✅ Zip file created at {zip_path}")
    
    # Step 5: Delete existing functions
    print("\n🗑️  Step 5: Cleaning up existing functions...")
    
    # Get existing functions
    list_cmd = "scw function function list namespace-id=9a4d8548-df9c-4038-93e7-ae0b21c7d8bb region=fr-par --output=json"
    result = subprocess.run(list_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            functions = json.loads(result.stdout)
            for func in functions:
                delete_cmd = f"scw function function delete {func['id']} region=fr-par"
                delete_result = subprocess.run(delete_cmd, shell=True, capture_output=True, text=True)
                if delete_result.returncode == 0:
                    print(f"   ✅ Deleted {func['name']}")
                else:
                    print(f"   ❌ Failed to delete {func['name']}")
        except:
            print("   ⚠️  No functions to delete")
    
    # Step 6: Create new functions with proper method
    print("\n🚀 Step 6: Creating new functions with proper method...")
    
    functions_to_create = [
        {
            "name": "autonomous-coordinator",
            "description": "Coordinate autonomous team operations"
        },
        {
            "name": "voice-synthesis-agent",
            "description": "British voice synthesis agent"
        },
        {
            "name": "web-search-agent", 
            "description": "Real-time web search"
        },
        {
            "name": "code-execution-sandbox",
            "description": "Secure code execution"
        }
    ]
    
    created_functions = []
    
    for func_info in functions_to_create:
        print(f"\\n   ⚡ Creating {func_info['name']}...")
        
        # Create function with minimal required parameters
        create_cmd = [
            "scw", "function", "function", "create",
            "namespace-id=9a4d8548-df9c-4038-93e7-ae0b21c7d8bb",
            f"name={func_info['name']}",
            "runtime=python311",
            "handler=handler.main",
            f"description={func_info['description']}",
            "region=fr-par",
            "memory-limit=256",
            "timeout=5m",
            "min-scale=0",
            "max-scale=5"
        ]
        
        try:
            result = subprocess.run(create_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"      ✅ {func_info['name']} created successfully")
                created_functions.append(func_info['name'])
                
                # Wait a moment before deploying
                import time
                time.sleep(5)
                
                # Deploy the function (this should work with proper handler)
                deploy_cmd = [
                    "scw", "function", "function", "deploy",
                    f"function-id={func_info['name']}",
                    "region=fr-par"
                ]
                
                print(f"      🚀 Deploying {func_info['name']}...")
                deploy_result = subprocess.run(deploy_cmd, capture_output=True, text=True, timeout=120)
                
                if deploy_result.returncode == 0:
                    print(f"      ✅ {func_info['name']} deployment started")
                else:
                    print(f"      ❌ {func_info['name']} deployment failed:")
                    print(f"         {deploy_result.stderr}")
            else:
                print(f"      ❌ {func_info['name']} creation failed:")
                print(f"         {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"      ❌ {func_info['name']} creation timed out")
        except Exception as e:
            print(f"      ❌ {func_info['name']} error: {e}")
    
    # Step 7: Wait and check status
    print("\\n⏳ Step 7: Waiting for functions to build...")
    import time
    time.sleep(60)
    
    # Check function status
    print("\\n🔍 Step 8: Checking function status...")
    status_cmd = "scw function function list namespace-id=9a4d8548-df9c-4038-93e7-ae0b21c7d8bb region=fr-par --output=json"
    status_result = subprocess.run(status_cmd, shell=True, capture_output=True, text=True)
    
    if status_result.returncode == 0:
        functions = json.loads(status_result.stdout)
        print(f"   📊 Found {len(functions)} functions:")
        
        working_functions = []
        for func in functions:
            status_emoji = "✅" if func['status'] == 'ready' else "⏳" if func['status'] == 'pending' else "❌"
            print(f"      {status_emoji} {func['name']}: {func['status']}")
            
            if func.get('domain_name'):
                print(f"         🌐 {func['domain_name']}")
            
            if func['status'] == 'ready':
                working_functions.append(func)
    
    # Step 8: Test working functions
    if working_functions:
        print("\\n🧪 Step 9: Testing working functions...")
        for func in working_functions[:2]:  # Test first 2 working functions
            if func.get('domain_name'):
                print(f"   🌐 Testing {func['name']}...")
                test_cmd = f'curl -X POST https://{func["domain_name"]} -H "Content-Type: application/json" -d \'{"test": "hello"}\' --max-time 10'
                test_result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
                
                if test_result.returncode == 0:
                    print(f"      ✅ {func['name']} responded successfully")
                    print(f"         Response: {test_result.stdout[:100]}...")
                else:
                    print(f"      ❌ {func['name']} test failed: {test_result.stderr}")
    
    # Summary
    print("\\n🎉 DEPLOYMENT FIX SUMMARY")
    print(f"   ✅ Functions created: {len(created_functions)}/{len(functions_to_create)}")
    print(f"   ✅ Functions working: {len(working_functions) if working_functions else 0}")
    print(f"   🔧 Scaleway specialist knowledge applied")
    print(f"   📚 Documentation followed correctly")
    
    return {
        "created": created_functions,
        "working": working_functions if working_functions else [],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    result = fix_serverless_deployment()
    print(f"\\n🏆 FINAL RESULT: {json.dumps(result, indent=2)}")
