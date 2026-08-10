#!/usr/bin/env python3
"""
Testing with `trix.testing.MockTrix`

The SDK ships its own in-memory test double, so you can unit-test code that
depends on a Trix client **without HTTP, respx, or a network** at all. Unlike
respx (which mocks the wire - see ``testing_mock_patterns.py``), ``MockTrix``
mocks the *client*: you configure return values, and it records every call for
you to assert on.

    from trix.testing import MockTrix, create_mock_memory

    mock = MockTrix()
    mock.memories.mock_create(create_mock_memory(content="Test"))
    memory = mock.memories.create(content="Test")
    assert memory.content == "Test"
    assert mock.memories.create_calls[0]["content"] == "Test"

Covered here: configuring responses, asserting recorded calls, injecting
errors, mocking list results, and the async client (``MockAsyncTrix``).

Run: python mock_client_testing.py   (executes the tests below)
"""

from __future__ import annotations

import pytest
from trix import Trix
from trix.exceptions import NotFoundError
from trix.testing import (
    MockAsyncTrix,
    MockTrix,
    create_mock_memory,
    create_mock_paginated_response,
)

# =============================================================================
# Code under test - a tiny service that depends on a Trix client.
# It is typed against the real `Trix`; `MockTrix` is a structural stand-in that
# exposes the same methods, so the very same code runs under test.
# =============================================================================


def remember(client: Trix, text: str) -> str:
    """Store a note and return the new memory's id."""
    memory = client.memories.create(content=text, tags=["note"])
    return memory.id


def recent_titles(client: Trix, limit: int = 5) -> list[str]:
    """Return the first line of each recent memory."""
    page = client.memories.list(limit=limit)
    return [m.content.splitlines()[0] for m in page.data]


# =============================================================================
# 1. Configure a response and assert on the recorded call
# =============================================================================


def test_remember_records_the_call():
    """`mock_create` sets the return value; `create_calls` captures the args."""
    mock = MockTrix()
    mock.memories.mock_create(create_mock_memory(id="mem_1", content="Buy milk"))

    memory_id = remember(mock, "Buy milk")  # type: ignore[arg-type]

    assert memory_id == "mem_1"
    assert mock.memories.create_calls[0]["content"] == "Buy milk"
    assert mock.memories.create_calls[0]["tags"] == ["note"]


# =============================================================================
# 2. Mock a list result (factories build valid typed models for you)
# =============================================================================


def test_recent_titles_from_a_mocked_list():
    """`create_mock_paginated_response` builds a `.data` list of real models."""
    mock = MockTrix()
    mock.memories.mock_list(
        create_mock_paginated_response(
            [
                create_mock_memory(content="First note\nbody"),
                create_mock_memory(content="Second note\nbody"),
            ]
        )
    )

    assert recent_titles(mock) == ["First note", "Second note"]  # type: ignore[arg-type]
    assert mock.memories.list_calls[0]["limit"] == 5


# =============================================================================
# 3. Inject errors - a configured Exception is raised on the next call
# =============================================================================


def test_error_paths_with_injected_exceptions():
    """Pass an exception instance to a `mock_*` method to exercise error paths."""
    mock = MockTrix()
    mock.memories.mock_get(NotFoundError("missing", 404, None))

    with pytest.raises(NotFoundError):
        mock.memories.get("nope")

    assert mock.memories.get_calls == ["nope"]


# =============================================================================
# 4. Async code uses MockAsyncTrix with the same API
# =============================================================================


@pytest.mark.asyncio
async def test_async_service_with_mock_async_trix():
    """`MockAsyncTrix` mirrors `MockTrix` with awaitable methods."""
    mock = MockAsyncTrix()
    mock.memories.mock_create(create_mock_memory(id="mem_2", content="Async note"))

    memory = await mock.memories.create(content="Async note")

    assert memory.id == "mem_2"
    assert len(mock.memories.create_calls) == 1


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
