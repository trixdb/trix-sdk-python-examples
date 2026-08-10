#!/usr/bin/env python3
"""
Agent Orchestration - Synchronous Version

Compose the three agent primitives into a working pipeline:

1. **Bots** - create specialist agents and run them (single + batch)
2. **Crews** - group bots that collaborate on a task
3. **Workflows** - automate a multi-step job and trigger a run

Run: python main.py
"""

from trix import Trix
from trix.types import BotRunBatchRequest, CrewMember


def main() -> None:
    """Wire bots, a crew, and a workflow together."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("AGENT ORCHESTRATION")
        print("=" * 60)

        # ======================================================================
        # BOTS - create two specialists
        # ======================================================================
        print("\n1. Creating specialist bots...")
        researcher = client.bots.create(
            name="Researcher",
            system_prompt="You gather concise, well-sourced facts.",
        )
        writer = client.bots.create(
            name="Writer",
            system_prompt="You turn facts into a tight summary.",
        )
        print(f"   researcher={researcher.id}  writer={writer.id}")

        # ======================================================================
        # RUN ONE BOT
        # ======================================================================
        print("\n2. Running a single bot...")
        run = client.bots.run(researcher.id, message="Find three facts about octopuses.")
        print(f"   status={run.status}  message={run.output_message!r}")

        # ======================================================================
        # RUN A BATCH OF BOTS (in parallel)
        # ======================================================================
        print("\n3. Running a batch of bots in parallel...")
        results = client.bots.run_batch(
            [
                BotRunBatchRequest(bot_id=researcher.id, message="Research tidal energy."),
                BotRunBatchRequest(bot_id=writer.id, message="Draft a one-line intro."),
            ]
        )
        for result in results:
            outcome = "ok" if result.run else f"error: {result.error}"
            print(f"   {result.bot_id}: {outcome}")

        # ======================================================================
        # CREWS - group the bots to collaborate
        # ======================================================================
        print("\n4. Grouping the bots into a crew...")
        crew = client.crews.create(
            name="Content Team",
            strategy="sequential",
            members=[
                CrewMember(bot_id=researcher.id, role="research", position=0),
                CrewMember(bot_id=writer.id, role="writing", position=1),
            ],
        )
        print(f"   crew={crew.id} ({crew.strategy}, {len(crew.members)} members)")

        # ======================================================================
        # WORKFLOWS - automate and trigger a multi-step job
        # ======================================================================
        print("\n5. Creating and triggering a workflow...")
        workflow = client.workflows.create(
            name="Daily Digest",
            description="Summarize the day's new memories.",
            steps=[
                {"type": "search", "config": {"query": "created today"}},
                {"type": "summarize", "config": {"style": "bullets"}},
            ],
        )
        wf_run = client.workflows.trigger(workflow.id, input={"date": "2026-08-10"})
        print(f"   workflow={workflow.id}  run={wf_run.id} status={wf_run.status}")

        runs = client.workflows.list_runs(workflow.id, limit=5)
        print(f"   workflow has {len(runs.runs)} run(s) so far")

        print("\n" + "=" * 60)
        print("Agent orchestration complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
