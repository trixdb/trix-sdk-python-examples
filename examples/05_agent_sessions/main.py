#!/usr/bin/env python3
"""
Agent Sessions - Synchronous Version

This example demonstrates agent session management:
1. Creating and managing conversation sessions
2. Adding memories to sessions
3. Context retrieval for conversations
4. Session end with summary

Run: python main.py
"""

from trix import Trix


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
            session_id="chat_123",
            metadata={"channel": "web", "language": "en"}
        )

        print(f"   Session created: {session.session_id}")

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
                session_id=session.session_id,
                content=conv["content"],
                role=conv["role"],
                importance=0.8 if conv["role"] == "user" else 0.5
            )
            print(f"   Added {conv['role']} message: {mem.id}")

        # ======================================================================
        # GET SESSION
        # ======================================================================
        print("\n3. Getting session details...")

        retrieved = client.agent.get_session(session.session_id)
        print(f"   Session: {session.session_id}")
        print(f"   Memories retrieved")

        # ======================================================================
        # GET CONTEXT
        # ======================================================================
        print("\n4. Retrieving conversation context...")

        context = client.agent.get_context(
            query="What topics were discussed?",
            session_id=session.session_id,
            limit=5
        )

        print(f"   Found {len(context.memories)} relevant memories:")
        for mem in context.memories:
            print(f"      - {mem.content[:50]}...")

        # ======================================================================
        # LIST SESSIONS
        # ======================================================================
        print("\n5. Listing sessions...")

        sessions = client.agent.list_sessions(limit=10)

        print(f"   Found {len(sessions.data)} sessions")

        # ======================================================================
        # END SESSION WITH SUMMARY
        # ======================================================================
        print("\n6. Ending session with summary...")

        ended = client.agent.end_session(
            session_id=session.session_id,
            summary="Discussion about learning Python programming",
            key_insights=["User is a beginner", "Interested in Python basics"]
        )

        print(f"   Session ended")

        # ======================================================================
        # CREATE ANOTHER SESSION
        # ======================================================================
        print("\n7. Creating another session...")

        new_session = client.agent.create_session(
            session_id="chat_456",
        )

        # Add some memories
        client.agent.add_session_memory(
            session_id=new_session.session_id,
            content="Discussion about Python decorators",
            role="user"
        )

        # End the session
        client.agent.end_session(
            session_id=new_session.session_id,
            summary="Brief discussion about decorators"
        )

        print("   Session created and ended")

        print("\n" + "=" * 60)
        print("Agent sessions complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
