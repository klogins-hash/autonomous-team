#!/usr/bin/env python3
"""
MCP Server Manager - Autonomous Team
Add, configure, and manage MCP servers
"""

import json
import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class MCPServerManager:
    """Manage MCP servers for autonomous team"""
    
    def __init__(self):
        self.mcp_config_path = Path("/root/CascadeProjects/autonomous_team_workspace/integration/mcp_servers/mcp_config.json")
        self.servers_config = self.load_mcp_config()
        
    def load_mcp_config(self) -> Dict[str, Any]:
        """Load MCP server configuration"""
        if self.mcp_config_path.exists():
            with open(self.mcp_config_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "mcpServers": {},
                "deployment_status": "initialized",
                "last_updated": None
            }
    
    def save_mcp_config(self):
        """Save MCP server configuration"""
        self.servers_config["last_updated"] = datetime.now().isoformat()
        with open(self.mcp_config_path, 'w') as f:
            json.dump(self.servers_config, f, indent=2)
    
    def add_mcp_server(self, 
                      server_name: str,
                      command: str,
                      args: List[str] = None,
                      env: Dict[str, str] = None,
                      description: str = None) -> bool:
        """Add a new MCP server"""
        print(f"🌐 Adding MCP server: {server_name}")
        
        server_config = {
            "command": command,
            "args": args or [],
            "env": env or {},
            "description": description or f"MCP server: {server_name}",
            "added_at": datetime.now().isoformat(),
            "status": "configured"
        }
        
        self.servers_config["mcpServers"][server_name] = server_config
        self.save_mcp_config()
        
        print(f"   ✅ MCP server {server_name} added successfully")
        return True
    
    def remove_mcp_server(self, server_name: str) -> bool:
        """Remove an MCP server"""
        if server_name in self.servers_config["mcpServers"]:
            del self.servers_config["mcpServers"][server_name]
            self.save_mcp_config()
            print(f"   ✅ MCP server {server_name} removed")
            return True
        else:
            print(f"   ❌ MCP server {server_name} not found")
            return False
    
    def list_mcp_servers(self) -> List[Dict[str, Any]]:
        """List all configured MCP servers"""
        servers = []
        for name, config in self.servers_config["mcpServers"].items():
            servers.append({
                "name": name,
                "description": config.get("description", ""),
                "command": config["command"],
                "status": config.get("status", "unknown"),
                "added_at": config.get("added_at", "")
            })
        return servers
    
    def test_mcp_server(self, server_name: str) -> bool:
        """Test MCP server connectivity"""
        if server_name not in self.servers_config["mcpServers"]:
            print(f"   ❌ MCP server {server_name} not found")
            return False
        
        server_config = self.servers_config["mcpServers"][server_name]
        
        try:
            # Test server command
            cmd = [server_config["command"]] + server_config["args"]
            
            # Set environment variables
            env = subprocess.os.environ.copy()
            env.update(server_config.get("env", {}))
            
            # Run test (timeout after 10 seconds)
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"   ✅ MCP server {server_name} is responding")
                server_config["status"] = "active"
                server_config["last_test"] = datetime.now().isoformat()
            else:
                print(f"   ❌ MCP server {server_name} test failed")
                server_config["status"] = "error"
                server_config["error"] = result.stderr
            
            self.save_mcp_config()
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"   ⏰ MCP server {server_name} test timed out")
            server_config["status"] = "timeout"
            self.save_mcp_config()
            return False
        except Exception as e:
            print(f"   ❌ MCP server {server_name} test error: {e}")
            server_config["status"] = "error"
            server_config["error"] = str(e)
            self.save_mcp_config()
            return False
    
    def deploy_mcp_servers_to_scaleway(self) -> bool:
        """Deploy MCP servers to Scaleway infrastructure"""
        print("🚀 Deploying MCP servers to Scaleway...")
        
        # Create Scaleway deployment configuration
        deployment_config = {
            "name": "autonomous-team-mcp-servers",
            "project_id": "a4b7c9d3-e2f1-4a5b-8c9d-0e1f2a3b4c5d",
            "region": "fr-par-2",
            "servers": {}
        }
        
        for server_name, server_config in self.servers_config["mcpServers"].items():
            deployment_config["servers"][server_name] = {
                "command": server_config["command"],
                "args": server_config["args"],
                "env": server_config.get("env", {}),
                "instance_type": "PLAY2-PICO",  # Lightweight for MCP servers
                "description": server_config.get("description", "")
            }
        
        # Save deployment configuration
        deployment_file = Path("/root/CascadeProjects/autonomous_team_workspace/infrastructure/scaleway/mcp_deployment.yaml")
        with open(deployment_file, 'w') as f:
            yaml.dump(deployment_config, f, default_flow_style=False)
        
        print(f"   ✅ MCP deployment configuration saved to {deployment_file}")
        return True

# Global MCP manager instance
mcp_manager = MCPServerManager()

def add_mcp_server(name: str, command: str, **kwargs) -> bool:
    return mcp_manager.add_mcp_server(name, command, **kwargs)

def list_mcp_servers() -> List[Dict[str, Any]]:
    return mcp_manager.list_mcp_servers()

def test_mcp_server(name: str) -> bool:
    return mcp_manager.test_mcp_server(name)

def deploy_to_scaleway() -> bool:
    return mcp_manager.deploy_mcp_servers_to_scaleway()

print("✅ MCP server manager initialized for autonomous team")