# AI Agent Memory Use Case

A comprehensive memory system for AI agents inspired by human memory architecture.

## Memory Types

### 1. Working Memory (Session-based)
Current task context, cleared when task completes.

### 2. Episodic Memory
Experiences and events, stored with emotional context.

### 3. Semantic Memory  
Facts and knowledge, organized by topic.

### 4. Core Identity
Persistent agent identity and user model.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent Memory                      │
├─────────────────────────────────────────────────────────┤
│  Core Identity (Persistent)                             │
│  ┌──────────────────┐  ┌─────────────────────┐         │
│  │    Identity      │  │    User Model       │         │
│  │  (Who am I)      │  │  (What I know       │         │
│  │                  │  │   about user)       │         │
│  └──────────────────┘  └─────────────────────┘         │
├─────────────────────────────────────────────────────────┤
│  Working Memory (Current Task)                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Task context, recent observations, goals       │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Long-term Memory                                       │
│  ┌────────────────────┐  ┌────────────────────┐        │
│  │  Episodic Memory   │  │  Semantic Memory   │        │
│  │  (Experiences)     │  │  (Facts/Knowledge) │        │
│  │  - Past events     │  │  - Python facts    │        │
│  │  - Conversations   │  │  - User preferences│        │
│  └────────────────────┘  └────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## Usage

```python
from trix import Trix

with Trix.from_env() as client:
    agent = AgentMemory(client, agent_id="my_agent")
    
    # Set identity
    agent.set_identity("I am a helpful assistant")
    
    # Store memories
    agent.store_semantic("Python is interpreted", topic="python")
    agent.store_episodic("User was confused about decorators", emotion="neutral")
    
    # Start task
    agent.start_task("user_123", "Help with Python")
    agent.add_to_working_memory("User needs help with decorators")
    
    # Recall
    memories = agent.recall("Python concepts")
    context = agent.get_working_context("decorators")
    
    # Complete
    agent.complete_task()
```

## Running

```bash
python main.py
```

