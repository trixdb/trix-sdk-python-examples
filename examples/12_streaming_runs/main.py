#!/usr/bin/env python3
"""
Streaming Bot Runs - Synchronous Version

Instead of blocking for a bot's final answer, stream the run over
Server-Sent Events (SSE) and react to each typed ``BotRunStep`` as it
arrives:

1. Create (or reference) a bot
2. Stream a run with ``client.bots.run_stream(...)``
3. Dispatch on each step's ``event`` type (run.started, tool, step, run.completed)
4. Assemble the streamed assistant message from the step chunks

``run_stream`` returns a plain ``Iterator[BotRunStep]``, so a normal ``for``
loop drives it - no callbacks, no polling.

Run: python main.py
"""

from trix import Trix
from trix.types import BotRunStep


def render_step(step: BotRunStep, transcript: list[str]) -> None:
    """Print a single streamed step and collect any assistant text."""
    if step.event == "run.started":
        print(f"   > run started (run_id={step.run_id})")
    elif step.event == "tool":
        print(f"   > tool call: {step.tool} args={step.args}")
    elif step.event == "step":
        if step.message:
            transcript.append(step.message)
        print(f"   > step {step.step_index}: {step.message or ''}")
    elif step.event == "run.completed":
        print(f"   > run completed (status={step.status})")
    elif step.event == "error":
        print(f"   ! error: {step.error}")


def main() -> None:
    """Stream a bot run and react to each event as it arrives."""

    with Trix.from_env() as client:
        print("=" * 60)
        print("STREAMING BOT RUNS")
        print("=" * 60)

        # ======================================================================
        # CREATE A BOT
        # ======================================================================
        print("\n1. Creating a bot to stream...")

        bot = client.bots.create(
            name="Streaming Assistant",
            system_prompt="You are a concise research assistant. Think step by step.",
        )
        print(f"   Bot created: {bot.id} ({bot.slug})")

        # ======================================================================
        # STREAM A RUN
        # ======================================================================
        print("\n2. Streaming a run (events arrive live)...")

        transcript: list[str] = []
        for step in client.bots.run_stream(
            bot.id,
            message="Summarize what you know about vector databases.",
        ):
            render_step(step, transcript)

        # ======================================================================
        # ASSEMBLE THE STREAMED MESSAGE
        # ======================================================================
        print("\n3. Assembled streamed message:")
        print("   " + (" ".join(transcript) if transcript else "(no text streamed)"))

        print("\n" + "=" * 60)
        print("Streaming complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
