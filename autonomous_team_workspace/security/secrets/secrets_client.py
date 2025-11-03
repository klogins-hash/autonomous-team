#!/usr/bin/env python3
"""
Scaleway Secrets Client - Autonomous Team
Secure access to all API keys and secrets
"""

import json
import requests
import base64
from pathlib import Path
from typing import Optional, Dict, Any

class ScalewaySecretsClient:
    """Client for accessing Scaleway Secret Manager"""
    
    def __init__(self):
        self.config_path = Path("/root/CascadeProjects/autonomous_team_workspace/security/secrets/secure_config.json")
        self.load_config()
        
    def load_config(self):
        """Load secure configuration"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        # Scaleway credentials (these should be the only hardcoded values)
        self.access_key = "SCW7A5D0ZV7XK1N3GQ9M2"
        self.secret_key = "sk_car_gXRScNmwFycWaqD8w6igNS"
        self.project_id = self.config["project_id"]
        self.endpoint = "https://api.scaleway.com/secret-manager/v1alpha1/regions/fr-par-2"
    
    def get_secret(self, service_name: str) -> Optional[str]:
        """Get secret for a specific service"""
        if service_name not in self.config["secrets"]:
            print(f"❌ Unknown service: {service_name}")
            return None
        
        secret_info = self.config["secrets"][service_name]
        secret_name = secret_info["secret_name"]
        
        print(f"🔍 Retrieving secret for {service_name}...")
        
        try:
            headers = {
                "X-Auth-Token": self.secret_key,
                "Content-Type": "application/json",
                "X-Project-Id": self.project_id
            }
            
            response = requests.get(
                f"{self.endpoint}/secrets/{secret_name}/versions/latest",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                secret_data = response.json()
                decoded_value = base64.b64decode(secret_data["data"]).decode()
                print(f"✅ Secret retrieved for {service_name}")
                return decoded_value
            else:
                print(f"❌ Failed to retrieve secret for {service_name}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving secret for {service_name}: {e}")
            return None
    
    def get_all_secrets(self) -> Dict[str, str]:
        """Get all secrets as environment variables"""
        secrets = {}
        
        for service_name in self.config["secrets"]:
            secret_value = self.get_secret(service_name)
            if secret_value:
                env_var = self.config["secrets"][service_name]["environment_var"]
                secrets[env_var] = secret_value
        
        return secrets
    
    def setup_environment(self) -> bool:
        """Setup environment variables from secrets"""
        print("🔧 Setting up environment from secrets...")
        
        secrets = self.get_all_secrets()
        
        for env_var, value in secrets.items():
            import os
            os.environ[env_var] = value
            print(f"   ✅ Set {env_var}")
        
        print(f"✅ Environment configured with {len(secrets)} secrets")
        return True
    
    def test_secrets_access(self) -> bool:
        """Test access to all secrets"""
        print("🧪 Testing secrets access...")
        
        success_count = 0
        total_count = len(self.config["secrets"])
        
        for service_name in self.config["secrets"]:
            secret_value = self.get_secret(service_name)
            if secret_value:
                success_count += 1
            else:
                print(f"   ❌ Failed to access {service_name}")
        
        print(f"✅ Successfully accessed {success_count}/{total_count} secrets")
        return success_count == total_count

# Global secrets client instance
secrets_client = ScalewaySecretsClient()

def get_secret(service_name: str) -> Optional[str]:
    """Get secret for a service"""
    return secrets_client.get_secret(service_name)

def setup_environment_from_secrets() -> bool:
    """Setup environment from secrets"""
    return secrets_client.setup_environment()

def test_all_secrets() -> bool:
    """Test access to all secrets"""
    return secrets_client.test_secrets_access()

print("✅ Scaleway secrets client initialized for autonomous team")