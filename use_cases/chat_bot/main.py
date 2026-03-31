#!/usr/bin/env python3
"""
Chat Bot - Synchronous Version

A complete chatbot implementation demonstrating:
1. Agent session management
2. Context retrieval for responses
3. Memory storage for conversations
4. Session end with summary
5. Multi-turn conversation patterns

Run: python main.py
"""

from trix import Trix
from trix.exceptions import NotFoundError


class ChatBot:
    """A memory-enabled chatbot using Trix."""

    def __init__(self, client: Trix, bot_name: str = "chatbot_v1"):
        self.client = client
        self.bot_name = bot_name
        self.session_id: str | None = None

    def start_session(self, user_id: str, metadata: dict | None = None) -> str:
        """Start a new conversation session."""
        session_id = f"chat_{user_id}_{self.bot_name}"
        session = self.client.agent.create_session(
            session_id=session_id,
            metadata=metadata or {}
        )
        self.session_id = session.session_id
        return session.session_id

    def end_session(self) -> None:
        """End the current session with a summary."""
        if self.session_id:
            self.client.agent.end_session(
                session_id=self.session_id,
                summary="Conversation ended",
                key_insights=["Session completed"]
            )
            self.session_id = None

    def get_context(self, user_message: str, limit: int = 5) -> list[str]:
        """Retrieve relevant context for responding."""
        if not self.session_id:
            return []

        context = self.client.agent.get_context(
            query=user_message,
            session_id=self.session_id,
            limit=limit
        )

        return [m.content for m in context.memories]

    def record_turn(self, role: str, content: str) -> None:
        """Record a conversation turn."""
        if not self.session_id:
            raise ValueError("No active session")

        self.client.agent.add_session_memory(
            session_id=self.session_id,
            content=content,
            role=role,
        )

    def respond(self, user_message: str) -> str:
        """
        Generate a response to the user message.

        In a real implementation, this would call an LLM with:
        - The user message
        - Retrieved context from memory
        """
        # Record user message
        self.record_turn("user", user_message)

        # Get relevant context
        context = self.get_context(user_message)

        # In a real chatbot, you would call your LLM here
        # For demo, we'll create a simple response
        response = f"[Bot received: '{user_message}']"

        if context:
            response += f"\n[Found {len(context)} relevant memories]"

        # Record assistant response
        self.record_turn("assistant", response)

        return response


def main():
    """Demonstrate the chatbot."""
    print("=" * 60)
    print("CHAT BOT USE CASE")
    print("=" * 60)

    with Trix.from_env() as client:
        # Create chatbot
        bot = ChatBot(client)

        # Start a session
        print("\n1. Starting session...")
        bot.start_session(
            user_id="user_123",
            metadata={"channel": "cli", "language": "en"}
        )
        print("   Session started")

        # Multi-turn conversation
        print("\n2. Multi-turn conversation...")

        turns = [
            "Hi, I'd like to learn about Python.",
            "What are list comprehensions?",
            "Can you show me an example?",
        ]

        for turn in turns:
            print(f"   User: {turn}")
            response = bot.respond(turn)
            print(f"   Bot: {response}\n")

        # End session
        print("3. Ending session...")
        bot.end_session()
        print("   Session ended")

        print("\n" + "=" * 60)
        print("Chat bot complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
