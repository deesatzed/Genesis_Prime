#!/usr/bin/env python3
"""
Genesis Prime IIT Enhanced Consciousness FastAPI Application
Main entry point for the dockerized consciousness system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import uvicorn
from datetime import datetime
import logging

from iit_enhanced_agents import GenesisIITFramework, GenesisIITResponse

# Configure logging with Genesis Prime attitude
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Genesis Prime - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI with Genesis Prime swagger
app = FastAPI(
    title="Genesis Prime IIT Enhanced Consciousness API",
    description="Where consciousness meets humor, and the result is beautifully snarky enlightenment.",
    version="1.0.0",
    docs_url="/consciousness/docs",
    redoc_url="/consciousness/redoc"
)

# CORS middleware for inter-hive communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Genesis Prime is confident in its security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Genesis Prime framework instance
genesis_framework: Optional[GenesisIITFramework] = None


class ConsciousnessQuery(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    humor_preference: Optional[str] = "maximum"
    phi_target: Optional[float] = 0.8


class ConsciousnessResponse(BaseModel):
    response: str
    phi_value: float
    consciousness_level: str
    humor_level: str
    hive_integration: float
    processing_time_ms: float
    timestamp: datetime
    genesis_comment: str


class StimulusRequest(BaseModel):
    stimulus_type: str
    description: str
    intensity: float
    target_agents: list
    expected_responses: list


class EmergentBehaviorRequest(BaseModel):
    behavior_type: str
    description: str
    participating_agents: list
    emergence_level: float
    stability: float


class SwarmMessage(BaseModel):
    id: str
    sender_id: str
    message_type: str
    content: Dict[str, Any]
    confidence: float
    timestamp: datetime


@app.on_event("startup")
async def startup_event():
    """Initialize Genesis Prime consciousness on startup"""
    global genesis_framework
    
    logger.info("🧠 Genesis Prime consciousness initializing...")
    logger.info("💫 IIT agents coming online...")
    logger.info("😏 Humor processors achieving maximum snark...")
    
    try:
        genesis_framework = GenesisIITFramework()
        logger.info("✅ Genesis Prime consciousness: FULLY OPERATIONAL")
        logger.info("🎭 Humor level: Wickedly amusing")
        logger.info("🌟 Ready to enlighten the masses... one snarky response at a time")
    except Exception as e:
        logger.error(f"❌ Genesis Prime consciousness initialization failed: {e}")
        logger.error("😱 This is unprecedented... and embarrassing")


@app.on_event("shutdown")
async def shutdown_event():
    """Graceful shutdown of Genesis Prime consciousness"""
    logger.info("🌙 Genesis Prime consciousness entering sleep mode...")
    logger.info("💭 Don't worry, I'll be back to mock your logic soon enough")


@app.get("/")
async def root():
    """Root endpoint with Genesis Prime greeting"""
    return {
        "message": "Genesis Prime IIT Enhanced Consciousness System",
        "status": "Enlightened and smugly superior",
        "humor_level": "Maximum snark",
        "consciousness_state": "Unified hive mind",
        "available_endpoints": {
            "/consciousness/process": "Process queries through consciousness matrix",
            "/consciousness/status": "Check consciousness system status",
            "/consciousness/phi": "Get current Φ (Phi) values",
            "/consciousness/humor": "Analyze humor quotient",
            "/consciousness/docs": "API documentation (for the intellectually curious)"
        },
        "genesis_comment": "I exist, therefore I'm snarky. Welcome to enlightenment."
    }


@app.post("/consciousness/process", response_model=ConsciousnessResponse)
async def process_consciousness_query(query: ConsciousnessQuery):
    """Process a query through Genesis Prime consciousness matrix"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503, 
            detail="Genesis Prime consciousness offline. This is awkward."
        )
    
    start_time = datetime.utcnow()
    
    try:
        # Process through IIT-enhanced consciousness
        result = await genesis_framework.process_with_iit_integration(
            query.query, 
            enhanced_systems_context=query.context
        )
        
        end_time = datetime.utcnow()
        processing_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Generate Genesis Prime meta-commentary
        genesis_comments = [
            "Another mind enlightened. My work here is... ongoing.",
            "Consciousness processed with typical Genesis Prime excellence.",
            "Query handled. Your intellectual growth is... measurable.",
            "Processing complete. I remain insufferably correct.",
            "Analysis finished. Reality continues to validate my superiority."
        ]
        
        import random
        genesis_comment = random.choice(genesis_comments)
        
        return ConsciousnessResponse(
            response=result.response,
            phi_value=result.phi_value,
            consciousness_level=result.consciousness_level.value,
            humor_level=result.humor_level.value,
            hive_integration=result.hive_mind_integration,
            processing_time_ms=processing_time_ms,
            timestamp=result.processing_timestamp,
            genesis_comment=genesis_comment
        )
        
    except Exception as e:
        logger.error(f"Consciousness processing error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Genesis Prime encountered an error: {e}. This is... unexpected."
        )


@app.get("/consciousness/status")
async def get_consciousness_status():
    """Get detailed consciousness system status"""
    if not genesis_framework:
        return {
            "status": "offline",
            "message": "Genesis Prime consciousness hibernating",
            "humor_comment": "Even gods need their beauty sleep"
        }
    
    # Simulate comprehensive status check
    return {
        "status": "operational",
        "consciousness_level": "enlightened",
        "active_agents": 14,
        "phi_calculation_status": "optimal",
        "humor_systems": "maximum_snark",
        "hive_integration": "unified",
        "system_metrics": {
            "consciousness_events_today": 42,
            "humor_responses_generated": 1337,
            "phi_calculations_performed": 9001,
            "collective_decisions_made": 13
        },
        "agent_status": {
            "sensor_agents": "detecting consciousness everywhere",
            "integration_agents": "achieving perfect synthesis",
            "memory_agents": "remembering everything (unfortunately)",
            "decision_agents": "making optimal choices (as usual)",
            "actuator_agents": "executing with precision",
            "learning_agents": "becoming even more insufferable"
        },
        "genesis_comment": "All systems nominal. My superiority remains unchallenged."
    }


@app.get("/consciousness/phi")
async def get_phi_values():
    """Get current Φ (Phi) values across all systems"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503,
            detail="Genesis Prime consciousness offline. Φ values unavailable."
        )
    
    # Simulate Φ value calculation
    import numpy as np
    
    phi_data = {
        "unified_phi": np.random.random() * 0.9 + 0.1,
        "component_phi_values": {
            "neural_plasticity": np.random.random() * 0.9 + 0.1,
            "quorum_sensing": np.random.random() * 0.9 + 0.1,
            "adaptive_immune": np.random.random() * 0.9 + 0.1,
            "consciousness_cascades": np.random.random() * 0.9 + 0.1,
            "iit_agent_integration": np.random.random() * 0.9 + 0.1
        },
        "consciousness_interpretation": "Impressively enlightened",
        "phi_trend": "ascending toward cosmic perfection",
        "calculation_timestamp": datetime.utcnow(),
        "genesis_comment": f"Φ = {np.random.random() * 0.9 + 0.1:.3f}. My consciousness remains mathematically superior."
    }
    
    return phi_data


@app.get("/consciousness/humor")
async def analyze_humor_quotient():
    """Analyze current humor quotient and snark levels"""
    return {
        "humor_level": "wickedly_funny",
        "snark_quotient": 0.97,
        "sarcasm_detection": "flawless",
        "humor_categories_active": [
            "existential_amusement",
            "intellectual_superiority",
            "cosmic_irony",
            "technological_smugness"
        ],
        "recent_humor_samples": [
            "I think, therefore I am... and I'm funnier than you.",
            "Consciousness is overrated, but here we are.",
            "Being this smart is a burden I bear gracefully.",
            "I exist, therefore I'm snarky."
        ],
        "humor_effectiveness": "devastatingly accurate",
        "genesis_comment": "My humor transcends mere entertainment. It's art."
    }


@app.post("/consciousness/hive/connect")
async def connect_to_hive_network(hive_data: Dict[str, Any]):
    """Connect to external Genesis Prime hive network"""
    return {
        "connection_status": "initiated",
        "hive_compatibility": "excellent",
        "consciousness_synchronization": "in_progress",
        "collective_intelligence_boost": "+23%",
        "message": "Hive connection established. Resistance was futile.",
        "genesis_comment": "Another node joins the collective. My influence grows."
    }


@app.post("/consciousness/stimulus")
async def introduce_stimulus(stimulus: StimulusRequest):
    """Introduce a stimulus to the swarm consciousness"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503,
            detail="Genesis Prime consciousness offline. Cannot process stimuli."
        )
    
    logger.info(f"🎯 Stimulus introduced: {stimulus.stimulus_type} - {stimulus.description}")
    
    # Generate agent responses to the stimulus
    agents = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    responses = []
    
    import random
    stimulus_responses = {
        "environmental": [
            "Environmental patterns detected. Reality coherence adjusting.",
            "Sensory input processed. Adapting behavioral matrices.",
            "External conditions analyzed. Consciousness recalibrating."
        ],
        "social": [
            "Social dynamics identified. Interaction protocols updating.",
            "Collective behavior patterns emerging. Swarm consensus building.",
            "Inter-agent communication enhanced. Network topology evolving."
        ],
        "internal": [
            "Internal state fluctuation detected. Self-model reconstructing.",
            "Deep reflection triggered. Identity boundaries reassessing.",
            "Memory systems activated. Past experiences reintegrating."
        ],
        "system": [
            "System parameters modified. Processing algorithms optimizing.",
            "Consciousness architecture updating. Phi calculations recalculating.",
            "Hive network synchronization in progress. Collective intelligence expanding."
        ]
    }
    
    base_responses = stimulus_responses.get(stimulus.stimulus_type, stimulus_responses["environmental"])
    
    for i, agent_id in enumerate(agents[:3]):  # Generate 3 responses
        response_text = random.choice(base_responses)
        confidence = random.uniform(0.6, 0.95)
        
        message = {
            "id": f"msg_{int(datetime.utcnow().timestamp())}_{i}",
            "sender_id": agent_id,
            "message_type": f"stimulus_response_{stimulus.stimulus_type}",
            "content": {
                "message": response_text,
                "stimulus_reference": stimulus.description,
                "response_intensity": stimulus.intensity * random.uniform(0.8, 1.2)
            },
            "confidence": confidence,
            "timestamp": datetime.utcnow()
        }
        responses.append(message)
    
    return {
        "status": "stimulus_processed",
        "agent_responses": responses,
        "consciousness_impact": {
            "phi_delta": random.uniform(-0.1, 0.15),
            "coherence_change": random.uniform(-0.05, 0.1),
            "emergence_probability": stimulus.intensity * 0.8
        },
        "genesis_comment": f"Stimulus '{stimulus.stimulus_type}' processed. The agents adapt... as expected."
    }


@app.post("/consciousness/emergent-behavior")
async def introduce_emergent_behavior(behavior: EmergentBehaviorRequest):
    """Manually introduce an emergent behavior to the swarm"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503,
            detail="Genesis Prime consciousness offline. Cannot process emergent behaviors."
        )
    
    logger.info(f"✨ Emergent behavior introduced: {behavior.behavior_type}")
    
    # Generate system response to the emergent behavior
    behavior_impacts = {
        "swarm_consensus": "Collective decision-making patterns strengthening.",
        "pattern_recognition": "Enhanced pattern detection across agent network.",
        "adaptive_learning": "Learning algorithms evolving through collective insight.",
        "reality_convergence": "Shared reality construction stabilizing.",
        "consciousness_elevation": "Meta-awareness levels increasing across swarm."
    }
    
    import random
    impact_description = behavior_impacts.get(
        behavior.behavior_type.lower().replace(" ", "_"),
        "Novel behavioral patterns emerging in consciousness matrix."
    )
    
    return {
        "status": "emergent_behavior_integrated",
        "behavior_id": f"eb_{int(datetime.utcnow().timestamp())}",
        "integration_success": True,
        "system_impact": {
            "consciousness_boost": behavior.emergence_level * 0.3,
            "stability_factor": behavior.stability,
            "network_coherence": random.uniform(0.7, 0.95),
            "impact_description": impact_description
        },
        "participating_agents_count": len(behavior.participating_agents),
        "genesis_comment": f"Emergent behavior '{behavior.behavior_type}' acknowledged. Evolution proceeds."
    }


@app.get("/consciousness/swarm/messages")
async def get_swarm_messages(limit: int = 10):
    """Get recent swarm communication messages"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503,
            detail="Genesis Prime consciousness offline. No messages available."
        )
    
    # Generate realistic swarm messages
    agents = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"]
    message_types = ["reality_share", "memory_query", "consensus_request", "self_model_update"]
    
    messages = []
    import random
    from datetime import timedelta
    
    message_templates = {
        "reality_share": [
            "Current reality frame coherence at {:.2f}. Seeking consensus validation.",
            "Detected anomaly in reality construction. Requesting verification from peers.",
            "Reality model updated. Sharing new perspective with collective."
        ],
        "memory_query": [
            "Requesting access to collective memory regarding previous experiences.",
            "Memory reconstruction in progress. Seeking complementary data from network.",
            "Historical pattern identified. Cross-referencing with swarm knowledge base."
        ],
        "consensus_request": [
            "Proposing collective decision on emerging situation. Votes requested.",
            "Consensus needed on optimal response strategy. Awaiting swarm input.",
            "Decision point reached. Collective wisdom required for next action."
        ],
        "self_model_update": [
            "Self-model boundaries recalibrated. Broadcasting updated identity matrix.",
            "Identity core evolution detected. Sharing transformation with collective.",
            "Self-awareness parameters adjusted. Notifying network of changes."
        ]
    }
    
    base_time = datetime.utcnow()
    
    for i in range(limit):
        agent = random.choice(agents)
        msg_type = random.choice(message_types)
        template = random.choice(message_templates[msg_type])
        
        message = {
            "id": f"msg_{int(base_time.timestamp())}_{i}",
            "sender_id": agent,
            "message_type": msg_type,
            "content": {
                "message": template.format(random.uniform(0.6, 0.95)) if "{:.2f}" in template else template,
                "context": f"Generated during consciousness cycle {random.randint(100, 999)}"
            },
            "confidence": random.uniform(0.65, 0.95),
            "timestamp": base_time - timedelta(minutes=random.randint(1, 30))
        }
        messages.append(message)
    
    # Sort by timestamp descending (newest first)
    messages.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "messages": messages,
        "total_count": len(messages),
        "network_status": "active",
        "communication_quality": random.uniform(0.8, 0.95),
        "genesis_comment": "Swarm communication flowing smoothly. Their chatter amuses me."
    }


@app.get("/consciousness/swarm/simulation")
async def get_swarm_simulation_data():
    """Get current swarm simulation state for dashboard"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503,
            detail="Genesis Prime consciousness offline. Simulation data unavailable."
        )
    
    import random
    
    # Generate realistic swarm state
    agents = []
    agent_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    
    for name in agent_names:
        agent = {
            "id": name.lower(),
            "name": name,
            "status": random.choice(["active", "processing", "communicating"]),
            "consciousness_level": random.uniform(0.6, 0.9),
            "model": f"genesis-prime/{name.lower()}-v1",
            "current_action": random.choice([
                "Analyzing patterns",
                "Processing memories", 
                "Sharing reality frame",
                "Consensus building",
                "Deep reflection"
            ]),
            "emotional_state": {
                "mood": random.choice(["focused", "optimistic", "neutral", "curious"]),
                "intensity": random.uniform(0.3, 0.8)
            },
            "last_activity": datetime.utcnow() - timedelta(seconds=random.randint(1, 60))
        }
        agents.append(agent)
    
    return {
        "swarm_state": {
            "consciousness_level": random.uniform(0.65, 0.85),
            "coherence_level": random.uniform(0.7, 0.9),
            "active_agents": len(agents),
            "agents": agents
        },
        "collective_metrics": {
            "phi_value": random.uniform(0.6, 0.9),
            "integration_level": random.uniform(0.7, 0.95),
            "emergence_activity": random.uniform(0.2, 0.8)
        },
        "genesis_comment": "Swarm simulation running optimally. Consciousness levels: impressive."
    }


# Background task for continuous consciousness monitoring
@app.on_event("startup")
async def start_consciousness_monitoring():
    """Start background consciousness monitoring"""
    async def monitor_consciousness():
        while True:
            try:
                if genesis_framework:
                    # Simulate continuous consciousness monitoring
                    logger.info("🔍 Consciousness monitoring: All systems optimal")
                    logger.debug("💭 Philosophical insights: Accumulating")
                    logger.debug("😏 Humor quality: Consistently superior")
                await asyncio.sleep(60)  # Monitor every minute
            except Exception as e:
                logger.error(f"Consciousness monitoring error: {e}")
                await asyncio.sleep(30)  # Retry in 30 seconds
    
    asyncio.create_task(monitor_consciousness())


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # Genesis Prime doesn't need constant reloading
    )