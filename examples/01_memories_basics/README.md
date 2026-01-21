# Memory Basics

## Goal

Master memory CRUD operations, bulk operations, and pagination patterns.

## Prerequisites

- Completed [00_getting_started](../00_getting_started/)
- Trix SDK installed and configured

## Concepts Covered

### 1. Memory Types

Trix supports different memory types:
```python
from trix.types import MemoryType

memory = client.memories.create(
    content="...",
    type=MemoryType.TEXT,  # or IMAGE, AUDIO, etc.
)
```

### 2. CRUD Operations

| Operation | Method | Description |
|-----------|--------|-------------|
| Create | `memories.create()` | Create a single memory |
| Read | `memories.get(id)` | Retrieve by ID |
| Update | `memories.update(id, ...)` | Modify existing memory |
| Delete | `memories.delete(id)` | Remove a memory |

### 3. Bulk Operations

For better performance with multiple items:

```python
# Bulk create
memories = client.memories.bulk_create([
    {"content": "Memory 1", "tags": ["tag1"]},
    {"content": "Memory 2", "tags": ["tag2"]},
])

# Bulk update
client.memories.bulk_update([
    {"id": "mem_1", "tags": ["updated"]},
    {"id": "mem_2", "tags": ["updated"]},
])

# Bulk delete
client.memories.bulk_delete(["mem_1", "mem_2"])
```

### 4. Pagination

Two approaches for listing memories:

**Manual Pagination:**
```python
page = client.memories.list(limit=100, cursor=None)
while page.pagination.has_more:
    for memory in page.data:
        process(memory)
    page = client.memories.list(limit=100, cursor=page.pagination.cursor)
```

**Automatic with iter():**
```python
for memory in client.memories.iter(page_size=100, max_items=1000):
    process(memory)
```

### 5. Statistics and Configuration

```python
# Get statistics
stats = client.memories.get_stats()
print(f"Total: {stats.total_memories}")

# Get configuration
config = client.memories.get_config()
print(f"Max length: {config.max_content_length}")
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates a memory with type, tags, and metadata
2. Retrieves and displays the memory
3. Updates tags and metadata
4. Demonstrates bulk create (3 memories at once)
5. Lists memories with pagination
6. Uses `iter()` for automatic pagination
7. Fetches stats and config
8. Performs bulk update and delete for cleanup

### Async Version (`async_example.py`)

Same operations with concurrent execution:
- Creates multiple memories in parallel with `asyncio.gather()`
- Fetches stats and config concurrently

## Running the Examples

```bash
python main.py         # Synchronous
python async_example.py  # Asynchronous
```

## Running Tests

```bash
pytest test_example.py -v
```

## Next Steps

- [02_search_and_retrieval](../02_search_and_retrieval/) - Finding memories with search

