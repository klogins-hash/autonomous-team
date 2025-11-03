#!/usr/bin/env python3
"""
Unified Tools Interface - Autonomous Team
"""

import sys
from pathlib import Path

# Add tools to path
tools_path = Path(__file__).parent
sys.path.insert(0, str(tools_path))

# Import all tools
from web_search import search_web
from e2b_sandbox import create_sandbox
from code_execution import execute_code_local
from api_testing import test_api, test_cartesia_api_integration
from file_operations import search_repositories

class UnifiedToolsInterface:
    def __init__(self):
        self.tools = {
            "web_search": {"function": search_web, "description": "Search the web"},
            "e2b_sandbox": {"function": create_sandbox, "description": "Create E2B sandbox"},
            "code_execution": {"function": execute_code_local, "description": "Execute code locally"},
            "api_testing": {"function": test_api, "description": "Test API endpoints"},
            "repository_search": {"function": search_repositories, "description": "Search repositories"}
        }
        
        print(f"🔧 Unified tools interface loaded with {len(self.tools)} tools")
    
    def solve_problem_with_tools(self, problem: str) -> dict:
        print(f"🎯 Solving problem: {problem}")
        print("=" * 50)
        
        solution_steps = []
        
        # Step 1: Search web
        print("🌐 Step 1: Searching web...")
        web_results = self.use_tool("web_search", problem + " solution")
        if web_results:
            solution_steps.append({
                "step": "Web Search",
                "result": f"Found {len(web_results)} results",
                "data": web_results[:3]
            })
        
        # Step 2: Search repositories
        print("📁 Step 2: Searching repositories...")
        repo_results = self.use_tool("repository_search", problem, "*.py")
        if repo_results:
            solution_steps.append({
                "step": "Repository Search", 
                "result": f"Found {len(repo_results)} matches",
                "data": repo_results[:3]
            })
        
        # Step 3: Test API if relevant
        if "api" in problem.lower():
            print("🔌 Step 3: Testing API...")
            api_test = test_cartesia_api_integration()
            solution_steps.append({
                "step": "API Test",
                "result": "API test completed" if api_test else "API test failed",
                "data": {"success": api_test}
            })
        
        return {
            "problem": problem,
            "solution_steps": solution_steps,
            "total_steps": len(solution_steps)
        }
    
    def use_tool(self, tool_name: str, *args, **kwargs):
        if tool_name not in self.tools:
            print(f"❌ Unknown tool: {tool_name}")
            return None
        
        tool_info = self.tools[tool_name]
        print(f"🛠️  Using tool: {tool_name}")
        
        try:
            result = tool_info["function"](*args, **kwargs)
            return result
        except Exception as e:
            print(f"❌ Tool {tool_name} error: {e}")
            return None

unified_tools = UnifiedToolsInterface()

def solve_problem(problem: str) -> dict:
    return unified_tools.solve_problem_with_tools(problem)

print("✅ Unified tools interface ready")