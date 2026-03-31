#!/usr/bin/env python3
"""
Agent Sessions - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix


async def main() -> None:
    """Demonstrate async agent session management."""

    async with AsyncTrix.from_env() as client:
        print("=" * 60)
        print("ASYNC AGENT SESSIONS")
        print("=" * 60)

        # ======================================================================
        # CREATE SESSION
        # ======================================================================
        print("\n1. Creating session...")

        session = await client.agent.create_session(
            session_id="async_sess_123",
            metadata={"channel": "api"}
        )
        print(f"   Created session: {session.session_id}")

        # ======================================================================
        # ADD MEMORIES
        # ======================================================================
        print("\n2. Adding memories...")

        messages = [
            ("user", "What is machine learning?"),
            ("assistant", "ML is a subset of AI that learns from data."),
            ("user", "Can you give an example?"),
            ("assistant", "Image recognition is a common ML application."),
        ]

        # Add memories (sequential for conversation order)
        for role, content in messages:
            await client.agent.add_session_memory(
                session_id=session.session_id,
                content=content,
                role=role,
            )
        print(f"   Added {len(messages)} messages")

        # ======================================================================
        # PARALLEL OPERATIONS
        # ======================================================================
        print("\n3. Parallel context and session fetch...")

        context, session_info = await asyncio.gather(
            client.agent.get_context(
                query="What was discussed?",
                session_id=session.session_id,
                limit=5
            ),
            client.agent.get_session(session.session_id)
        )

        print(f"   Context memories: {len(context.memories)}")
        print(f"   Session retrieved")

        # ======================================================================
        # END AND SUMMARIZE
        # ======================================================================
        print("\n4. Ending session with summary...")

        ended = await client.agent.end_session(
            session_id=session.session_id,
            summary="Discussion about machine learning concepts",
            key_insights=["User learning about ML", "Covered image recognition"]
        )
        print(f"   Session ended")

        print("\n" + "=" * 60)
        print("Async agent sessions complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
