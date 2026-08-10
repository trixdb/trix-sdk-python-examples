# Streaming Bot Runs

## Goal

Stream a bot run token-by-token (really, event-by-event) over Server-Sent
Events instead of blocking for the final result - the same technique that
powers a live "typing" UI.

## Prerequisites

- Completed [05_agent_sessions](../05_agent_sessions/)
- A bot to run (this example creates one)

## Concepts Covered

### 1. `run_stream` is a plain iterator

The sync client returns an `Iterator[BotRunStep]`; the async client returns an
`AsyncIterator[BotRunStep]`. Drive them with the language's native loops - no
callbacks, no manual polling:

```python
# Synchronous
for step in client.bots.run_stream(bot_id, message="Hello"):
    print(step.event, step.message)

# Asynchronous - note: no `await` on the call, just `async for`
async for step in client.bots.run_stream(bot_id, message="Hello"):
    print(step.event, step.message)
```

### 2. Typed step events

Each SSE line is parsed into a `BotRunStep` with typed fields, so you dispatch
on `step.event` rather than digging through raw dicts:

| `event`         | Useful fields                       |
|-----------------|-------------------------------------|
| `run.started`   | `run_id`                            |
| `tool`          | `tool`, `args`, `result`            |
| `step`          | `step_index`, `message`             |
| `run.completed` | `status`                            |
| `error`         | `error`                             |

```python
from trix.types import BotRunStep

def render(step: BotRunStep) -> None:
    if step.event == "tool":
        print("tool call:", step.tool, step.args)
    elif step.event == "step":
        print(step.message)
```

### 3. Assembling the message

`step` events carry incremental `message` chunks. Collect them to reconstruct
the full assistant reply:

```python
transcript: list[str] = []
for step in client.bots.run_stream(bot_id, message="..."):
    if step.event == "step" and step.message:
        transcript.append(step.message)
answer = " ".join(transcript)
```

### 4. Errors surface as exceptions, not empty streams

If the run fails to start (401/403/404/5xx), the SDK raises a typed error
(`PermissionError`, `NotFoundError`, `ServerError`, ...) *before* yielding -
a failed run is never mistaken for an empty one.

## Walkthrough

### Sync Version (`main.py`)

1. Creates a bot
2. Streams a run, dispatching each `BotRunStep` by event type
3. Assembles the streamed `step` chunks into the final message

### Async Version (`async_example.py`)

Same flow driven by `async for` over the `AsyncIterator[BotRunStep]`.

## Running the Examples

```bash
python main.py           # Synchronous
python async_example.py  # Asynchronous
```

## Next Steps

- [13_file_uploads](../13_file_uploads/) - Upload files and stream binary content back
