#!/usr/bin/env python3
"""
Chat Bot - Asynchronous Version

Run: python async_example.py
"""

import asyncio
from trix import AsyncTrix
from trix.types import ConsolidationStrategy


class AsyncChatBot:
    """An async memory-enabled chatbot using Trix."""
    
    def __init__(self, client: AsyncTrix, agent_id: str = "async_chatbot_v1"):
        self.client = client
        self.agent_id = agent_id
        self.session_id: str | None = None
    
    async def setup(self) -> None:
        """Initialize core memory blocks."""
        await asyncio.gather(
            self.client.agent.update_block(
                agent_id=self.agent_id,
                block_name="persona",
                content="I am a helpful async AI assistant.",
            ),
            self.client.agent.update_block(
                agent_id=self.agent_id,
                block_name="user_preferences",
                content="No preferences recorded yet.",
            ),
        )
    
    async def start_session(self, user_id: str) -> str:
        """Start a new conversation session."""
        session = await self.client.agent.create_session(
            user_id=user_id,
            agent_id=self.agent_id,
        )
        self.session_id = session.id
        return session.id
    
    async def end_session(self) -> None:
        """End the current session with consolidation."""
        if self.session_id:
            await self.client.agent.end_session(
                session_id=self.session_id,
                consolidate=True,
                strategy=ConsolidationStrategy.SUMMARIZE
            )
            self.session_id = None
    
    async def respond(self, user_message: str) -> str:
        """Generate a response with parallel context retrieval."""
        if not self.session_id:
            raise ValueError("No active session")
        
        # Record user message and get context in parallel
        record_task = self.client.agent.add_session_memory(
            session_id=self.session_id,
            content=user_message,
            role="user",
        )
        
        context_task = self.client.agent.get_context(
            session_id=self.session_id,
            query=user_message,
            limit=5
        )
        
        core_task = self.client.agent.get_core_memory(agent_id=self.agent_id)
        
        _, context, core = await asyncio.gather(
            record_task, context_task, core_task
        )
        
        # Generate response (in real app, call LLM here)
        response = f"[Async bot received: '{user_message}']"
        
        if context.memories:
            response += f"\n[Context: {len(context.memories)} memories]"
        
        # Record response
        await self.client.agent.add_session_memory(
            session_id=self.session_id,
            content=response,
            role="assistant",
        )
        
        return response
    
    async def cleanup(self) -> None:
        """Clean up core memory blocks."""
        await asyncio.gather(
            self.client.agent.delete_block(self.agent_id, "persona"),
            self.client.agent.delete_block(self.agent_id, "user_preferences"),
        )


async def main():
    """Demonstrate the async chatbot."""
    print("=" * 60)
    print("ASYNC CHAT BOT USE CASE")
    print("=" * 60)
    
    async with AsyncTrix.from_env() as client:
        bot = AsyncChatBot(client)
        
        print("\n1. Setting up bot...")
        await bot.setup()
        print("   ✓ Bot initialized")
        
        print("\n2. Starting session...")
        await bot.start_session(user_id="async_user")
        print("   ✓ Session started")
        
        print("\n3. Conversation (with parallel operations)...")
        
        messages = [
            "Hello! Tell me about async programming.",
            "What are the benefits?",
            "How does it work in Python?",
        ]
        
        for msg in messages:
            print(f"   User: {msg}")
            response = await bot.respond(msg)
            print(f"   Bot: {response}\n")
        
        print("4. Ending session...")
        await bot.end_session()
        print("   ✓ Session ended")
        
        print("\n5. Cleaning up...")
        await bot.cleanup()
        print("   ✓ Cleaned up")
        
        print("\n" + "=" * 60)
        print("🎉 Async chat bot complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

