"""Tests for the Pipeline Presets example.

These mock the real ADR-109a pipeline-preset routes: the dry-run resolver
(GET /pipeline-presets/_resolve), the account default
(GET/POST/DELETE /pipeline-presets/_default), and the per-space default.
"""

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix

BASE = "https://api.trixdb.com/v1"


# =============================================================================
# Resolver (dry-run 3-tier resolution)
# =============================================================================


@respx.mock
def test_resolve_pipeline_baseline():
    """With nothing set, the resolver reports no preset."""
    respx.get(f"{BASE}/pipeline-presets/_resolve").mock(
        return_value=Response(200, json={"name": None, "source": None, "preset": None})
    )

    with Trix(api_key="test") as client:
        resolved = client.agent.resolve_pipeline()

    assert resolved["name"] is None
    assert resolved["source"] is None


@respx.mock
def test_resolve_pipeline_caller_override():
    """An explicit caller preset resolves with source 'caller'."""
    respx.get(f"{BASE}/pipeline-presets/_resolve").mock(
        return_value=Response(200, json={"name": "high-precision", "source": "caller"})
    )

    with Trix(api_key="test") as client:
        resolved = client.agent.resolve_pipeline(pipeline="high-precision")

    assert resolved["name"] == "high-precision"
    assert resolved["source"] == "caller"


# =============================================================================
# Account default
# =============================================================================


@respx.mock
def test_set_default_pipeline():
    """set_default_pipeline posts to /pipeline-presets/:name/set-default."""
    route = respx.post(f"{BASE}/pipeline-presets/default/set-default").mock(
        return_value=Response(200, json={"name": "default"})
    )

    with Trix(api_key="test") as client:
        name = client.agent.set_default_pipeline("default")

    assert route.called
    assert name == "default"


@respx.mock
def test_get_default_pipeline():
    """get_default_pipeline reads /pipeline-presets/_default."""
    respx.get(f"{BASE}/pipeline-presets/_default").mock(
        return_value=Response(200, json={"name": "default"})
    )

    with Trix(api_key="test") as client:
        current = client.agent.get_default_pipeline()

    assert current == "default"


# =============================================================================
# Asynchronous
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_resolve_pipeline_async():
    """The account default resolves with source 'account'."""
    respx.get(f"{BASE}/pipeline-presets/_resolve").mock(
        return_value=Response(200, json={"name": "default", "source": "account"})
    )

    async with AsyncTrix(api_key="test") as client:
        resolved = await client.agent.resolve_pipeline()

    assert resolved["name"] == "default"
    assert resolved["source"] == "account"
