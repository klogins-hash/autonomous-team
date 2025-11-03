#!/usr/bin/env python3
"""
MCP Server Management Script - Autonomous Team
Add, remove, and manage MCP servers
"""

import sys
import json
from pathlib import Path

# Add MCP manager to path
sys.path.append("/root/CascadeProjects/autonomous_team_workspace/integration/mcp_servers")
from mcp_manager import add_mcp_server, list_mcp_servers, test_mcp_server, deploy_to_scaleway

def main():
    print("🌐 MCP Server Management - Autonomous Team")
    print("=" * 50)
    
    # List current servers
    print("📋 Current MCP servers:")
    servers = list_mcp_servers()
    for server in servers:
        print(f"   ✅ {server['name']}: {server['description']}")
    
    # Add example new server
    print("\n➕ Adding example MCP server...")
    add_mcp_server(
        name="web-search-server",
        command="python3",
        args=["/root/CascadeProjects/autonomous_team_workspace/tools/comprehensive/web_search.py"],
        description="Custom web search server for autonomous team"
    )
    
    # Test servers
    print("\n🧪 Testing MCP servers...")
    for server in list_mcp_servers():
        test_mcp_server(server['name'])
    
    # Deploy to Scaleway
    print("\n🚀 Deploying to Scaleway...")
    deploy_to_scaleway()
    
    print("\n✅ MCP server management complete")

if __name__ == "__main__":
    main()