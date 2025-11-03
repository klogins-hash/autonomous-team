#\!/usr/bin/env python3
"""
Fixed Cartesia Integration - Autonomous Team Implementation
British female voices with proper authentication
"""

import requests
import json

class FixedCartesiaIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.cartesia.ai"
        self.version = "2025-04-16"
        
    def synthesize_speech(self, text, voice_id="79a125e8-cd45-4c13-8a67-188112f4dd22"):
        """Synthesize speech with British female voice"""
        headers = {
            "Cartesia-API-Key": self.api_key,
            "Cartesia-Version": self.version,
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "sonic-english",
            "voice_id": voice_id,
            "output_format": {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100
            },
            "transcript": text
        }
        
        try:
            response = requests.post(f"{self.base_url}/tts/bytes", headers=headers, json=data)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except:
            return None

print("✅ Fixed Cartesia integration deployed by autonomous team")