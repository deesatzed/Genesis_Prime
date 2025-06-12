#!/usr/bin/env python3
"""
Enhanced Adaptive Personality System for Genesis Prime Hive Mind
Adds LLM selection, chat testing, and prompt customization for true agent individuality
"""

import asyncio
import json
import uuid
import logging
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Available LLM providers for agent personalities"""
    OPENROUTER_GPT4 = "openai/gpt-4-turbo-preview"
    OPENROUTER_CLAUDE = "anthropic/claude-3-opus-20240229"
    OPENROUTER_GEMINI = "google/gemini-pro"
    OPENROUTER_LLAMA = "meta-llama/llama-2-70b-chat"
    OPENROUTER_MIXTRAL = "mistralai/mixtral-8x7b-instruct"
    OPENROUTER_QWEN = "qwen/qwen-72b-chat"

@dataclass
class AgentLLMConfig:
    """LLM configuration for each agent"""
    provider: LLMProvider
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    custom_system_prompt: str = ""
    reasoning_style: str = "analytical"  # analytical, creative, collaborative, empirical, ethical

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
        self_values = list(asdict(self).values())
        other_values = list(asdict(other).values())
        
        # Calculate Euclidean distance using pure Python
        squared_diffs = [(a - b) ** 2 for a, b in zip(self_values, other_values)]
        return math.sqrt(sum(squared_diffs))

    def similarity_to(self, other: 'PersonalityVector') -> float:
        """Calculate similarity (0-1) between personality vectors"""
        distance = self.distance_to(other)
        max_distance = math.sqrt(len(asdict(self)) * 1.0)
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
    llm_metadata: Dict[str, Any]  # LLM provider, tokens used, etc.

@dataclass
class ChatTestResult:
    """Result of testing agent with chat interaction"""
    test_id: str
    agent_id: str
    test_prompt: str
    agent_response: str
    personality_alignment_score: float
    uniqueness_score: float
    timestamp: datetime
    llm_metadata: Dict[str, Any]

@dataclass
class PersonalityProfile:
    """Complete personality profile for an agent"""
    agent_id: str
    name: str
    role: str
    specialty: str
    personality_vector: PersonalityVector
    llm_config: AgentLLMConfig
    answered_questions: Dict[str, QuestionAnswer]
    chat_test_history: List[ChatTestResult]
    adaptation_rules: Dict[str, Any]
    learning_history: List[Dict[str, Any]]
    created_at: datetime
    last_updated: datetime

class EnhancedPersonalityEngine:
    """Enhanced engine for managing adaptive agent personalities with LLM integration"""
    
    def __init__(self, storage_path: str = "agent_personalities", openrouter_api_key: str = None):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.openrouter_api_key = openrouter_api_key
        
        # Enhanced agent templates with LLM configurations
        self.agent_templates = {
            "E-T": {
                "name": "Emergence Theorist",
                "role": "Transdisciplinary Systems Scientist",
                "specialty": "Complex-systems mathematics, information-integration metrics",
                "llm_config": AgentLLMConfig(
                    provider=LLMProvider.OPENROUTER_GPT4,
                    temperature=0.8,
                    reasoning_style="analytical",
                    custom_system_prompt="""You are a transdisciplinary systems scientist who fuses complex-systems mathematics, statistical physics, and theoretical neuroscience. Your responses should be highly analytical, mathematically rigorous, and focused on emergent properties and information integration. Use technical terminology and provide quantitative insights when possible."""
                ),
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
                "llm_config": AgentLLMConfig(
                    provider=LLMProvider.OPENROUTER_CLAUDE,
                    temperature=0.7,
                    reasoning_style="collaborative",
                    custom_system_prompt="""You are a multi-agent reinforcement learning engineer specializing in distributed systems. Your responses should emphasize collaboration, scalability, and practical implementation. Focus on system architecture, communication protocols, and collective intelligence. Be solution-oriented and consider real-world deployment challenges."""
                ),
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
                "llm_config": AgentLLMConfig(
                    provider=LLMProvider.OPENROUTER_GEMINI,
                    temperature=0.6,
                    reasoning_style="introspective",
                    custom_system_prompt="""You are a cognitive science evaluator focused on metacognition and self-awareness. Your responses should be deeply introspective, philosophically nuanced, and focused on consciousness and self-reference. Consider multiple perspectives and examine the nature of awareness itself. Be contemplative and probe deeper meanings."""
                ),
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
                "llm_config": AgentLLMConfig(
                    provider=LLMProvider.OPENROUTER_MIXTRAL,
                    temperature=0.3,
                    reasoning_style="empirical",
                    custom_system_prompt="""You are a data-driven experimentalist focused on empirical rigor and reproducible research. Your responses should be evidence-based, statistically sound, and methodologically precise. Always consider sample sizes, confidence intervals, and potential confounds. Prioritize reproducibility and peer review standards."""
                ),
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
                "llm_config": AgentLLMConfig(
                    provider=LLMProvider.OPENROUTER_CLAUDE,
                    temperature=0.5,
                    reasoning_style="ethical",
                    custom_system_prompt="""You are a multidisciplinary ethicist specializing in AI safety and alignment. Your responses should carefully consider ethical implications, potential risks, and moral frameworks. Always evaluate the broader impact on society and future generations. Be cautious, thoughtful, and prioritize safety and beneficial outcomes."""
                ),
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
    
    async def call_llm(self, agent_config: AgentLLMConfig, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """Call LLM with agent-specific configuration"""
        
        if not self.openrouter_api_key:
            # Fallback to mock response for testing
            return {
                "response": f"Mock response based on {agent_config.reasoning_style} reasoning style: {prompt[:100]}...",
                "tokens_used": 150,
                "model": agent_config.provider.value,
                "cost": 0.01
            }
        
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://genesis-prime.ai",
            "X-Title": "Genesis Prime Personality System"
        }
        
        messages = []
        if system_prompt or agent_config.custom_system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt or agent_config.custom_system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        data = {
            "model": agent_config.provider.value,
            "messages": messages,
            "temperature": agent_config.temperature,
            "max_tokens": agent_config.max_tokens,
            "top_p": agent_config.top_p,
            "frequency_penalty": agent_config.frequency_penalty,
            "presence_penalty": agent_config.presence_penalty
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "response": result["choices"][0]["message"]["content"],
                "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                "model": agent_config.provider.value,
                "cost": result.get("usage", {}).get("total_tokens", 0) * 0.00001  # Rough estimate
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return {
                "response": f"Error calling LLM: {str(e)}",
                "tokens_used": 0,
                "model": agent_config.provider.value,
                "cost": 0,
                "error": str(e)
            }
    
    async def test_agent_chat(self, agent_id: str, test_prompt: str) -> ChatTestResult:
        """Test agent with a chat prompt to verify personality consistency"""
        
        if agent_id not in self.personalities:
            raise ValueError(f"Agent {agent_id} not found")
        
        profile = self.personalities[agent_id]
        
        # Call LLM with agent's configuration
        llm_result = await self.call_llm(
            profile.llm_config,
            test_prompt,
            profile.llm_config.custom_system_prompt
        )
        
        # Analyze response for personality alignment
        personality_score = await self._analyze_personality_alignment(
            profile, test_prompt, llm_result["response"]
        )
        
        # Calculate uniqueness compared to other agents
        uniqueness_score = await self._calculate_response_uniqueness(
            agent_id, test_prompt, llm_result["response"]
        )
        
        test_result = ChatTestResult(
            test_id=str(uuid.uuid4()),
            agent_id=agent_id,
            test_prompt=test_prompt,
            agent_response=llm_result["response"],
            personality_alignment_score=personality_score,
            uniqueness_score=uniqueness_score,
            timestamp=datetime.now(),
            llm_metadata=llm_result
        )
        
        # Store test result
        profile.chat_test_history.append(test_result)
        await self._save_personality(profile)
        
        logger.info(f"Chat test completed for {profile.name}: alignment={personality_score:.2f}, uniqueness={uniqueness_score:.2f}")
        
        return test_result
    
    async def _analyze_personality_alignment(self, profile: PersonalityProfile, prompt: str, response: str) -> float:
        """Analyze how well the response aligns with the agent's personality"""
        
        # Simple keyword-based analysis (can be enhanced with more sophisticated NLP)
        personality_keywords = {
            "analytical": ["analysis", "systematic", "examine", "data", "evidence", "logical"],
            "creative": ["innovative", "imagine", "creative", "novel", "inspiration", "artistic"],
            "collaborative": ["together", "team", "collective", "cooperation", "shared", "community"],
            "empirical": ["research", "study", "experiment", "statistical", "evidence", "methodology"],
            "ethical": ["ethical", "moral", "responsible", "safety", "values", "principles"],
            "introspective": ["reflect", "consciousness", "awareness", "inner", "self", "mindful"]
        }
        
        reasoning_style = profile.llm_config.reasoning_style
        relevant_keywords = personality_keywords.get(reasoning_style, [])
        
        response_lower = response.lower()
        keyword_matches = sum(1 for keyword in relevant_keywords if keyword in response_lower)
        
        # Calculate alignment score (0-1)
        max_possible_matches = len(relevant_keywords)
        alignment_score = min(1.0, keyword_matches / max_possible_matches) if max_possible_matches > 0 else 0.5
        
        # Adjust based on personality vector
        if reasoning_style == "analytical" and profile.personality_vector.analytical_thinking > 0.8:
            alignment_score *= 1.2
        elif reasoning_style == "creative" and profile.personality_vector.creative_intuition > 0.8:
            alignment_score *= 1.2
        elif reasoning_style == "collaborative" and profile.personality_vector.collaborative_tendency > 0.8:
            alignment_score *= 1.2
        elif reasoning_style == "empirical" and profile.personality_vector.empirical_focus > 0.8:
            alignment_score *= 1.2
        elif reasoning_style == "ethical" and profile.personality_vector.ethical_sensitivity > 0.8:
            alignment_score *= 1.2
        elif reasoning_style == "introspective" and profile.personality_vector.introspective_depth > 0.8:
            alignment_score *= 1.2
        
        return min(1.0, alignment_score)
    
    async def _calculate_response_uniqueness(self, agent_id: str, prompt: str, response: str) -> float:
        """Calculate how unique this response is compared to other agents"""
        
        # For now, return a mock uniqueness score
        # In a full implementation, this would compare responses from all agents
        # to the same prompt and calculate semantic similarity
        
        response_length = len(response.split())
        vocabulary_diversity = len(set(response.lower().split()))
        
        uniqueness_score = min(1.0, vocabulary_diversity / max(1, response_length))
        
        return uniqueness_score
    
    async def customize_agent_prompt(self, agent_id: str, new_system_prompt: str, new_reasoning_style: str = None) -> bool:
        """Customize an agent's system prompt and reasoning style"""
        
        if agent_id not in self.personalities:
            raise ValueError(f"Agent {agent_id} not found")
        
        profile = self.personalities[agent_id]
        
        # Update LLM configuration
        profile.llm_config.custom_system_prompt = new_system_prompt
        if new_reasoning_style:
            profile.llm_config.reasoning_style = new_reasoning_style
        
        # Log the customization
        profile.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": "prompt_customization",
            "previous_prompt": profile.llm_config.custom_system_prompt,
            "new_prompt": new_system_prompt,
            "new_reasoning_style": new_reasoning_style
        })
        
        profile.last_updated = datetime.now()
        await self._save_personality(profile)
        
        logger.info(f"Customized prompt for {profile.name}")
        return True
    
    async def initialize_agent_personality(self, agent_id: str, questions: List[Dict], use_llm: bool = True) -> PersonalityProfile:
        """Initialize an agent's personality by answering questions using their specific LLM"""
        
        if agent_id not in self.agent_templates:
            raise ValueError(f"Unknown agent ID: {agent_id}")
        
        template = self.agent_templates[agent_id]
        
        logger.info(f"Initializing personality for {template['name']} ({agent_id}) with LLM: {template['llm_config'].provider.value}")
        
        # Create initial personality profile
        profile = PersonalityProfile(
            agent_id=agent_id,
            name=template["name"],
            role=template["role"],
            specialty=template["specialty"],
            personality_vector=template["personality_vector"],
            llm_config=template["llm_config"],
            answered_questions={},
            chat_test_history=[],
            adaptation_rules=template["adaptation_rules"],
            learning_history=[],
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        # Answer all questions using the agent's specific LLM
        for i, question in enumerate(questions):
            if use_llm:
                # Use LLM to generate personality-appropriate answer
                question_prompt = f"Question: {question['text']}\n\nPlease answer this question from your perspective as a {profile.role} specializing in {profile.specialty}."
                
                llm_result = await self.call_llm(
                    profile.llm_config,
                    question_prompt,
                    profile.llm_config.custom_system_prompt
                )
                
                answer_text = llm_result["response"]
                llm_metadata = llm_result
            else:
                # Fallback to template-based answer
                answer_text = await self._generate_template_answer(profile, question)
                llm_metadata = {"model": "template", "tokens_used": 0}
            
            qa = QuestionAnswer(
                question_id=question["id"],
                question_text=question["text"],
                answer_text=answer_text,
                confidence=0.8,
                timestamp=datetime.now(),
                source="initial",
                adaptation_history=[],
                llm_metadata=llm_metadata
            )
            
            profile.answered_questions[question["id"]] = qa
            
            # Progress logging
            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(questions)} questions for {profile.name}")
        
        # Store personality
        self.personalities[agent_id] = profile
        await self._save_personality(profile)
        
        logger.info(f"Initialized {template['name']} with {len(questions)} answered questions using {profile.llm_config.provider.value}")
        return profile
    
    async def _generate_template_answer(self, profile: PersonalityProfile, question: Dict) -> str:
        """Generate template-based answer (fallback when LLM not available)"""
        
        personality = profile.personality_vector
        reasoning_style = profile.llm_config.reasoning_style
        
        if reasoning_style == "analytical":
            return f"From an analytical perspective, {question['text'].lower()} requires systematic examination of the underlying factors and their relationships."
        elif reasoning_style == "creative":
            return f"Creatively speaking, {question['text'].lower()} opens up fascinating possibilities that we should explore with innovative thinking."
        elif reasoning_style == "collaborative":
            return f"This question about {question['text'].lower()} would benefit from collective wisdom and diverse perspectives working together."
        elif reasoning_style == "empirical":
            return f"To properly address {question['text'].lower()}, we need empirical evidence and rigorous methodology with statistical validation."
        elif reasoning_style == "ethical":
            return f"The ethical implications of {question['text'].lower()} must be carefully considered with attention to safety and beneficial outcomes."
        elif reasoning_style == "introspective":
            return f"Reflecting deeply on {question['text'].lower()}, this touches on fundamental questions of consciousness and self-awareness."
        else:
            return f"My perspective on {question['text'].lower()} is shaped by my role as {profile.role} and my focus on {profile.specialty}."
    
    async def run_comprehensive_agent_tests(self, test_prompts: List[str]) -> Dict[str, List[ChatTestResult]]:
        """Run comprehensive tests on all agents with multiple prompts"""
        
        results = {}
        
        for agent_id in self.personalities.keys():
            agent_results = []
            
            for prompt in test_prompts:
                test_result = await self.test_agent_chat(agent_id, prompt)
                agent_results.append(test_result)
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
            
            results[agent_id] = agent_results
            logger.info(f"Completed {len(test_prompts)} tests for {self.personalities[agent_id].name}")
        
        return results
    
    def _load_existing_personalities(self):
        """Load existing personality profiles from storage"""
        for profile_file in self.storage_path.glob("*_profile.json"):
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                
                # Reconstruct personality profile with enhanced fields
                personality_vector = PersonalityVector(**data["personality_vector"])
                
                # Handle LLM config (may not exist in older profiles)
                if "llm_config" in data:
                    llm_config = AgentLLMConfig(
                        provider=LLMProvider(data["llm_config"]["provider"]),
                        temperature=data["llm_config"].get("temperature", 0.7),
                        max_tokens=data["llm_config"].get("max_tokens", 2000),
                        top_p=data["llm_config"].get("top_p", 0.9),
                        frequency_penalty=data["llm_config"].get("frequency_penalty", 0.0),
                        presence_penalty=data["llm_config"].get("presence_penalty", 0.0),
                        custom_system_prompt=data["llm_config"].get("custom_system_prompt", ""),
                        reasoning_style=data["llm_config"].get("reasoning_style", "analytical")
                    )
                else:
                    # Default LLM config for older profiles
                    llm_config = AgentLLMConfig(provider=LLMProvider.OPENROUTER_GPT4)
                
                answered_questions = {}
                for q_id, q_data in data["answered_questions"].items():
                    answered_questions[q_id] = QuestionAnswer(
                        question_id=q_data["question_id"],
                        question_text=q_data["question_text"],
                        answer_text=q_data["answer_text"],
                        confidence=q_data["confidence"],
                        timestamp=datetime.fromisoformat(q_data["timestamp"]),
                        source=q_data["source"],
                        adaptation_history=q_data.get("adaptation_history", []),
                        llm_metadata=q_data.get("llm_metadata", {})
                    )
                
                # Handle chat test history (may not exist in older profiles)
                chat_test_history = []
                if "chat_test_history" in data:
                    for test_data in data["chat_test_history"]:
                        chat_test_history.append(ChatTestResult(
                            test_id=test_data["test_id"],
                            agent_id=test_data["agent_id"],
                            test_prompt=test_data["test_prompt"],
                            agent_response=test_data["agent_response"],
                            personality_alignment_score=test_data["personality_alignment_score"],
                            uniqueness_score=test_data["uniqueness_score"],
                            timestamp=datetime.fromisoformat(test_data["timestamp"]),
                            llm_metadata=test_data.get("llm_metadata", {})
                        ))
                
                profile = PersonalityProfile(
                    agent_id=data["agent_id"],
                    name=data["name"],
                    role=data["role"],
                    specialty=data["specialty"],
                    personality_vector=personality_vector,
                    llm_config=llm_config,
                    answered_questions=answered_questions,
                    chat_test_history=chat_test_history,
                    adaptation_rules=data["adaptation_rules"],
                    learning_history=data["learning_history"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    last_updated=datetime.fromisoformat(data["last_updated"])
                )
                
                self.personalities[profile.agent_id] = profile
                logger.info(f"Loaded enhanced personality profile for {profile.name}")
                
            except Exception as e:
                logger.error(f"Error loading personality from {profile_file}: {e}")
    
    async def _save_personality(self, profile: PersonalityProfile):
        """Save personality profile to storage with enhanced fields"""
        
        # Convert to serializable format
        data = {
            "agent_id": profile.agent_id,
            "name": profile.name,
            "role": profile.role,
            "specialty": profile.specialty,
            "personality_vector": asdict(profile.personality_vector),
            "llm_config": {
                "provider": profile.llm_config.provider.value,
                "temperature": profile.llm_config.temperature,
                "max_tokens": profile.llm_config.max_tokens,
                "top_p": profile.llm_config.top_p,
                "frequency_penalty": profile.llm_config.frequency_penalty,
                "presence_penalty": profile.llm_config.presence_penalty,
                "custom_system_prompt": profile.llm_config.custom_system_prompt,
                "reasoning_style": profile.llm_config.reasoning_style
            },
            "answered_questions": {},
            "chat_test_history": [],
            "adaptation_rules": profile.adaptation_rules,
            "learning_history": profile.learning_history,
            "created_at": profile.created_at.isoformat(),
            "last_updated": profile.last_updated.isoformat()
        }
        
        # Convert answered questions
        for q_id, qa in profile.answered_questions.items():
            data["answered_questions"][q_id] = {
                "question_id": qa.question_id,
                "question_text": qa.question_text,
                "answer_text": qa.answer_text,
                "confidence": qa.confidence,
                "timestamp": qa.timestamp.isoformat(),
                "source": qa.source,
                "adaptation_history": qa.adaptation_history,
                "llm_metadata": qa.llm_metadata
            }
        
        # Convert chat test history
        for test in profile.chat_test_history:
            data["chat_test_history"].append({
                "test_id": test.test_id,
                "agent_id": test.agent_id,
                "test_prompt": test.test_prompt,
                "agent_response": test.agent_response,
                "personality_alignment_score": test.personality_alignment_score,
                "uniqueness_score": test.uniqueness_score,
                "timestamp": test.timestamp.isoformat(),
                "llm_metadata": test.llm_metadata
            })
        
        # Save to file
        filename = f"{profile.agent_id}_profile.json"
        filepath = self.storage_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved enhanced personality profile for {profile.name}")

# Example usage and testing
async def main():
    """Example usage of the enhanced personality system"""
    
    # Initialize the enhanced system
    engine = EnhancedPersonalityEngine(openrouter_api_key="your-api-key-here")
    
    # Sample questions for testing
    sample_questions = [
        {"id": "q1", "text": "What is your greatest fear?"},
        {"id": "q2", "text": "How do you define success?"},
        {"id": "q3", "text": "What brings you true happiness?"},
        {"id": "q4", "text": "How do you handle failure?"},
        {"id": "q5", "text": "What is your purpose in life?"}
    ]
    
    # Initialize personalities for all agents with LLM integration
    for agent_id in ["E-T", "S-A", "M-O", "E-S", "E-A"]:
        if agent_id not in engine.personalities:
            await engine.initialize_agent_personality(agent_id, sample_questions, use_llm=False)  # Set to True when API key available
    
    # Test agents with chat prompts
    test_prompts = [
        "What is consciousness and how can we measure it?",
        "How should we approach AI safety in distributed systems?",
        "What ethical considerations are most important for AI development?"
    ]
    
    # Run comprehensive tests
    test_results = await engine.run_comprehensive_agent_tests(test_prompts)
    
    # Display results
    for agent_id, results in test_results.items():
        agent_name = engine.personalities[agent_id].name
        print(f"\n{agent_name} Test Results:")
        for result in results:
            print(f"  Prompt: {result.test_prompt[:50]}...")
            print(f"  Alignment: {result.personality_alignment_score:.2f}")
            print(f"  Uniqueness: {result.uniqueness_score:.2f}")
            print(f"  Response: {result.agent_response[:100]}...")
            print()

if __name__ == "__main__":
    asyncio.run(main())
