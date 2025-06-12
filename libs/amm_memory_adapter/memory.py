"""
AMM-compatible memory adapter for Thousand Questions system
Provides the same interface as agno.memory.v2 but works with our PostgreSQL schema
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import asyncio
import psycopg
from psycopg.rows import dict_row
import openai

class Memory:
    """
    AMM-compatible memory class for persistent conversation memory
    """
    
    def __init__(self, model: str, memory_db, enable_vector_index: bool = False):
        self.model = model
        self.memory_db = memory_db
        self.enable_vector_index = enable_vector_index
        self.openai_client = openai.OpenAI()
        
    async def get_user_memories(self, user_id: str, limit: int = 5, query: Optional[str] = None) -> List[Dict]:
        """
        Retrieve user memories, optionally filtered by semantic similarity to query
        """
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            user_uuid = uuid.uuid4()  # Generate if invalid
            
        conn = await self.memory_db.get_connection()
        
        if query and self.enable_vector_index:
            # Use vector similarity search
            query_embedding = await self._get_embedding(query)
            memories = await conn.fetch("""
                SELECT content, metadata, created_at,
                       1 - (embedding <=> $3::vector) as similarity
                FROM user_memories 
                WHERE user_id = $1 
                ORDER BY similarity DESC
                LIMIT $2
            """, user_uuid, limit, query_embedding)
        else:
            # Simple recency-based retrieval
            memories = await conn.fetch("""
                SELECT content, metadata, created_at
                FROM user_memories 
                WHERE user_id = $1 
                ORDER BY created_at DESC 
                LIMIT $2
            """, user_uuid, limit)
        
        await conn.close()
        
        return [
            {
                "content": m["content"],
                "metadata": m["metadata"] or {},
                "created_at": m["created_at"]
            }
            for m in memories
        ]
    
    async def create_user_memories(self, user_id: str, conversation_turns: List[tuple]) -> None:
        """
        Extract and store memories from conversation turns
        """
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            user_uuid = uuid.uuid4()
            
        # Extract memories using LLM
        memory_content = await self._extract_memories_from_turns(conversation_turns)
        
        if not memory_content:
            return
            
        conn = await self.memory_db.get_connection()
        
        for memory in memory_content:
            embedding = None
            if self.enable_vector_index:
                embedding = await self._get_embedding(memory["content"])
                
            await conn.execute("""
                INSERT INTO user_memories (user_id, content, embedding, metadata)
                VALUES ($1, $2, $3, $4)
            """, user_uuid, memory["content"], embedding, json.dumps(memory.get("metadata", {})))
        
        await conn.close()
    
    async def clear_user_memories(self, user_id: str) -> None:
        """Clear all memories for a user"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return
            
        conn = await self.memory_db.get_connection()
        await conn.execute("DELETE FROM user_memories WHERE user_id = $1", user_uuid)
        await conn.close()
    
    async def search(self, user_id: str, query: str, top_k: int = 5) -> List[Dict]:
        """Search memories by semantic similarity"""
        return await self.get_user_memories(user_id, limit=top_k, query=query)
    
    async def _extract_memories_from_turns(self, turns: List[tuple]) -> List[Dict]:
        """Use LLM to extract salient facts from conversation turns"""
        if not turns:
            return []
            
        # Format conversation for LLM
        conversation = []
        for user_msg, assistant_msg in turns:
            conversation.append(f"User: {user_msg}")
            conversation.append(f"Assistant: {assistant_msg}")
        
        conversation_text = "\n".join(conversation)
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Extract important facts about the user from this conversation that should be remembered for future interactions. Return a JSON array of objects with 'content' and 'metadata' fields. Focus on:
- Personal preferences and interests
- Important life details (family, work, location, etc.)
- Values and beliefs expressed
- Goals and aspirations mentioned
- Personality traits demonstrated

Example format:
[
  {"content": "User lives in San Francisco and works as a software engineer", "metadata": {"type": "personal_info"}},
  {"content": "User prefers hiking over indoor activities", "metadata": {"type": "preferences"}}
]

If no significant facts are found, return an empty array."""
                    },
                    {
                        "role": "user", 
                        "content": conversation_text
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result if isinstance(result, list) else result.get("memories", [])
            
        except Exception as e:
            print(f"Error extracting memories: {e}")
            return []
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.embeddings.create,
                model="text-embedding-3-large",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return [0.0] * 1536  # Return zero vector as fallback

class PostgresMemoryDb:
    """PostgreSQL memory database backend"""
    
    def __init__(self, database_url: str, table_name: str = "user_memories"):
        self.database_url = database_url
        self.table_name = table_name
    
    async def get_connection(self):
        """Get async database connection"""
        return await psycopg.AsyncConnection.connect(
            self.database_url,
            row_factory=dict_row
        )

class MemoryManager:
    """Higher-level memory management utilities"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    async def extract_and_store(self, user_id: str, conversation_turn: tuple):
        """Extract and store memories from a single conversation turn"""
        await self.memory.create_user_memories(user_id, [conversation_turn])
    
    async def consistency_score(self, user_id: str, new_answer: str, question_context: str) -> float:
        """Check consistency of new answer against stored memories"""
        related_memories = await self.memory.search(user_id, question_context, top_k=3)
        
        if not related_memories:
            return 0.8  # Default confidence if no memories
        
        # Use LLM to score consistency
        memory_context = "\n".join([f"- {m['content']}" for m in related_memories])
        
        try:
            response = await asyncio.to_thread(
                self.memory.openai_client.chat.completions.create,
                model=self.memory.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Rate the consistency of the new answer with the user's past statements on a scale of 0.0 to 1.0, where:
- 1.0 = Perfectly consistent with past statements
- 0.7-0.9 = Mostly consistent, minor variations acceptable
- 0.4-0.6 = Some inconsistencies but not contradictory
- 0.0-0.3 = Contradicts past statements

Return only a number between 0.0 and 1.0."""
                    },
                    {
                        "role": "user",
                        "content": f"""Past user statements:
{memory_context}

New answer to evaluate: "{new_answer}"
Context: {question_context}

Consistency score:"""
                    }
                ],
                temperature=0.1
            )
            
            score_text = response.choices[0].message.content.strip()
            return max(0.0, min(1.0, float(score_text)))
            
        except Exception as e:
            print(f"Error scoring consistency: {e}")
            return 0.5  # Default to moderate confidence on error

class SessionSummarizer:
    """Conversation session summarization"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.openai_client = openai.OpenAI()
    
    async def summarize(self, transcript: List[Dict]) -> str:
        """Summarize a conversation transcript"""
        if not transcript:
            return "Empty conversation"
        
        # Format transcript
        conversation = []
        for turn in transcript:
            if turn.get("role") == "user":
                conversation.append(f"User: {turn.get('content', '')}")
            elif turn.get("role") == "assistant":
                conversation.append(f"Assistant: {turn.get('content', '')}")
        
        conversation_text = "\n".join(conversation)
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Summarize this conversation in 2-3 sentences, focusing on:
- Key topics discussed
- Important decisions or insights
- User's main questions or concerns
- Any personal information shared

Keep it concise but informative for future reference."""
                    },
                    {
                        "role": "user",
                        "content": conversation_text
                    }
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error summarizing session: {e}")
            return f"Conversation with {len(transcript)} turns - summary unavailable"