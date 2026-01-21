#!/usr/bin/env python3
"""
Agent Sessions - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix
from trix.types import ConsolidationStrategy


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
            user_id="async_user",
            agent_id="async_assistant",
            metadata={"channel": "api"}
        )
        print(f"   ✓ Created session: {session.id}")
        
        # ======================================================================
        # ADD MEMORIES CONCURRENTLY
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
                session_id=session.id,
                content=content,
                role=role,
            )
        print(f"   ✓ Added {len(messages)} messages")
        
        # ======================================================================
        # PARALLEL OPERATIONS
        # ======================================================================
        print("\n3. Parallel context and session fetch...")
        
        context, session_info = await asyncio.gather(
            client.agent.get_context(
                session_id=session.id,
                query="What was discussed?",
                limit=5
            ),
            client.agent.get_session(session.id)
        )
        
        print(f"   Context memories: {len(context.memories)}")
        print(f"   Session status: {session_info.status}")
        
        # ======================================================================
        # CORE MEMORY MANAGEMENT
        # ======================================================================
        print("\n4. Managing core memory blocks...")
        
        # Update multiple blocks concurrently
        persona_task = client.agent.update_block(
            agent_id="async_assistant",
            block_name="persona",
            content="I am an ML expert assistant."
        )
        
        prefs_task = client.agent.update_block(
            agent_id="async_assistant",
            block_name="user_prefs",
            content="User is a beginner in ML."
        )
        
        persona_block, prefs_block = await asyncio.gather(persona_task, prefs_task)
        print(f"   ✓ Updated blocks: {persona_block.name}, {prefs_block.name}")
        
        # ======================================================================
        # GET CORE MEMORY
        # ======================================================================
        print("\n5. Getting complete core memory...")
        
        core = await client.agent.get_core_memory(agent_id="async_assistant")
        print(f"   Core memory has {len(core.blocks)} blocks:")
        for block in core.blocks:
            print(f"      - {block.name}: {block.content[:40]}...")
        
        # ======================================================================
        # END AND CONSOLIDATE
        # ======================================================================
        print("\n6. Ending session with consolidation...")
        
        ended = await client.agent.end_session(
            session_id=session.id,
            consolidate=True,
            strategy=ConsolidationStrategy.SUMMARIZE
        )
        print(f"   ✓ Session ended: {ended.status}")
        
        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n7. Cleaning up blocks...")
        
        await asyncio.gather(
            client.agent.delete_block(agent_id="async_assistant", block_name="persona"),
            client.agent.delete_block(agent_id="async_assistant", block_name="user_prefs"),
        )
        print("   ✓ Cleaned up")
        
        print("\n" + "=" * 60)
        print("🎉 Async agent sessions complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

