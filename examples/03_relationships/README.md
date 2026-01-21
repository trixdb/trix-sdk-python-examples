# Relationships

## Goal

Learn to create and manage relationships between memories to build knowledge graphs.

## Prerequisites

- Completed [02_search_and_retrieval](../02_search_and_retrieval/)
- Understanding of memory operations

## Concepts Covered

### 1. Relationship Types

Built-in relationship types:
- `RELATED_TO` - General association
- `SIMILAR_TO` - Content similarity
- `DERIVED_FROM` - Source/derivation
- `PART_OF` - Component relationship
- `CAUSES` - Causal relationship

### 2. Creating Relationships

```python
from trix.types import RelationshipType

relationship = client.relationships.create(
    source_id="mem_123",
    target_id="mem_456",
    relationship_type=RelationshipType.RELATED_TO,
    weight=0.9,            # Strength (0.0-1.0)
    bidirectional=False,   # One-way or two-way
    metadata={"context": "technical"}
)
```

### 3. Relationship Weights

Weights indicate relationship strength:
- **1.0** - Strongest connection
- **0.5** - Moderate connection
- **0.0** - Weakest (typically removed)

### 4. Reinforcement and Weakening

Dynamically adjust relationship strength:

```python
# Strengthen a relationship
client.relationships.reinforce("rel_123", amount=0.1)

# Weaken a relationship
client.relationships.weaken("rel_123", amount=0.2)

# Bulk reinforce
client.relationships.reinforce_group(
    relationship_ids=["rel_1", "rel_2"],
    amount=0.05
)
```

### 5. Querying Relationships

```python
# Get incoming relationships
incoming = client.relationships.get_incoming(memory_id)

# Get outgoing relationships
outgoing = client.relationships.get_outgoing(memory_id)

# Get all related memories with weights
related = client.relationships.get_related(
    memory_id="mem_123",
    limit=10,
    min_weight=0.5
)
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates 4 memories (Python and frameworks)
2. Creates relationships: Django→Python, Flask→Python, etc.
3. Creates a bidirectional relationship (Django↔Flask)
4. Queries incoming/outgoing relationships
5. Reinforces and weakens relationships
6. Finds all related memories
7. Lists available relationship types

### Async Version (`async_example.py`)

Same concepts with concurrent execution:
- Creates multiple relationships in parallel
- Queries relationships concurrently
- Reinforces multiple relationships at once

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [04_spaces_multitenancy](../04_spaces_multitenancy/) - Organize with spaces

