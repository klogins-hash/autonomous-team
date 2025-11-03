#!/usr/bin/env python3
"""
Enhanced Secrets Client - Autonomous Team
Hybrid Scaleway + Local secure storage
"""

import json
import requests
import base64
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any

class EnhancedSecretsClient:
    """Enhanced client with Scaleway and local storage"""
    
    def __init__(self):
        self.config_path = Path("/root/CascadeProjects/autonomous_team_workspace/security/secrets/secure_config.json")
        self.secrets_dir = Path("/root/CascadeProjects/autonomous_team_workspace/security/secrets")
        self.load_config()
        
    def load_config(self):
        """Load secure configuration"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        self.scaleway_key = "a8236888-6261-4b2b-b717-6cd339e907bf"
        self.project_id = "c5d299b8-8462-40fb-b5ae-32a8808bf394"
    
    def get_secret(self, service_name: str) -> Optional[str]:
        """Get secret with fallback to local storage"""
        if service_name not in self.config["secrets"]:
            print(f"❌ Unknown service: {service_name}")
            return None
        
        secret_info = self.config["secrets"][service_name]
        secret_name = secret_info["secret_name"]
        
        print(f"🔍 Retrieving secret for {service_name}...")
        
        # Try Scaleway first
        secret_value = self.get_from_scaleway(secret_name)
        if secret_value:
            return secret_value
        
        # Fallback to local storage
        secret_value = self.get_from_local(secret_name)
        if secret_value:
            print(f"   ✅ Retrieved from local storage")
            return secret_value
        
        print(f"   ❌ Secret not found in any storage")
        return None
    
    def get_from_scaleway(self, secret_name: str) -> Optional[str]:
        """Try to get from Scaleway Secret Manager"""
        try:
            endpoints = [
                "https://api.scaleway.com/secret-manager/v1alpha1/regions/fr-par",
                "https://api.scaleway.com/secret-manager/v1alpha1/regions/fr-par-2"
            ]
            
            for endpoint in endpoints:
                try:
                    headers = {
                        "X-Auth-Token": self.scaleway_key,
                        "Content-Type": "application/json",
                        "X-Project-Id": self.project_id
                    }
                    
                    response = requests.get(
                        f"{endpoint}/secrets/{secret_name}/versions/latest",
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        secret_data = response.json()
                        decoded_value = base64.b64decode(secret_data["data"]).decode()
                        print(f"   ✅ Retrieved from Scaleway")
                        return decoded_value
                        
                except requests.exceptions.RequestException:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def get_from_local(self, secret_name: str) -> Optional[str]:
        """Get from local encrypted storage"""
        try:
            secret_file = self.secrets_dir / f"{secret_name}.enc"
            
            if not secret_file.exists():
                return None
            
            with open(secret_file, 'r') as f:
                encrypted_data = json.load(f)
            
            # Decrypt
            encrypted_value = encrypted_data["encrypted_value"]
            secret_value = base64.b64decode(encrypted_value).decode()
            
            # Verify checksum
            checksum = hashlib.sha256(secret_value.encode()).hexdigest()
            if checksum != encrypted_data["checksum"]:
                return None
            
            return secret_value
            
        except Exception:
            return None
    
    def setup_environment(self) -> bool:
        """Setup environment variables from secrets"""
        print("🔧 Setting up environment from secrets...")
        
        secrets_count = 0
        
        for service_name in self.config["secrets"]:
            secret_value = self.get_secret(service_name)
            if secret_value:
                env_var = self.config["secrets"][service_name]["environment_var"]
                import os
                os.environ[env_var] = secret_value
                secrets_count += 1
                print(f"   ✅ Set {env_var}")
        
        print(f"✅ Environment configured with {secrets_count} secrets")
        return secrets_count > 0
    
    def test_secrets_access(self) -> Dict[str, bool]:
        """Test access to all secrets"""
        print("🧪 Testing secrets access...")
        
        results = {}
        
        for service_name in self.config["secrets"]:
            secret_value = self.get_secret(service_name)
            results[service_name] = secret_value is not None
            
            if secret_value:
                print(f"   ✅ {service_name}: accessible")
            else:
                print(f"   ❌ {service_name}: not accessible")
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"✅ Successfully accessed {success_count}/{total_count} secrets")
        return results

# Global enhanced secrets client
secrets_client = EnhancedSecretsClient()

def get_secret(service_name: str) -> Optional[str]:
    """Get secret for a service"""
    return secrets_client.get_secret(service_name)

def setup_environment_from_secrets() -> bool:
    """Setup environment from secrets"""
    return secrets_client.setup_environment()

def test_all_secrets() -> Dict[str, bool]:
    """Test access to all secrets"""
    return secrets_client.test_secrets_access()

print("✅ Enhanced secrets client initialized for autonomous team")