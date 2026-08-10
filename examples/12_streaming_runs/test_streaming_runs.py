"""Tests for the Streaming Bot Runs example.

The SDK exposes ``bots.run_stream`` as a Server-Sent Events (SSE) iterator.
These tests mock the raw SSE body with respx and assert the SDK parses each
line into a typed ``BotRunStep``.
"""

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix
from trix.types import BotRunStep

# A realistic multi-event SSE stream terminated by the [DONE] sentinel. Each
# event is a `data:` line; the SDK skips [DONE] and yields one step per event.
SSE_BODY = (
    b'data: {"event": "run.started", "run_id": "run_1"}\n\n'
    b'data: {"event": "tool", "tool": "search_memory", "args": {"q": "vectors"}}\n\n'
    b'data: {"event": "step", "step_index": 0, "message": "Vector databases"}\n\n'
    b'data: {"event": "step", "step_index": 1, "message": "index embeddings."}\n\n'
    b'data: {"event": "run.completed", "status": "completed"}\n\n'
    b"data: [DONE]\n\n"
)


def _mock_stream() -> None:
    respx.post("https://api.trixdb.com/v1/agents/bot_1/run").mock(
        return_value=Response(200, content=SSE_BODY, headers={"content-type": "text/event-stream"})
    )


# =============================================================================
# Synchronous Tests
# =============================================================================


@respx.mock
def test_run_stream_yields_typed_steps_sync():
    """A sync stream yields one typed BotRunStep per SSE event."""
    _mock_stream()

    with Trix(api_key="test") as client:
        steps = list(client.bots.run_stream("bot_1", message="hi"))

    assert [s.event for s in steps] == [
        "run.started",
        "tool",
        "step",
        "step",
        "run.completed",
    ]
    assert all(isinstance(s, BotRunStep) for s in steps)


@respx.mock
def test_run_stream_exposes_step_fields_sync():
    """Typed fields (tool, message, status) are populated from the payload."""
    _mock_stream()

    with Trix(api_key="test") as client:
        steps = list(client.bots.run_stream("bot_1", message="hi"))

    tool_step = next(s for s in steps if s.event == "tool")
    assert tool_step.tool == "search_memory"
    assert tool_step.args == {"q": "vectors"}

    transcript = [s.message for s in steps if s.event == "step" and s.message]
    assert transcript == ["Vector databases", "index embeddings."]

    assert steps[-1].status == "completed"


# =============================================================================
# Asynchronous Tests
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_run_stream_async():
    """The async client drives the same stream with `async for`."""
    _mock_stream()

    async with AsyncTrix(api_key="test") as client:
        steps = [step async for step in client.bots.run_stream("bot_1", message="hi")]

    assert [s.event for s in steps] == [
        "run.started",
        "tool",
        "step",
        "step",
        "run.completed",
    ]
    assert steps[2].message == "Vector databases"
