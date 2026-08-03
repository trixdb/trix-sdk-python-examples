# Facts and Entities

## Goal

Learn how structured knowledge works in Trix. Facts and entities are
**read-mostly** and **derived from memories** — you don't create them
standalone.

## Prerequisites

- Completed [06_knowledge_graph](../06_knowledge_graph/)

## The mental model

```
Memory (you create this)
   │
   ├── facts.create_for_memory(...)   ← attach an explicit fact
   │
   └── enrichment (server-side, async)
          ├── extracts entities  ──►  entities.{list, get, find_by_type}
          └── extracts facts     ──►  facts.{list, list_for_memory}
```

There is **no** `facts.create`, `entities.create`, `entities.extract`,
`facts.verify`, `entities.resolve`, or `entities.update` — those endpoints do
not exist on the API. The real surface is below.

## Concepts Covered

### 1. Create the source memory

Everything derives from a memory:

```python
memory = client.memories.create(
    content="Guido van Rossum created Python in 1991.",
    tags=["knowledge", "programming"],
)
```

### 2. Attach an explicit fact

Facts are attached **to a memory** as free-form content plus an importance
score (1–10) — not as a raw subject/predicate/object triple:

```python
fact = client.facts.create_for_memory(
    memory.id,
    content="Python was created by Guido van Rossum.",
    importance=8,
    category="history",
)
```

### 3. Extract entities and facts via enrichment

Entity and fact extraction runs as an **asynchronous** enrichment operation:

```python
from trix import EnrichmentOperation

client.enrichments.enrich(
    memory.id,
    operations=[EnrichmentOperation.ENTITIES, EnrichmentOperation.TOPICS],
)
```

### 4. Read facts

```python
# Facts for one memory
memory_facts = client.facts.list_for_memory(memory.id)

# Facts across the account, with server-side filters
created = client.facts.list(predicate="created", min_confidence=0.5, limit=10)
```

### 5. Read entities

```python
people = client.entities.find_by_type("person", limit=5)
entity = client.entities.get(people.data[0].id)
entity_facts = client.entities.get_facts(entity.id)   # facts mentioning it
```

### 6. Merge duplicate entities

The source entity is merged into the target and deleted:

```python
merged = client.entities.merge(target_id=primary.id, source_id=duplicate.id)
print(merged.merged_entity.id, merged.deleted_id)
```

## Walkthrough

### Sync Version (`main.py`)

1. Create a source memory
2. Attach an explicit fact to it
3. Trigger entity/fact extraction (enrichment)
4. Read the memory's facts
5. Query account-wide facts with filters
6. Explore extracted entities (list → get → get_facts)
7. Merge duplicate entities

### Async Version (`async_example.py`)

Same flow with `AsyncTrix`, running the independent reads concurrently via
`asyncio.gather`.

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [08_clustering](../08_clustering/) - Automatic memory organization
