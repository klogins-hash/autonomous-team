#!/usr/bin/env python3
"""
E2B Sandbox Tool - Autonomous Team
"""

import requests

class E2BSandboxTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.e2b.dev"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def create_session(self, template: str = "python3"):
        print(f"🏗️  Creating E2B sandbox: {template}")
        
        try:
            data = {
                "templateID": template,
                "settings": {
                    "cpuCount": 2,
                    "memoryMB": 2048
                }
            }
            
            response = requests.post(
                f"{self.base_url}/sandboxes",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                session = response.json()
                session_id = session["sandboxID"]
                print(f"   ✅ Session created: {session_id}")
                return session_id
            else:
                print(f"   ❌ Failed to create session: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ E2B session error: {e}")
            return None

e2b_sandbox = E2BSandboxTool("e2b_08cd803fb0f53235473753396ec7e5c987cdd8fd")

def create_sandbox(template: str = "python3"):
    return e2b_sandbox.create_session(template)

print("✅ E2B sandbox tool initialized")