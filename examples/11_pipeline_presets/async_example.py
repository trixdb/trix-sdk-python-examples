#!/usr/bin/env python3
"""
Pipeline Presets - Asynchronous Version

Async walkthrough of the ADR-109a 3-tier preset resolver:

    caller > space > account > none (built-in hybrid fallback)

Mirrors main.py using AsyncTrix. See main.py / README.md for the full
explanation.

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix


async def main() -> None:
    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("PIPELINE PRESETS - 3-tier resolver (async)")
        print("=" * 60)

        # Baseline: nothing set anywhere.
        print("\n1. Baseline resolve (no caller/space/account default)...")
        baseline = await client.agent.resolve_pipeline()
        print(f"   -> name={baseline['name']!r} source={baseline['source']!r}")

        # Account default applies to every request that omits ?pipeline=.
        print("\n2. Setting account default to 'default'...")
        await client.agent.set_default_pipeline("default")
        resolved_account = await client.agent.resolve_pipeline()
        print(f"   -> name={resolved_account['name']!r} source={resolved_account['source']!r}")

        # Per-space default beats the account default.
        print("\n3. Creating a space + setting its default to 'high-recall'...")
        space = await client.spaces.create(name="pipeline-demo-space-async")
        await client.agent.set_space_default_pipeline(space_id=space.id, name="high-recall")
        resolved_space = await client.agent.resolve_pipeline(space_id=space.id)
        print(f"   -> name={resolved_space['name']!r} source={resolved_space['source']!r}")

        # Explicit caller preset beats every tier.
        print("\n4. Explicit caller preset beats every tier...")
        resolved_caller = await client.agent.resolve_pipeline(
            space_id=space.id, pipeline="high-precision"
        )
        print(f"   -> name={resolved_caller['name']!r} source={resolved_caller['source']!r}")

        # Clean up so this example is idempotent across re-runs.
        print("\n5. Cleaning up...")
        await client.agent.clear_space_default_pipeline(space.id)
        await client.agent.clear_default_pipeline()
        await client.spaces.delete(space.id)
        print("   Defaults cleared, demo space deleted")


if __name__ == "__main__":
    asyncio.run(main())
