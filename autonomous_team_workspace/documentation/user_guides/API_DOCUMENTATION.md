# 📡 Autonomous Team API Documentation

## Base URL
```
https://163.172.191.225
```

## Endpoints

### POST /voice
Synthesize speech with British voice profiles.

**Request:**
```json
{
  "text": "Hello from autonomous team!",
  "voice_profile": "professional_british",
  "format": "mp3"
}
```

**Response:**
```json
{
  "status": "success",
  "audio_url": "https://...",
  "duration": 2.5,
  "voice_profile": "professional_british"
}
```

### POST /search
Perform real-time web search.

**Request:**
```json
{
  "query": "serverless best practices",
  "max_results": 10,
  "semantic": true
}
```

**Response:**
```json
{
  "status": "success",
  "results": [
    {
      "title": "Serverless Best Practices",
      "url": "https://...",
      "snippet": "...",
      "relevance": 0.95
    }
  ],
  "total_results": 10
}
```

### POST /execute
Execute code in secure sandbox.

**Request:**
```json
{
  "code": "print('Hello World')",
  "language": "python",
  "timeout": 30
}
```

**Response:**
```json
{
  "status": "success",
  "output": "Hello World\n",
  "execution_time": 0.1,
  "memory_used": "12MB"
}
```

## Authentication

Currently open access. Enterprise features will include API key authentication.

## Rate Limits

- Free tier: 100 requests/minute
- Pro tier: 1000 requests/minute
- Enterprise: Unlimited

## Error Handling

All errors return JSON format:
```json
{
  "status": "error",
  "error": "Description of error",
  "error_code": "INVALID_REQUEST"
}
```
