#!/usr/bin/env python3
"""
File Operations Tool - Autonomous Team
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class FileOperationsTool:
    def __init__(self):
        self.repositories = {
            "strands_core": "/root/CascadeProjects/strands-agent-team",
            "python_repos": "/root/CascadeProjects"
        }
        
    def search_in_repositories(self, query: str, file_pattern: str = "*.py"):
        print(f"🔍 Searching repositories for: {query}")
        
        results = []
        
        for repo_name, repo_path in self.repositories.items():
            if not os.path.exists(repo_path):
                continue
            
            try:
                cmd = ["grep", "-r", "-n", query, repo_path, "--include=" + file_pattern]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if ':' in line:
                            parts = line.split(':', 2)
                            if len(parts) >= 3:
                                file_path, line_num, content = parts[:3]
                                results.append({
                                    "repository": repo_name,
                                    "file": file_path,
                                    "line_number": int(line_num),
                                    "content": content.strip()
                                })
                
            except Exception as e:
                print(f"   ❌ Search error in {repo_name}: {e}")
        
        print(f"   ✅ Found {len(results)} matches")
        return results

file_ops = FileOperationsTool()

def search_repositories(query: str, pattern: str = "*.py"):
    return file_ops.search_in_repositories(query, pattern)

print("✅ File operations tool initialized")