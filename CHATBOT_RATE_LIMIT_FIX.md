# Chatbot Rate Limit Issue - Fixed

## Problem Diagnosis

The chatbot was failing with **429 (Too Many Requests)** errors from Cohere's embedding API. This happened because:

1. **Cohere Free Tier Limits**: The free API has very strict rate limits
2. **No Retry Logic**: Every failed request immediately returned an error
3. **Poor Error Handling**: Users saw raw technical errors instead of helpful messages

### Error Evidence (from logs):
```
ERROR - Embedding generation failed: status_code: 429, body: {'message': 'Please wait and try again later'}
ERROR - Retrieval failed: headers: {...}, status_code: 429
```

## What Was Fixed

### 1. **Added Exponential Backoff Retry Logic**
Location: `backend/src/services/chatbot_service.py:1615-1650`

The `get_embedding()` function now:
- Retries up to 3 times on rate limit errors
- Uses exponential backoff: waits 2s → 4s → 8s between retries
- Provides clear logging for each retry attempt
- Throws user-friendly error after max retries

### 2. **Improved Error Messages**
Location: `backend/src/services/chatbot_service.py:1678-1688`

The `retrieve()` function now provides context-aware messages:
- **Rate limit**: "The system is experiencing high load. Please wait a moment and try again."
- **Timeout**: "The search took too long. Please try rephrasing your question."
- **Other errors**: "Unable to search the knowledge base. Please try again."

## Test the Fix

### 1. Restart the Backend Server
```bash
cd backend
uvicorn src.main:app
```

### 2. Test with Multiple Queries
Try asking several questions in quick succession:
- "What is Physical AI?"
- "Explain ROS2"
- "How does Gazebo work?"

**Expected Behavior**:
- First few queries work normally
- If rate limit hit, system waits and retries automatically
- Users see helpful messages instead of errors

## Long-Term Solutions

### Option 1: Upgrade Cohere Plan (Recommended)
**Cost**: $20-40/month for Production tier
**Benefits**:
- 1000 requests/minute (vs ~10/minute free)
- Better reliability
- No exponential backoff needed

**To upgrade**:
1. Go to https://dashboard.cohere.com/billing
2. Choose "Production" plan
3. Update `.env` with new API key (if changed)

### Option 2: Use Alternative Embedding Services

#### A. OpenAI Embeddings
**Pros**: Very reliable, good rate limits
**Cons**: $0.00002 per 1K tokens (~$0.20 per 1M tokens)

```python
# In backend/src/services/chatbot_service.py
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_embedding(text: str) -> List[float]:
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
```

Add to `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

#### B. Google Gemini Embeddings (Free)
**Pros**: Free, generous limits
**Cons**: Requires Google Cloud setup

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def get_embedding(text: str) -> List[float]:
    result = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return result['embedding']
```

### Option 3: Implement Caching

Add embedding caching to avoid redundant API calls:

```python
from functools import lru_cache
import hashlib

# Simple in-memory cache (loses on restart)
embedding_cache = {}

async def get_embedding_cached(text: str) -> List[float]:
    # Create hash of text for cache key
    cache_key = hashlib.md5(text.encode()).hexdigest()

    if cache_key in embedding_cache:
        logger.info(f"Cache hit for embedding")
        return embedding_cache[cache_key]

    # Generate new embedding
    embedding = await get_embedding(text)
    embedding_cache[cache_key] = embedding
    return embedding
```

### Option 4: Rate Limiting on Your Backend

Add request throttling to prevent overwhelming the API:

```bash
pip install slowapi
```

```python
# In backend/src/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.websocket("/ws")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def websocket_endpoint(websocket: WebSocket):
    # existing code...
```

## Monitoring

### Watch the Logs
Look for these patterns:
```bash
# Good: Successful retrieval
INFO - Retrieved 5 results from Qdrant

# Warning: Retry in progress
WARNING - Rate limit hit (attempt 1/3). Waiting 2s...

# Error: All retries exhausted
ERROR - Rate limit exceeded after 3 retries
```

### Check Cohere Dashboard
1. Go to https://dashboard.cohere.com/
2. View "Usage" tab
3. Monitor API calls and rate limits

## Current Configuration

- **Embedding Model**: `embed-english-v3.0` (Cohere)
- **Retry Attempts**: 3
- **Backoff Times**: 2s, 4s, 8s
- **LLM Model**: `google/gemini-2.0-flash-001` (OpenRouter)
- **Vector DB**: Qdrant Cloud
- **Collection**: `physical-ai-humanoid_robotics_book1`

## Next Steps

1. **Test the fix** - Try multiple queries in quick succession
2. **Monitor logs** - Watch for retry patterns and success rates
3. **Consider upgrade** - If retries aren't enough, upgrade Cohere or switch providers
4. **Add caching** - Implement embedding cache for frequently asked questions
5. **User feedback** - Add loading states in frontend during retries

## Files Modified

- `backend/src/services/chatbot_service.py` (Lines 1550-1688)
  - Added `asyncio` import
  - Updated `get_embedding()` with retry logic
  - Improved error handling in `retrieve()`

## Contact

If issues persist after these fixes, check:
1. Cohere API status: https://status.cohere.com/
2. Backend logs: `backend/logs/` (if logging to file)
3. Network connectivity to Cohere and Qdrant
