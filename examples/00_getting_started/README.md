# Getting Started with Trix SDK

## Goal

Learn the fundamentals of the Trix Python SDK by creating, retrieving, searching, and managing memories.

## Prerequisites

- Python 3.11+
- Trix SDK installed: `pip install trixdb`
- A Trix API key (get one at https://trixdb.com)

## Setup

1. Set your API key as an environment variable:
   ```bash
   export TRIX_API_KEY=your_api_key_here
   ```

2. Or create a `.env` file (using python-dotenv):
   ```
   TRIX_API_KEY=your_api_key_here
   ```

## Concepts Covered

### 1. Client Initialization

The SDK provides two client classes:
- `Trix` - Synchronous client for blocking operations
- `AsyncTrix` - Asynchronous client for non-blocking operations

Both support the same methods with identical signatures.

### 2. Environment-Based Configuration

Use `from_env()` for production code:
```python
from trix import Trix

client = Trix.from_env()  # Reads TRIX_API_KEY automatically
```

### 3. Context Managers

Always use context managers to ensure proper resource cleanup:
```python
with Trix.from_env() as client:
    # Your code here
    pass  # Resources cleaned up automatically
```

### 4. Basic Memory Operations

- **Create**: `client.memories.create(content="...", tags=[...])`
- **Read**: `client.memories.get(memory_id)`
- **Update**: `client.memories.update(memory_id, tags=[...])`
- **Delete**: `client.memories.delete(memory_id)`

### 5. Searching

Use semantic search to find relevant memories:
```python
results = client.search.query(query="your question", limit=5)
```

## Walkthrough

### Synchronous Version (`main.py`)

1. Creates a client using environment variables
2. Creates a memory with content, tags, and metadata
3. Retrieves the memory by ID
4. Performs a semantic search
5. Updates the memory's tags
6. Cleans up by deleting the memory

### Async Version (`async_example.py`)

Same operations using `async/await`:
1. Uses `AsyncTrix` client
2. Demonstrates concurrent memory creation with `asyncio.gather()`
3. Shows non-blocking search operations

## Running the Examples

```bash
# Synchronous version
python main.py

# Asynchronous version
python async_example.py
```

## Running Tests

```bash
pytest test_example.py -v
```

## Next Steps

- [01_memories_basics](../01_memories_basics/) - Deep dive into memory operations
- [02_search_and_retrieval](../02_search_and_retrieval/) - Advanced search techniques

