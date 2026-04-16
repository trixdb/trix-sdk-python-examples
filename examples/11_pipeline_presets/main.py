#!/usr/bin/env python3
"""
Pipeline Presets — ADR-111 / ADR-109a / ADR-112

This example walks through the 3-tier resolver for Trix's pipeline
presets. Every search / chat endpoint in Trix is configured by these
presets. When a caller doesn't pass ``pipeline=<name>`` explicitly,
the server falls back through:

    caller > space > account > none (built-in hybrid fallback)

The example uses the built-in ``default`` preset (shipped with the
server — always available) so you don't need to create one first.
To create your own preset, see the CLI docs:
``trix pipeline create --file=./my-preset.json`` or the
``POST /v1/pipeline-presets`` REST endpoint.

Run: python main.py
"""

from trix import Trix


def main() -> None:
    with Trix.from_env() as client:
        print("=" * 60)
        print("PIPELINE PRESETS — 3-tier resolver")
        print("=" * 60)

        # --------------------------------------------------------------
        # Baseline: dry-run resolver with nothing set anywhere
        # --------------------------------------------------------------
        print("\n1. Baseline — no caller, no space, no account default...")
        baseline = client.agent.resolve_pipeline()
        print(f"   → name={baseline['name']!r} source={baseline['source']!r}")
        # Expected: both None (server will use its built-in fallback).

        # --------------------------------------------------------------
        # Set an account default — applies to every request that omits
        # ?pipeline=<name> and doesn't target a space with its own default.
        # --------------------------------------------------------------
        print("\n2. Setting account default to 'default'...")
        client.agent.set_default_pipeline("default")
        current = client.agent.get_default_pipeline()
        print(f"   ✓ Account default = {current!r}")

        resolved_account = client.agent.resolve_pipeline()
        print(
            f"   → resolve(): name={resolved_account['name']!r} "
            f"source={resolved_account['source']!r}"
        )
        # Expected: name='default', source='account'.

        # --------------------------------------------------------------
        # Per-space default beats account default.
        # --------------------------------------------------------------
        print("\n3. Creating a space + setting its default to 'high-recall'...")
        space = client.spaces.create(name="pipeline-demo-space")
        client.agent.set_space_default_pipeline(
            space_id=space.id,
            name="high-recall",
        )
        resolved_space = client.agent.resolve_pipeline(space_id=space.id)
        print(
            f"   → resolve(space='{space.id}'): name={resolved_space['name']!r} "
            f"source={resolved_space['source']!r}"
        )
        # Expected: name='high-recall', source='space'.

        # --------------------------------------------------------------
        # Explicit caller preset beats everything.
        # --------------------------------------------------------------
        print("\n4. Explicit caller preset beats every tier...")
        resolved_caller = client.agent.resolve_pipeline(
            space_id=space.id,
            pipeline="high-precision",
        )
        print(
            f"   → resolve(space, pipeline='high-precision'): "
            f"name={resolved_caller['name']!r} source={resolved_caller['source']!r}"
        )
        # Expected: name='high-precision', source='caller'.

        # --------------------------------------------------------------
        # Clean up so this example is idempotent across re-runs.
        # --------------------------------------------------------------
        print("\n5. Cleaning up...")
        client.agent.clear_space_default_pipeline(space.id)
        client.agent.clear_default_pipeline()
        client.spaces.delete(space.id)
        print("   ✓ Defaults cleared, demo space deleted")

        print("\nDone. Live search/chat responses carry the resolution in")
        print("the X-Pipeline-Name + X-Pipeline-Source response headers —")
        print("try `curl -I '$BASE/v1/search?q=hello'` to see them.")


if __name__ == "__main__":
    main()
