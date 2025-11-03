#!/usr/bin/env python3
"""
Web Search Tool - Autonomous Team
"""

import requests
import re
from typing import List, Dict, Any

class WebSearchTool:
    def __init__(self):
        self.max_results = 10
        
    def search(self, query: str, engine: str = "duckduckgo") -> List[Dict[str, Any]]:
        print(f"🔍 Web Search: {query}")
        
        try:
            # DuckDuckGo HTML search
            headers = {"User-Agent": "Mozilla/5.0 (compatible; AutonomousAgent/1.0)"}
            params = {"q": query}
            
            response = requests.get(
                "https://duckduckgo.com/html/",
                params=params,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = self.parse_ddg_results(response.text)
                print(f"   ✅ Found {len(results)} results")
                return results[:self.max_results]
            else:
                print(f"   ❌ Search failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Search error: {e}")
            return []
    
    def parse_ddg_results(self, html: str) -> List[Dict[str, Any]]:
        results = []
        pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)".*?>(.*?)</a>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        for url, title in matches:
            results.append({
                "title": self.clean_text(title),
                "url": url,
                "snippet": "",
                "engine": "duckduckgo"
            })
        
        return results
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-zA-Z]+;', '', text)
        text = ' '.join(text.split())
        return text

web_search = WebSearchTool()

def search_web(query: str) -> List[Dict[str, Any]]:
    return web_search.search(query)

print("✅ Web search tool initialized")