#!/usr/bin/env python3
"""
Agent Sessions - Synchronous Version

This example demonstrates agent session management:
1. Creating and managing conversation sessions
2. Adding memories to sessions
3. Core memory blocks for persistent agent state
4. Context retrieval for conversations
5. Session consolidation on end

Run: python main.py
"""

from trix import Trix
from trix.types import ConsolidationStrategy


def main() -> None:
    """Demonstrate agent session management."""
    
    with Trix.from_env() as client:
        print("=" * 60)
        print("AGENT SESSIONS")
        print("=" * 60)
        
        # ======================================================================
        # CREATE SESSION
        # ======================================================================
        print("\n1. Creating agent session...")
        
        session = client.agent.create_session(
            user_id="user_123",
            agent_id="assistant_v1",
            metadata={"channel": "web", "language": "en"}
        )
        
        print(f"   ✓ Session created: {session.id}")
        print(f"   Status: {session.status}")
        
        # ======================================================================
        # ADD SESSION MEMORIES
        # ======================================================================
        print("\n2. Adding conversation memories to session...")
        
        # Simulate a conversation
        conversations = [
            {"role": "user", "content": "Hi, I'm interested in learning Python."},
            {"role": "assistant", "content": "Great choice! Python is excellent for beginners."},
            {"role": "user", "content": "What should I start with?"},
            {"role": "assistant", "content": "Start with basic syntax, then move to data structures."},
        ]
        
        for conv in conversations:
            mem = client.agent.add_session_memory(
                session_id=session.id,
                content=conv["content"],
                role=conv["role"],
                metadata={"turn": conversations.index(conv) + 1}
            )
            print(f"   ✓ Added {conv['role']} message: {mem.id}")
        
        # ======================================================================
        # GET SESSION
        # ======================================================================
        print("\n3. Getting session details...")
        
        retrieved = client.agent.get_session(session.id)
        print(f"   Session: {retrieved.id}")
        print(f"   User: {retrieved.user_id}")
        print(f"   Metadata: {retrieved.metadata}")
        
        # ======================================================================
        # GET CONTEXT
        # ======================================================================
        print("\n4. Retrieving conversation context...")
        
        context = client.agent.get_context(
            session_id=session.id,
            query="What topics were discussed?",
            limit=5
        )
        
        print(f"   Found {len(context.memories)} relevant memories:")
        for mem in context.memories:
            print(f"      - {mem.content[:50]}...")
        
        # ======================================================================
        # CORE MEMORY BLOCKS
        # ======================================================================
        print("\n5. Managing core memory blocks...")
        
        # Get current core memory
        core = client.agent.get_core_memory(agent_id="assistant_v1")
        print(f"   Current core memory blocks: {len(core.blocks)}")
        
        # Update or create a persona block
        persona_block = client.agent.update_block(
            agent_id="assistant_v1",
            block_name="persona",
            content="I am a helpful Python tutor. I explain concepts clearly.",
        )
        print(f"   ✓ Updated persona block: {persona_block.name}")
        
        # Create a user preferences block
        prefs_block = client.agent.update_block(
            agent_id="assistant_v1",
            block_name="user_preferences",
            content="User prefers concise explanations with code examples.",
        )
        print(f"   ✓ Updated preferences block: {prefs_block.name}")
        
        # Append to a block
        client.agent.append_block(
            agent_id="assistant_v1",
            block_name="user_preferences",
            content=" User is interested in web development."
        )
        print("   ✓ Appended to preferences block")
        
        # Get a specific block
        block = client.agent.get_block(
            agent_id="assistant_v1",
            block_name="user_preferences"
        )
        print(f"   Current preferences: {block.content}")
        
        # ======================================================================
        # LIST SESSIONS
        # ======================================================================
        print("\n6. Listing sessions...")
        
        sessions = client.agent.list_sessions(
            user_id="user_123",
            limit=10
        )
        
        print(f"   Found {len(sessions.data)} sessions for user_123")
        
        # ======================================================================
        # END SESSION WITH CONSOLIDATION
        # ======================================================================
        print("\n7. Ending session with consolidation...")
        
        ended = client.agent.end_session(
            session_id=session.id,
            consolidate=True,
            strategy=ConsolidationStrategy.SUMMARIZE
        )
        
        print(f"   ✓ Session ended: {ended.status}")
        
        # ======================================================================
        # EXPLICIT CONSOLIDATION
        # ======================================================================
        print("\n8. Explicit consolidation (for active sessions)...")
        
        # Create a new session for demonstration
        new_session = client.agent.create_session(
            user_id="user_123",
            agent_id="assistant_v1"
        )
        
        # Add some memories
        client.agent.add_session_memory(
            session_id=new_session.id,
            content="Discussion about Python decorators",
            role="user"
        )
        
        # Consolidate without ending
        result = client.agent.consolidate(
            session_id=new_session.id,
            strategy=ConsolidationStrategy.SUMMARIZE
        )
        
        print(f"   ✓ Consolidated: {result.memories_processed} memories")
        
        # End the session
        client.agent.end_session(new_session.id)
        
        # ======================================================================
        # CLEANUP CORE MEMORY BLOCKS
        # ======================================================================
        print("\n9. Cleaning up...")
        
        client.agent.delete_block(agent_id="assistant_v1", block_name="user_preferences")
        client.agent.delete_block(agent_id="assistant_v1", block_name="persona")
        
        print("   ✓ Cleaned up core memory blocks")
        
        print("\n" + "=" * 60)
        print("🎉 Agent sessions complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

