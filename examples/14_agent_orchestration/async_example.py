#!/usr/bin/env python3
"""
Agent Orchestration - Asynchronous Version

The async client creates bots concurrently, runs a batch (fanned out with
``asyncio.gather`` under the hood), and drives a workflow - all with
``await``.

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix
from trix.types import BotRunBatchRequest, CrewMember


async def main() -> None:
    """Wire bots, a crew, and a workflow together, asynchronously."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC AGENT ORCHESTRATION")
        print("=" * 60)

        # ======================================================================
        # CREATE BOTS CONCURRENTLY
        # ======================================================================
        print("\n1. Creating specialist bots concurrently...")
        researcher, writer = await asyncio.gather(
            client.bots.create(name="Researcher", system_prompt="You gather facts."),
            client.bots.create(name="Writer", system_prompt="You draft summaries."),
        )
        print(f"   researcher={researcher.id}  writer={writer.id}")

        # ======================================================================
        # BATCH RUN
        # ======================================================================
        print("\n2. Running a batch of bots...")
        results = await client.bots.run_batch(
            [
                BotRunBatchRequest(bot_id=researcher.id, message="Research tidal energy."),
                BotRunBatchRequest(bot_id=writer.id, message="Draft a one-line intro."),
            ]
        )
        print(f"   {sum(1 for r in results if r.run)}/{len(results)} runs succeeded")

        # ======================================================================
        # CREW + WORKFLOW
        # ======================================================================
        print("\n3. Creating a crew...")
        crew = await client.crews.create(
            name="Content Team",
            strategy="sequential",
            members=[
                CrewMember(bot_id=researcher.id, role="research", position=0),
                CrewMember(bot_id=writer.id, role="writing", position=1),
            ],
        )
        print(f"   crew={crew.id} ({len(crew.members)} members)")

        print("\n4. Creating and triggering a workflow...")
        workflow = await client.workflows.create(
            name="Daily Digest",
            steps=[{"type": "summarize", "config": {}}],
        )
        wf_run = await client.workflows.trigger(workflow.id, input={"date": "2026-08-10"})
        print(f"   workflow={workflow.id}  run={wf_run.id} status={wf_run.status}")

        print("\n" + "=" * 60)
        print("Async agent orchestration complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
