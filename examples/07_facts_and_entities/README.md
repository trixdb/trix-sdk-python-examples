# Facts and Entities

## Goal

Learn to extract and manage structured knowledge using facts and entities.

## Prerequisites

- Completed [06_knowledge_graph](../06_knowledge_graph/)

## Concepts Covered

### 1. Entities

Named things with types and properties:

```python
entity = client.entities.create(
    name="Python",
    entity_type="programming_language",
    properties={"paradigm": "multi-paradigm"},
    aliases=["Py", "Python3"]
)
```

### 2. Facts

Structured knowledge as subject-predicate-object triples:

```python
# Fact linking two entities
fact = client.facts.create(
    subject=guido.id,
    predicate="created",
    obj=python.id,
    confidence=1.0,
    metadata={"source": "Wikipedia"}
)

# Fact with a value instead of entity
fact = client.facts.create(
    subject=python.id,
    predicate="has_feature",
    obj="dynamic typing"
)
```

### 3. Entity Extraction

Extract entities from a memory:

```python
# First create a memory with the text
memory = client.memories.create(content="Guido van Rossum created Python in 1991.")

# Then extract entities from it
result = client.entities.extract(memory_id=memory.id, save=False)

for entity in result.entities:
    print(f"{entity.name} ({entity.entity_type})")
```

### 4. Fact Extraction

Extract structured facts from a memory:

```python
result = client.facts.extract(memory_id=memory.id, save=False)

for fact in result.facts:
    print(f"{fact.subject} {fact.predicate} {fact.object}")
```

### 5. Entity Resolution

Resolve text to known entities:

```python
resolved = client.entities.resolve(text="Py")
# Returns: Python (if entity with alias exists)
```

### 6. Fact Verification

Verify a fact against the knowledge base:

```python
# Get a fact ID first (e.g., from create or list)
fact = client.facts.create(subject="Guido", predicate="created", obj="Python")

# Then verify it
verification = client.facts.verify(fact_id=fact.id)
print(f"Verified: {verification.is_verified}")
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates entities (Python, Guido van Rossum)
2. Creates facts linking them
3. Queries facts by subject and predicate
4. Extracts entities from text
5. Extracts facts from text
6. Searches for entities
7. Resolves aliases to entities
8. Verifies a fact
9. Merges duplicate entities

### Async Version (`async_example.py`)

Parallel operations:
- Concurrent entity creation
- Concurrent fact creation
- Parallel extraction

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [08_clustering](../08_clustering/) - Automatic memory organization

