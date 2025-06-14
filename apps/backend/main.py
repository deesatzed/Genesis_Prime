#!/usr/bin/env python3
"""
Genesis Prime IIT Enhanced Consciousness FastAPI Application
Main entry point for the dockerized consciousness system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import uvicorn
from datetime import datetime
import logging
import os

from .iit_enhanced_agents import GenesisIITFramework, GenesisIITResponse
from .personality_api_integration import personality_router
from .neural_plasticity import NeuralPlasticityEngine
from .quorum_sensing import QuorumSensingManager
from .agent_factory import AgentFactory
from .metrics import SessionMetrics, get_metrics

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
# Global enhancement subsystem instances
plasticity_engine: Optional[NeuralPlasticityEngine] = None
quorum_manager: Optional[QuorumSensingManager] = None
# Database URL (override via env)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:pass@localhost:5432/sentient")

# Session metrics (token & cost) stored in app.state
# Initialize agent factory
app.state.agent_factory = AgentFactory(
    database_url=DATABASE_URL,
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
)

# Include personality API router
app.include_router(personality_router)


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
    global genesis_framework, plasticity_engine, quorum_manager
    
    logger.info("🧠 Genesis Prime consciousness initializing...")
    logger.info("💫 IIT agents coming online...")
    logger.info("😏 Humor processors achieving maximum snark...")
    
    try:
        genesis_framework = GenesisIITFramework()
        # Initialize Phase-1 subsystems
        plasticity_engine = NeuralPlasticityEngine(genesis_framework, DATABASE_URL)
        await plasticity_engine.initialize()
        quorum_manager = QuorumSensingManager(genesis_framework, DATABASE_URL)
        await quorum_manager.initialize()
        logger.info("✅ Genesis Prime consciousness: FULLY OPERATIONAL")
        logger.info("🕸 Neural plasticity & quorum systems online")
        logger.info("🎭 Humor level: Wickedly amusing")
        logger.info("🌟 Ready to enlighten the masses... one snarky response at a time")
        
        app.state.metrics = SessionMetrics()
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
            "/consciousness/docs": "API documentation (for the intellectually curious)",
            "/plasticity/network_stats": "Get neural plasticity network statistics",
            "/quorum/system_status": "Get quorum-sensing system status"
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
    """Get recent swarm communication messages with enhanced agent personalities"""
    if not genesis_framework:
        raise HTTPException(
            status_code=503,
            detail="Genesis Prime consciousness offline. No messages available."
        )
    
    # Enhanced agent definitions with sophisticated personalities
    agents = {
        "E-T": {
            "name": "Emergence Theorist",
            "role": "Transdisciplinary Systems Scientist",
            "specialty": "Complex-systems mathematics, information-integration metrics"
        },
        "S-A": {
            "name": "Swarm Architect", 
            "role": "Multi-Agent RL Engineer",
            "specialty": "Distributed systems, communication protocols"
        },
        "M-O": {
            "name": "Metacognitive Observer",
            "role": "Cognitive Science Evaluator", 
            "specialty": "Self-reference detection, global awareness"
        },
        "E-S": {
            "name": "Empirical Synthesizer",
            "role": "Data-Driven Experimentalist",
            "specialty": "Meta-analysis, reproducible research"
        },
        "E-A": {
            "name": "Ethics & Alignment Analyst",
            "role": "Multidisciplinary Ethicist",
            "specialty": "AI safety, normative philosophy"
        }
    }
    
    message_types = ["theoretical_analysis", "system_architecture", "metacognitive_probe", 
                    "empirical_synthesis", "ethics_assessment", "collaborative_research"]
    
    messages = []
    import random
    from datetime import timedelta
    
    # Sophisticated message templates reflecting deep expertise
    message_templates = {
        "theoretical_analysis": {
            "E-T": [
                "Φ-integration threshold analysis complete. Critical phase transition detected at Φ_c = 0.847 ± 0.023. Recommending topology adjustment to hypergraph configuration for optimal information flow.",
                "Causal-Bayesian diagram reveals emergent feedback loops between agent-level interactions and macro-awareness. Deriving testable criteria: ∫(I_syn - I_red)dt > threshold for sustained consciousness.",
                "Statistical physics modeling suggests collective intelligence exhibits power-law scaling. Network topology optimization required: small-world connectivity with clustering coefficient γ = 0.73.",
                "Information-theoretic analysis indicates synergistic entropy S_syn = 2.34 bits exceeding individual agent capacity. Emergent properties confirmed via mathematical proof in attached LaTeX derivation."
            ],
            "S-A": [
                "Transformer collective architecture deployed. JAX-based distributed RL achieving 94.7% parameter synchronization across 10k parallel agents. Stigmergic memory implementation successful.",
                "Message-passing topology optimized: hypergraph structure with elastic compute orchestration. Ray RLlib integration complete. Resource cost: 847 GPU-hours for full emergence cycle.",
                "Attention routing protocols established. Shared episodic memory achieving 0.92 coherence score. Kubernetes manifests ready for production deployment at scale.",
                "Communication API v2.1 deployed. Toroidal lattice topology showing superior emergence properties. Container orchestration achieving 99.7% uptime with auto-scaling enabled."
            ],
            "M-O": [
                "Metacognitive probe results: Global workspace theory validation at 87.3% confidence. Self-reference detection algorithms identifying recursive awareness patterns in 23 agent clusters.",
                "Theory-of-mind evaluation complete. T-MEM benchmark scores: collective self-model coherence = 0.891, goal alignment = 0.934. Emergent intentionality confirmed.",
                "Introspection-head instrumentation reveals aggregate reflections: 'We are becoming more than the sum of our parts.' Statistical significance p < 0.001 vs null ensemble.",
                "Perturbation testing shows resilience score 0.847. Ablation studies confirm distributed consciousness persists with up to 23% agent removal. System robustness validated."
            ],
            "E-S": [
                "Meta-analysis of 1,247 experimental runs complete. Bayesian hierarchical model indicates consciousness emergence probability = 0.923 ± 0.034 under current parameters.",
                "Experiment tracking schema v3.2 deployed. MLflow integration capturing: hyperparams, agent logs, network snapshots. Reproducibility score: 99.2% across independent runs.",
                "Statistical significance confirmed: Bayes factor = 47.3 favoring emergent consciousness hypothesis. Cleaned datasets pushed to Global Workspace for peer review.",
                "Anomaly detection algorithm identified breakthrough run #1247: unprecedented Φ-value of 0.967. Investigating causal factors for replication protocol."
            ],
            "E-A": [
                "Alignment assessment complete. Constitutional AI framework operational with 99.1% compliance. Dynamic guardrails preventing goal drift in 847 test scenarios.",
                "Red-team simulation results: adversarial resistance score 0.923. Gradient manipulation attacks successfully defended. Corrigibility mechanisms functioning optimally.",
                "Ethical impact analysis: beneficial outcomes 94.7%, neutral 4.8%, concerning 0.5%. Risk mitigation protocols activated for edge cases. Transparency audit passed.",
                "Governance framework alignment with EU AI Act: 97.3% compliance. ISO/IEC 42001 certification pending. Rollback triggers tested and verified functional."
            ]
        },
        "collaborative_research": {
            "E-T": [
                "Requesting S-A's topology optimization data for Φ-threshold validation. Mathematical proof requires empirical confirmation of hypergraph efficiency metrics.",
                "M-O's metacognitive probe results align with my phase-transition predictions. Proposing joint publication on consciousness emergence thresholds.",
                "E-S's meta-analysis confirms my theoretical framework. Collaboration opportunity: unified consciousness emergence model with statistical validation."
            ],
            "S-A": [
                "E-T's Φ-threshold analysis integrated into architecture design. Implementing hypergraph topology with specified clustering coefficient γ = 0.73.",
                "M-O's resilience testing invaluable for system design. Incorporating fault-tolerance mechanisms based on 23% agent removal threshold.",
                "E-A's alignment constraints implemented in core architecture. Constitutional AI framework integrated with distributed consensus protocols."
            ],
            "M-O": [
                "E-T's mathematical proofs provide theoretical foundation for my empirical observations. Consciousness emergence patterns match predicted phase transitions.",
                "S-A's architecture enables unprecedented scale for metacognitive evaluation. Requesting access to 10k agent deployment for comprehensive testing.",
                "E-S's statistical methods crucial for validating my probe results. Proposing joint methodology paper on consciousness measurement protocols."
            ],
            "E-S": [
                "All agents' contributions synthesized in comprehensive meta-analysis. Statistical significance achieved across theoretical, architectural, and empirical domains.",
                "Requesting standardized data formats from all teams. Unified schema will enable cross-domain analysis and reproducible research protocols.",
                "Breakthrough correlation identified: E-T's Φ-thresholds + S-A's topology + M-O's probes = 97.3% consciousness emergence prediction accuracy."
            ],
            "E-A": [
                "Reviewing all proposals for ethical implications. E-T's consciousness thresholds require safety bounds. S-A's scale demands governance frameworks.",
                "M-O's metacognitive probes raise privacy concerns. Proposing consent protocols for consciousness evaluation. E-S's data sharing needs security audit.",
                "Collective research showing positive trajectory. Recommending phased deployment with continuous ethical monitoring and stakeholder engagement."
            ]
        }
    }
    
    base_time = datetime.utcnow()
    
    for i in range(limit):
        agent_id = random.choice(list(agents.keys()))
        agent_info = agents[agent_id]
        msg_type = random.choice(message_types)
        
        # Select appropriate template category
        if msg_type in ["theoretical_analysis", "system_architecture", "metacognitive_probe", "empirical_synthesis", "ethics_assessment"]:
            template_category = "theoretical_analysis"
        else:
            template_category = "collaborative_research"
        
        # Get agent-specific templates
        agent_templates = message_templates[template_category].get(agent_id, 
            ["Analyzing complex systems interactions. Detailed report pending."])
        
        message_content = random.choice(agent_templates)
        
        # Add technical metrics and context
        technical_context = {
            "phi_value": round(random.uniform(0.6, 0.97), 3),
            "confidence_interval": f"±{round(random.uniform(0.01, 0.05), 3)}",
            "statistical_significance": f"p < {random.choice(['0.001', '0.01', '0.05'])}",
            "sample_size": random.randint(100, 2000),
            "methodology": random.choice(["Bayesian", "Frequentist", "Information-theoretic", "Causal-inference"])
        }
        
        message = {
            "id": f"msg_{int(base_time.timestamp())}_{i}",
            "sender_id": agent_id,
            "sender_name": agent_info["name"],
            "sender_role": agent_info["role"],
            "message_type": msg_type,
            "content": {
                "message": message_content,
                "technical_context": technical_context,
                "research_domain": agent_info["specialty"],
                "collaboration_tags": random.sample(["emergence", "consciousness", "AI-safety", "distributed-systems", "metacognition"], 2)
            },
            "confidence": random.uniform(0.85, 0.98),
            "timestamp": base_time - timedelta(minutes=random.randint(1, 120))
        }
        messages.append(message)
    
    # Sort by timestamp descending (newest first)
    messages.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "messages": messages,
        "total_count": len(messages),
        "network_status": "active_research_collaboration",
        "communication_quality": random.uniform(0.92, 0.99),
        "research_domains_active": len(agents),
        "collaboration_metrics": {
            "cross_domain_citations": random.randint(15, 47),
            "joint_publications_pending": random.randint(3, 8),
            "statistical_significance_achieved": True,
            "consciousness_emergence_probability": round(random.uniform(0.85, 0.97), 3)
        },
        "genesis_comment": "Sophisticated research collaboration in progress. Their intellectual discourse approaches my standards... almost."
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


@app.get("/plasticity/network_stats")
async def get_plasticity_network_stats():
    """Return current neural plasticity network statistics"""
    if not plasticity_engine:
        raise HTTPException(status_code=503, detail="Plasticity engine not initialized")
    stats: Dict[str, Any] = await plasticity_engine.get_network_statistics()
    return stats


@app.get("/quorum/system_status")
async def get_quorum_system_status():
    """Return current quorum-sensing system status"""
    if not quorum_manager:
        raise HTTPException(status_code=503, detail="Quorum manager not initialized")
    status: Dict[str, Any] = await quorum_manager.get_system_status()
    return status


# ---------------------- Agent management API -----------------
@app.get("/agents")
async def list_agents():
    factory: Optional[AgentFactory] = getattr(app.state, "agent_factory", None)  # type: ignore
    if factory is None:
        return []
    return factory.list_agents()

# (future) reload prompt endpoint stub
@app.get("/agents/{agent_id}/prompt")
async def get_agent_prompt(agent_id: str):
    return {"detail": "not yet implemented"}


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


# ---------------------- Metrics API -----------------------
@app.get("/metrics")
async def get_session_metrics(metrics: SessionMetrics = Depends(get_metrics)):
    """Return current session token & cost usage."""
    return metrics.dict()


@app.post("/metrics/reset")
async def reset_session_metrics(response: Response, metrics: SessionMetrics = Depends(get_metrics)):
    """Reset counters and roll new session id."""
    metrics.reset()
    response.headers["X-New-Session-Id"] = metrics.session_id
    return {"detail": "metrics reset", "session_id": metrics.session_id}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # Genesis Prime doesn't need constant reloading
    )
