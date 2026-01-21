# Knowledge Graph

## Goal

Learn to traverse and analyze the knowledge graph formed by memory relationships.

## Prerequisites

- Completed [05_agent_sessions](../05_agent_sessions/)
- Understanding of relationships

## Concepts Covered

### 1. Graph Traversal

Walk the graph from a starting point:

```python
traversal = client.graph.traverse(
    start_id="mem_123",
    max_depth=3,           # How far to explore
    direction="both",      # "outgoing", "incoming", or "both"
    limit=50
)

for node in traversal.nodes:
    print(f"Depth {node.depth}: {node.content}")
```

### 2. Shortest Path

Find the shortest connection between two memories:

```python
path = client.graph.shortest_path(
    source_id="mem_123",
    target_id="mem_456",
    max_depth=10
)

print(f"Path length: {len(path.path)} hops")
for node in path.path:
    print(f"  → {node.content}")
```

### 3. Neighbors

Get directly connected memories:

```python
neighbors = client.graph.neighbors(
    memory_id="mem_123",
    direction="both",
    limit=20
)
```

### 4. Graph Expansion

Expand context from multiple starting points:

```python
expanded = client.graph.expand(
    memory_ids=["mem_1", "mem_2", "mem_3"],
    depth=2,
    limit=100
)
```

### 5. Graph Statistics

Get overall graph metrics:

```python
stats = client.graph.get_stats()
print(f"Nodes: {stats.total_nodes}")
print(f"Edges: {stats.total_edges}")
print(f"Average degree: {stats.average_degree}")
```

### 6. Context Retrieval

Get graph-aware context for queries:

```python
context = client.graph.get_context(
    query="web frameworks",
    start_ids=["mem_1", "mem_2"],
    max_depth=2,
    limit=10
)
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates a tech stack knowledge graph (React, Next.js, etc.)
2. Traverses from Next.js to discover connected nodes
3. Finds shortest path: Vercel → JavaScript
4. Gets React's neighbors
5. Expands from TypeScript
6. Retrieves graph statistics
7. Gets context for a query

### Async Version (`async_example.py`)

Parallel graph operations:
- Concurrent edge creation
- Parallel traversal, neighbors, and stats queries

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [07_facts_and_entities](../07_facts_and_entities/) - Extract structured knowledge

