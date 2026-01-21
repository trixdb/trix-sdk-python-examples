# Chat Bot Use Case

A complete chatbot implementation demonstrating memory-augmented conversations.

## Features

- **Session Management**: Start/end conversation sessions
- **Context Retrieval**: Find relevant past conversations
- **Core Memory**: Persistent persona and user preferences
- **Consolidation**: Summarize conversations on session end
- **Multi-turn Patterns**: Handle ongoing conversations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      ChatBot                            │
├─────────────────────────────────────────────────────────┤
│  Core Memory                                            │
│  ┌─────────────┐  ┌─────────────────────┐              │
│  │   Persona   │  │  User Preferences   │              │
│  │  (Who am I) │  │  (What user likes)  │              │
│  └─────────────┘  └─────────────────────┘              │
├─────────────────────────────────────────────────────────┤
│  Session                                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Conversation Memories (user/assistant turns)   │   │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐                   │   │
│  │  │ U1 │→│ A1 │→│ U2 │→│ A2 │→ ...              │   │
│  │  └────┘ └────┘ └────┘ └────┘                   │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Long-term Memory (consolidated from past sessions)     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Summaries, facts, learned preferences          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Key Patterns

### 1. Core Memory Blocks

Persistent information about the agent and user:

```python
# Persona - who the bot is
client.agent.update_block(
    agent_id="chatbot",
    block_name="persona",
    content="I am a helpful assistant..."
)

# User preferences - learned over time
client.agent.append_block(
    agent_id="chatbot",
    block_name="user_preferences",
    content=" User prefers concise answers."
)
```

### 2. Session Lifecycle

```python
# Start session
session = client.agent.create_session(user_id="user_123", agent_id="chatbot")

# Record turns
client.agent.add_session_memory(session_id=session.id, content="Hi", role="user")
client.agent.add_session_memory(session_id=session.id, content="Hello!", role="assistant")

# End with consolidation
client.agent.end_session(session_id=session.id, consolidate=True)
```

### 3. Context Retrieval

```python
context = client.agent.get_context(
    session_id=session.id,
    query="What did we discuss about Python?",
    limit=5
)
# Returns relevant memories from this session and past sessions
```

### 4. Building Prompts

When calling your LLM, include:

```python
prompt = f"""
{core_memory["persona"]}

User preferences: {core_memory["user_preferences"]}

Recent context:
{chr(10).join(context)}

User: {user_message}
Assistant:
"""
```

## Running

```bash
python main.py           # Synchronous version
python async_example.py  # Asynchronous version (parallel operations)
```

## Integration with LLMs

This example shows the memory layer. To integrate with an LLM:

1. Replace the `respond()` method's response generation
2. Call your LLM (OpenAI, Anthropic, etc.) with the context
3. The memory retrieval and storage patterns remain the same

```python
def respond(self, user_message: str) -> str:
    context = self.get_context(user_message)
    core = self.get_core_memory()
    
    # Call your LLM here
    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": core["persona"]},
            *[{"role": "assistant", "content": c} for c in context],
            {"role": "user", "content": user_message}
        ]
    )
    
    return response.choices[0].message.content
```

