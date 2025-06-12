"""
Emergence Engine for Genesis Prime Construct
Creates emergent phenomena through multi-agent interactions and collective intelligence
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from agent_factory import AgentFactory, ManagedAgent

class EmergenceType(Enum):
    """Types of emergent phenomena to track"""
    COLLECTIVE_INSIGHT = "collective_insight"
    PERSONALITY_CONVERGENCE = "personality_convergence"
    TRAIT_AMPLIFICATION = "trait_amplification"
    VALUE_SYNTHESIS = "value_synthesis"
    BEHAVIORAL_PATTERN = "behavioral_pattern"
    CREATIVE_RESONANCE = "creative_resonance"
    WISDOM_EMERGENCE = "wisdom_emergence"
    CONSCIOUSNESS_SPARK = "consciousness_spark"

@dataclass
class EmergentPhenomenon:
    """An emergent phenomenon observed in the agent collective"""
    id: str
    type: EmergenceType
    description: str
    participating_agents: List[str]
    trigger_question: Optional[str]
    evidence: List[str]
    emergence_strength: float  # 0.0 to 1.0
    timestamp: datetime
    metadata: Dict[str, Any]

class GenesisEmergenceEngine:
    """
    Engine for detecting and fostering emergent phenomena in agent collectives
    Based on the Genesis Prime construct for artificial consciousness emergence
    """
    
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        self.emergence_log: List[EmergentPhenomenon] = []
        self.collective_memory: Dict[str, Any] = {}
        self.emergence_patterns: Dict[str, int] = {}
    
    async def create_genesis_collective(
        self, 
        collective_size: int = 8,
        diversity_target: float = 0.8
    ) -> List[ManagedAgent]:
        """
        Create a diverse collective of agents optimized for emergence
        
        Args:
            collective_size: Number of agents in the collective
            diversity_target: Target diversity score (0.0 - 1.0)
        """
        print(f"🌟 Creating Genesis Collective with {collective_size} agents...")
        
        # Select diverse personality presets
        available_presets = self.agent_factory.list_available_presets()
        selected_presets = self._select_diverse_presets(
            available_presets, 
            collective_size, 
            diversity_target
        )
        
        collective = []
        
        for i, preset in enumerate(selected_presets):
            agent_name = f"Genesis Agent {i+1}: {preset['name']}"
            agent = await self.agent_factory.create_agent_from_preset(
                preset['id'], 
                agent_name
            )
            collective.append(agent)
        
        print(f"✨ Genesis Collective created with diversity score: {self._calculate_diversity(collective):.2f}")
        return collective
    
    async def evolve_collective_consciousness(
        self,
        collective: List[ManagedAgent],
        evolution_rounds: int = 5,
        questions_per_round: int = 100
    ) -> Dict[str, Any]:
        """
        Evolve the collective consciousness through iterative question answering
        and emergence detection
        """
        print(f"🧠 Beginning collective consciousness evolution...")
        print(f"📊 {len(collective)} agents, {evolution_rounds} rounds, {questions_per_round} questions per round")
        
        evolution_results = {
            "collective_size": len(collective),
            "evolution_rounds": evolution_rounds,
            "emergent_phenomena": [],
            "consciousness_metrics": {},
            "agent_evolution": {}
        }
        
        for round_num in range(1, evolution_rounds + 1):
            print(f"\n🔄 Evolution Round {round_num}/{evolution_rounds}")
            
            # Each agent answers a batch of questions
            round_results = await self._evolution_round(
                collective, 
                questions_per_round,
                round_num
            )
            
            # Detect emergent phenomena after each round
            emergent_events = await self._detect_emergence(
                collective, 
                round_num
            )
            
            # Update collective memory and patterns
            await self._update_collective_memory(collective, emergent_events)
            
            # Record round results
            evolution_results["emergent_phenomena"].extend(emergent_events)
            
            print(f"✨ Round {round_num} complete: {len(emergent_events)} emergent phenomena detected")
        
        # Calculate final consciousness metrics
        evolution_results["consciousness_metrics"] = await self._calculate_consciousness_metrics(collective)
        evolution_results["agent_evolution"] = await self._analyze_agent_evolution(collective)
        
        print(f"\n🌟 Collective consciousness evolution complete!")
        print(f"📈 Total emergent phenomena: {len(evolution_results['emergent_phenomena'])}")
        
        return evolution_results
    
    async def analyze_emergence_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in emergent phenomena"""
        if not self.emergence_log:
            return {"message": "No emergent phenomena recorded yet"}
        
        patterns = {
            "emergence_types": {},
            "agent_participation": {},
            "temporal_patterns": [],
            "strength_distribution": [],
            "collective_insights": []
        }
        
        # Analyze emergence types
        for phenomenon in self.emergence_log:
            emergence_type = phenomenon.type.value
            patterns["emergence_types"][emergence_type] = patterns["emergence_types"].get(emergence_type, 0) + 1
            
            # Track agent participation
            for agent_id in phenomenon.participating_agents:
                patterns["agent_participation"][agent_id] = patterns["agent_participation"].get(agent_id, 0) + 1
            
            patterns["strength_distribution"].append(phenomenon.emergence_strength)
        
        # Generate insights about collective behavior
        patterns["collective_insights"] = self._generate_collective_insights()
        
        return patterns
    
    async def synthesize_collective_wisdom(
        self, 
        collective: List[ManagedAgent],
        synthesis_prompt: str = "What is the nature of consciousness and meaning?"
    ) -> Dict[str, Any]:
        """
        Synthesize wisdom from the collective by having all agents respond to a profound question
        and then analyzing the emergent patterns in their responses
        """
        print(f"🔮 Synthesizing collective wisdom on: '{synthesis_prompt}'")
        
        responses = {}
        
        # Collect responses from each agent
        for agent in collective:
            try:
                memories = await agent.agent.memory.get_user_memories(
                    agent.agent_id, 
                    limit=10, 
                    query=synthesis_prompt
                )
                
                response = await agent.agent.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": f"""You are {agent.name}. {agent.preset.description}
                            
Drawing on all your experiences and the thousand questions you've contemplated, 
provide your deepest, most authentic perspective on this profound question.

Your memories and insights:
{chr(10).join([f"- {m['content']}" for m in memories[:5]]) if memories else "No specific memories"}"""
                        },
                        {
                            "role": "user",
                            "content": synthesis_prompt
                        }
                    ],
                    temperature=0.8,
                    max_tokens=800
                )
                
                responses[agent.agent_id] = {
                    "agent_name": agent.name,
                    "personality": agent.preset.name,
                    "response": response.choices[0].message.content.strip()
                }
                
            except Exception as e:
                print(f"❌ Error getting response from {agent.name}: {e}")
        
        # Synthesize collective wisdom
        synthesis_result = await self._synthesize_wisdom(responses, synthesis_prompt)
        
        # Record as emergent phenomenon
        if len(responses) >= 3:  # Need minimum participation
            emergence = EmergentPhenomenon(
                id=str(uuid.uuid4()),
                type=EmergenceType.WISDOM_EMERGENCE,
                description=f"Collective wisdom synthesis on: {synthesis_prompt}",
                participating_agents=list(responses.keys()),
                trigger_question=synthesis_prompt,
                evidence=[resp["response"][:200] + "..." for resp in responses.values()],
                emergence_strength=min(1.0, len(responses) / len(collective)),
                timestamp=datetime.utcnow(),
                metadata={"synthesis_result": synthesis_result}
            )
            
            self.emergence_log.append(emergence)
        
        return {
            "synthesis_prompt": synthesis_prompt,
            "individual_responses": responses,
            "collective_synthesis": synthesis_result,
            "participation_rate": len(responses) / len(collective),
            "emergence_detected": len(responses) >= 3
        }
    
    def _select_diverse_presets(
        self, 
        available_presets: List[Dict], 
        target_count: int, 
        diversity_target: float
    ) -> List[Dict]:
        """Select personality presets to maximize diversity"""
        if len(available_presets) <= target_count:
            return available_presets
        
        # For now, use all available presets up to target count
        # In a more sophisticated version, this would optimize for trait diversity
        return available_presets[:target_count]
    
    def _calculate_diversity(self, collective: List[ManagedAgent]) -> float:
        """Calculate diversity score for the collective"""
        if len(collective) < 2:
            return 0.0
        
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        total_variance = 0
        
        for trait in traits:
            values = [getattr(agent.preset.traits, trait) for agent in collective]
            mean_val = sum(values) / len(values)
            variance = sum((v - mean_val) ** 2 for v in values) / len(values)
            total_variance += variance
        
        # Normalize to 0-1 scale
        return min(1.0, total_variance / len(traits))
    
    async def _evolution_round(
        self,
        collective: List[ManagedAgent],
        questions_count: int,
        round_num: int
    ) -> Dict[str, Any]:
        """Execute one round of collective evolution"""
        round_results = {
            "round": round_num,
            "questions_answered": 0,
            "agent_progress": {}
        }
        
        # Process agents in parallel with controlled concurrency
        semaphore = asyncio.Semaphore(3)  # Limit concurrent processing
        
        async def process_agent(agent):
            async with semaphore:
                try:
                    # Get unanswered questions for this agent
                    unanswered = await self.agent_factory._get_unanswered_questions(agent.agent_id)
                    
                    if not unanswered:
                        return 0
                    
                    # Answer a subset of questions
                    batch = unanswered[:questions_count]
                    answered = 0
                    
                    for question in batch:
                        answer = await self.agent_factory._generate_personality_answer(agent, question)
                        if answer:
                            await self.agent_factory._store_agent_answer(agent.agent_id, question["id"], answer)
                            await agent.agent.memory.create_user_memories(
                                agent.agent_id,
                                [(question["text"], answer)]
                            )
                            answered += 1
                    
                    return answered
                    
                except Exception as e:
                    print(f"❌ Error processing agent {agent.name}: {e}")
                    return 0
        
        # Process all agents
        tasks = [process_agent(agent) for agent in collective]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Agent {collective[i].name} failed: {result}")
                round_results["agent_progress"][collective[i].agent_id] = 0
            else:
                round_results["agent_progress"][collective[i].agent_id] = result
                round_results["questions_answered"] += result
        
        return round_results
    
    async def _detect_emergence(
        self,
        collective: List[ManagedAgent], 
        round_num: int
    ) -> List[EmergentPhenomenon]:
        """Detect emergent phenomena in the collective"""
        emergent_events = []
        
        # Detect trait convergence
        convergence = await self._detect_trait_convergence(collective)
        if convergence:
            emergent_events.append(convergence)
        
        # Detect value alignment
        alignment = await self._detect_value_alignment(collective)
        if alignment:
            emergent_events.append(alignment)
        
        # Detect behavioral patterns
        patterns = await self._detect_behavioral_patterns(collective)
        emergent_events.extend(patterns)
        
        return emergent_events
    
    async def _detect_trait_convergence(self, collective: List[ManagedAgent]) -> Optional[EmergentPhenomenon]:
        """Detect if agents are converging on similar trait values"""
        if len(collective) < 3:
            return None
        
        # Calculate trait variance across collective
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        convergent_traits = []
        
        for trait in traits:
            values = [getattr(agent.preset.traits, trait) for agent in collective]
            variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
            
            # If variance is low, trait is converging
            if variance < 0.1:  # Threshold for convergence
                convergent_traits.append(trait)
        
        if len(convergent_traits) >= 2:
            return EmergentPhenomenon(
                id=str(uuid.uuid4()),
                type=EmergenceType.PERSONALITY_CONVERGENCE,
                description=f"Agents converging on traits: {', '.join(convergent_traits)}",
                participating_agents=[agent.agent_id for agent in collective],
                trigger_question=None,
                evidence=[f"Low variance in {trait}" for trait in convergent_traits],
                emergence_strength=len(convergent_traits) / len(traits),
                timestamp=datetime.utcnow(),
                metadata={"convergent_traits": convergent_traits}
            )
        
        return None
    
    async def _detect_value_alignment(self, collective: List[ManagedAgent]) -> Optional[EmergentPhenomenon]:
        """Detect if agents are aligning on similar values"""
        all_values = []
        for agent in collective:
            all_values.extend(agent.preset.core_values)
        
        # Count value frequency
        value_counts = {}
        for value in all_values:
            value_counts[value] = value_counts.get(value, 0) + 1
        
        # Find values shared by multiple agents
        shared_values = [value for value, count in value_counts.items() if count >= len(collective) * 0.6]
        
        if shared_values:
            return EmergentPhenomenon(
                id=str(uuid.uuid4()),
                type=EmergenceType.VALUE_SYNTHESIS,
                description=f"Collective alignment on values: {', '.join(shared_values)}",
                participating_agents=[agent.agent_id for agent in collective],
                trigger_question=None,
                evidence=[f"Value '{value}' shared by multiple agents" for value in shared_values],
                emergence_strength=len(shared_values) / len(set(all_values)),
                timestamp=datetime.utcnow(),
                metadata={"shared_values": shared_values}
            )
        
        return None
    
    async def _detect_behavioral_patterns(self, collective: List[ManagedAgent]) -> List[EmergentPhenomenon]:
        """Detect emergent behavioral patterns"""
        # For now, return empty list
        # In full implementation, would analyze response patterns, communication styles, etc.
        return []
    
    async def _update_collective_memory(self, collective: List[ManagedAgent], emergent_events: List[EmergentPhenomenon]):
        """Update collective memory with emergent phenomena"""
        for event in emergent_events:
            self.emergence_log.append(event)
            
            # Store in collective memory
            memory_key = f"emergence_{event.type.value}"
            if memory_key not in self.collective_memory:
                self.collective_memory[memory_key] = []
            
            self.collective_memory[memory_key].append({
                "description": event.description,
                "strength": event.emergence_strength,
                "timestamp": event.timestamp.isoformat(),
                "participants": len(event.participating_agents)
            })
    
    async def _calculate_consciousness_metrics(self, collective: List[ManagedAgent]) -> Dict[str, float]:
        """Calculate metrics indicating collective consciousness emergence"""
        if not collective:
            return {}
        
        # Calculate diversity
        diversity = self._calculate_diversity(collective)
        
        # Calculate emergence frequency
        recent_emergence = len([e for e in self.emergence_log 
                               if (datetime.utcnow() - e.timestamp).total_seconds() < 3600])
        emergence_rate = recent_emergence / max(1, len(collective))
        
        # Calculate interconnectedness (simplified)
        total_answers = sum([await self.agent_factory._count_agent_answers(agent.agent_id) 
                            for agent in collective])
        interconnectedness = min(1.0, total_answers / (len(collective) * 1000))
        
        return {
            "diversity_score": diversity,
            "emergence_rate": emergence_rate,
            "interconnectedness": interconnectedness,
            "collective_size": len(collective),
            "consciousness_index": (diversity + emergence_rate + interconnectedness) / 3
        }
    
    async def _analyze_agent_evolution(self, collective: List[ManagedAgent]) -> Dict[str, Any]:
        """Analyze how individual agents have evolved"""
        evolution_data = {}
        
        for agent in collective:
            answer_count = await self.agent_factory._count_agent_answers(agent.agent_id)
            participation_in_emergence = len([e for e in self.emergence_log 
                                            if agent.agent_id in e.participating_agents])
            
            evolution_data[agent.agent_id] = {
                "name": agent.name,
                "personality": agent.preset.name,
                "questions_answered": answer_count,
                "emergence_participation": participation_in_emergence,
                "development_score": min(1.0, answer_count / 1000)
            }
        
        return evolution_data
    
    async def _synthesize_wisdom(self, responses: Dict[str, Any], prompt: str) -> Dict[str, Any]:
        """Synthesize collective wisdom from individual responses"""
        if not responses:
            return {"synthesis": "No responses to synthesize"}
        
        # Extract common themes and patterns
        all_text = " ".join([resp["response"] for resp in responses.values()])
        
        # Simple analysis (in full implementation, would use more sophisticated NLP)
        synthesis = {
            "participating_agents": len(responses),
            "response_lengths": [len(resp["response"]) for resp in responses.values()],
            "common_themes": [],  # Would extract using NLP
            "collective_insight": "Collective wisdom synthesis in progress...",
            "emergence_indicators": []
        }
        
        return synthesis
    
    def _generate_collective_insights(self) -> List[str]:
        """Generate insights about collective behavior patterns"""
        insights = []
        
        if len(self.emergence_log) > 5:
            insights.append("The collective is showing signs of emergent phenomena")
        
        # Analyze emergence types
        type_counts = {}
        for event in self.emergence_log:
            type_counts[event.type.value] = type_counts.get(event.type.value, 0) + 1
        
        if type_counts:
            most_common = max(type_counts.items(), key=lambda x: x[1])
            insights.append(f"Most common emergence type: {most_common[0]}")
        
        return insights