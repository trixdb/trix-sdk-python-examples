#!/usr/bin/env python3
"""
Streaming Bot Runs - Asynchronous Version

The async client streams the very same events. ``run_stream`` returns an
``AsyncIterator[BotRunStep]``, so drive it with ``async for`` - no ``await``
on the call itself.

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix
from trix.types import BotRunStep


def render_step(step: BotRunStep, transcript: list[str]) -> None:
    """Print a single streamed step and collect any assistant text."""
    if step.event == "step" and step.message:
        transcript.append(step.message)
    label = step.message or step.tool or step.status or ""
    print(f"   > {step.event}: {label}")


async def main() -> None:
    """Stream a bot run asynchronously."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC STREAMING BOT RUNS")
        print("=" * 60)

        # ======================================================================
        # CREATE A BOT
        # ======================================================================
        print("\n1. Creating a bot...")

        bot = await client.bots.create(
            name="Async Streaming Assistant",
            system_prompt="You are a concise research assistant.",
        )
        print(f"   Bot created: {bot.id}")

        # ======================================================================
        # STREAM A RUN
        # ======================================================================
        print("\n2. Streaming a run with `async for`...")

        transcript: list[str] = []
        async for step in client.bots.run_stream(
            bot.id,
            message="Give me three uses for a knowledge graph.",
        ):
            render_step(step, transcript)

        # ======================================================================
        # ASSEMBLE THE STREAMED MESSAGE
        # ======================================================================
        print("\n3. Assembled streamed message:")
        print("   " + (" ".join(transcript) if transcript else "(no text streamed)"))

        print("\n" + "=" * 60)
        print("Async streaming complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
