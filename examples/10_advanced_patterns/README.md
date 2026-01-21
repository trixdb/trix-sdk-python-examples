# Advanced Patterns

## Goal

Learn production-ready patterns for error handling, retries, and performance.

## Prerequisites

- Completed all previous examples

## Concepts Covered

### 1. Exception Handling

The SDK provides specific exception types:

```python
from trix.exceptions import (
    TrixError,           # Base exception
    AuthenticationError, # 401 errors
    RateLimitError,      # 429 rate limiting
    NotFoundError,       # 404 not found
    ValidationError,     # 400 validation errors
    ServerError,         # 5xx server errors
)

try:
    client.memories.get("invalid_id")
except NotFoundError as e:
    print(f"Not found: {e.message}")
except ValidationError as e:
    print(f"Validation: {e.errors}")
except RateLimitError as e:
    time.sleep(e.retry_after)
except TrixError as e:
    print(f"API error: {e}")
```

### 2. Rate Limit Handling

```python
def with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                time.sleep(e.retry_after or (2 ** attempt))
            else:
                raise
```

### 3. Client Configuration

```python
client = Trix.from_env(
    timeout=30.0,      # Request timeout
    max_retries=3,     # Automatic retries
)
```

### 4. Batch Processing with Chunking

```python
def chunked_create(items: list, chunk_size: int = 100):
    results = []
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        created = client.memories.bulk_create(chunk)
        results.extend(created)
    return results
```

### 5. Async Concurrency Control

```python
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

async def limited_operation(id: str):
    async with semaphore:
        return await client.memories.get(id)

tasks = [limited_operation(id) for id in ids]
results = await asyncio.gather(*tasks)
```

### 6. Pagination

```python
# Manual pagination
cursor = None
while True:
    result = client.memories.list(limit=100, cursor=cursor)
    process(result.data)
    if not result.pagination.has_more:
        break
    cursor = result.pagination.cursor

# Using iterator (recommended)
for memory in client.memories.iter(limit=100):
    process(memory)
```

## Walkthrough

### Sync Version (`main.py`)

1. Demonstrates exception type handling
2. Shows rate limit retry pattern
3. Custom client configuration
4. Chunked batch operations
5. Manual and iterator pagination

### Async Version (`async_example.py`)

1. Async error handling
2. Semaphore-based concurrency control
3. Async iteration
4. Timeout handling
5. gather with return_exceptions

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Summary

You've completed all examples! You now know how to:

- ✅ Create, read, update, delete memories
- ✅ Search and retrieve with various methods
- ✅ Build knowledge graphs with relationships
- ✅ Implement multi-tenancy with spaces
- ✅ Create conversational agents with sessions
- ✅ Traverse and analyze graphs
- ✅ Extract and manage facts and entities
- ✅ Organize memories with clustering
- ✅ Set up webhook notifications
- ✅ Handle errors and optimize performance

