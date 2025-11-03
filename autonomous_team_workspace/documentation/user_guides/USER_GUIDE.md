# 🚀 Autonomous Team User Guide

## Quick Start

### 1. URL-based MCP Integration
```json
{
  "mcpServers": {
    "autonomous-team-url": {
      "command": "python3",
      "args": ["/path/to/autonomous_team_url_mcp.py"],
      "env": {
        "BASE_URL": "https://163.172.191.225"
      }
    }
  }
}
```

### 2. Direct API Usage
```bash
# Voice Synthesis
curl -X POST https://163.172.191.225/voice \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello!", "voice_profile": "professional_british"}'

# Web Search
curl -X POST https://163.172.191.225/search \
  -H "Content-Type: application/json" \
  -d '{"query": "serverless architecture", "max_results": 10}'
```

## Capabilities

### Voice Synthesis
- 3 British voice profiles
- Real-time synthesis
- Multiple audio formats
- Emotion control

### Web Search
- Real-time search
- Semantic capabilities
- Source filtering
- Result caching

### Code Execution
- 8 programming languages
- Secure sandbox
- Package installation
- 60s timeout

### API Testing
- Multiple auth methods
- Test suites
- Mock servers
- Performance testing

## Deployment Methods

1. **GitHub Repository**: Complete source code
2. **NPX Package**: `npx @autonomous-team/mcp-server`
3. **Scaleway Serverless**: Production deployment
4. **URL-based MCP**: HTTP endpoint integration
