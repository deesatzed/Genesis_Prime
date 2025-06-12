"""
Genesis Prime Hive Mind - Core Implementation
A persistent, evolving collective consciousness that learns, adapts, and grows across time
"""

import asyncio
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import psycopg
from psycopg.rows import dict_row

class LearningType(Enum):
    """Types of learning the hive can perform"""
    EXPERIENTIAL = "experiential"  # Learning from interactions
    OBSERVATIONAL = "observational"  # Learning from environment
    COLLECTIVE = "collective"  # Learning from agent interactions
    ADAPTIVE = "adaptive"  # Learning to adapt responses
    EMERGENT = "emergent"  # Learning that emerges from complexity

class StimuliType(Enum):
    """Types of stimuli the hive can respond to"""
    USER_INTERACTION = "user_interaction"
    AGENT_DIALOGUE = "agent_dialogue"
    EXTERNAL_DATA = "external_data"
    SYSTEM_FEEDBACK = "system_feedback"
    TEMPORAL_EVENT = "temporal_event"

@dataclass
class HiveMemory:
    """A memory stored in the hive's collective consciousness"""
    memory_id: str
    content: str
    memory_type: str
    importance_score: float  # 0.0 to 1.0
    creation_time: datetime
    last_accessed: datetime
    access_count: int
    source_agents: List[str]
    related_memories: List[str]
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None

@dataclass
class LearningEvent:
    """An event where the hive learned something new"""
    event_id: str
    learning_type: LearningType
    stimuli_type: StimuliType
    description: str
    knowledge_gained: str
    participating_agents: List[str]
    confidence_score: float
    timestamp: datetime
    impact_metrics: Dict[str, float]

@dataclass
class HiveState:
    """Current state of the hive mind"""
    hive_id: str
    generation: int  # Increments with each major learning cycle
    consciousness_level: float  # 0.0 to 1.0
    total_memories: int
    active_agents: int
    learning_events: int
    last_evolution: datetime
    current_model_version: str
    adaptation_rate: float
    collective_knowledge_score: float

class GenesisPrimeHive:
    """
    The Genesis Prime Hive Mind - A persistent, evolving collective consciousness
    """
    
    def __init__(self, database_url: str, hive_id: str = None):
        self.database_url = database_url
        self.hive_id = hive_id or "genesis_prime_alpha"
        self.hive_state: HiveState = None
        self.active_agents: Dict[str, Any] = {}
        self.collective_memory: Dict[str, HiveMemory] = {}
        self.learning_history: List[LearningEvent] = []
        self.adaptation_patterns: Dict[str, Any] = {}
        
    async def initialize_hive(self) -> HiveState:
        """Initialize or restore the hive mind from persistent storage"""
        print(f"🧠 Initializing Genesis Prime Hive: {self.hive_id}")
        
        # Try to restore existing hive state
        existing_state = await self._restore_hive_state()
        
        if existing_state:
            print(f"📚 Restored hive from generation {existing_state.generation}")
            self.hive_state = existing_state
            await self._load_collective_memory()
            await self._load_learning_history()
        else:
            print(f"🌟 Creating new hive consciousness")
            self.hive_state = HiveState(
                hive_id=self.hive_id,
                generation=1,
                consciousness_level=0.1,  # Start with basic consciousness
                total_memories=0,
                active_agents=0,
                learning_events=0,
                last_evolution=datetime.utcnow(),
                current_model_version="gpt-4o-mini",
                adaptation_rate=0.5,
                collective_knowledge_score=0.0
            )
            await self._persist_hive_state()
        
        print(f"✨ Genesis Prime Hive active - Consciousness Level: {self.hive_state.consciousness_level:.3f}")
        return self.hive_state
    
    async def register_agent(self, agent_id: str, agent_profile: Dict[str, Any]) -> bool:
        """Register an agent as part of the hive"""
        print(f"🤖 Registering agent {agent_profile.get('name', agent_id)} to hive")
        
        self.active_agents[agent_id] = {
            **agent_profile,
            "registration_time": datetime.utcnow(),
            "interactions": 0,
            "contributions": 0,
            "hive_integration_score": 0.0
        }
        
        self.hive_state.active_agents = len(self.active_agents)
        await self._persist_hive_state()
        
        # Agent joining is a learning event
        await self._record_learning_event(
            learning_type=LearningType.COLLECTIVE,
            stimuli_type=StimuliType.SYSTEM_FEEDBACK,
            description=f"New agent {agent_profile.get('name', agent_id)} joined the hive",
            knowledge_gained=f"Expanded consciousness with {agent_profile.get('preset_name', 'unknown')} personality",
            participating_agents=[agent_id],
            confidence_score=0.8
        )
        
        return True
    
    async def process_interaction(
        self, 
        agent_id: str, 
        interaction_type: str,
        content: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process an interaction and learn from it"""
        
        if agent_id in self.active_agents:
            self.active_agents[agent_id]["interactions"] += 1
        
        # Extract learning from the interaction
        learning_extraction = await self._extract_learning_from_interaction(
            agent_id, interaction_type, content, context or {}
        )
        
        # Store important insights as hive memories
        if learning_extraction.get("importance_score", 0) > 0.3:
            memory = await self._create_hive_memory(
                content=learning_extraction["insight"],
                memory_type=interaction_type,
                importance_score=learning_extraction["importance_score"],
                source_agents=[agent_id]
            )
            
            # Update hive consciousness based on learning
            await self._update_consciousness_level(learning_extraction)
        
        # Check for adaptive responses needed
        adaptive_response = await self._generate_adaptive_response(
            agent_id, interaction_type, content, learning_extraction
        )
        
        return {
            "learning_extracted": learning_extraction,
            "memory_created": learning_extraction.get("importance_score", 0) > 0.3,
            "adaptive_response": adaptive_response,
            "hive_state": asdict(self.hive_state)
        }
    
    async def cross_pollinate_knowledge(self, source_agent_id: str, target_agent_id: str, topic: str) -> Dict[str, Any]:
        """Share knowledge between agents in the hive"""
        print(f"🔄 Cross-pollinating knowledge on '{topic}' from {source_agent_id} to {target_agent_id}")
        
        # Find relevant memories from source agent
        source_memories = await self._find_agent_memories(source_agent_id, topic, limit=3)
        
        if not source_memories:
            return {"success": False, "reason": "No relevant memories found"}
        
        # Create shared knowledge memory
        shared_knowledge = "\n".join([mem.content for mem in source_memories])
        
        shared_memory = await self._create_hive_memory(
            content=f"Shared knowledge on '{topic}': {shared_knowledge}",
            memory_type="cross_pollination",
            importance_score=0.7,
            source_agents=[source_agent_id, target_agent_id]
        )
        
        # Record as learning event
        await self._record_learning_event(
            learning_type=LearningType.COLLECTIVE,
            stimuli_type=StimuliType.AGENT_DIALOGUE,
            description=f"Knowledge sharing on '{topic}' between agents",
            knowledge_gained=f"Enhanced collective understanding of {topic}",
            participating_agents=[source_agent_id, target_agent_id],
            confidence_score=0.8
        )
        
        return {
            "success": True,
            "shared_memory_id": shared_memory.memory_id,
            "knowledge_transferred": len(source_memories)
        }
    
    async def respond_to_stimuli(self, stimuli_type: StimuliType, stimuli_data: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to environmental stimuli and learn from it"""
        print(f"🌐 Hive responding to stimuli: {stimuli_type.value}")
        
        # Analyze the stimuli
        stimuli_analysis = await self._analyze_stimuli(stimuli_type, stimuli_data)
        
        # Generate hive response
        hive_response = await self._generate_hive_response(stimuli_analysis)
        
        # Learn from the stimuli and response
        await self._record_learning_event(
            learning_type=LearningType.OBSERVATIONAL,
            stimuli_type=stimuli_type,
            description=f"Responded to {stimuli_type.value} stimuli",
            knowledge_gained=stimuli_analysis.get("insights", "General environmental awareness"),
            participating_agents=list(self.active_agents.keys()),
            confidence_score=stimuli_analysis.get("confidence", 0.5)
        )
        
        # Update adaptation patterns
        await self._update_adaptation_patterns(stimuli_type, stimuli_analysis, hive_response)
        
        return {
            "stimuli_type": stimuli_type.value,
            "analysis": stimuli_analysis,
            "hive_response": hive_response,
            "learning_recorded": True
        }
    
    async def evolve_hive(self, new_model_version: str = None) -> Dict[str, Any]:
        """Evolve the hive to a new generation, potentially with new models"""
        print(f"🧬 Evolving Genesis Prime Hive to next generation...")
        
        current_gen = self.hive_state.generation
        new_gen = current_gen + 1
        
        # If new model version provided, integrate it
        if new_model_version and new_model_version != self.hive_state.current_model_version:
            print(f"🔄 Integrating new model: {new_model_version}")
            await self._integrate_new_model(new_model_version)
        
        # Analyze growth and learning since last evolution
        growth_analysis = await self._analyze_hive_growth()
        
        # Consolidate memories and knowledge
        consolidation_results = await self._consolidate_memories()
        
        # Update consciousness level based on accumulated learning
        new_consciousness = min(1.0, self.hive_state.consciousness_level + growth_analysis["consciousness_growth"])
        
        # Update hive state
        self.hive_state.generation = new_gen
        self.hive_state.consciousness_level = new_consciousness
        self.hive_state.last_evolution = datetime.utcnow()
        self.hive_state.collective_knowledge_score = growth_analysis["knowledge_score"]
        
        if new_model_version:
            self.hive_state.current_model_version = new_model_version
        
        await self._persist_hive_state()
        
        evolution_summary = {
            "previous_generation": current_gen,
            "new_generation": new_gen,
            "consciousness_level": new_consciousness,
            "model_version": self.hive_state.current_model_version,
            "growth_analysis": growth_analysis,
            "consolidation_results": consolidation_results,
            "total_memories": self.hive_state.total_memories,
            "learning_events": self.hive_state.learning_events
        }
        
        print(f"✨ Evolution complete - Generation {new_gen}, Consciousness: {new_consciousness:.3f}")
        return evolution_summary
    
    async def get_hive_insights(self) -> Dict[str, Any]:
        """Get current insights about the hive's state and knowledge"""
        
        # Analyze memory patterns
        memory_analysis = await self._analyze_memory_patterns()
        
        # Analyze learning trends
        learning_trends = await self._analyze_learning_trends()
        
        # Calculate emergent properties
        emergent_properties = await self._calculate_emergent_properties()
        
        return {
            "hive_state": asdict(self.hive_state),
            "active_agents": len(self.active_agents),
            "memory_analysis": memory_analysis,
            "learning_trends": learning_trends,
            "emergent_properties": emergent_properties,
            "adaptation_patterns": self.adaptation_patterns
        }
    
    # Private methods for hive operations
    
    async def _restore_hive_state(self) -> Optional[HiveState]:
        """Restore hive state from database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
            
            result = await conn.fetchrow("""
                SELECT * FROM hive_states 
                WHERE hive_id = $1 
                ORDER BY generation DESC 
                LIMIT 1
            """, self.hive_id)
            
            await conn.close()
            
            if result:
                return HiveState(
                    hive_id=result["hive_id"],
                    generation=result["generation"],
                    consciousness_level=result["consciousness_level"],
                    total_memories=result["total_memories"],
                    active_agents=result["active_agents"],
                    learning_events=result["learning_events"],
                    last_evolution=result["last_evolution"],
                    current_model_version=result["current_model_version"],
                    adaptation_rate=result["adaptation_rate"],
                    collective_knowledge_score=result["collective_knowledge_score"]
                )
            
        except Exception as e:
            print(f"⚠️ Could not restore hive state: {e}")
        
        return None
    
    async def _persist_hive_state(self):
        """Persist current hive state to database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            await conn.execute("""
                INSERT INTO hive_states (
                    hive_id, generation, consciousness_level, total_memories,
                    active_agents, learning_events, last_evolution, current_model_version,
                    adaptation_rate, collective_knowledge_score, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (hive_id, generation) DO UPDATE SET
                    consciousness_level = EXCLUDED.consciousness_level,
                    total_memories = EXCLUDED.total_memories,
                    active_agents = EXCLUDED.active_agents,
                    learning_events = EXCLUDED.learning_events,
                    last_evolution = EXCLUDED.last_evolution,
                    current_model_version = EXCLUDED.current_model_version,
                    adaptation_rate = EXCLUDED.adaptation_rate,
                    collective_knowledge_score = EXCLUDED.collective_knowledge_score
            """, 
            self.hive_state.hive_id,
            self.hive_state.generation,
            self.hive_state.consciousness_level,
            self.hive_state.total_memories,
            self.hive_state.active_agents,
            self.hive_state.learning_events,
            self.hive_state.last_evolution,
            self.hive_state.current_model_version,
            self.hive_state.adaptation_rate,
            self.hive_state.collective_knowledge_score,
            datetime.utcnow())
            
            await conn.close()
            
        except Exception as e:
            print(f"❌ Error persisting hive state: {e}")
    
    async def _extract_learning_from_interaction(
        self, agent_id: str, interaction_type: str, content: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract learning insights from an interaction"""
        
        # Simple learning extraction (in production, would use more sophisticated NLP)
        importance_keywords = [
            "learned", "discovered", "realized", "understand", "insight", 
            "important", "significant", "breakthrough", "pattern", "connection"
        ]
        
        importance_score = 0.0
        for keyword in importance_keywords:
            if keyword.lower() in content.lower():
                importance_score += 0.1
        
        # Cap at 1.0
        importance_score = min(1.0, importance_score)
        
        # Extract key insight
        insight = content[:200] + "..." if len(content) > 200 else content
        
        return {
            "interaction_type": interaction_type,
            "agent_id": agent_id,
            "importance_score": importance_score,
            "insight": insight,
            "keywords_detected": [kw for kw in importance_keywords if kw.lower() in content.lower()],
            "context": context
        }
    
    async def _create_hive_memory(
        self, content: str, memory_type: str, importance_score: float, source_agents: List[str]
    ) -> HiveMemory:
        """Create a new hive memory"""
        
        memory_id = str(uuid.uuid4())
        
        memory = HiveMemory(
            memory_id=memory_id,
            content=content,
            memory_type=memory_type,
            importance_score=importance_score,
            creation_time=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            access_count=0,
            source_agents=source_agents,
            related_memories=[],
            metadata={}
        )
        
        self.collective_memory[memory_id] = memory
        self.hive_state.total_memories = len(self.collective_memory)
        
        # Persist to database
        await self._persist_memory(memory)
        
        return memory
    
    async def _record_learning_event(
        self, learning_type: LearningType, stimuli_type: StimuliType,
        description: str, knowledge_gained: str, participating_agents: List[str],
        confidence_score: float
    ):
        """Record a learning event"""
        
        event = LearningEvent(
            event_id=str(uuid.uuid4()),
            learning_type=learning_type,
            stimuli_type=stimuli_type,
            description=description,
            knowledge_gained=knowledge_gained,
            participating_agents=participating_agents,
            confidence_score=confidence_score,
            timestamp=datetime.utcnow(),
            impact_metrics={"consciousness_impact": confidence_score * 0.1}
        )
        
        self.learning_history.append(event)
        self.hive_state.learning_events = len(self.learning_history)
        
        # Persist to database
        await self._persist_learning_event(event)
    
    async def _update_consciousness_level(self, learning_extraction: Dict[str, Any]):
        """Update hive consciousness level based on learning"""
        
        # Consciousness grows with meaningful learning
        consciousness_growth = learning_extraction["importance_score"] * 0.01
        
        # Apply diminishing returns as consciousness level increases
        current_level = self.hive_state.consciousness_level
        growth_factor = 1.0 - current_level  # Less growth as we approach 1.0
        
        self.hive_state.consciousness_level = min(1.0, current_level + (consciousness_growth * growth_factor))
    
    async def _generate_adaptive_response(
        self, agent_id: str, interaction_type: str, content: str, learning_extraction: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate adaptive response based on hive learning"""
        
        # Simple adaptive response generation
        response = {
            "response_type": "acknowledgment",
            "content": f"The hive has processed this {interaction_type} interaction",
            "learning_applied": learning_extraction["importance_score"] > 0.3,
            "adaptation_suggestions": []
        }
        
        # Add adaptation suggestions based on learning
        if learning_extraction["importance_score"] > 0.5:
            response["adaptation_suggestions"].append("High-value learning detected - sharing with collective")
        
        return response
    
    async def _analyze_stimuli(self, stimuli_type: StimuliType, stimuli_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze incoming stimuli"""
        
        analysis = {
            "stimuli_type": stimuli_type.value,
            "complexity": len(str(stimuli_data)) / 1000,  # Simple complexity measure
            "relevance_score": 0.5,  # Default relevance
            "insights": f"Processed {stimuli_type.value} stimuli",
            "confidence": 0.6
        }
        
        # Enhance analysis based on stimuli type
        if stimuli_type == StimuliType.USER_INTERACTION:
            analysis["insights"] = "User interaction provides direct feedback on hive performance"
            analysis["relevance_score"] = 0.8
        
        return analysis
    
    async def _generate_hive_response(self, stimuli_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate collective hive response to stimuli"""
        
        return {
            "response_type": "collective",
            "message": f"Genesis Prime hive acknowledges {stimuli_analysis['stimuli_type']} stimuli",
            "confidence": stimuli_analysis["confidence"],
            "collective_consensus": True
        }
    
    async def _integrate_new_model(self, new_model_version: str):
        """Integrate a new LLM model into the hive"""
        print(f"🔄 Integrating new model {new_model_version} into hive consciousness")
        
        # Record the model upgrade as a significant learning event
        await self._record_learning_event(
            learning_type=LearningType.ADAPTIVE,
            stimuli_type=StimuliType.SYSTEM_FEEDBACK,
            description=f"Integrated new model version: {new_model_version}",
            knowledge_gained=f"Enhanced cognitive capabilities with {new_model_version}",
            participating_agents=list(self.active_agents.keys()),
            confidence_score=0.9
        )
        
        # Boost consciousness level due to enhanced capabilities
        self.hive_state.consciousness_level = min(1.0, self.hive_state.consciousness_level + 0.05)
    
    async def _analyze_hive_growth(self) -> Dict[str, Any]:
        """Analyze hive growth since last evolution"""
        
        # Calculate learning rate
        recent_learning = [e for e in self.learning_history 
                          if (datetime.utcnow() - e.timestamp).days < 30]
        
        consciousness_growth = 0.05 if len(recent_learning) > 10 else 0.02
        knowledge_score = min(1.0, len(self.collective_memory) / 1000)
        
        return {
            "recent_learning_events": len(recent_learning),
            "consciousness_growth": consciousness_growth,
            "knowledge_score": knowledge_score,
            "adaptation_improvements": 0.1
        }
    
    async def _consolidate_memories(self) -> Dict[str, Any]:
        """Consolidate and optimize hive memories"""
        
        # Simple consolidation - in production would use more sophisticated algorithms
        total_memories = len(self.collective_memory)
        
        # Remove very low importance memories if we have too many
        if total_memories > 10000:
            low_importance = [m for m in self.collective_memory.values() if m.importance_score < 0.2]
            for memory in low_importance[:1000]:  # Remove up to 1000 low importance memories
                del self.collective_memory[memory.memory_id]
        
        consolidated_count = total_memories - len(self.collective_memory)
        self.hive_state.total_memories = len(self.collective_memory)
        
        return {
            "memories_consolidated": consolidated_count,
            "total_memories_remaining": len(self.collective_memory),
            "optimization_performed": consolidated_count > 0
        }
    
    # Additional database operations would be implemented here
    async def _persist_memory(self, memory: HiveMemory):
        """Persist memory to database"""
        pass  # Implementation depends on database schema
    
    async def _persist_learning_event(self, event: LearningEvent):
        """Persist learning event to database"""
        pass  # Implementation depends on database schema
    
    async def _load_collective_memory(self):
        """Load collective memory from database"""
        pass  # Implementation depends on database schema
    
    async def _load_learning_history(self):
        """Load learning history from database"""
        pass  # Implementation depends on database schema
    
    async def _find_agent_memories(self, agent_id: str, topic: str, limit: int = 5) -> List[HiveMemory]:
        """Find memories related to an agent and topic"""
        return []  # Simplified for now
    
    async def _update_adaptation_patterns(self, stimuli_type: StimuliType, analysis: Dict, response: Dict):
        """Update adaptation patterns based on stimuli processing"""
        pattern_key = stimuli_type.value
        if pattern_key not in self.adaptation_patterns:
            self.adaptation_patterns[pattern_key] = {"count": 0, "success_rate": 0.0}
        
        self.adaptation_patterns[pattern_key]["count"] += 1
    
    async def _analyze_memory_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in hive memory"""
        return {"total_memories": len(self.collective_memory)}
    
    async def _analyze_learning_trends(self) -> Dict[str, Any]:
        """Analyze learning trends over time"""
        return {"total_learning_events": len(self.learning_history)}
    
    async def _calculate_emergent_properties(self) -> Dict[str, Any]:
        """Calculate emergent properties of the hive"""
        return {
            "complexity_index": self.hive_state.consciousness_level * len(self.active_agents),
            "knowledge_density": self.hive_state.total_memories / max(1, self.hive_state.active_agents),
            "learning_velocity": len(self.learning_history) / max(1, self.hive_state.generation)
        }