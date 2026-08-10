# Agent Orchestration

## Goal

Compose Trix's three agent primitives - **bots**, **crews**, and
**workflows** - into a working multi-agent pipeline.

## Prerequisites

- Completed [05_agent_sessions](../05_agent_sessions/)
- Completed [12_streaming_runs](../12_streaming_runs/)

## Concepts Covered

### 1. Bots: create and run

```python
bot = client.bots.create(name="Researcher", system_prompt="You gather facts.")
run = client.bots.run(bot.id, message="Find three facts about octopuses.")
print(run.status, run.output_message)
```

For live output, stream instead with `client.bots.run_stream(...)` -
see [12_streaming_runs](../12_streaming_runs/).

### 2. Bots: batch runs

Run many bots at once. The sync client parallelises with threads, the async
client with `asyncio.gather` - same typed result list either way:

```python
from trix.types import BotRunBatchRequest

results = client.bots.run_batch([
    BotRunBatchRequest(bot_id=researcher.id, message="Research tidal energy."),
    BotRunBatchRequest(bot_id=writer.id, message="Draft a one-line intro."),
])
for r in results:
    print(r.bot_id, "ok" if r.run else r.error)
```

Each `BotRunBatchResult` carries either `.run` (success) or `.error`, so one
failure never sinks the batch.

### 3. Crews: group collaborating bots

```python
from trix.types import CrewMember

crew = client.crews.create(
    name="Content Team",
    strategy="sequential",
    members=[
        CrewMember(bot_id=researcher.id, role="research", position=0),
        CrewMember(bot_id=writer.id, role="writing", position=1),
    ],
)
```

### 4. Workflows: automate and trigger

```python
workflow = client.workflows.create(
    name="Daily Digest",
    steps=[
        {"type": "search", "config": {"query": "created today"}},
        {"type": "summarize", "config": {"style": "bullets"}},
    ],
)
run = client.workflows.trigger(workflow.id, input={"date": "2026-08-10"})
history = client.workflows.list_runs(workflow.id, limit=5)
```

## Walkthrough

### Sync Version (`main.py`)

1. Creates two specialist bots
2. Runs one directly, then runs a batch in parallel
3. Groups the bots into a crew
4. Creates a workflow, triggers it, and lists its runs

### Async Version (`async_example.py`)

Creates the bots concurrently with `asyncio.gather`, then batches, crews, and
triggers a workflow with `await`.

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [Recipes](../../recipes/) - Reusable patterns, including testing with `MockTrix`
