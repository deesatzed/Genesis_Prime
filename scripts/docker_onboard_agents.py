#!/usr/bin/env python3
"""
Genesis Prime Docker Agent Onboarding Script
Automated agent personality development for containerized deployment
"""

import os
import sys
import time
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional

# Add the app directory to Python path
sys.path.insert(0, '/app')

from enhanced_personality_system import EnhancedPersonalityEngine, LLMProvider
from thousand_questions_agent_builder import ThousandQuestionsAgentBuilder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DockerAgentOnboarder:
    """Handles automated agent onboarding in Docker environment"""
    
    def __init__(self):
        self.backend_url = os.getenv('BACKEND_URL', 'http://genesis-backend:8000')
        self.agent_profiles_dir = Path('/app/agent_profiles')
        self.agent_profiles_dir.mkdir(exist_ok=True)
        
        # Agent configuration with optimized models for Docker deployment
        self.agent_configs = {
            'E-T': {
                'name': 'Emergence Theorist',
                'model': 'openai/gpt-4o',
                'style': 'analytical',
                'temperature': 0.8,
                'specialization': 'Complex-systems mathematics, information-integration metrics'
            },
            'S-A': {
                'name': 'Swarm Architect', 
                'model': 'anthropic/claude-3.5-sonnet',
                'style': 'collaborative',
                'temperature': 0.7,
                'specialization': 'Distributed systems, communication protocols'
            },
            'M-O': {
                'name': 'Metacognitive Observer',
                'model': 'anthropic/claude-3.5-sonnet',
                'style': 'introspective',
                'temperature': 0.6,
                'specialization': 'Self-reference detection, global awareness'
            },
            'E-S': {
                'name': 'Empirical Synthesizer',
                'model': 'mistralai/mixtral-8x7b-instruct',
                'style': 'empirical',
                'temperature': 0.3,
                'specialization': 'Meta-analysis, reproducible research'
            },
            'E-A': {
                'name': 'Ethics & Alignment Analyst',
                'model': 'anthropic/claude-3-haiku',
                'style': 'ethical',
                'temperature': 0.5,
                'specialization': 'AI safety, normative philosophy'
            }
        }
        
    def wait_for_backend(self, max_retries: int = 30, delay: int = 10) -> bool:
        """Wait for backend service to be ready"""
        logger.info(f"🔍 Waiting for backend at {self.backend_url}")
        
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Backend is ready!")
                    return True
            except requests.exceptions.RequestException as e:
                logger.info(f"⏳ Backend not ready (attempt {attempt + 1}/{max_retries}): {e}")
                
            if attempt < max_retries - 1:
                time.sleep(delay)
                
        logger.error("❌ Backend failed to become ready")
        return False
        
    def check_existing_agents(self) -> Dict[str, bool]:
        """Check which agents already have profiles"""
        existing = {}
        for agent_id, config in self.agent_configs.items():
            profile_file = self.agent_profiles_dir / f"{agent_id}_profile.json"
            existing[agent_id] = profile_file.exists()
            if existing[agent_id]:
                logger.info(f"✅ Found existing profile for {config['name']}")
            else:
                logger.info(f"🆕 Need to create profile for {config['name']}")
        return existing
        
    def onboard_agent(self, agent_id: str, config: Dict) -> bool:
        """Onboard a single agent with progress tracking"""
        logger.info(f"🤖 Starting onboarding for {config['name']} ({agent_id})")
        logger.info(f"   Model: {config['model']}")
        logger.info(f"   Style: {config['style']}")
        logger.info(f"   Specialization: {config['specialization']}")
        
        try:
            # Initialize personality engine
            engine = EnhancedPersonalityEngine()
            
            # Initialize agent with LLM configuration
            llm_provider = LLMProvider(
                provider_name=config['model'].split('/')[0],
                model_name=config['model'],
                temperature=config['temperature']
            )
            
            # Create agent builder
            builder = ThousandQuestionsAgentBuilder(
                agent_name=config['name'],
                agent_id=agent_id,
                llm_provider=llm_provider,
                reasoning_style=config['style']
            )
            
            # Load questions (use sample if thousand questions file not available)
            questions_file = Path('/app/Prior_QA_Parts/Thousand_Questions.txt')
            if questions_file.exists():
                with open(questions_file, 'r') as f:
                    questions = [line.strip() for line in f if line.strip()]
                logger.info(f"📚 Loaded {len(questions)} questions from file")
            else:
                # Use sample questions for Docker deployment
                questions = self.get_sample_questions()
                logger.info(f"📚 Using {len(questions)} sample questions")
            
            # Initialize agent in personality engine
            engine.initialize_agent(
                agent_id=agent_id,
                agent_name=config['name'],
                llm_provider=llm_provider,
                reasoning_style=config['style']
            )
            
            # Process questions with progress tracking
            total_questions = min(len(questions), 100)  # Limit for Docker deployment
            logger.info(f"🔄 Processing {total_questions} questions...")
            
            for i, question in enumerate(questions[:total_questions]):
                if i % 10 == 0:  # Progress update every 10 questions
                    progress = (i / total_questions) * 100
                    logger.info(f"   Progress: {progress:.1f}% ({i}/{total_questions})")
                
                # Answer question through personality engine
                try:
                    response = engine.chat_with_agent(agent_id, question)
                    if response:
                        logger.debug(f"   Q{i+1}: {question[:50]}...")
                except Exception as e:
                    logger.warning(f"   Failed to process question {i+1}: {e}")
                    continue
            
            logger.info(f"✅ Completed onboarding for {config['name']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to onboard {config['name']}: {e}")
            return False
            
    def get_sample_questions(self) -> List[str]:
        """Generate sample questions for agent development"""
        return [
            "What is consciousness and how can we measure it in artificial systems?",
            "How should we approach AI safety in distributed multi-agent systems?",
            "What ethical frameworks should guide AI development and deployment?",
            "How can we ensure AI systems remain beneficial as they become more capable?",
            "What role does emergence play in collective intelligence systems?",
            "How do we balance innovation with safety in AI research?",
            "What are the implications of artificial consciousness for society?",
            "How should AI systems handle uncertainty and ambiguous situations?",
            "What mechanisms ensure accountability in autonomous AI systems?",
            "How can we design AI systems that align with human values?",
            "What is the relationship between intelligence and consciousness?",
            "How do we prevent unintended consequences in AI development?",
            "What role should transparency play in AI decision-making?",
            "How can AI systems learn and adapt while maintaining safety?",
            "What are the long-term implications of artificial general intelligence?",
            "How do we ensure AI systems respect human autonomy and dignity?",
            "What mechanisms prevent AI systems from becoming misaligned?",
            "How should AI systems handle conflicting objectives or values?",
            "What role does interpretability play in AI safety and trust?",
            "How can we design AI systems that are robust and reliable?",
            "What are the philosophical implications of machine consciousness?",
            "How do we ensure AI development benefits all of humanity?",
            "What safeguards prevent AI systems from causing harm?",
            "How should AI systems interact with humans and other AI systems?",
            "What principles should guide the governance of AI technology?",
            "How can we maintain human agency in an AI-augmented world?",
            "What role does diversity play in AI system design and deployment?",
            "How do we address bias and fairness in AI decision-making?",
            "What are the implications of AI for privacy and surveillance?",
            "How should society prepare for the transformative impact of AI?",
            "What mechanisms ensure AI systems remain under human control?",
            "How can AI systems contribute to solving global challenges?",
            "What role does collaboration play in AI safety research?",
            "How do we balance AI capabilities with safety considerations?",
            "What are the economic implications of advanced AI systems?",
            "How should AI systems handle moral and ethical dilemmas?",
            "What safeguards prevent AI systems from being misused?",
            "How can we ensure AI development is inclusive and equitable?",
            "What role does public engagement play in AI governance?",
            "How do we prepare for the societal changes brought by AI?",
            "What principles should guide AI research and development?",
            "How can AI systems support human flourishing and well-being?",
            "What are the implications of AI for human identity and purpose?",
            "How should AI systems be designed to be trustworthy and reliable?",
            "What role does international cooperation play in AI governance?",
            "How do we ensure AI systems are aligned with democratic values?",
            "What safeguards prevent AI systems from becoming too powerful?",
            "How can AI systems be designed to be beneficial and harmless?",
            "What are the long-term risks and benefits of AI technology?",
            "How should society navigate the transition to an AI-enabled future?"
        ]
        
    def run_onboarding(self) -> bool:
        """Run the complete onboarding process"""
        logger.info("🚀 Starting Genesis Prime Docker Agent Onboarding")
        logger.info("=" * 60)
        
        # Wait for backend to be ready
        if not self.wait_for_backend():
            logger.error("❌ Backend not available, cannot proceed with onboarding")
            return False
            
        # Check existing agents
        existing_agents = self.check_existing_agents()
        agents_to_onboard = [
            (agent_id, config) for agent_id, config in self.agent_configs.items()
            if not existing_agents.get(agent_id, False)
        ]
        
        if not agents_to_onboard:
            logger.info("✅ All agents already onboarded!")
            return True
            
        logger.info(f"🎯 Need to onboard {len(agents_to_onboard)} agents")
        
        # Onboard each agent
        success_count = 0
        for agent_id, config in agents_to_onboard:
            if self.onboard_agent(agent_id, config):
                success_count += 1
            else:
                logger.error(f"❌ Failed to onboard {config['name']}")
                
        # Summary
        total_agents = len(agents_to_onboard)
        logger.info("=" * 60)
        logger.info(f"🎉 Onboarding Complete: {success_count}/{total_agents} agents successful")
        
        if success_count == total_agents:
            logger.info("✅ All agents successfully onboarded!")
            return True
        else:
            logger.warning(f"⚠️  {total_agents - success_count} agents failed onboarding")
            return False

def main():
    """Main entry point for Docker onboarding"""
    try:
        onboarder = DockerAgentOnboarder()
        success = onboarder.run_onboarding()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"❌ Onboarding failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
