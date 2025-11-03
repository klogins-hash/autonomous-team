#!/usr/bin/env python3
"""
Code Execution Tool - Autonomous Team
"""

import subprocess
import tempfile
import os

class CodeExecutionTool:
    def __init__(self):
        self.supported_languages = {
            "python": {
                "extension": ".py",
                "command": ["python3"],
                "timeout": 30
            },
            "bash": {
                "extension": ".sh",
                "command": ["bash"],
                "timeout": 30
            }
        }
        
    def execute_code(self, code: str, language: str = "python"):
        print(f"💻 Executing {language} code locally")
        
        if language not in self.supported_languages:
            print(f"   ❌ Unsupported language: {language}")
            return None
        
        lang_config = self.supported_languages[language]
        
        try:
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix=lang_config["extension"], 
                delete=False
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            result = subprocess.run(
                lang_config["command"] + [temp_file_path],
                capture_output=True,
                text=True,
                timeout=lang_config["timeout"]
            )
            
            os.unlink(temp_file_path)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "language": language
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": ""
            }

code_executor = CodeExecutionTool()

def execute_code_local(code: str, language: str = "python"):
    return code_executor.execute_code(code, language)

print("✅ Code execution tool initialized")