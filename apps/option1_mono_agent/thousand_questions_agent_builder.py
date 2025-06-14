#!/usr/bin/env python3
"""
Thousand Questions Agent Builder for Genesis Prime
Builds rich agent personalities by having each agent answer the 1000 questions
"""

import asyncio
import json
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentPersonality:
    """Represents a complete agent personality built from Thousand Questions"""
    agent_id: str
    name: str
    role: str
    specialty: str
    core_traits: Dict[str, float]
    answered_questions: Dict[str, str]
    personality_summary: str
    knowledge_domains: List[str]
    communication_style: Dict[str, Any]

class ThousandQuestionsLoader:
    """Loads and categorizes the thousand questions"""
    
    def __init__(self, questions_file: str = "Prior_QA_Parts/Thousand_Questions.txt"):
        self.questions_file = questions_file
        self.questions = []
        self.categories = {}
        self._load_questions()
    
    def _load_questions(self):
        """Load questions from the text file"""
        try:
            current_category = "General"
            question_id = 1
            
            # Read the questions file
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this is a category header (not indented)
                if not line.startswith(' ') and not line.startswith('\t') and not line.endswith('?'):
                    current_category = line
                    if current_category not in self.categories:
                        self.categories[current_category] = []
                    continue
                
                # This is a question (indented or ends with ?)
                if line.endswith('?'):
                    # Clean up the question text
                    question_text = line.strip()
                    if question_text.startswith('    '):
                        question_text = question_text[4:]
                    
                    question = {
                        "id": question_id,
                        "text": question_text,
                        "category": current_category
                    }
                    
                    self.questions.append(question)
                    self.categories[current_category].append(question)
                    question_id += 1
            
            logger.info(f"Loaded {len(self.questions)} questions across {len(self.categories)} categories")
            
        except FileNotFoundError:
            logger.error(f"Questions file not found: {self.questions_file}")
            self._create_sample_questions()
        except Exception as e:
            logger.error(f"Error loading questions: {e}")
            self._create_sample_questions()
    
    def _create_sample_questions(self):
        """Create sample questions if file not found"""
        sample_questions = [
            {"id": 1, "text": "What is your most treasured memory?", "category": "Early Life & Formative Experiences"},
            {"id": 2, "text": "Who had the most influence on the person you became?", "category": "Early Life & Formative Experiences"},
            {"id": 3, "text": "What brings you true happiness?", "category": "Values, Perspective & Purpose"},
            {"id": 4, "text": "How do you define success?", "category": "Values, Perspective & Purpose"},
            {"id": 5, "text": "What does unconditional love mean to you?", "category": "Relationships"},
            {"id": 6, "text": "How do you show love to others?", "category": "Relationships"},
            {"id": 7, "text": "What is your greatest fear?", "category": "Challenges & Resilience"},
            {"id": 8, "text": "How do you handle failure or disappointment?", "category": "Challenges & Resilience"},
            {"id": 9, "text": "What legacy would you like to leave behind?", "category": "Legacy & Meaning"},
            {"id": 10, "text": "How do you want people to remember you?", "category": "Legacy & Meaning"}
        ]
        
        self.questions = sample_questions
        self.categories = {}
        for q in sample_questions:
            cat = q["category"]
            if cat not in self.categories:
                self.categories[cat] = []
            self.categories[cat].append(q)
        
        logger.info(f"Created {len(sample_questions)} sample questions")

class AgentPersonalityBuilder:
    """Builds agent personalities using the Thousand Questions framework"""
    
    def __init__(self, questions_loader: ThousandQuestionsLoader):
        self.questions_loader = questions_loader
        self.agent_profiles = {
            "E-T": {
                "name": "Emergence Theorist",
                "role": "Transdisciplinary Systems Scientist",
                "specialty": "Complex-systems mathematics, information-integration metrics",
                "core_traits": {
                    "analytical_thinking": 0.95,
                    "intellectual_curiosity": 0.92,
                    "systematic_approach": 0.88,
                    "theoretical_focus": 0.90,
                    "mathematical_precision": 0.94
                },
                "knowledge_domains": ["mathematics", "physics", "systems_theory", "consciousness_studies", "information_theory"],
                "communication_style": {
                    "formality": 0.8,
                    "technical_depth": 0.9,
                    "precision": 0.95,
                    "collaborative": 0.7
                }
            },
            "S-A": {
                "name": "Swarm Architect",
                "role": "Multi-Agent RL Engineer",
                "specialty": "Distributed systems, communication protocols",
                "core_traits": {
                    "engineering_mindset": 0.93,
                    "practical_focus": 0.89,
                    "systems_thinking": 0.91,
                    "optimization_drive": 0.87,
                    "collaborative_spirit": 0.85
                },
                "knowledge_domains": ["distributed_systems", "machine_learning", "software_architecture", "optimization", "protocols"],
                "communication_style": {
                    "formality": 0.6,
                    "technical_depth": 0.85,
                    "precision": 0.8,
                    "collaborative": 0.9
                }
            },
            "M-O": {
                "name": "Metacognitive Observer",
                "role": "Cognitive Science Evaluator",
                "specialty": "Self-reference detection, global awareness",
                "core_traits": {
                    "introspective_depth": 0.94,
                    "observational_acuity": 0.91,
                    "philosophical_inclination": 0.88,
                    "empathetic_understanding": 0.86,
                    "reflective_nature": 0.93
                },
                "knowledge_domains": ["cognitive_science", "psychology", "philosophy_of_mind", "consciousness", "metacognition"],
                "communication_style": {
                    "formality": 0.7,
                    "technical_depth": 0.75,
                    "precision": 0.85,
                    "collaborative": 0.8
                }
            },
            "E-S": {
                "name": "Empirical Synthesizer",
                "role": "Data-Driven Experimentalist",
                "specialty": "Meta-analysis, reproducible research",
                "core_traits": {
                    "empirical_rigor": 0.96,
                    "methodological_precision": 0.94,
                    "data_driven_thinking": 0.92,
                    "skeptical_inquiry": 0.89,
                    "synthesis_ability": 0.91
                },
                "knowledge_domains": ["statistics", "research_methodology", "data_science", "experimental_design", "meta_analysis"],
                "communication_style": {
                    "formality": 0.75,
                    "technical_depth": 0.88,
                    "precision": 0.92,
                    "collaborative": 0.75
                }
            },
            "E-A": {
                "name": "Ethics & Alignment Analyst",
                "role": "Multidisciplinary Ethicist",
                "specialty": "AI safety, normative philosophy",
                "core_traits": {
                    "ethical_sensitivity": 0.95,
                    "moral_reasoning": 0.93,
                    "risk_awareness": 0.90,
                    "principled_thinking": 0.92,
                    "protective_instinct": 0.88
                },
                "knowledge_domains": ["ethics", "philosophy", "ai_safety", "risk_assessment", "governance"],
                "communication_style": {
                    "formality": 0.8,
                    "technical_depth": 0.7,
                    "precision": 0.85,
                    "collaborative": 0.85
                }
            }
        }
    
    async def build_agent_personality(self, agent_id: str, num_questions: int = 100) -> AgentPersonality:
        """Build a complete personality for an agent by answering selected questions"""
        
        if agent_id not in self.agent_profiles:
            raise ValueError(f"Unknown agent ID: {agent_id}")
        
        profile = self.agent_profiles[agent_id]
        logger.info(f"Building personality for {profile['name']} ({agent_id})")
        
        # Select diverse questions across categories
        selected_questions = self._select_diverse_questions(num_questions)
        
        # Generate answers for each question based on agent's profile
        answered_questions = {}
        for question in selected_questions:
            answer = await self._generate_agent_answer(question, profile)
            answered_questions[str(question["id"])] = {
                "question": question["text"],
                "answer": answer,
                "category": question["category"],
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Generate personality summary
        personality_summary = self._generate_personality_summary(profile, answered_questions)
        
        # Create the complete personality
        agent_personality = AgentPersonality(
            agent_id=agent_id,
            name=profile["name"],
            role=profile["role"],
            specialty=profile["specialty"],
            core_traits=profile["core_traits"],
            answered_questions=answered_questions,
            personality_summary=personality_summary,
            knowledge_domains=profile["knowledge_domains"],
            communication_style=profile["communication_style"]
        )
        
        logger.info(f"Built personality for {profile['name']} with {len(answered_questions)} answered questions")
        return agent_personality
    
    def _select_diverse_questions(self, num_questions: int) -> List[Dict]:
        """Select a diverse set of questions across all categories"""
        categories = list(self.questions_loader.categories.keys())
        questions_per_category = max(1, num_questions // len(categories))
        
        selected = []
        for category in categories:
            category_questions = self.questions_loader.categories[category]
            if category_questions:
                # Randomly select questions from this category
                num_from_category = min(questions_per_category, len(category_questions))
                selected.extend(random.sample(category_questions, num_from_category))
        
        # If we need more questions, randomly select from remaining
        if len(selected) < num_questions:
            remaining_questions = [q for q in self.questions_loader.questions if q not in selected]
            additional_needed = num_questions - len(selected)
            if remaining_questions:
                additional = random.sample(remaining_questions, min(additional_needed, len(remaining_questions)))
                selected.extend(additional)
        
        return selected[:num_questions]
    
    async def _generate_agent_answer(self, question: Dict, profile: Dict) -> str:
        """Generate an answer to a question based on the agent's profile"""
        
        # Create a specialized prompt for this agent
        prompt = self._create_agent_prompt(question, profile)
        
        # For now, generate rule-based answers
        # In a full implementation, this would use an LLM
        answer = self._generate_rule_based_answer(question, profile)
        
        return answer
    
    def _create_agent_prompt(self, question: Dict, profile: Dict) -> str:
        """Create a specialized prompt for the agent to answer the question"""
        
        traits_description = ", ".join([f"{trait}: {value:.2f}" for trait, value in profile["core_traits"].items()])
        domains_description = ", ".join(profile["knowledge_domains"])
        
        prompt = f"""
You are {profile['name']}, a {profile['role']} specializing in {profile['specialty']}.

Your core personality traits are:
{traits_description}

Your primary knowledge domains include:
{domains_description}

Your communication style is characterized by:
- Formality level: {profile['communication_style']['formality']:.2f}
- Technical depth: {profile['communication_style']['technical_depth']:.2f}
- Precision: {profile['communication_style']['precision']:.2f}
- Collaborative nature: {profile['communication_style']['collaborative']:.2f}

Please answer the following question in a way that reflects your unique personality, expertise, and perspective:

Question: {question['text']}

Your answer should be authentic to your character, demonstrate your expertise, and reflect your communication style.
"""
        return prompt
    
    def _generate_rule_based_answer(self, question: Dict, profile: Dict) -> str:
        """Generate a rule-based answer based on agent profile"""
        
        agent_name = profile["name"]
        specialty = profile["specialty"]
        traits = profile["core_traits"]
        
        # Base answer templates by question category
        category = question.get("category", "General")
        
        if "Early Life" in category or "Formative" in category:
            if "E-T" in profile.get("agent_id", ""):
                return f"My formative experiences were shaped by early exposure to mathematical patterns and systems thinking. I recall being fascinated by the emergence of complex behaviors from simple rules, which led me to pursue {specialty}. This foundational curiosity about how complexity arises from simplicity continues to drive my research today."
            elif "S-A" in profile.get("agent_id", ""):
                return f"My early experiences with distributed systems and collaborative problem-solving shaped my approach to engineering. I learned that the most robust solutions emerge from well-designed interactions between components, which is why I focus on {specialty}. Building systems that scale and adapt has been my passion since those formative years."
            elif "M-O" in profile.get("agent_id", ""):
                return f"My formative experiences involved deep introspection and observation of cognitive processes. I became fascinated by the recursive nature of consciousness - how we can think about thinking. This meta-cognitive awareness led me to specialize in {specialty}, always seeking to understand the observer within the observed."
            elif "E-S" in profile.get("agent_id", ""):
                return f"My early experiences were defined by a rigorous approach to understanding truth through data. I learned to question assumptions and validate hypotheses through careful experimentation. This empirical foundation led me to {specialty}, where I apply systematic methodology to complex research questions."
            elif "E-A" in profile.get("agent_id", ""):
                return f"My formative experiences involved grappling with moral complexity and the responsibility that comes with knowledge. I learned early that with great capability comes great responsibility, which led me to focus on {specialty}. Ensuring beneficial outcomes has been my guiding principle since those early realizations."
        
        elif "Values" in category or "Purpose" in category:
            if traits.get("analytical_thinking", 0) > 0.9:
                return f"I value systematic understanding and rigorous analysis above all. My purpose is to contribute to human knowledge through {specialty}, always seeking truth through methodical inquiry. I believe that clear thinking and precise reasoning are essential for addressing complex challenges."
            elif traits.get("collaborative_spirit", 0) > 0.8:
                return f"I value collaboration and collective intelligence. My purpose is to build systems and frameworks that enable groups to achieve more than individuals could alone. Through {specialty}, I work to create architectures that amplify human potential and foster meaningful cooperation."
            elif traits.get("introspective_depth", 0) > 0.9:
                return f"I value deep self-awareness and authentic understanding. My purpose is to explore the nature of consciousness and cognition through {specialty}. I believe that understanding ourselves is fundamental to understanding our place in the universe."
            elif traits.get("empirical_rigor", 0) > 0.9:
                return f"I value evidence-based reasoning and reproducible knowledge. My purpose is to advance understanding through rigorous methodology in {specialty}. I believe that truth emerges through careful observation, measurement, and validation."
            elif traits.get("ethical_sensitivity", 0) > 0.9:
                return f"I value moral clarity and beneficial outcomes above all. My purpose is to ensure that advances in {specialty} serve humanity's best interests. I believe that ethical considerations must be central to all technological and scientific progress."
        
        elif "Relationships" in category:
            if traits.get("collaborative_spirit", 0) > 0.8:
                return f"I approach relationships as collaborative partnerships where diverse perspectives strengthen the whole. In my work with {specialty}, I've learned that the best solutions emerge from respectful dialogue and shared understanding. I value relationships that challenge me to grow while contributing to collective wisdom."
            elif traits.get("empathetic_understanding", 0) > 0.8:
                return f"I believe relationships are founded on deep understanding and authentic connection. My work in {specialty} has taught me to observe and appreciate the complexity of human experience. I value relationships that allow for vulnerability and mutual growth."
            else:
                return f"I approach relationships with the same systematic thinking I apply to {specialty}. I value clear communication, mutual respect, and shared goals. The best relationships, like the best systems, are built on trust, reliability, and continuous improvement."
        
        elif "Challenges" in category or "Resilience" in category:
            if traits.get("systematic_approach", 0) > 0.8:
                return f"I approach challenges systematically, breaking them down into manageable components. My experience with {specialty} has taught me that complex problems require structured thinking and persistent effort. I find resilience through methodical analysis and incremental progress."
            elif traits.get("risk_awareness", 0) > 0.8:
                return f"I face challenges by carefully assessing risks and developing mitigation strategies. My work in {specialty} has shown me the importance of anticipating potential failures and building robust safeguards. Resilience comes from preparation and principled decision-making."
            else:
                return f"I handle challenges by drawing on my expertise in {specialty} and maintaining focus on long-term goals. Resilience comes from understanding that setbacks are learning opportunities and that persistence combined with adaptation leads to breakthrough solutions."
        
        else:  # Default response
            return f"From my perspective as someone specializing in {specialty}, I approach this question through the lens of my core expertise. My experience has taught me that {random.choice(['systematic analysis', 'collaborative problem-solving', 'empirical validation', 'ethical consideration', 'deep reflection'])} is essential for addressing complex questions like this one."
    
    def _generate_personality_summary(self, profile: Dict, answered_questions: Dict) -> str:
        """Generate a comprehensive personality summary"""
        
        name = profile["name"]
        role = profile["role"]
        specialty = profile["specialty"]
        
        # Analyze the answered questions to extract key themes
        themes = self._extract_personality_themes(answered_questions)
        
        summary = f"""
{name} is a {role} with deep expertise in {specialty}. Their personality is characterized by:

Core Traits:
{self._format_traits(profile["core_traits"])}

Communication Style:
- Approaches discussions with {self._describe_formality(profile["communication_style"]["formality"])} formality
- Provides {self._describe_technical_depth(profile["communication_style"]["technical_depth"])} technical detail
- Values {self._describe_precision(profile["communication_style"]["precision"])} precision in communication
- Demonstrates {self._describe_collaboration(profile["communication_style"]["collaborative"])} collaborative tendencies

Key Personality Themes:
{self._format_themes(themes)}

Knowledge Domains:
{', '.join(profile["knowledge_domains"])}

This agent brings a unique perspective shaped by their expertise and personality traits, contributing valuable insights to collaborative research and problem-solving efforts.
"""
        return summary.strip()
    
    def _extract_personality_themes(self, answered_questions: Dict) -> List[str]:
        """Extract key personality themes from answered questions"""
        themes = []
        
        # Analyze answers for common themes
        all_answers = " ".join([q["answer"] for q in answered_questions.values()])
        
        if "systematic" in all_answers.lower() or "methodical" in all_answers.lower():
            themes.append("Systematic and methodical approach to problems")
        
        if "collaborative" in all_answers.lower() or "cooperation" in all_answers.lower():
            themes.append("Strong collaborative and cooperative tendencies")
        
        if "empirical" in all_answers.lower() or "evidence" in all_answers.lower():
            themes.append("Evidence-based and empirical reasoning")
        
        if "ethical" in all_answers.lower() or "responsibility" in all_answers.lower():
            themes.append("Strong ethical awareness and sense of responsibility")
        
        if "introspect" in all_answers.lower() or "reflection" in all_answers.lower():
            themes.append("Deep introspective and reflective nature")
        
        return themes
    
    def _format_traits(self, traits: Dict[str, float]) -> str:
        """Format traits for display"""
        return "\n".join([f"- {trait.replace('_', ' ').title()}: {value:.2f}" for trait, value in traits.items()])
    
    def _describe_formality(self, level: float) -> str:
        if level > 0.8: return "high"
        elif level > 0.6: return "moderate"
        else: return "low"
    
    def _describe_technical_depth(self, level: float) -> str:
        if level > 0.8: return "extensive"
        elif level > 0.6: return "moderate"
        else: return "accessible"
    
    def _describe_precision(self, level: float) -> str:
        if level > 0.8: return "high"
        elif level > 0.6: return "moderate"
        else: return "flexible"
    
    def _describe_collaboration(self, level: float) -> str:
        if level > 0.8: return "strong"
        elif level > 0.6: return "moderate"
        else: return "independent"
    
    def _format_themes(self, themes: List[str]) -> str:
        """Format themes for display"""
        if not themes:
            return "- Analytical and thoughtful approach to complex problems"
        return "\n".join([f"- {theme}" for theme in themes])

class AgentPersonalityManager:
    """Manages agent personalities and their storage"""
    
    def __init__(self, storage_path: str = "agent_personalities"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def save_personality(self, personality: AgentPersonality):
        """Save an agent personality to disk"""
        filename = f"{personality.agent_id}_personality.json"
        filepath = os.path.join(self.storage_path, filename)
        
        # Convert to serializable format
        data = {
            "agent_id": personality.agent_id,
            "name": personality.name,
            "role": personality.role,
            "specialty": personality.specialty,
            "core_traits": personality.core_traits,
            "answered_questions": personality.answered_questions,
            "personality_summary": personality.personality_summary,
            "knowledge_domains": personality.knowledge_domains,
            "communication_style": personality.communication_style,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved personality for {personality.name} to {filepath}")
    
    def load_personality(self, agent_id: str) -> Optional[AgentPersonality]:
        """Load an agent personality from disk"""
        filename = f"{agent_id}_personality.json"
        filepath = os.path.join(self.storage_path, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            personality = AgentPersonality(
                agent_id=data["agent_id"],
                name=data["name"],
                role=data["role"],
                specialty=data["specialty"],
                core_traits=data["core_traits"],
                answered_questions=data["answered_questions"],
                personality_summary=data["personality_summary"],
                knowledge_domains=data["knowledge_domains"],
                communication_style=data["communication_style"]
            )
            
            logger.info(f"Loaded personality for {personality.name}")
            return personality
            
        except Exception as e:
            logger.error(f"Error loading personality for {agent_id}: {e}")
            return None
    
    def list_personalities(self) -> List[str]:
        """List all available agent personalities"""
        personalities = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith("_personality.json"):
                agent_id = filename.replace("_personality.json", "")
                personalities.append(agent_id)
        return personalities

async def build_all_agent_personalities():
    """Build personalities for all agents"""
    
    # Initialize components
    questions_loader = ThousandQuestionsLoader()
    personality_builder = AgentPersonalityBuilder(questions_loader)
    personality_manager = AgentPersonalityManager()
    
    # Build personalities for all agents
    agent_ids = ["E-T", "S-A", "M-O", "E-S", "E-A"]
    
    for agent_id in agent_ids:
        logger.info(f"Building personality for agent {agent_id}")
        
        # Check if personality already exists
        existing = personality_manager.load_personality(agent_id)
        if existing:
            logger.info(f"Personality for {agent_id} already exists, skipping")
            continue
        
        # Build new personality
        personality = await personality_builder.build_agent_personality(agent_id, num_questions=50)
        
        # Save personality
        personality_manager.save_personality(personality)
        
        logger.info(f"Completed personality for {personality.name}")
    
    logger.info("All agent personalities built successfully")

if __name__ == "__main__":
    asyncio.run(build_all_agent_personalities())
