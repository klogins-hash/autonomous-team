#!/usr/bin/env python3
"""
API Testing Tool - Autonomous Team
"""

import requests

class APITestingTool:
    def __init__(self):
        self.default_headers = {"User-Agent": "AutonomousTeam/1.0"}
        self.timeout = 30
        
    def test_api_endpoint(self, url: str, method: str = "GET", headers: dict = None, data: dict = None):
        print(f"🔌 Testing API: {method} {url}")
        
        try:
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)
            
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers, timeout=self.timeout)
            elif method.upper() == "POST":
                response = requests.post(url, headers=request_headers, json=data, timeout=self.timeout)
            else:
                print(f"   ❌ Unsupported method: {method}")
                return None
            
            result = {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "content_length": len(response.content),
                "content": response.text[:500]  # First 500 chars
            }
            
            print(f"   ✅ API test completed: {response.status_code}")
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": None
            }
    
    def test_cartesia_api(self):
        print("🎙️  Testing Cartesia API...")
        
        headers = {
            "Cartesia-API-Key": "sk_car_J5wk4g3bzwyggQ6uBftGMC",
            "Cartesia-Version": "2025-04-16",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "sonic-english",
            "voice_id": "79a125e8-cd45-4c13-8a67-188112f4dd22",
            "output_format": {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100
            },
            "transcript": "Hello from autonomous team"
        }
        
        result = self.test_api_endpoint(
            "https://api.cartesia.ai/tts/bytes",
            "POST",
            headers,
            data
        )
        
        if result and result["success"]:
            print(f"   ✅ Cartesia API working! Audio size: {result['content_length']} bytes")
            return True
        else:
            print(f"   ❌ Cartesia API test failed")
            return False

api_tester = APITestingTool()

def test_api(url: str, method: str = "GET", **kwargs):
    return api_tester.test_api_endpoint(url, method, **kwargs)

def test_cartesia_api_integration():
    return api_tester.test_cartesia_api()

print("✅ API testing tool initialized")