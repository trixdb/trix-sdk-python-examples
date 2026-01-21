# Search and Retrieval

## Goal

Learn to find memories using semantic search, similarity matching, and topic-based retrieval.

## Prerequisites

- Completed [01_memories_basics](../01_memories_basics/)
- Understanding of CRUD operations

## Concepts Covered

### 1. Semantic Query Search

Find memories based on meaning, not just keywords:

```python
results = client.search.query(
    query="How do neural networks learn?",
    limit=10,
    threshold=0.5,  # Minimum similarity score (0.0-1.0)
    tags=["ml"],    # Optional: filter by tags
)

for result in results.results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.memory.content}")
```

### 2. Similar Memory Search

Find memories similar to a specific memory:

```python
similar = client.search.similar(
    memory_id="mem_123",
    limit=5,
    exclude_self=True,  # Don't include source memory
)
```

### 3. Embedding Generation

Generate vector embeddings for custom use:

```python
# Single text
embedding = client.search.embed(text="Your text here")
vector = embedding.embedding  # List of floats

# Batch embedding
embeddings = client.search.embed_all(
    texts=["Text 1", "Text 2", "Text 3"]
)
```

### 4. Topic-Based Search

Retrieve memories by topic:

```python
results = client.search.by_topic(
    topic="machine learning",
    limit=10
)
```

### 5. Search Configuration

Get search system configuration:

```python
config = client.search.get_config()
print(f"Max results: {config.max_limit}")
print(f"Embedding size: {config.embedding_dimensions}")
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `query` | Natural language search query | Required |
| `limit` | Maximum results to return | 10 |
| `threshold` | Minimum similarity score (0-1) | 0.0 |
| `tags` | Filter by tags | None |
| `space_id` | Limit to specific space | None |

## Walkthrough

### Sync Version (`main.py`)

1. Creates sample memories about various topics
2. Performs semantic search with natural language
3. Applies tag filters to narrow results
4. Finds similar memories to a specific one
5. Generates embeddings for custom text
6. Batch generates multiple embeddings
7. Performs topic-based retrieval

### Async Version (`async_example.py`)

Same operations with concurrent execution:
- Runs multiple searches in parallel
- Generates embeddings concurrently
- Demonstrates `asyncio.gather()` for batch operations

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Running Tests

```bash
pytest test_example.py -v
```

## Next Steps

- [03_relationships](../03_relationships/) - Connect memories with relationships

