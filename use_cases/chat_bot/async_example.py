#!/usr/bin/env python3
"""
Chat Bot - Asynchronous Version

Run: python async_example.py
"""

import asyncio

from trix import AsyncTrix


class AsyncChatBot:
    """An async memory-enabled chatbot using Trix."""

    def __init__(self, client: AsyncTrix, bot_name: str = "async_chatbot_v1"):
        self.client = client
        self.bot_name = bot_name
        self.session_id: str | None = None

    async def start_session(self, user_id: str) -> str:
        """Start a new conversation session."""
        session_id = f"chat_{user_id}_{self.bot_name}"
        session = await self.client.agent.create_session(
            session_id=session_id,
        )
        self.session_id = session.session_id
        return session.session_id

    async def end_session(self) -> None:
        """End the current session with summary."""
        if self.session_id:
            await self.client.agent.end_session(
                session_id=self.session_id,
                summary="Async conversation ended",
                key_insights=["Session completed"],
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
            query=user_message, session_id=self.session_id, limit=5
        )

        _, context = await asyncio.gather(record_task, context_task)

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


async def main():
    """Demonstrate the async chatbot."""
    print("=" * 60)
    print("ASYNC CHAT BOT USE CASE")
    print("=" * 60)

    async with AsyncTrix.from_env() as client:
        bot = AsyncChatBot(client)

        print("\n1. Starting session...")
        await bot.start_session(user_id="async_user")
        print("   Session started")

        print("\n2. Conversation (with parallel operations)...")

        messages = [
            "Hello! Tell me about async programming.",
            "What are the benefits?",
            "How does it work in Python?",
        ]

        for msg in messages:
            print(f"   User: {msg}")
            response = await bot.respond(msg)
            print(f"   Bot: {response}\n")

        print("3. Ending session...")
        await bot.end_session()
        print("   Session ended")

        print("\n" + "=" * 60)
        print("Async chat bot complete!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
