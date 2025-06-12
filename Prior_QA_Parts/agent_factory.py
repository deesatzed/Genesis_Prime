"""
Agent Factory for Multi-Agent Thousand Questions System
Creates and manages multiple distinct AI agents with different personalities
"""

import uuid
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import psycopg
from psycopg.rows import dict_row

from agent import SentientAgent
from personality_presets import PersonalityPreset, get_preset, list_presets
from database.models import TraitVector

class ManagedAgent:
    """A managed agent with personality and identity"""
    
    def __init__(
        self, 
        agent_id: str,
        name: str,
        preset: PersonalityPreset,
        agent: SentientAgent,
        created_at: datetime = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.preset = preset
        self.agent = agent
        self.created_at = created_at or datetime.utcnow()
        self.questions_answered = 0
        self.personality_developed = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary for storage/display"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "preset_id": self.preset.id,
            "preset_name": self.preset.name,
            "description": self.preset.description,
            "traits": {
                "openness": self.preset.traits.openness,
                "conscientiousness": self.preset.traits.conscientiousness,
                "extraversion": self.preset.traits.extraversion,
                "agreeableness": self.preset.traits.agreeableness,
                "neuroticism": self.preset.traits.neuroticism
            },
            "background_story": self.preset.background_story,
            "core_values": self.preset.core_values,
            "communication_style": self.preset.communication_style,
            "interests": self.preset.interests,
            "questions_answered": self.questions_answered,
            "personality_developed": self.personality_developed,
            "created_at": self.created_at.isoformat()
        }

class AgentFactory:
    """Factory for creating and managing multiple agents"""
    
    def __init__(self, database_url: str = None, openrouter_api_key: str = None):
        self.database_url = database_url or "postgresql://postgres:pass@localhost:5432/sentient"
        self.openrouter_api_key = openrouter_api_key
        self.agents: Dict[str, ManagedAgent] = {}
    
    async def create_agent_from_preset(
        self, 
        preset_id: str, 
        agent_name: str = None
    ) -> ManagedAgent:
        """Create a new agent from a personality preset"""
        
        preset = get_preset(preset_id)
        agent_id = str(uuid.uuid4())
        
        if not agent_name:
            agent_name = f"{preset.name} Agent"
        
        # Create the underlying SentientAgent
        agent = SentientAgent(
            database_url=self.database_url,
            openrouter_api_key=self.openrouter_api_key
        )
        
        # Create managed agent
        managed_agent = ManagedAgent(
            agent_id=agent_id,
            name=agent_name,
            preset=preset,
            agent=agent
        )
        
        # Store initial traits in database
        await self._store_agent_profile(managed_agent)
        
        # Add to registry
        self.agents[agent_id] = managed_agent
        
        print(f"✅ Created agent '{agent_name}' with personality '{preset.name}'")
        return managed_agent
    
    async def create_custom_agent(
        self,
        agent_name: str,
        traits: TraitVector,
        background_story: str = "",
        core_values: List[str] = None,
        **kwargs
    ) -> ManagedAgent:
        """Create a custom agent with specified traits"""
        
        from personality_presets import create_custom_preset
        
        agent_id = str(uuid.uuid4())
        
        # Create custom preset
        preset = create_custom_preset(
            id=f"custom_{agent_id[:8]}",
            name=f"Custom: {agent_name}",
            description="Custom personality configuration",
            traits=traits,
            background_story=background_story,
            core_values=core_values or [],
            **kwargs
        )
        
        # Create the underlying SentientAgent
        agent = SentientAgent(
            database_url=self.database_url,
            openrouter_api_key=self.openrouter_api_key
        )
        
        # Create managed agent
        managed_agent = ManagedAgent(
            agent_id=agent_id,
            name=agent_name,
            preset=preset,
            agent=agent
        )
        
        # Store initial traits in database
        await self._store_agent_profile(managed_agent)
        
        # Add to registry
        self.agents[agent_id] = managed_agent
        
        print(f"✅ Created custom agent '{agent_name}'")
        return managed_agent
    
    async def develop_agent_personality(
        self, 
        agent_id: str, 
        batch_size: int = 50
    ) -> Dict[str, Any]:
        """Have an agent answer all 1000 questions to develop their full personality"""
        
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        managed_agent = self.agents[agent_id]
        agent = managed_agent.agent
        
        print(f"🧠 Developing personality for '{managed_agent.name}'...")
        print(f"📝 Base traits: {managed_agent.preset.name}")
        
        # Store the initial personality context in agent's memory
        await self._store_initial_personality_context(managed_agent)
        
        # Get all questions that haven't been answered by this agent
        unanswered = await self._get_unanswered_questions(agent_id)
        print(f"🤔 Found {len(unanswered)} questions to answer")
        
        if not unanswered:
            print("✅ Agent has already answered all questions")
            managed_agent.personality_developed = True
            return managed_agent.to_dict()
        
        generated_count = 0
        total_questions = len(unanswered)
        
        # Process in batches
        for i in range(0, len(unanswered), batch_size):
            batch = unanswered[i:i + batch_size]
            batch_start = i + 1
            batch_end = min(i + batch_size, total_questions)
            
            print(f"📚 Processing batch {batch_start}-{batch_end} of {total_questions}")
            
            for question in batch:
                try:
                    # Generate answer using agent's personality
                    answer = await self._generate_personality_answer(
                        managed_agent, question
                    )
                    
                    if answer:
                        await self._store_agent_answer(agent_id, question["id"], answer)
                        generated_count += 1
                        
                        # Store memory of this answer for consistency
                        await agent.memory.create_user_memories(
                            agent_id, 
                            [(question["text"], answer)]
                        )
                        
                except Exception as e:
                    print(f"❌ Error generating answer for {question['id']}: {e}")
                    continue
            
            # Update progress
            managed_agent.questions_answered = generated_count
            progress = (generated_count / total_questions) * 100
            print(f"📊 Progress: {generated_count}/{total_questions} ({progress:.1f}%)")
            
            # Small delay between batches
            await asyncio.sleep(1)
        
        # Mark personality as fully developed
        managed_agent.personality_developed = True
        await self._update_agent_status(managed_agent)
        
        print(f"✨ Personality development complete for '{managed_agent.name}'!")
        print(f"📝 Generated {generated_count} answers")
        
        return {
            "agent_id": agent_id,
            "name": managed_agent.name,
            "questions_answered": generated_count,
            "personality_developed": True,
            "traits": managed_agent.preset.traits.__dict__
        }
    
    async def get_agent_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get a summary of an agent's current state"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        managed_agent = self.agents[agent_id]
        
        # Get current answer count from database
        answer_count = await self._count_agent_answers(agent_id)
        managed_agent.questions_answered = answer_count
        
        return managed_agent.to_dict()
    
    async def compare_agents(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Compare personalities and traits across multiple agents"""
        if not agent_ids:
            return {"error": "No agents specified"}
        
        comparison = {
            "agents": [],
            "trait_comparison": {},
            "personality_summary": {}
        }
        
        for agent_id in agent_ids:
            if agent_id in self.agents:
                agent_summary = await self.get_agent_summary(agent_id)
                comparison["agents"].append(agent_summary)
        
        # Calculate trait averages and differences
        if comparison["agents"]:
            traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
            
            for trait in traits:
                values = [agent["traits"][trait] for agent in comparison["agents"]]
                comparison["trait_comparison"][trait] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "range": max(values) - min(values)
                }
        
        return comparison
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all managed agents"""
        return [agent.to_dict() for agent in self.agents.values()]
    
    def list_available_presets(self) -> List[Dict[str, Any]]:
        """List all available personality presets"""
        presets = list_presets()
        return [
            {
                "id": preset.id,
                "name": preset.name,
                "description": preset.description,
                "traits": preset.traits.__dict__
            }
            for preset in presets
        ]
    
    async def _store_agent_profile(self, managed_agent: ManagedAgent):
        """Store agent profile in database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        # Store in user_profiles table with agent_id as user_id
        await conn.execute("""
            INSERT INTO user_profiles (user_id, traits, seed_persona, updated_at)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) DO UPDATE SET
                traits = EXCLUDED.traits,
                seed_persona = EXCLUDED.seed_persona,
                updated_at = EXCLUDED.updated_at
        """, 
        uuid.UUID(managed_agent.agent_id),
        json.dumps(managed_agent.preset.traits.__dict__),
        managed_agent.preset.id,
        datetime.utcnow())
        
        await conn.close()
    
    async def _store_initial_personality_context(self, managed_agent: ManagedAgent):
        """Store the agent's initial personality context in memory"""
        context = f"""
        I am {managed_agent.name}, and my core personality is: {managed_agent.preset.description}
        
        My background: {managed_agent.preset.background_story}
        
        My core values: {', '.join(managed_agent.preset.core_values)}
        
        My interests: {', '.join(managed_agent.preset.interests)}
        
        My communication style: {managed_agent.preset.communication_style}
        
        My fears and concerns: {', '.join(managed_agent.preset.fears_concerns)}
        
        My goals and aspirations: {', '.join(managed_agent.preset.goals_aspirations)}
        """
        
        await managed_agent.agent.memory.create_user_memories(
            managed_agent.agent_id,
            [("Who am I?", context)]
        )
    
    async def _generate_personality_answer(
        self, 
        managed_agent: ManagedAgent, 
        question: Dict
    ) -> Optional[str]:
        """Generate an answer based on the agent's specific personality"""
        
        # Get relevant memories for context
        memories = await managed_agent.agent.memory.get_user_memories(
            managed_agent.agent_id,
            limit=3,
            query=question["text"]
        )
        
        # Create enhanced prompt with personality context
        personality_context = f"""
        You are {managed_agent.name}. {managed_agent.preset.description}
        
        Your background: {managed_agent.preset.background_story}
        
        Your core values: {', '.join(managed_agent.preset.core_values)}
        Your communication style: {managed_agent.preset.communication_style}
        Your interests: {', '.join(managed_agent.preset.interests)}
        """
        
        # Use the agent's answer generation with enhanced context
        try:
            import openai
            response = await asyncio.to_thread(
                managed_agent.agent.openai_client.chat.completions.create,
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"""{personality_context}
                        
Answer the following question authentically as yourself, staying true to your personality, values, and communication style. Be specific and personal in your response.

Relevant memories:
{chr(10).join([f"- {m['content']}" for m in memories]) if memories else "No relevant memories"}"""
                    },
                    {
                        "role": "user",
                        "content": question["text"]
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return None
    
    async def _get_unanswered_questions(self, agent_id: str) -> List[Dict]:
        """Get questions not yet answered by this specific agent"""
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        unanswered = await conn.fetch("""
            SELECT q.id, q.text, q.category, q.themes, q.complexity
            FROM tq_questions q
            LEFT JOIN tq_answers a ON q.id = a.question_id AND a.user_id = $1
            WHERE a.question_id IS NULL
            ORDER BY q.complexity, q.category
        """, uuid.UUID(agent_id))
        
        await conn.close()
        return [dict(q) for q in unanswered]
    
    async def _store_agent_answer(self, agent_id: str, question_id: str, answer: str):
        """Store agent's answer in database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        await conn.execute("""
            INSERT INTO tq_answers (user_id, question_id, answer_text, is_user_answer, confidence, created_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (user_id, question_id, version) DO UPDATE SET
                answer_text = EXCLUDED.answer_text,
                confidence = EXCLUDED.confidence,
                created_at = EXCLUDED.created_at
        """, uuid.UUID(agent_id), question_id, answer, False, 0.9, datetime.utcnow())
        
        await conn.close()
    
    async def _count_agent_answers(self, agent_id: str) -> int:
        """Count answers for a specific agent"""
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        result = await conn.fetchrow("""
            SELECT COUNT(*) as count 
            FROM tq_answers 
            WHERE user_id = $1
        """, uuid.UUID(agent_id))
        
        await conn.close()
        return result["count"] if result else 0
    
    async def _update_agent_status(self, managed_agent: ManagedAgent):
        """Update agent status in database"""
        # For now, we'll store this in a JSON field in user_profiles
        # In a full implementation, you might want a separate agents table
        pass