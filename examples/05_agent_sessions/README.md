# Agent Sessions

## Goal

Learn to build conversational AI agents with persistent memory and context.

## Prerequisites

- Completed [04_spaces_multitenancy](../04_spaces_multitenancy/)

## Concepts Covered

### 1. Sessions

Sessions track conversations between users and agents:

```python
session = client.agent.create_session(
    user_id="user_123",
    agent_id="my_assistant",
    metadata={"channel": "web"}
)
```

### 2. Session Memories

Store conversation turns in a session:

```python
client.agent.add_session_memory(
    session_id=session.id,
    content="What is Python?",
    role="user",
    metadata={"turn": 1}
)
```

### 3. Context Retrieval

Get relevant context for responding:

```python
context = client.agent.get_context(
    session_id=session.id,
    query="What topics were discussed?",
    limit=5
)
```

### 4. Core Memory Blocks

Persistent agent state across sessions:

```python
# Update persona block
client.agent.update_block(
    agent_id="my_assistant",
    block_name="persona",
    content="I am a helpful Python tutor."
)

# Append to a block
client.agent.append_block(
    agent_id="my_assistant",
    block_name="user_preferences",
    content=" User likes code examples."
)

# Get all core memory
core = client.agent.get_core_memory(agent_id="my_assistant")
```

### 5. Session Consolidation

Summarize conversations when ending:

```python
from trix.types import ConsolidationStrategy

# End with automatic consolidation
client.agent.end_session(
    session_id=session.id,
    consolidate=True,
    strategy=ConsolidationStrategy.SUMMARIZE
)

# Or consolidate explicitly during session
client.agent.consolidate(
    session_id=session.id,
    strategy=ConsolidationStrategy.SUMMARIZE
)
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates an agent session
2. Adds conversation memories (user/assistant turns)
3. Retrieves session details
4. Gets relevant context for a query
5. Manages core memory blocks (persona, preferences)
6. Lists user sessions
7. Ends session with consolidation

### Async Version (`async_example.py`)

Same concepts with async/await:
- Concurrent block updates
- Parallel context and session fetching

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [06_knowledge_graph](../06_knowledge_graph/) - Graph traversal and analysis

