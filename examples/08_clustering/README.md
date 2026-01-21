# Clustering

## Goal

Learn to automatically organize memories into clusters for better retrieval.

## Prerequisites

- Completed [07_facts_and_entities](../07_facts_and_entities/)

## Concepts Covered

### 1. Manual Cluster Creation

Create clusters explicitly:

```python
cluster = client.clusters.create(
    name="Python Topics",
    description="Memories about Python programming",
    metadata={"topic": "programming"}
)
```

### 2. Adding Memories to Clusters

```python
client.clusters.add_memory(
    cluster_id=cluster.id,
    memory_id=memory.id
)
```

### 3. Incremental Clustering

Automatically assign memories to clusters:

```python
result = client.clusters.incremental_clustering(
    memory_ids=["mem_1", "mem_2", "mem_3"],
    min_cluster_size=2,
    similarity_threshold=0.7
)

print(f"Created {result.clusters_created} clusters")
print(f"Assigned {result.memories_assigned} memories")
```

### 4. Cluster Expansion

Find similar memories to add:

```python
expansion = client.clusters.expand(
    cluster_id=cluster.id,
    limit=10,
    similarity_threshold=0.6
)

for suggestion in expansion.suggestions:
    print(f"{suggestion.memory.content} (score: {suggestion.score})")
```

### 5. Cluster Operations

```python
# Get cluster details
cluster = client.clusters.get(cluster_id)

# List all clusters
clusters = client.clusters.list(limit=20)

# Get memories in a cluster
memories = client.clusters.get_memories(cluster_id, limit=50)

# Remove memory from cluster
client.clusters.remove_memory(cluster_id, memory_id)

# Update cluster
client.clusters.update(cluster_id, name="New Name")

# Delete cluster
client.clusters.delete(cluster_id)
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates diverse memories (Python, Database, Web topics)
2. Creates a manual cluster
3. Adds Python memories to the cluster
4. Lists clusters and their contents
5. Runs incremental clustering on remaining memories
6. Expands cluster to find similar memories
7. Updates and removes from cluster

### Async Version (`async_example.py`)

Parallel operations:
- Concurrent cluster creation
- Parallel memory assignment
- Parallel cluster queries and expansion

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [09_webhooks](../09_webhooks/) - Event notifications

