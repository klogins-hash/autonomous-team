#!/usr/bin/env python3
"""
Documentation-First Workflow - Autonomous Team
Always check DeepWiki documentation before implementation
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add DeepWiki integration
sys.path.insert(0, '/root/CascadeProjects/autonomous_team_workspace/integration/deepwiki')
from deepwiki_client import check_documentation_first, doc_client

class DocumentationFirstWorkflow:
    """Workflow that prioritizes documentation for autonomous agents"""
    
    def __init__(self):
        self.workspace = Path("/root/CascadeProjects/autonomous_team_workspace")
        
    def execute_task_with_docs(self, task: str, specialty: str = None):
        """Execute task with documentation-first approach"""
        print(f"🎯 Executing task: {task}")
        print("=" * 40)
        
        # Step 1: Always check documentation first
        print("🔍 Step 1: Checking DeepWiki documentation...")
        doc_results = check_documentation_first(task, specialty)
        
        if doc_results:
            print("✅ Documentation found - proceeding with best practices")
            self.apply_documentation_guidance(doc_results, task)
        else:
            print("📚 No specific documentation found - using autonomous approach")
            self.use_autonomous_approach(task, specialty)
        
        # Step 2: Log documentation usage
        self.log_documentation_usage(task, doc_results)
        
        print(f"✅ Task completed: {task}")
    
    def apply_documentation_guidance(self, doc_results, task):
        """Apply guidance from documentation"""
        print("📖 Applying documentation guidance...")
        
        for result in doc_results.get("results", []):
            title = result.get("title", "Documentation")
            content = result.get("content", "")
            
            print(f"   📚 {title}")
            
            # Extract key insights
            if "best practice" in content.lower():
                print("      ✨ Best practice identified")
            if "example" in content.lower():
                print("      💡 Code example available")
            if "warning" in content.lower() or "caution" in content.lower():
                print("      ⚠️  Warning noted")
    
    def use_autonomous_approach(self, task, specialty):
        """Use autonomous approach when documentation is limited"""
        print("🤖 Using autonomous reasoning...")
        print(f"   🧠 Specialty: {specialty}")
        print(f"   🎯 Task: {task}")
        
        # Check for related documentation
        related_docs = doc_client.search_documentation(f"general {specialty}")
        if related_docs:
            print("   📚 Found related documentation for guidance")
    
    def log_documentation_usage(self, task, doc_results):
        """Log documentation usage for learning"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "documentation_found": doc_results is not None,
            "doc_count": len(doc_results.get("results", [])) if doc_results else 0
        }
        
        log_file = self.workspace / "logs" / "documentation_usage.json"
        
        # Load existing logs
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        # Save updated logs
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print("📊 Documentation usage logged")

# Global workflow instance
workflow = DocumentationFirstWorkflow()

def execute_with_documentation(task: str, specialty: str = None):
    """Execute task with documentation-first approach"""
    workflow.execute_task_with_docs(task, specialty)

print("✅ Documentation-first workflow initialized")