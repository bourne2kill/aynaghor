# 🔮 AYNAGH0R API Documentation

This document describes the APIs available in the AYNAGH0R system, including both the KH4NK1 Agent API and the AYNAGH0R Engine API.

## 🤖 KH4NK1 Agent API

The KH4NK1 Agent provides a FastAPI-based REST API for system management and task execution.

### Base URL
```
http://localhost:3000
```

### Authentication
Currently, no authentication is required for local development. In production, implement proper authentication mechanisms.

### Endpoints

#### GET /status
Get the current status of the KH4NK1 agent.

**Response:**
```json
{
  "status": "alive",
  "pid": 12345,
  "uptime": "2h 30m",
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:3000/status
```

#### GET /health
Comprehensive health check including system resources.

**Response:**
```json
{
  "status": "healthy",
  "system": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_percent": 23.1
  },
  "services": {
    "aynaghor_ui": "running",
    "agent_api": "running"
  }
}
```

#### POST /execute
Execute a shell command with sudo whitelist security.

**Request Body:**
```json
{
  "command": "echo 'Hello AYNAGH0R'",
  "timeout": 30
}
```

**Response:**
```json
{
  "success": true,
  "output": "Hello AYNAGH0R\n",
  "error": null,
  "exit_code": 0,
  "execution_time": 0.05
}
```

**Example:**
```bash
curl -X POST http://localhost:3000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la", "timeout": 10}'
```

#### POST /generate-app
Trigger the AYNAGH0R application generation process.

**Request Body:**
```json
{
  "force_regenerate": false,
  "config_overrides": {
    "use_gemini": true,
    "default_theme": "dark_fantasy"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "AYNAGH0R application generated successfully",
  "generated_files": [
    "workspace/aynaghor/ui/app.py",
    "workspace/aynaghor/core/engine.py",
    "workspace/aynaghor/modules/gemini.py"
  ],
  "generation_time": 2.34
}
```

#### GET /logs
Retrieve recent system logs.

**Query Parameters:**
- `lines` (optional): Number of log lines to return (default: 100)
- `level` (optional): Log level filter (DEBUG, INFO, WARNING, ERROR)

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-11-03T10:30:00Z",
      "level": "INFO",
      "message": "AYNAGH0R engine initialized successfully",
      "source": "engine.py"
    }
  ],
  "total_lines": 150
}
```

## 🌙 AYNAGH0R Engine API

The AYNAGH0R Engine provides programmatic access to story generation capabilities.

### Python API

#### Engine Class

```python
from core.engine import Engine

# Initialize the engine
engine = Engine()

# Generate a story
story = engine.route("A dark castle on a stormy night")

# Check engine health
health = engine.health_check()
```

#### Methods

##### `route(prompt: str) -> str`
Generate a story based on the provided prompt.

**Parameters:**
- `prompt` (str): The story prompt or request

**Returns:**
- `str`: Generated story content or error message

**Example:**
```python
engine = Engine()
story = engine.route("Tell me about a haunted forest")
print(story)
```

##### `health_check() -> dict`
Check the health status of all AI clients.

**Returns:**
```python
{
    "engine_status": "healthy",
    "use_gemini": True,
    "clients": {
        "gemini": {
            "initialized": True,
            "healthy": True
        },
        "localai": {
            "initialized": False,
            "healthy": False
        }
    }
}
```

### Gemini Client API

#### GeminiClient Class

```python
from modules.gemini import GeminiClient

# Initialize with API key
client = GeminiClient(api_key="your_api_key", model_name="gemini-1.5-flash")

# Generate content
story = client.generate("A mysterious tale of ancient magic")

# Test connection
is_healthy = client.test_connection()
```

#### Methods

##### `generate(prompt: str, max_retries: int = 3) -> str`
Generate story content using the Gemini API.

**Parameters:**
- `prompt` (str): The story prompt
- `max_retries` (int): Maximum retry attempts (default: 3)

**Returns:**
- `str`: Generated story with atmospheric formatting

**Features:**
- Automatic dark fantasy prompt enhancement
- Rate limiting (10 requests/minute)
- Safety filtering
- Error handling with user-friendly messages

##### `test_connection() -> bool`
Test if the Gemini API is accessible and responding.

**Returns:**
- `bool`: True if connection is healthy, False otherwise

## 🔧 Configuration API

### Environment Variables

The system uses environment variables for configuration. These can be set in a `.env` file:

```bash
# AI Provider
USE_GEMINI=true
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Local AI (alternative)
LLM_HOST=http://localhost:8080
LLM_MODEL=llama2-7b-chat

# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Security
MAX_REQUESTS_PER_MINUTE=10
MAX_TOKENS_PER_DAY=15000
```

### Configuration Loading

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access configuration
use_gemini = os.getenv('USE_GEMINI', 'true').lower() == 'true'
api_key = os.getenv('GEMINI_API_KEY')
model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
```

## 🚨 Error Handling

### Common Error Responses

#### Rate Limit Exceeded
```json
{
  "error": "rate_limit_exceeded",
  "message": "⏱️ Rate limit exceeded. Please wait a moment before generating another story.",
  "retry_after": 60
}
```

#### API Key Invalid
```json
{
  "error": "authentication_failed",
  "message": "❌ Gemini model not initialized. Please check your API key.",
  "details": "Invalid API key provided"
}
```

#### Content Filtered
```json
{
  "error": "content_filtered",
  "message": "🛡️ Content filtered for safety. Please try a different story theme.",
  "category": "safety_filter"
}
```

#### Quota Exceeded
```json
{
  "error": "quota_exceeded",
  "message": "📊 Daily quota exceeded. The storyteller needs rest until tomorrow.",
  "reset_time": "2025-11-04T00:00:00Z"
}
```

## 📊 Monitoring & Metrics

### Health Check Endpoints

#### Engine Health
```python
from core.engine import Engine

engine = Engine()
health = engine.health_check()

# Check if engine is operational
if health["engine_status"] == "healthy":
    print("✅ Engine is healthy")
else:
    print("❌ Engine has issues")
```

#### Client Status
```python
# Check Gemini client
gemini_status = health["clients"]["gemini"]
if gemini_status["initialized"] and gemini_status["healthy"]:
    print("✅ Gemini client is ready")

# Check LocalAI client
localai_status = health["clients"]["localai"]
if localai_status["initialized"] and localai_status["healthy"]:
    print("✅ LocalAI client is ready")
```

### Logging

The system provides comprehensive logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log levels used:
# DEBUG: Detailed debugging information
# INFO: General operational messages
# WARNING: Warning messages (non-critical issues)
# ERROR: Error messages (critical issues)
```

## 🔒 Security Considerations

### API Security

1. **Rate Limiting**: Built-in rate limiting prevents abuse
2. **Input Validation**: All inputs are validated and sanitized
3. **Error Handling**: Errors don't expose sensitive information
4. **Content Filtering**: AI-generated content is filtered for safety

### Best Practices

1. **API Keys**: Store API keys in environment variables, never in code
2. **HTTPS**: Use HTTPS in production environments
3. **Authentication**: Implement proper authentication for production
4. **Monitoring**: Monitor API usage and set up alerts
5. **Logging**: Log security events and API access

## 📝 Examples

### Complete Story Generation Example

```python
#!/usr/bin/env python3
"""
Complete example of using the AYNAGH0R API for story generation
"""

import os
from dotenv import load_dotenv
from core.engine import Engine

def main():
    # Load configuration
    load_dotenv()

    # Initialize engine
    engine = Engine()

    # Check health
    health = engine.health_check()
    print(f"Engine Status: {health['engine_status']}")

    # Generate a story
    prompt = "A mysterious traveler arrives at a haunted inn during a thunderstorm"

    print(f"\nGenerating story for prompt: {prompt}")
    print("-" * 50)

    story = engine.route(prompt)
    print(story)

    print("-" * 50)
    print("Story generation complete!")

if __name__ == "__main__":
    main()
```

### Batch Story Generation

```python
#!/usr/bin/env python3
"""
Example of generating multiple stories with different settings
"""

from core.engine import Engine
import time

def generate_stories():
    engine = Engine()

    prompts = [
        "A cursed sword in an ancient tomb",
        "A witch's cottage in the deep woods",
        "A ghost ship on a foggy sea",
        "A vampire's castle at midnight",
        "A dragon's lair in the mountains"
    ]

    stories = []

    for i, prompt in enumerate(prompts, 1):
        print(f"Generating story {i}/{len(prompts)}: {prompt}")

        story = engine.route(prompt)
        stories.append({
            'prompt': prompt,
            'story': story,
            'length': len(story)
        })

        # Respect rate limits
        time.sleep(6)  # Wait 6 seconds between requests

    return stories

if __name__ == "__main__":
    stories = generate_stories()

    print(f"\nGenerated {len(stories)} stories:")
    for i, story_data in enumerate(stories, 1):
        print(f"{i}. {story_data['prompt']} ({story_data['length']} chars)")
```

## 🔗 Integration Examples

### Web API Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.engine import Engine

app = FastAPI(title="AYNAGH0R Story API")
engine = Engine()

class StoryRequest(BaseModel):
    prompt: str
    max_length: int = 1000

class StoryResponse(BaseModel):
    story: str
    prompt: str
    length: int
    status: str

@app.post("/generate", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        story = engine.route(request.prompt)

        return StoryResponse(
            story=story,
            prompt=request.prompt,
            length=len(story),
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return engine.health_check()
```

---

*🌙 For more information, see the main [README](../workspace/aynaghor/README.md) or visit the [GitHub repository](https://github.com/bourne2kill/aynaghor) 🌙*