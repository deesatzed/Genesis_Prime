import os
import uuid
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import psycopg
from psycopg.rows import dict_row
import openai
from jinja2 import Environment, FileSystemLoader

# Import our local libraries
import sys
sys.path.append('/Users/o2satz/sentient-ai-suite/libs')

from amm_memory_adapter import Memory, PostgresMemoryDb, MemoryManager
from persona_traits.builder import extract_traits, BIG_FIVE
from tq_dataset.sampler import sample_questions

class SentientAgent:
    def __init__(self, database_url: str = None, openrouter_api_key: str = None):
        # Set up database connection
        self.database_url = database_url or "postgresql://postgres:pass@localhost:5432/sentient"
        
        # Set up OpenRouter (OpenAI-compatible API)
        if openrouter_api_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_api_key
        
        api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.")
            
        self.openai_client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:3000"),
                "X-Title": os.getenv("OPENROUTER_SITE_NAME", "Genesis Prime Hive Mind"),
            }
        )
        
        # Set up memory system
        memory_db = PostgresMemoryDb(
            database_url=self.database_url,
            table_name="user_memories"
        )
        self.memory = Memory(
            model="openai/gpt-4o-mini",
            memory_db=memory_db,
            enable_vector_index=True
        )
        self.memory_manager = MemoryManager(self.memory)
        
        # Set up Jinja2 for prompts
        template_dir = os.path.join(os.path.dirname(__file__), "prompts")
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    async def run_sentience_setup(self, user_id: str, n_sample: int = 30) -> Dict[str, Any]:
        """
        Complete sentience setup flow:
        1. Sample questions for user to answer
        2. Build personality profile from answers
        3. Auto-generate remaining answers
        """
        print(f"🧠 Starting sentience setup for user {user_id}")
        
        # Step 1: Get sample questions
        sample_qs = await self.ask_sample_questions(user_id, n_sample)
        print(f"📝 Sampled {len(sample_qs)} questions across categories")
        
        # Step 2: Build personality profile (after user answers)
        # Note: This assumes user answers are already stored in tq_answers table
        traits = await self.build_persona(user_id)
        print(f"🎭 Extracted personality traits: {traits}")
        
        # Step 3: Generate remaining answers
        generated_count = await self.answer_remaining(user_id, traits)
        print(f"✨ Generated {generated_count} answers")
        
        return {
            "user_id": user_id,
            "sample_questions": len(sample_qs),
            "traits": traits,
            "generated_answers": generated_count,
            "total_answered": await self._count_user_answers(user_id)
        }

    async def ask_sample_questions(self, user_id: str, n: int) -> List[Dict]:
        """Get stratified sample of questions for user to answer"""
        try:
            questions = sample_questions(user_id, n)
            return questions
        except Exception as e:
            print(f"Error sampling questions: {e}")
            # Fallback: get random questions from database
            return await self._get_fallback_questions(n)

    async def build_persona(self, user_id: str) -> Dict[str, Any]:
        """Extract personality traits from user's sample answers"""
        try:
            traits_dict = extract_traits(user_id)
            
            # Store traits in user_profiles table
            await self._store_user_profile(user_id, traits_dict)
            
            return traits_dict
        except Exception as e:
            print(f"Error building persona: {e}")
            # Return default traits
            return {trait: 0.5 for trait in BIG_FIVE}

    async def answer_remaining(self, user_id: str, traits: Dict[str, Any]) -> int:
        """Auto-generate answers for all unanswered questions"""
        # Get all unanswered questions
        unanswered = await self._get_unanswered_questions(user_id)
        print(f"🤔 Found {len(unanswered)} unanswered questions")
        
        if not unanswered:
            return 0
        
        generated_count = 0
        
        # Process in batches to avoid overwhelming the LLM
        batch_size = 10
        for i in range(0, len(unanswered), batch_size):
            batch = unanswered[i:i + batch_size]
            
            for question in batch:
                try:
                    answer = await self._generate_answer(user_id, question, traits)
                    if answer:
                        await self._store_generated_answer(user_id, question["id"], answer)
                        generated_count += 1
                        
                        # Store memory of this answer for consistency
                        await self.memory.create_user_memories(
                            user_id, 
                            [(question["text"], answer)]
                        )
                        
                except Exception as e:
                    print(f"Error generating answer for {question['id']}: {e}")
                    continue
            
            # Small delay between batches
            await asyncio.sleep(0.5)
        
        return generated_count

    async def _generate_answer(self, user_id: str, question: Dict, traits: Dict) -> Optional[str]:
        """Generate a single answer using LLM with personality context"""
        try:
            # Get relevant memories for context
            memories = await self.memory.get_user_memories(
                user_id, 
                limit=5, 
                query=question["text"]
            )
            
            # Load and render prompt template
            template = self.jinja_env.get_template("mono_agent.jinja2")
            prompt = template.render(
                traits=self._format_traits(traits),
                memories=memories,
                question=question
            )
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Answer this question as yourself: {question['text']}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in LLM generation: {e}")
            return None

    async def _get_unanswered_questions(self, user_id: str) -> List[Dict]:
        """Get all questions not yet answered by user or system"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            user_uuid = uuid.uuid4()
            
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        unanswered = await conn.fetch("""
            SELECT q.id, q.text, q.category, q.themes, q.complexity
            FROM tq_questions q
            LEFT JOIN tq_answers a ON q.id = a.question_id AND a.user_id = $1
            WHERE a.question_id IS NULL
            ORDER BY q.complexity, q.category
        """, user_uuid)
        
        await conn.close()
        return [dict(q) for q in unanswered]

    async def _store_generated_answer(self, user_id: str, question_id: str, answer: str):
        """Store AI-generated answer in database"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            user_uuid = uuid.uuid4()
            
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        await conn.execute("""
            INSERT INTO tq_answers (user_id, question_id, answer_text, is_user_answer, confidence, created_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (user_id, question_id, version) DO UPDATE SET
                answer_text = EXCLUDED.answer_text,
                confidence = EXCLUDED.confidence,
                created_at = EXCLUDED.created_at
        """, user_uuid, question_id, answer, False, 0.8, datetime.utcnow())
        
        await conn.close()

    async def _store_user_profile(self, user_id: str, traits: Dict[str, Any]):
        """Store user personality profile"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            user_uuid = uuid.uuid4()
            
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        await conn.execute("""
            INSERT INTO user_profiles (user_id, traits, updated_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO UPDATE SET
                traits = EXCLUDED.traits,
                updated_at = EXCLUDED.updated_at
        """, user_uuid, json.dumps(traits), datetime.utcnow())
        
        await conn.close()

    async def _count_user_answers(self, user_id: str) -> int:
        """Count total answers for user"""
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            return 0
            
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        result = await conn.fetchrow("""
            SELECT COUNT(*) as count 
            FROM tq_answers 
            WHERE user_id = $1
        """, user_uuid)
        
        await conn.close()
        return result["count"] if result else 0

    async def _get_fallback_questions(self, n: int) -> List[Dict]:
        """Fallback method to get questions if sampler fails"""
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        questions = await conn.fetch("""
            SELECT id, text, category, themes, complexity
            FROM tq_questions
            ORDER BY RANDOM()
            LIMIT $1
        """, n)
        
        await conn.close()
        return [dict(q) for q in questions]

    def _format_traits(self, traits: Dict[str, Any]) -> str:
        """Format traits for prompt inclusion"""
        if not traits:
            return "Traits not yet determined"
            
        formatted = []
        for trait in BIG_FIVE:
            if trait in traits:
                value = traits[trait]
                level = "High" if value > 0.6 else "Moderate" if value > 0.4 else "Low"
                formatted.append(f"{trait.title()}: {value:.2f} ({level})")
        
        return "\n".join(formatted)
