#!/usr/bin/env python3
"""
API Integration for Adaptive Personality System
Connects the personality engine with Genesis Prime's consciousness system
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from adaptive_personality_system import AdaptivePersonalityEngine, PersonalityChangeType

# Configure logging
logger = logging.getLogger(__name__)

# Pydantic models for API
class LearningEventRequest(BaseModel):
    content: str
    evidence_strength: float = 0.5
    source_credibility: float = 0.5
    topic_relevance: float = 0.5
    keywords: List[str] = []
    topic: str = ""
    source_agent: Optional[str] = None

class PersonalityInitRequest(BaseModel):
    agent_id: str
    use_full_questions: bool = False

class PersonalityComparisonRequest(BaseModel):
    agent_ids: List[str]

# Global personality engine instance
personality_engine = None

def get_personality_engine() -> AdaptivePersonalityEngine:
    """Get or create the global personality engine instance"""
    global personality_engine
    if personality_engine is None:
        personality_engine = AdaptivePersonalityEngine()
    return personality_engine

# Create API router
personality_router = APIRouter(prefix="/personality", tags=["personality"])

@personality_router.get("/status")
async def get_personality_system_status():
    """Get the status of the personality system"""
    engine = get_personality_engine()
    
    personalities = list(engine.personalities.keys())
    
    status = {
        "system_status": "operational",
        "initialized_agents": personalities,
        "total_agents": len(personalities),
        "storage_path": str(engine.storage_path),
        "available_templates": list(engine.agent_templates.keys()),
        "timestamp": datetime.now().isoformat()
    }
    
    return status

@personality_router.post("/initialize/{agent_id}")
async def initialize_agent_personality(agent_id: str, request: PersonalityInitRequest):
    """Initialize an agent's personality with the Thousand Questions"""
    engine = get_personality_engine()
    
    try:
        # Load questions
        if request.use_full_questions:
            questions = await load_thousand_questions()
        else:
            # Use sample questions for testing
            questions = [
                {"id": "q1", "text": "What is your greatest fear?"},
                {"id": "q2", "text": "How do you define success?"},
                {"id": "q3", "text": "What brings you true happiness?"},
                {"id": "q4", "text": "How do you handle failure?"},
                {"id": "q5", "text": "What is your purpose in life?"},
                {"id": "q6", "text": "What motivates you to learn?"},
                {"id": "q7", "text": "How do you approach collaboration?"},
                {"id": "q8", "text": "What ethical principles guide you?"},
                {"id": "q9", "text": "How do you handle uncertainty?"},
                {"id": "q10", "text": "What does wisdom mean to you?"}
            ]
        
        # Initialize personality
        profile = await engine.initialize_agent_personality(agent_id, questions)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "name": profile.name,
            "role": profile.role,
            "questions_answered": len(profile.answered_questions),
            "personality_vector": profile.personality_vector.__dict__,
            "adaptation_rules": profile.adaptation_rules,
            "message": f"Successfully initialized {profile.name} with {len(questions)} questions"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error initializing personality for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize personality: {str(e)}")

@personality_router.get("/agent/{agent_id}")
async def get_agent_personality(agent_id: str):
    """Get detailed personality information for an agent"""
    engine = get_personality_engine()
    
    summary = engine.get_personality_summary(agent_id)
    
    if "error" in summary:
        raise HTTPException(status_code=404, detail=summary["error"])
    
    return summary

@personality_router.get("/agent/{agent_id}/questions")
async def get_agent_questions(agent_id: str, limit: int = 10):
    """Get answered questions for an agent"""
    engine = get_personality_engine()
    
    if agent_id not in engine.personalities:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    profile = engine.personalities[agent_id]
    questions = list(profile.answered_questions.values())
    
    # Sort by timestamp (most recent first)
    questions.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Limit results
    questions = questions[:limit]
    
    return {
        "agent_id": agent_id,
        "agent_name": profile.name,
        "total_questions": len(profile.answered_questions),
        "questions": [
            {
                "question_id": q.question_id,
                "question_text": q.question_text,
                "answer_text": q.answer_text,
                "confidence": q.confidence,
                "source": q.source,
                "timestamp": q.timestamp.isoformat(),
                "adaptations": len(q.adaptation_history)
            }
            for q in questions
        ]
    }

@personality_router.post("/learning-event")
async def process_learning_event(request: LearningEventRequest, background_tasks: BackgroundTasks):
    """Process a learning event that may update agent personalities"""
    engine = get_personality_engine()
    
    # Create learning event
    learning_event = {
        "id": f"learning_{int(datetime.now().timestamp())}",
        "content": request.content,
        "evidence_strength": request.evidence_strength,
        "source_credibility": request.source_credibility,
        "topic_relevance": request.topic_relevance,
        "keywords": request.keywords,
        "topic": request.topic,
        "source_agent": request.source_agent,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # Process the learning event
        results = await engine.process_hive_learning(learning_event)
        
        return {
            "success": True,
            "learning_event_id": learning_event["id"],
            "processing_results": results,
            "total_agents_affected": sum(len(agents) for agents in results.values()),
            "summary": {
                "adaptations": len(results["adaptations"]),
                "reinforcements": len(results["reinforcements"]),
                "integrations": len(results["integrations"]),
                "rejections": len(results["rejections"])
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing learning event: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process learning event: {str(e)}")

@personality_router.post("/compare")
async def compare_personalities(request: PersonalityComparisonRequest):
    """Compare personalities across multiple agents"""
    engine = get_personality_engine()
    
    try:
        comparison = engine.compare_personalities(request.agent_ids)
        
        if "error" in comparison:
            raise HTTPException(status_code=400, detail=comparison["error"])
        
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing personalities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to compare personalities: {str(e)}")

@personality_router.get("/diversity-metrics")
async def get_diversity_metrics():
    """Get diversity metrics for all initialized agents"""
    engine = get_personality_engine()
    
    if len(engine.personalities) < 2:
        return {
            "error": "Need at least 2 agents to calculate diversity metrics",
            "initialized_agents": len(engine.personalities)
        }
    
    agent_ids = list(engine.personalities.keys())
    comparison = engine.compare_personalities(agent_ids)
    
    return {
        "total_agents": len(agent_ids),
        "diversity_score": comparison["diversity_score"],
        "average_similarity": comparison["average_similarity"],
        "agent_names": [engine.personalities[aid].name for aid in agent_ids],
        "personality_distribution": {
            aid: engine.personalities[aid].personality_vector.__dict__ 
            for aid in agent_ids
        }
    }

@personality_router.get("/learning-history/{agent_id}")
async def get_learning_history(agent_id: str, limit: int = 20):
    """Get learning history for an agent"""
    engine = get_personality_engine()
    
    if agent_id not in engine.personalities:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    profile = engine.personalities[agent_id]
    history = profile.learning_history[-limit:]  # Get most recent entries
    
    return {
        "agent_id": agent_id,
        "agent_name": profile.name,
        "total_learning_events": len(profile.learning_history),
        "recent_history": history
    }

@personality_router.post("/simulate-hive-learning")
async def simulate_hive_learning():
    """Simulate various hive learning scenarios for testing"""
    engine = get_personality_engine()
    
    # Create diverse learning events
    learning_events = [
        {
            "id": "sim_collab_001",
            "content": "Collaborative problem-solving increases solution quality by 35% in complex scenarios",
            "evidence_strength": 0.8,
            "source_credibility": 0.9,
            "topic_relevance": 0.85,
            "keywords": ["collaboration", "problem-solving", "quality"],
            "topic": "teamwork"
        },
        {
            "id": "sim_ethics_001", 
            "content": "AI systems must prioritize human welfare in all decision-making processes",
            "evidence_strength": 0.95,
            "source_credibility": 0.85,
            "topic_relevance": 0.9,
            "keywords": ["ethics", "AI", "human welfare", "decisions"],
            "topic": "ethics"
        },
        {
            "id": "sim_analysis_001",
            "content": "Systematic analysis reduces error rates by 60% compared to intuitive approaches",
            "evidence_strength": 0.75,
            "source_credibility": 0.8,
            "topic_relevance": 0.7,
            "keywords": ["analysis", "systematic", "error reduction"],
            "topic": "methodology"
        }
    ]
    
    results = {}
    
    for event in learning_events:
        try:
            result = await engine.process_hive_learning(event)
            results[event["id"]] = result
        except Exception as e:
            results[event["id"]] = {"error": str(e)}
    
    return {
        "simulation_complete": True,
        "events_processed": len(learning_events),
        "results": results,
        "summary": "Simulated diverse learning scenarios to test personality adaptation"
    }

async def load_thousand_questions() -> List[Dict]:
    """Load the full thousand questions from file"""
    try:
        questions = []
        questions_file = "Prior_QA_Parts/Thousand_Questions.txt"
        
        with open(questions_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        question_id = 1
        for line in lines:
            line = line.strip()
            if line.endswith('?'):
                # Clean up the question text
                question_text = line.strip()
                if question_text.startswith('    '):
                    question_text = question_text[4:]
                
                questions.append({
                    "id": f"tq_{question_id:04d}",
                    "text": question_text
                })
                question_id += 1
        
        logger.info(f"Loaded {len(questions)} questions from {questions_file}")
        return questions
        
    except FileNotFoundError:
        logger.warning("Thousand Questions file not found, using sample questions")
        return []
    except Exception as e:
        logger.error(f"Error loading thousand questions: {e}")
        return []

# Initialize personality engine on module load
def initialize_personality_system():
    """Initialize the personality system"""
    try:
        engine = get_personality_engine()
        logger.info("Personality system initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize personality system: {e}")
        return False

# Auto-initialize when module is imported
initialize_personality_system()
