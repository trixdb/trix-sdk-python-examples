#!/usr/bin/env python3
"""
Chat Bot - Synchronous Version

A complete chatbot implementation demonstrating:
1. Agent session management
2. Context retrieval for responses
3. Core memory blocks for persona/preferences
4. Memory consolidation on session end
5. Multi-turn conversation patterns

Run: python main.py
"""

from trix import Trix
from trix.exceptions import NotFoundError
from trix.types import ConsolidationStrategy


class ChatBot:
    """A memory-enabled chatbot using Trix."""
    
    def __init__(self, client: Trix, agent_id: str = "chatbot_v1"):
        self.client = client
        self.agent_id = agent_id
        self.session_id: str | None = None
        self._setup_core_memory()
    
    def _setup_core_memory(self) -> None:
        """Initialize core memory blocks for the chatbot."""
        # Set up persona
        self.client.agent.update_block(
            agent_id=self.agent_id,
            block_name="persona",
            content=(
                "I am a helpful AI assistant. "
                "I remember our conversations and learn your preferences. "
                "I aim to be concise and helpful."
            ),
        )
        
        # Initialize empty user preferences block
        try:
            self.client.agent.get_block(self.agent_id, "user_preferences")
        except NotFoundError:
            self.client.agent.update_block(
                agent_id=self.agent_id,
                block_name="user_preferences",
                content="No preferences recorded yet.",
            )
    
    def start_session(self, user_id: str, metadata: dict | None = None) -> str:
        """Start a new conversation session."""
        session = self.client.agent.create_session(
            user_id=user_id,
            agent_id=self.agent_id,
            metadata=metadata or {}
        )
        self.session_id = session.id
        return session.id
    
    def end_session(self, consolidate: bool = True) -> None:
        """End the current session with optional consolidation."""
        if self.session_id:
            self.client.agent.end_session(
                session_id=self.session_id,
                consolidate=consolidate,
                strategy=ConsolidationStrategy.SUMMARIZE
            )
            self.session_id = None
    
    def get_context(self, user_message: str, limit: int = 5) -> list[str]:
        """Retrieve relevant context for responding."""
        if not self.session_id:
            return []
        
        context = self.client.agent.get_context(
            session_id=self.session_id,
            query=user_message,
            limit=limit
        )
        
        return [m.content for m in context.memories]
    
    def get_core_memory(self) -> dict[str, str]:
        """Get all core memory blocks."""
        core = self.client.agent.get_core_memory(agent_id=self.agent_id)
        return {block.name: block.content for block in core.blocks}
    
    def update_preference(self, preference: str) -> None:
        """Append a user preference to core memory."""
        self.client.agent.append_block(
            agent_id=self.agent_id,
            block_name="user_preferences",
            content=f" {preference}"
        )
    
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
        - Core memory (persona, preferences)
        """
        # Record user message
        self.record_turn("user", user_message)
        
        # Get relevant context
        context = self.get_context(user_message)
        core_memory = self.get_core_memory()
        
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
        print("   ✓ Session started")
        
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
        
        # Update preferences
        print("3. Recording user preference...")
        bot.update_preference("User prefers code examples.")
        print("   ✓ Preference recorded")
        
        # Show core memory
        print("\n4. Core memory state...")
        for name, content in bot.get_core_memory().items():
            print(f"   [{name}]: {content[:50]}...")
        
        # End session with consolidation
        print("\n5. Ending session with consolidation...")
        bot.end_session(consolidate=True)
        print("   ✓ Session ended and consolidated")
        
        # Cleanup core memory
        print("\n6. Cleaning up...")
        client.agent.delete_block(bot.agent_id, "persona")
        client.agent.delete_block(bot.agent_id, "user_preferences")
        print("   ✓ Cleaned up")
        
        print("\n" + "=" * 60)
        print("🎉 Chat bot complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()

