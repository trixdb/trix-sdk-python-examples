#!/usr/bin/env python3
"""
AI Agent Memory - Synchronous Version

A memory system for AI agents demonstrating:
1. Long-term memory storage
2. Working memory (session-based)
3. Episodic memory (experiences)
4. Semantic memory (facts and knowledge)

Run: python main.py
"""

from trix import Trix


class AgentMemory:
    """A comprehensive memory system for AI agents."""

    def __init__(self, client: Trix, agent_id: str):
        self.client = client
        self.agent_id = agent_id
        self.session_id: str | None = None

    # =========================================================================
    # Working Memory (Current Session)
    # =========================================================================

    def start_task(self, task_description: str) -> str:
        """Start a new task/session."""
        session = self.client.agent.create_session(
            session_id=f"task_{self.agent_id}", metadata={"task": task_description}
        )
        self.session_id = session.session_id
        return session.session_id

    def add_to_working_memory(self, content: str, importance: float = 0.5) -> str:
        """Add something to working memory."""
        if not self.session_id:
            raise ValueError("No active session")

        mem = self.client.agent.add_session_memory(
            session_id=self.session_id, content=content, role="system", importance=importance
        )
        return mem.id

    def get_working_context(self, query: str, limit: int = 5) -> list[str]:
        """Get relevant working memory for current task."""
        if not self.session_id:
            return []

        context = self.client.agent.get_context(
            query=query, session_id=self.session_id, limit=limit
        )
        return [m.content for m in context.memories]

    def complete_task(self) -> None:
        """Complete current task and summarize session."""
        if self.session_id:
            self.client.agent.end_session(
                session_id=self.session_id,
                summary="Task completed",
                key_insights=["Task finished successfully"],
            )
            self.session_id = None

    # =========================================================================
    # Long-term Memory
    # =========================================================================

    def store_episodic(self, experience: str, emotion: str | None = None) -> str:
        """Store an episodic memory (experience/event)."""
        memory = self.client.memories.create(
            content=experience,
            tags=["episodic", emotion] if emotion else ["episodic"],
            metadata={"type": "episodic", "emotion": emotion},
        )
        return memory.id

    def store_semantic(self, fact: str, topic: str) -> str:
        """Store a semantic memory (fact/knowledge)."""
        memory = self.client.memories.create(
            content=fact, tags=["semantic", topic], metadata={"type": "semantic", "topic": topic}
        )
        return memory.id

    def recall(self, query: str, memory_type: str | None = None, limit: int = 10) -> list[dict]:
        """Recall memories by query and optional type."""
        tags = [memory_type] if memory_type else None

        results = self.client.search.query(query=query, tags=tags, limit=limit)

        return [
            {"content": r.memory.content, "score": r.score, "type": r.memory.metadata.get("type")}
            for r in results.data
        ]


def main():
    """Demonstrate the AI agent memory system."""
    print("=" * 60)
    print("AI AGENT MEMORY")
    print("=" * 60)

    with Trix.from_env() as client:
        agent = AgentMemory(client, agent_id="smart_agent_v1")

        # Store some semantic memories (facts)
        print("\n1. Storing semantic memories...")
        mem_ids = []
        facts = [
            ("Python was created by Guido van Rossum.", "python"),
            ("Machine learning requires training data.", "ml"),
            ("REST APIs use HTTP methods.", "web"),
        ]
        for fact, topic in facts:
            mem_id = agent.store_semantic(fact, topic)
            mem_ids.append(mem_id)
        print(f"   Stored {len(facts)} semantic memories")

        # Store episodic memory
        print("\n2. Storing episodic memory...")
        ep_id = agent.store_episodic(
            "User asked about Python and seemed excited to learn.", emotion="positive"
        )
        mem_ids.append(ep_id)
        print("   Stored episodic memory")

        # Start a task (working memory)
        print("\n3. Starting a task...")
        agent.start_task("Research Python web frameworks")
        print("   Task started")

        # Add to working memory
        print("\n4. Building working memory...")
        agent.add_to_working_memory("User wants to compare Flask and Django")
        agent.add_to_working_memory("Focus on ease of use and performance")
        print("   Working memory populated")

        # Get working context
        print("\n5. Getting working context...")
        context = agent.get_working_context("framework comparison")
        print(f"   Found {len(context)} relevant items")

        # Recall from long-term memory
        print("\n6. Recalling from long-term memory...")
        memories = agent.recall("Python programming", memory_type="semantic")
        print(f"   Recalled {len(memories)} semantic memories")

        # Complete task
        print("\n7. Completing task...")
        agent.complete_task()
        print("   Task completed and session ended")

        # Cleanup
        print("\n8. Cleaning up...")
        client.memories.bulk_delete(mem_ids)
        print("   Cleaned up")

        print("\n" + "=" * 60)
        print("AI agent memory complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
