#!/usr/bin/env python3
"""
DeepWiki Documentation Client - Autonomous Team
Always check documentation when help is needed
"""

import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class DeepWikiDocClient:
    """DeepWiki MCP server client for autonomous agents"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "your_deepwiki_api_key_here"
        self.base_url = "https://api.deepwiki.ai"
        self.cache = {}
        self.workspace = Path("/root/CascadeProjects/autonomous_team_workspace")
        
    def search_documentation(self, query: str, context: str = None) -> Optional[Dict[str, Any]]:
        """Search DeepWiki documentation for help"""
        print(f"🔍 DeepWiki Search: {query}")
        
        # Check cache first
        cache_key = f"{query}_{context}"
        if cache_key in self.cache:
            print("   📚 Found in documentation cache")
            return self.cache[cache_key]
        
        # Search DeepWiki
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            search_data = {
                "query": query,
                "context": context or "autonomous_agents",
                "max_results": 5,
                "include_code_examples": True
            }
            
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=search_data,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                # Cache results
                self.cache[cache_key] = results
                
                print(f"   ✅ Found {len(results.get('results', []))} documentation results")
                return results
            else:
                print(f"   ❌ DeepWiki search failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ DeepWiki client error: {e}")
            return None
    
    def get_best_practice(self, topic: str) -> Optional[str]:
        """Get best practices for a specific topic"""
        results = self.search_documentation(f"best practices {topic}")
        
        if results and results.get("results"):
            best_result = results["results"][0]
            return best_result.get("content", "")
        
        return None
    
    def get_code_example(self, language: str, task: str) -> Optional[str]:
        """Get code examples from documentation"""
        results = self.search_documentation(f"{language} {task} example", "code_examples")
        
        if results and results.get("results"):
            for result in results["results"]:
                if result.get("type") == "code_example":
                    return result.get("code", "")
        
        return None
    
    def should_check_docs(self, task: str, confidence: float = 0.7) -> bool:
        """Determine if documentation should be checked"""
        # Always check docs for complex tasks
        complex_keywords = [
            "integration", "authentication", "api", "deployment",
            "configuration", "optimization", "troubleshooting"
        ]
        
        if any(keyword in task.lower() for keyword in complex_keywords):
            return True
        
        # Check docs if confidence is low
        if confidence < 0.7:
            return True
        
        # Check docs for new patterns
        if "new" in task.lower() or "unknown" in task.lower():
            return True
        
        return False

# Import local documentation as fallback
from local_documentation import search_local_documentation

# Global documentation client instance
doc_client = DeepWikiDocClient()

def check_documentation_first(task: str, context: str = None) -> Optional[Dict[str, Any]]:
    """Always check documentation first when help is needed"""
    print("🤖 Autonomous Agent: Checking documentation first...")
    
    if doc_client.should_check_docs(task):
        # Try external DeepWiki first
        results = doc_client.search_documentation(task, context)
        
        if results:
            print("   📚 External documentation found - applying best practices")
            return results
        else:
            print("   🌐 External docs unavailable - checking local documentation...")
            # Fallback to local documentation
            local_results = search_local_documentation(task, context)
            
            if local_results:
                print("   📚 Local documentation found - applying best practices")
                return local_results
            else:
                print("   📚 No documentation found - using autonomous reasoning")
    
    return None

print("✅ DeepWiki documentation client initialized for autonomous team")