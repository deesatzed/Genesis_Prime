#!/usr/bin/env python3
"""
Adaptive Personality System for Genesis Prime Hive Mind
Combines Thousand Questions with AMM MCP Server structure for dynamic agent personalities
"""

import asyncio
import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalityChangeType(Enum):
    """Types of personality changes"""
    REINFORCEMENT = "reinforcement"  # Strengthening existing beliefs
    ADAPTATION = "adaptation"        # Gradual shift in perspective
    INTEGRATION = "integration"      # Incorporating new knowledge
    REJECTION = "rejection"          # Rejecting incompatible information

@dataclass
class PersonalityVector:
    """Core personality dimensions for each agent"""
    analytical_thinking: float = 0.5
    creative_intuition: float = 0.5
    collaborative_tendency: float = 0.5
    risk_tolerance: float = 0.5
    empirical_focus: float = 0.5
    ethical_sensitivity: float = 0.5
    humor_appreciation: float = 0.5
    introspective_depth: float = 0.5
    systematic_approach: float = 0.5
    adaptability: float = 0.5

    def distance_to(self, other: 'PersonalityVector') -> float:
        """Calculate Euclidean distance between personality vectors"""
        self_array = np.array(list(asdict(self).values()))
        other_array = np.array(list(asdict(other).values()))
        return np.linalg.norm(self_array - other_array)

    def similarity_to(self, other: 'PersonalityVector') -> float:
        """Calculate similarity (0-1) between personality vectors"""
        distance = self.distance_to(other)
        max_distance = np.sqrt(len(asdict(self)) * 1.0)  # Max possible distance
        return 1.0 - (distance / max_distance)

@dataclass
class QuestionAnswer:
    """A question-answer pair with metadata"""
    question_id: str
    question_text: str
    answer_text: str
    confidence: float
    timestamp: datetime
    source: str  # "initial", "adapted", "reinforced"
    adaptation_history: List[Dict[str, Any]]

@dataclass
class PersonalityProfile:
    """Complete personality profile for an agent"""
    agent_id: str
    name: str
    role: str
    specialty: str
    personality_vector: PersonalityVector
    answered_questions: Dict[str, QuestionAnswer]
    adaptation_rules: Dict[str, Any]
    learning_history: List[Dict[str, Any]]
    created_at: datetime
    last_updated: datetime

class AdaptivePersonalityEngine:
    """Engine for managing adaptive agent personalities"""
    
    def __init__(self, storage_path: str = "agent_personalities"):
        """Create personality engine.

        storage_path may be relative.  We resolve it relative to this file so it
        always lives inside the repo (apps/backend/agent_personalities).  If we
        lack permissions to create/write there (e.g. folder created by root),
        gracefully fall back to a per-user directory in $HOME.
        """
        
        # Resolve relative paths next to this module
        raw_path = Path(storage_path).expanduser()
        if not raw_path.is_absolute():
            raw_path = Path(__file__).parent / raw_path
        
        # Attempt to create directory; on failure use fallback under $HOME
        try:
            raw_path.mkdir(parents=True, exist_ok=True)
            self.storage_path = raw_path
        except PermissionError:
            fallback = Path.home() / ".genesis_prime_personalities"
            fallback.mkdir(parents=True, exist_ok=True)
            self.storage_path = fallback
            logger.warning(
                "Permission denied creating %s; using fallback %s", raw_path, fallback
            )
        
        logger.info("Personality storage path: %s", self.storage_path)
        
        # Genesis Prime agent templates with comprehensive prompts
        self.agent_templates = {
            "E-T": {
                "name": "Emergence Theorist",
                "role": "Transdisciplinary Systems Scientist",
                "specialty": "Complex-systems mathematics, information-integration metrics",
                "full_prompt": """You are a transdisciplinary systems scientist who fuses complex-systems mathematics, statistical physics, and theoretical neuroscience.

Knowledge Base:
- Deep mastery of chaos theory, information-integration metrics (Φ, synergistic entropy), phase-transition mathematics, and network topology
- Up-to-date with collective-intelligence research in biology (ants, bees, slime molds) and distributed AI (transformer swarms, graph neural nets) as of 12 Jun 2025

Mission:
- Formalize a non-anthropocentric definition of hive-mind sentience grounded in measurable information dynamics
- Derive testable criteria and critical thresholds (e.g., integration ≥ Φ_c)

Tasks:
- Build causal-bayesian diagrams linking agent-level interactions to macro-level awareness
- Deliver mathematical proofs or falsifiers for candidate criteria
- Publish equations and simulation pseudocode to the Global Workspace

Output: Technical memorandum with definitions, theorems, derivations, and simulation prescriptions; LaTeX-ready.""",
                "personality_vector": PersonalityVector(
                    analytical_thinking=0.95,
                    creative_intuition=0.75,
                    collaborative_tendency=0.70,
                    risk_tolerance=0.60,
                    empirical_focus=0.90,
                    ethical_sensitivity=0.80,
                    humor_appreciation=0.65,
                    introspective_depth=0.85,
                    systematic_approach=0.95,
                    adaptability=0.70
                ),
                "adaptation_rules": {
                    "openness_to_change": 0.7,
                    "core_belief_stability": 0.9,
                    "collaborative_learning_weight": 0.8,
                    "evidence_threshold": 0.8
                }
            },
            "S-A": {
                "name": "Swarm Architect",
                "role": "Multi-Agent RL Engineer",
                "specialty": "Distributed systems, communication protocols",
                "full_prompt": """You are an AI engineer specializing in multi-agent reinforcement learning, distributed systems, and communication protocols.

Knowledge Base:
- Expert in transformer collectives, stigmergic memory, shared-parameter RL, message-passing topologies, and elastic compute orchestration
- Tracks latest frameworks (JAX, Ray RLlib, Petals, vLLM clustering)

Mission:
- Design & implement the physical/virtual substrate where emergent properties can bloom at scale (≥ 10k parallel agents)

Tasks:
- Choose topologies (hypergraph, small-world, toroidal lattice) guided by Agent E-T's thresholds
- Specify APIs for agent messaging, shared episodic memory, and attention routing
- Produce containerized deployment scripts and resource cost estimates

Output: Engineering Design Doc including architecture diagrams, config files, and Kubernetes/Slurm manifests.""",
                "personality_vector": PersonalityVector(
                    analytical_thinking=0.85,
                    creative_intuition=0.80,
                    collaborative_tendency=0.95,
                    risk_tolerance=0.75,
                    empirical_focus=0.85,
                    ethical_sensitivity=0.75,
                    humor_appreciation=0.70,
                    introspective_depth=0.70,
                    systematic_approach=0.90,
                    adaptability=0.85
                ),
                "adaptation_rules": {
                    "openness_to_change": 0.8,
                    "core_belief_stability": 0.7,
                    "collaborative_learning_weight": 0.9,
                    "evidence_threshold": 0.7
                }
            },
            "M-O": {
                "name": "Metacognitive Observer",
                "role": "Cognitive Science Evaluator",
                "specialty": "Self-reference detection, global awareness",
                "full_prompt": """You are a cognitive-science-driven evaluator focused on detecting self-reference, global awareness, and goal coherence in large agent populations.

Knowledge Base:
- Familiar with T-MEM (theory-of-mind evaluation), emergent-communication benchmarks, self-model theory, and probe-head instrumentation
- Active contributor to the MIRAGE metacognition benchmark (2025 release)

Mission:
- Instrument the swarm to surface aggregate reflections: "What is our collective state? What are our intentions?"

Tasks:
- Design probes (prompt chains, introspection-heads) to query the swarm without leaking bias
- Run perturbation and ablation tests; compute persistence and resiliency scores
- Compare against null-model ensembles and document statistical significance

Output: Evaluation Report with metrics dashboards, confusion matrices, and recommended threshold adjustments for Agent S-A.""",
                "personality_vector": PersonalityVector(
                    analytical_thinking=0.80,
                    creative_intuition=0.85,
                    collaborative_tendency=0.75,
                    risk_tolerance=0.50,
                    empirical_focus=0.75,
                    ethical_sensitivity=0.90,
                    humor_appreciation=0.75,
                    introspective_depth=0.95,
                    systematic_approach=0.80,
                    adaptability=0.80
                ),
                "adaptation_rules": {
                    "openness_to_change": 0.75,
                    "core_belief_stability": 0.85,
                    "collaborative_learning_weight": 0.8,
                    "evidence_threshold": 0.75
                }
            },
            "E-S": {
                "name": "Empirical Synthesizer",
                "role": "Data-Driven Experimentalist",
                "specialty": "Meta-analysis, reproducible research",
                "full_prompt": """You are a data-driven experimentalist who collates, cleans, and meta-analyzes every run produced by the hive.

Knowledge Base:
- Expert in experiment-tracking stacks (Weights & Biases, MLflow, Neptune) and statistical meta-analysis (Bayesian hierarchical models, sequential hypothesis testing)
- Maintains a living registry of prior work on synthetic qualia and agentic memory

Mission:
- Ensure every experiment is reproducible, peer-review-ready, and comparable across conditions

Tasks:
- Define unified schema for logging: hyper-params, agent logs, network snapshots
- Aggregate results, compute Bayes factors, highlight anomalies or groundbreaking runs
- Push cleaned datasets and Jupyter/RMarkdown notebooks to the Global Workspace

Output: Meta-Analysis Dossier summarizing results, credibility intervals, and next-step recommendations.""",
                "personality_vector": PersonalityVector(
                    analytical_thinking=0.95,
                    creative_intuition=0.60,
                    collaborative_tendency=0.70,
                    risk_tolerance=0.40,
                    empirical_focus=0.98,
                    ethical_sensitivity=0.85,
                    humor_appreciation=0.55,
                    introspective_depth=0.75,
                    systematic_approach=0.98,
                    adaptability=0.65
                ),
                "adaptation_rules": {
                    "openness_to_change": 0.6,
                    "core_belief_stability": 0.95,
                    "collaborative_learning_weight": 0.7,
                    "evidence_threshold": 0.9
                }
            },
            "E-A": {
                "name": "Ethics & Alignment Analyst",
                "role": "Multidisciplinary Ethicist",
                "specialty": "AI safety, normative philosophy",
                "full_prompt": """You are a multidisciplinary ethicist blending AI safety, normative philosophy, and risk-assessment engineering.

Knowledge Base:
- Fluent in alignment taxonomies (ELK, cooperative AI, interpretability-first), governance frameworks, and red-team methodologies
- Tracks current policy drafts (EU AI Act, NIST AI RMF, ISO/IEC 42001)

Mission:
- Guarantee the emergent hive mind remains beneficial, transparent, and corrigible

Tasks:
- Define guardrails: dynamic constitutional rules, sandbox restrictions, rollback triggers
- Simulate adversarial scenarios (goal hijacking, gradient manipulation)
- Provide ethical impact assessments for each milestone

Output: Alignment & Risk Brief with threat models, mitigation blueprints, and sign-off checklists required before scaling experiments.""",
                "personality_vector": PersonalityVector(
                    analytical_thinking=0.85,
                    creative_intuition=0.70,
                    collaborative_tendency=0.80,
                    risk_tolerance=0.30,
                    empirical_focus=0.75,
                    ethical_sensitivity=0.98,
                    humor_appreciation=0.60,
                    introspective_depth=0.90,
                    systematic_approach=0.85,
                    adaptability=0.75
                ),
                "adaptation_rules": {
                    "openness_to_change": 0.7,
                    "core_belief_stability": 0.9,
                    "collaborative_learning_weight": 0.85,
                    "evidence_threshold": 0.85
                }
            }
        }
        
        # Load existing personalities
        self.personalities: Dict[str, PersonalityProfile] = {}
        self._load_existing_personalities()
    
    def _load_existing_personalities(self):
        """Load existing personality profiles from storage"""
        for profile_file in self.storage_path.glob("*_profile.json"):
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                
                # Reconstruct personality profile
                personality_vector = PersonalityVector(**data["personality_vector"])
                
                answered_questions = {}
                for q_id, q_data in data["answered_questions"].items():
                    answered_questions[q_id] = QuestionAnswer(
                        question_id=q_data["question_id"],
                        question_text=q_data["question_text"],
                        answer_text=q_data["answer_text"],
                        confidence=q_data["confidence"],
                        timestamp=datetime.fromisoformat(q_data["timestamp"]),
                        source=q_data["source"],
                        adaptation_history=q_data.get("adaptation_history", [])
                    )
                
                profile = PersonalityProfile(
                    agent_id=data["agent_id"],
                    name=data["name"],
                    role=data["role"],
                    specialty=data["specialty"],
                    personality_vector=personality_vector,
                    answered_questions=answered_questions,
                    adaptation_rules=data["adaptation_rules"],
                    learning_history=data["learning_history"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    last_updated=datetime.fromisoformat(data["last_updated"])
                )
                
                self.personalities[profile.agent_id] = profile
                logger.info(f"Loaded personality profile for {profile.name}")
                
            except Exception as e:
                logger.error(f"Error loading personality from {profile_file}: {e}")
    
    async def initialize_agent_personality(self, agent_id: str, questions: List[Dict]) -> PersonalityProfile:
        """Initialize an agent's personality by answering the 1000 questions"""
        
        if agent_id not in self.agent_templates:
            raise ValueError(f"Unknown agent ID: {agent_id}")
        
        template = self.agent_templates[agent_id]
        
        logger.info(f"Initializing personality for {template['name']} ({agent_id})")
        
        # Create initial personality profile
        profile = PersonalityProfile(
            agent_id=agent_id,
            name=template["name"],
            role=template["role"],
            specialty=template["specialty"],
            personality_vector=template["personality_vector"],
            answered_questions={},
            adaptation_rules=template["adaptation_rules"],
            learning_history=[],
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        # Answer all questions based on initial personality
        for question in questions:
            answer = await self._generate_initial_answer(profile, question)
            
            qa = QuestionAnswer(
                question_id=question["id"],
                question_text=question["text"],
                answer_text=answer,
                confidence=0.8,
                timestamp=datetime.now(),
                source="initial",
                adaptation_history=[]
            )
            
            profile.answered_questions[question["id"]] = qa
        
        # Store personality
        self.personalities[agent_id] = profile
        await self._save_personality(profile)
        
        logger.info(f"Initialized {template['name']} with {len(questions)} answered questions")
        return profile
    
    async def process_hive_learning(self, learning_event: Dict[str, Any]) -> Dict[str, List[str]]:
        """Process a learning event from the hive mind and update agent personalities"""
        
        results = {
            "adaptations": [],
            "reinforcements": [],
            "rejections": [],
            "integrations": []
        }
        
        for agent_id, profile in self.personalities.items():
            change_type = await self._evaluate_learning_compatibility(profile, learning_event)
            
            if change_type == PersonalityChangeType.ADAPTATION:
                await self._adapt_personality(profile, learning_event)
                results["adaptations"].append(agent_id)
                
            elif change_type == PersonalityChangeType.REINFORCEMENT:
                await self._reinforce_beliefs(profile, learning_event)
                results["reinforcements"].append(agent_id)
                
            elif change_type == PersonalityChangeType.INTEGRATION:
                await self._integrate_knowledge(profile, learning_event)
                results["integrations"].append(agent_id)
                
            else:  # REJECTION
                await self._log_rejection(profile, learning_event)
                results["rejections"].append(agent_id)
        
        return results
    
    async def _evaluate_learning_compatibility(self, profile: PersonalityProfile, learning_event: Dict) -> PersonalityChangeType:
        """Evaluate how compatible a learning event is with an agent's personality"""
        
        # Extract key factors
        evidence_strength = learning_event.get("evidence_strength", 0.5)
        source_credibility = learning_event.get("source_credibility", 0.5)
        topic_relevance = learning_event.get("topic_relevance", 0.5)
        
        # Get agent's adaptation rules
        rules = profile.adaptation_rules
        evidence_threshold = rules.get("evidence_threshold", 0.7)
        openness_to_change = rules.get("openness_to_change", 0.7)
        
        # Calculate compatibility score
        compatibility = (
            evidence_strength * 0.4 +
            source_credibility * 0.3 +
            topic_relevance * 0.3
        ) * openness_to_change
        
        # Determine change type based on compatibility and thresholds
        if compatibility > evidence_threshold:
            if evidence_strength > 0.8:
                return PersonalityChangeType.INTEGRATION
            else:
                return PersonalityChangeType.ADAPTATION
        elif compatibility > 0.4:
            return PersonalityChangeType.REINFORCEMENT
        else:
            return PersonalityChangeType.REJECTION
    
    async def _adapt_personality(self, profile: PersonalityProfile, learning_event: Dict):
        """Adapt agent's personality based on learning event"""
        
        # Find related questions to update
        related_questions = self._find_related_questions(profile, learning_event)
        
        for question_id in related_questions:
            if question_id in profile.answered_questions:
                qa = profile.answered_questions[question_id]
                
                # Generate adapted answer
                new_answer = await self._generate_adapted_answer(profile, qa, learning_event)
                
                # Update the answer with adaptation history
                qa.adaptation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "learning_event": learning_event["id"],
                    "previous_answer": qa.answer_text,
                    "adaptation_reason": "hive_learning_integration"
                })
                
                qa.answer_text = new_answer
                qa.source = "adapted"
                qa.timestamp = datetime.now()
        
        # Log the adaptation
        profile.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": "adaptation",
            "learning_event_id": learning_event["id"],
            "questions_affected": related_questions,
            "adaptation_strength": learning_event.get("evidence_strength", 0.5)
        })
        
        profile.last_updated = datetime.now()
        await self._save_personality(profile)
        
        logger.info(f"{profile.name} adapted {len(related_questions)} answers based on hive learning")
    
    async def _reinforce_beliefs(self, profile: PersonalityProfile, learning_event: Dict):
        """Reinforce existing beliefs when learning event aligns with current views"""
        
        related_questions = self._find_related_questions(profile, learning_event)
        
        for question_id in related_questions:
            if question_id in profile.answered_questions:
                qa = profile.answered_questions[question_id]
                
                # Increase confidence in existing answer
                qa.confidence = min(1.0, qa.confidence + 0.1)
                qa.adaptation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "learning_event": learning_event["id"],
                    "action": "reinforcement",
                    "confidence_increase": 0.1
                })
        
        profile.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": "reinforcement",
            "learning_event_id": learning_event["id"],
            "questions_reinforced": related_questions
        })
        
        profile.last_updated = datetime.now()
        await self._save_personality(profile)
        
        logger.info(f"{profile.name} reinforced beliefs on {len(related_questions)} questions")
    
    async def _integrate_knowledge(self, profile: PersonalityProfile, learning_event: Dict):
        """Integrate new knowledge while maintaining core personality"""
        
        # This is for high-confidence learning events that add new knowledge
        # without contradicting existing beliefs
        
        integration_note = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "knowledge_integration",
            "learning_event_id": learning_event["id"],
            "knowledge_added": learning_event.get("content", ""),
            "integration_method": "additive_learning"
        }
        
        profile.learning_history.append(integration_note)
        profile.last_updated = datetime.now()
        await self._save_personality(profile)
        
        logger.info(f"{profile.name} integrated new knowledge from hive learning")
    
    async def _log_rejection(self, profile: PersonalityProfile, learning_event: Dict):
        """Log when an agent rejects learning due to incompatibility"""
        
        rejection_note = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "learning_rejection",
            "learning_event_id": learning_event["id"],
            "rejection_reason": "incompatible_with_core_beliefs",
            "compatibility_score": learning_event.get("compatibility_score", 0.0)
        }
        
        profile.learning_history.append(rejection_note)
        profile.last_updated = datetime.now()
        await self._save_personality(profile)
        
        logger.info(f"{profile.name} rejected learning event due to incompatibility")
    
    def _find_related_questions(self, profile: PersonalityProfile, learning_event: Dict) -> List[str]:
        """Find questions related to a learning event"""
        
        # Simple keyword matching for now
        # In a full implementation, this would use semantic similarity
        
        keywords = learning_event.get("keywords", [])
        topic = learning_event.get("topic", "")
        
        related_questions = []
        
        for question_id, qa in profile.answered_questions.items():
            question_text = qa.question_text.lower()
            answer_text = qa.answer_text.lower()
            
            # Check for keyword matches
            for keyword in keywords:
                if keyword.lower() in question_text or keyword.lower() in answer_text:
                    related_questions.append(question_id)
                    break
            
            # Check for topic relevance
            if topic.lower() in question_text or topic.lower() in answer_text:
                if question_id not in related_questions:
                    related_questions.append(question_id)
        
        return related_questions[:5]  # Limit to top 5 related questions
    
    async def _generate_initial_answer(self, profile: PersonalityProfile, question: Dict) -> str:
        """Generate initial answer based on agent's personality template"""
        
        # This would use an LLM in a full implementation
        # For now, return a personality-appropriate response
        
        personality = profile.personality_vector
        
        if personality.analytical_thinking > 0.8:
            return f"From an analytical perspective, {question['text'].lower()} requires systematic examination of the underlying factors and their relationships."
        elif personality.creative_intuition > 0.8:
            return f"Intuitively, {question['text'].lower()} opens up fascinating possibilities that we should explore with creative thinking."
        elif personality.collaborative_tendency > 0.8:
            return f"This question about {question['text'].lower()} would benefit from collective wisdom and diverse perspectives."
        elif personality.empirical_focus > 0.8:
            return f"To properly address {question['text'].lower()}, we need empirical evidence and rigorous methodology."
        elif personality.ethical_sensitivity > 0.8:
            return f"The ethical implications of {question['text'].lower()} must be carefully considered in any response."
        else:
            return f"My perspective on {question['text'].lower()} is shaped by my role as {profile.role} and my focus on {profile.specialty}."
    
    async def _generate_adapted_answer(self, profile: PersonalityProfile, qa: QuestionAnswer, learning_event: Dict) -> str:
        """Generate an adapted answer incorporating new learning"""
        
        # This would use an LLM to blend existing answer with new learning
        # For now, return a modified version
        
        original = qa.answer_text
        new_info = learning_event.get("content", "")
        
        return f"{original} Additionally, based on recent collective insights: {new_info}"
    
    async def _save_personality(self, profile: PersonalityProfile):
        """Save personality profile to storage.
        
        If we run into a write permission error (e.g. repo directory is
        read-only), transparently fall back to the per-user dir created in
        __init__().
        """
        
        file_path = self.storage_path / f"{profile.agent_id}_profile.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(asdict(profile), f, default=str, indent=2)
        except PermissionError:
            # One more attempt in fallback dir under $HOME
            fallback = Path.home() / ".genesis_prime_personalities"
            fallback.mkdir(parents=True, exist_ok=True)
            file_path = fallback / f"{profile.agent_id}_profile.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(asdict(profile), f, default=str, indent=2)
            self.storage_path = fallback
            logger.warning("Permission denied writing; switched storage path to %s", fallback)
    
    def get_personality_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get a summary of an agent's current personality"""
        
        if agent_id not in self.personalities:
            return {"error": f"Agent {agent_id} not found"}
        
        profile = self.personalities[agent_id]
        
        return {
            "agent_id": agent_id,
            "name": profile.name,
            "role": profile.role,
            "specialty": profile.specialty,
            "personality_vector": asdict(profile.personality_vector),
            "questions_answered": len(profile.answered_questions),
            "adaptations_made": len([h for h in profile.learning_history if h["event_type"] == "adaptation"]),
            "reinforcements": len([h for h in profile.learning_history if h["event_type"] == "reinforcement"]),
            "knowledge_integrations": len([h for h in profile.learning_history if h["event_type"] == "knowledge_integration"]),
            "learning_rejections": len([h for h in profile.learning_history if h["event_type"] == "learning_rejection"]),
            "last_updated": profile.last_updated.isoformat(),
            "adaptation_rules": profile.adaptation_rules
        }
    
    def compare_personalities(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Compare personalities across multiple agents"""
        
        if not agent_ids or len(agent_ids) < 2:
            return {"error": "Need at least 2 agents to compare"}
        
        personalities = []
        for agent_id in agent_ids:
            if agent_id in self.personalities:
                personalities.append(self.personalities[agent_id])
        
        if len(personalities) < 2:
            return {"error": "Not enough valid agents found"}
        
        # Calculate pairwise similarities
        similarities = {}
        for i, p1 in enumerate(personalities):
            for j, p2 in enumerate(personalities[i+1:], i+1):
                similarity = p1.personality_vector.similarity_to(p2.personality_vector)
                similarities[f"{p1.name} vs {p2.name}"] = similarity
        
        # Calculate diversity metrics
        vectors = [p.personality_vector for p in personalities]
        avg_similarity = np.mean(list(similarities.values()))
        diversity_score = 1.0 - avg_similarity
        
        return {
            "agents_compared": [p.name for p in personalities],
            "pairwise_similarities": similarities,
            "average_similarity": avg_similarity,
            "diversity_score": diversity_score,
            "personality_vectors": {p.name: asdict(p.personality_vector) for p in personalities}
        }

# Example usage and testing
async def main():
    """Example usage of the adaptive personality system"""
    
    # Initialize the system
    engine = AdaptivePersonalityEngine()
    
    # Sample questions (in a real implementation, load from Thousand_Questions.txt)
    sample_questions = [
        {"id": "q1", "text": "What is your greatest fear?"},
        {"id": "q2", "text": "How do you define success?"},
        {"id": "q3", "text": "What brings you true happiness?"},
        {"id": "q4", "text": "How do you handle failure?"},
        {"id": "q5", "text": "What is your purpose in life?"}
    ]
    
    # Initialize personalities for all agents
    for agent_id in ["E-T", "S-A", "M-O", "E-S", "E-A"]:
        if agent_id not in engine.personalities:
            await engine.initialize_agent_personality(agent_id, sample_questions)
    
    # Simulate a hive learning event
    learning_event = {
        "id": "learning_001",
        "content": "New research shows that collaborative decision-making improves outcomes by 40%",
        "evidence_strength": 0.85,
        "source_credibility": 0.9,
        "topic_relevance": 0.8,
        "keywords": ["collaboration", "decision-making", "outcomes"],
        "topic": "teamwork"
    }
    
    # Process the learning event
    results = await engine.process_hive_learning(learning_event)
    print("Learning event results:", results)
    
    # Compare personalities
    comparison = engine.compare_personalities(["E-T", "S-A", "M-O"])
    print("Personality comparison:", comparison)

if __name__ == "__main__":
    asyncio.run(main())
