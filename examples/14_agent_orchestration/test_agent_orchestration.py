"""Tests for the Agent Orchestration example.

Exercises the three agent primitives - bots (create / run / run_batch), crews,
and workflows (create / trigger / list_runs) - with respx-mocked endpoints.
"""

import pytest
import respx
from httpx import Response
from trix import AsyncTrix, Trix
from trix.types import BotRunBatchRequest

BOT = {
    "id": "bot_1",
    "account_id": "acc_1",
    "name": "Researcher",
    "slug": "researcher",
    "system_prompt": "You gather facts.",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}


def _bot_run(bot_id: str) -> dict:
    return {
        "id": f"run_{bot_id}",
        "bot_id": bot_id,
        "account_id": "acc_1",
        "trigger_type": "manual",
        "status": "completed",
        "output_message": "Octopuses have three hearts.",
        "created_at": "2026-01-01T00:00:00Z",
    }


CREW = {
    "id": "crew_1",
    "account_id": "acc_1",
    "name": "Content Team",
    "slug": "content-team",
    "strategy": "sequential",
    "members": [
        {"bot_id": "bot_1", "role": "research", "position": 0},
        {"bot_id": "bot_2", "role": "writing", "position": 1},
    ],
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}
WORKFLOW = {
    "id": "wf_1",
    "account_id": "acc_1",
    "name": "Daily Digest",
    "status": "active",
    "version": 1,
    "steps": [{"type": "summarize", "config": {}}],
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}
WF_RUN = {
    "id": "wfrun_1",
    "workflow_id": "wf_1",
    "account_id": "acc_1",
    "status": "running",
    "created_at": "2026-01-01T00:00:00Z",
}
WF_RUN_LIST = {"runs": [WF_RUN], "total": 1, "limit": 5, "offset": 0}


def _mock_all() -> None:
    respx.post("https://api.trixdb.com/v1/agents").mock(return_value=Response(200, json=BOT))
    respx.post("https://api.trixdb.com/v1/agents/bot_1/run").mock(
        return_value=Response(200, json=_bot_run("bot_1"))
    )
    respx.post("https://api.trixdb.com/v1/agents/bot_2/run").mock(
        return_value=Response(200, json=_bot_run("bot_2"))
    )
    respx.post("https://api.trixdb.com/v1/crews").mock(return_value=Response(200, json=CREW))
    respx.post("https://api.trixdb.com/v1/workflows").mock(
        return_value=Response(200, json=WORKFLOW)
    )
    respx.post("https://api.trixdb.com/v1/workflows/wf_1/trigger").mock(
        return_value=Response(200, json=WF_RUN)
    )
    respx.get("https://api.trixdb.com/v1/workflows/wf_1/runs").mock(
        return_value=Response(200, json=WF_RUN_LIST)
    )


# =============================================================================
# Synchronous Tests
# =============================================================================


@respx.mock
def test_create_and_run_bot_sync():
    """Create a bot and run it directly."""
    _mock_all()

    with Trix(api_key="test") as client:
        bot = client.bots.create(name="Researcher", system_prompt="You gather facts.")
        run = client.bots.run(bot.id, message="Find three facts about octopuses.")

    assert bot.id == "bot_1"
    assert run.status == "completed"
    assert "three hearts" in (run.output_message or "")


@respx.mock
def test_run_batch_sync():
    """A batch runs several bots and returns one result per request."""
    _mock_all()

    with Trix(api_key="test") as client:
        results = client.bots.run_batch(
            [
                BotRunBatchRequest(bot_id="bot_1", message="Research tidal energy."),
                BotRunBatchRequest(bot_id="bot_2", message="Draft an intro."),
            ]
        )

    assert {r.bot_id for r in results} == {"bot_1", "bot_2"}
    assert all(r.run is not None and r.error is None for r in results)


@respx.mock
def test_create_crew_sync():
    """A crew groups member bots with roles and ordering."""
    _mock_all()

    with Trix(api_key="test") as client:
        crew = client.crews.create(name="Content Team", strategy="sequential")

    assert crew.strategy == "sequential"
    assert [m.bot_id for m in crew.members] == ["bot_1", "bot_2"]


@respx.mock
def test_create_and_trigger_workflow_sync():
    """A workflow is created, triggered, and its runs listed."""
    _mock_all()

    with Trix(api_key="test") as client:
        workflow = client.workflows.create(name="Daily Digest", steps=[{"type": "summarize"}])
        run = client.workflows.trigger(workflow.id, input={"date": "2026-08-10"})
        runs = client.workflows.list_runs(workflow.id, limit=5)

    assert workflow.version == 1
    assert run.status == "running"
    assert len(runs.runs) == 1


# =============================================================================
# Asynchronous Tests
# =============================================================================


@respx.mock
@pytest.mark.asyncio
async def test_create_and_run_bot_async():
    """Create and run a bot with the async client."""
    _mock_all()

    async with AsyncTrix(api_key="test") as client:
        bot = await client.bots.create(name="Researcher", system_prompt="You gather facts.")
        run = await client.bots.run(bot.id, message="hi")

    assert bot.id == "bot_1"
    assert run.bot_id == "bot_1"


@respx.mock
@pytest.mark.asyncio
async def test_trigger_workflow_async():
    """Create and trigger a workflow with the async client."""
    _mock_all()

    async with AsyncTrix(api_key="test") as client:
        workflow = await client.workflows.create(name="Daily Digest")
        run = await client.workflows.trigger(workflow.id, input={"date": "2026-08-10"})

    assert workflow.id == "wf_1"
    assert run.workflow_id == "wf_1"
