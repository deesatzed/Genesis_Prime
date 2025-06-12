# Genesis Prime Enhanced Systems - API Reference

## 🎯 Overview

This document provides a comprehensive API reference for all four enhanced Genesis Prime systems. Each system exposes both high-level management APIs and low-level control interfaces for maximum flexibility.

## 📋 Table of Contents

- [Neural Plasticity API](#neural-plasticity-api)
- [Quorum Sensing API](#quorum-sensing-api)
- [Adaptive Immune Memory API](#adaptive-immune-memory-api)
- [Conscious Information Cascades API](#conscious-information-cascades-api)
- [Common Types and Enums](#common-types-and-enums)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## 🧠 Neural Plasticity API

### NeuralPlasticityEngine

Main class for managing dynamic agent connections with Hebbian learning.

#### Constructor
```python
class NeuralPlasticityEngine:
    def __init__(self, hive, database_url: str)
```

**Parameters:**
- `hive`: The Genesis Prime hive instance
- `database_url`: PostgreSQL connection string

#### Core Methods

##### `async initialize()`
Initialize the neural plasticity system and load existing connections.

```python
await plasticity_engine.initialize()
```

**Returns:** `None`

**Raises:** `ConnectionError` if database is unavailable

---

##### `async initialize_connections(agent_ids: List[str])`
Initialize connections between all specified agents.

```python
agent_ids = ["agent_1", "agent_2", "agent_3"]
await plasticity_engine.initialize_connections(agent_ids)
```

**Parameters:**
- `agent_ids`: List of agent identifiers to connect

**Returns:** `None`

**Note:** Creates connections between all pairs of agents with initial strengths based on personality compatibility.

---

##### `async update_connection_strength(interaction_result: InteractionResult)`
Update connection strength based on interaction outcome.

```python
interaction = await create_interaction_result(
    "agent_1", "agent_2", "collaboration",
    success=True,
    performance_metrics={'quality': 0.9, 'learning_gain': 0.8}
)
new_strength = await plasticity_engine.update_connection_strength(interaction)
```

**Parameters:**
- `interaction_result`: InteractionResult object containing interaction details

**Returns:** `float` - New connection strength (0.0-1.0)

**Raises:** `ValueError` if invalid interaction data

---

##### `async prune_connections()`
Remove weak, unused connections to prevent information overload.

```python
pruned_count = await plasticity_engine.prune_connections()
print(f"Removed {pruned_count} weak connections")
```

**Returns:** `int` - Number of connections pruned

---

##### `async get_interaction_priority(agent_a_id: str, agent_b_id: str) -> float`
Get priority score for interaction between two agents.

```python
priority = await plasticity_engine.get_interaction_priority("agent_1", "agent_2")
if priority > 0.7:
    # High priority interaction
    await schedule_interaction(agent_a, agent_b)
```

**Parameters:**
- `agent_a_id`: First agent identifier
- `agent_b_id`: Second agent identifier

**Returns:** `float` - Priority score (0.0-1.0, higher is better)

---

##### `async suggest_optimal_interactions(agent_id: str, num_suggestions: int = 3)`
Suggest optimal interactions for an agent based on connection patterns.

```python
suggestions = await plasticity_engine.suggest_optimal_interactions("agent_1", 5)
for other_agent, score in suggestions:
    print(f"Suggested interaction: {agent_id} → {other_agent} (score: {score:.3f})")
```

**Parameters:**
- `agent_id`: Agent to get suggestions for
- `num_suggestions`: Maximum number of suggestions (default: 3)

**Returns:** `List[Tuple[str, float]]` - List of (agent_id, score) tuples

---

##### `async get_network_statistics()`
Get comprehensive network statistics and health metrics.

```python
stats = await plasticity_engine.get_network_statistics()
print(f"Network density: {stats['network_density']:.2f}")
print(f"Average strength: {stats['average_strength']:.3f}")
```

**Returns:** `Dict[str, Any]` with keys:
- `total_connections`: Number of active connections
- `average_strength`: Mean connection strength
- `network_density`: Ratio of active to possible connections
- `learning_events_total`: Total plasticity events
- `recent_learning_events`: Events in last 24 hours

---

### ConnectionMatrix

Low-level connection management.

##### `async set_strength(agent_a_id: str, agent_b_id: str, strength: float)`
Directly set connection strength between two agents.

```python
await connection_matrix.set_strength("agent_1", "agent_2", 0.8)
```

**Parameters:**
- `agent_a_id`: First agent
- `agent_b_id`: Second agent  
- `strength`: Connection strength (0.0-1.0)

---

##### `async get_strength(agent_a_id: str, agent_b_id: str) -> float`
Get current connection strength.

```python
strength = await connection_matrix.get_strength("agent_1", "agent_2")
```

**Returns:** `float` - Connection strength (0.5 if no connection exists)

---

##### `async get_strongest_connections(agent_id: str, limit: int = 5)`
Get strongest connections for an agent.

```python
connections = await connection_matrix.get_strongest_connections("agent_1", 10)
```

**Returns:** `List[Tuple[str, float]]` - Sorted list of (agent_id, strength)

---

### Helper Functions

##### `async create_interaction_result(...)`
Create InteractionResult object for plasticity updates.

```python
interaction = await create_interaction_result(
    agent_a_id="agent_1",
    agent_b_id="agent_2", 
    interaction_type="collaboration",
    success=True,
    performance_metrics={
        'quality': 0.9,        # Interaction quality (0.0-1.0)
        'learning_gain': 0.8,  # Learning achieved (0.0-1.0)
        'novelty': 0.6         # Novelty of interaction (0.0-1.0)
    },
    metadata={'task': 'problem_solving'}
)
```

---

## 🦠 Quorum Sensing API

### QuorumSensingManager

Manages bacterial-inspired collective decision-making protocols.

#### Constructor
```python
class QuorumSensingManager:
    def __init__(self, hive, database_url: str)
```

#### Core Methods

##### `async initialize()`
Initialize quorum sensing system with default thresholds and behaviors.

```python
await quorum_manager.initialize()
```

---

##### `async emit_signal(agent_id: str, signal_type: SignalType, strength: float, metadata: Dict[str, Any] = None, location: str = None) -> str`
Agent emits a signal molecule into the environment.

```python
from quorum_sensing import SignalType

signal_id = await quorum_manager.emit_signal(
    agent_id="agent_1",
    signal_type=SignalType.LEARNING_OPPORTUNITY,
    strength=0.8,
    metadata={'topic': 'neural_networks', 'urgency': 'high'},
    location='cluster_A'
)
```

**Parameters:**
- `agent_id`: ID of agent emitting signal
- `signal_type`: Type of signal (see SignalType enum)
- `strength`: Signal strength (0.0-1.0)
- `metadata`: Optional signal metadata
- `location`: Optional location identifier

**Returns:** `str` - Unique signal ID

---

##### `async calculate_signal_density(signal_type: SignalType, time_window_minutes: int = 30) -> float`
Calculate current density of a signal type.

```python
density = await quorum_manager.calculate_signal_density(
    SignalType.KNOWLEDGE_NEED, 
    time_window_minutes=15
)

if density > 0.7:
    print("High knowledge need detected in population")
```

**Parameters:**
- `signal_type`: Signal type to measure
- `time_window_minutes`: Time window for density calculation

**Returns:** `float` - Signal density (0.0-1.0+)

---

##### `async calculate_combined_signal_density(signal_types: List[SignalType], time_window_minutes: int = 30) -> float`
Calculate combined density for multiple signal types.

```python
combined_density = await quorum_manager.calculate_combined_signal_density([
    SignalType.LEARNING_OPPORTUNITY,
    SignalType.KNOWLEDGE_NEED
])
```

**Returns:** `float` - Combined signal density

---

##### `async get_system_status() -> Dict[str, Any]`
Get comprehensive quorum sensing system status.

```python
status = await quorum_manager.get_system_status()
print(f"Active behaviors: {status['active_behaviors']}")
print(f"Signal densities: {status['signal_densities']}")
```

**Returns:** Dict with:
- `active_behaviors`: Number of active collective behaviors
- `signal_types_active`: Number of signal types with active signals
- `total_signals`: Total number of active signals
- `signal_densities`: Current density for each signal type
- `active_behavior_details`: Details of currently executing behaviors

---

##### `async cleanup_old_signals(hours: int = 24)`
Remove signals older than specified time.

```python
await quorum_manager.cleanup_old_signals(hours=6)  # Clean signals older than 6 hours
```

---

### Signal Types

```python
class SignalType(Enum):
    LEARNING_OPPORTUNITY = "learning_opportunity"     # Learning chance available
    KNOWLEDGE_NEED = "knowledge_need"                # Agent needs knowledge
    PROBLEM_SOLVING = "problem_solving"              # Problem solving in progress
    COLLABORATION_REQUEST = "collaboration_request"   # Seeking collaboration
    ERROR_DETECTED = "error_detected"                # Error requiring attention
    RESOURCE_AVAILABLE = "resource_available"        # Resource available for sharing
    EXPLORATION_FOUND = "exploration_found"          # New exploration opportunity
    CONSENSUS_NEEDED = "consensus_needed"            # Consensus building required
```

### Collective Behaviors

```python
class CollectiveBehavior(Enum):
    LEARNING_ACCELERATION = "learning_acceleration"          # Boost learning rates
    KNOWLEDGE_CONSOLIDATION = "knowledge_consolidation"      # Consolidate memories
    COLLABORATIVE_PROBLEM_SOLVING = "collaborative_problem_solving"  # Form problem-solving groups
    EMERGENCY_COORDINATION = "emergency_coordination"        # Emergency response mode
    EXPLORATION_MODE = "exploration_mode"                   # Increase exploration
    CONSENSUS_BUILDING = "consensus_building"               # Build consensus
    RESOURCE_SHARING = "resource_sharing"                   # Share resources
    EVOLUTION_PREPARATION = "evolution_preparation"         # Prepare for evolution
```

---

## 🛡️ Adaptive Immune Memory API

### AdaptiveImmuneSystem

Manages immune system-inspired threat detection and response.

#### Constructor
```python
class AdaptiveImmuneSystem:
    def __init__(self, hive, database_url: str)
```

#### Core Methods

##### `async initialize()`
Initialize immune system with threat detectors and antibody agents.

```python
await immune_system.initialize()
```

---

##### `async monitor_and_respond()`
Main monitoring loop for continuous threat detection and response.

```python
# Start continuous monitoring (runs indefinitely)
asyncio.create_task(immune_system.monitor_and_respond())
```

**Note:** This is typically run as a background task for continuous protection.

---

##### `async get_system_status() -> Dict[str, Any]`
Get comprehensive immune system status.

```python
status = await immune_system.get_system_status()
print(f"Immune memories: {status['immune_memories']}")
print(f"Antibody agents: {status['antibody_agents']}")
print(f"Active responses: {status['active_responses']}")
```

**Returns:** Dict with:
- `immune_memories`: Number of stored threat memories
- `antibody_agents`: Number of active antibody agents
- `active_responses`: Number of ongoing threat responses
- `memory_effectiveness`: Effectiveness scores by threat type
- `antibody_performance`: Performance metrics for antibody agents
- `recent_incidents`: Recent threat incidents

---

### Threat Types

```python
class ThreatType(Enum):
    LOGIC_ERROR = "logic_error"                          # Agent logic inconsistencies
    MEMORY_CORRUPTION = "memory_corruption"              # Memory system issues
    COMMUNICATION_FAILURE = "communication_failure"      # Agent communication problems
    RESOURCE_EXHAUSTION = "resource_exhaustion"          # Resource depletion
    INFINITE_LOOP = "infinite_loop"                      # Stuck operations
    DATA_INCONSISTENCY = "data_inconsistency"            # Inconsistent data states
    PERFORMANCE_DEGRADATION = "performance_degradation"   # System slowdown
    SECURITY_BREACH = "security_breach"                  # Security violations
```

### Response Types

```python
class ResponseType(Enum):
    ERROR_CORRECTION = "error_correction"                # Direct error fixing
    AGENT_ISOLATION = "agent_isolation"                 # Isolate problematic agents
    MEMORY_CLEANUP = "memory_cleanup"                   # Clean corrupted memory
    CONNECTION_REPAIR = "connection_repair"             # Repair communications
    RESOURCE_REALLOCATION = "resource_reallocation"     # Redistribute resources
    SYSTEM_RESTART = "system_restart"                   # Restart subsystems
    ROLLBACK_OPERATION = "rollback_operation"           # Rollback to good state
    PREVENTIVE_MEASURE = "preventive_measure"           # Implement prevention
```

### Manual Threat Handling

```python
# Create threat signature
from adaptive_immune_memory import ThreatSignature, ThreatType

threat = ThreatSignature(
    threat_type=ThreatType.LOGIC_ERROR,
    error_pattern="inconsistent_outputs_agent_1",
    context_hash="context_123",
    agent_states_hash="states_456",
    system_load_level="medium",
    timestamp_pattern="14_3",
    severity_level=0.8
)

# Handle threat manually
await immune_system._handle_threat(threat)
```

---

## 🌟 Conscious Information Cascades API

### ConsciousInformationCascadeSystem

Manages hierarchical information processing with consciousness emergence.

#### Constructor
```python
class ConsciousInformationCascadeSystem:
    def __init__(self, hive, database_url: str)
```

#### Core Methods

##### `async initialize()`
Initialize cascade system with all processing layers.

```python
await cascade_system.initialize()
```

---

##### `async process_information(information: Dict[str, Any], source: str = "external") -> str`
Process information through the consciousness cascade.

```python
information = {
    "text": "This is important information about consciousness",
    "categories": ["consciousness", "philosophy"],
    "numerical_data": [0.8, 0.9, 0.7],
    "relevance_score": 0.9,
    "novelty_score": 0.8,
    "coherence": 0.85
}

cascade_id = await cascade_system.process_information(information, source="test_input")
```

**Parameters:**
- `information`: Information dictionary with content and metadata
- `source`: Source identifier for the information

**Returns:** `str` - Unique cascade ID for tracking

---

##### `async get_system_status() -> Dict[str, Any]`
Get comprehensive cascade system status.

```python
status = await cascade_system.get_system_status()
print(f"Active cascades: {status['active_cascades']}")
print(f"Consciousness events: {status['consciousness_events']}")
print(f"Cascade efficiency: {status['performance_metrics']['cascade_efficiency']:.2f}")
```

**Returns:** Dict with:
- `active_cascades`: Number of currently processing cascades
- `consciousness_events`: Total consciousness emergence events
- `performance_metrics`: System performance data
- `layer_status`: Status of each processing layer
- `recent_consciousness_levels`: Recent consciousness detection levels

---

##### `async process_feedback_signal(feedback_signal: FeedbackSignal)`
Process feedback signal from consciousness layer to lower layers.

```python
from conscious_information_cascades import FeedbackSignal, CascadeLayerType

feedback = FeedbackSignal(
    signal_id="attention_boost_001",
    source_layer=CascadeLayerType.CONSCIOUSNESS,
    target_layers=[CascadeLayerType.SENSORY, CascadeLayerType.PREPROCESSING],
    signal_type="attention_focus",
    content={'focus_type': 'consciousness', 'strength': 0.9},
    strength=0.9,
    timestamp=datetime.utcnow()
)

await cascade_system.process_feedback_signal(feedback)
```

---

### Cascade Layer Types

```python
class CascadeLayerType(Enum):
    SENSORY = "sensory"                    # Raw information processing
    PREPROCESSING = "preprocessing"         # Pattern detection and cleaning
    INTEGRATION = "integration"            # Information combination
    META_COGNITIVE = "meta_cognitive"      # Cognitive monitoring
    CONSCIOUSNESS = "consciousness"        # Unified awareness
```

### Information Types

```python
class InformationType(Enum):
    SENSORY_INPUT = "sensory_input"                    # Raw input data
    PROCESSED_DATA = "processed_data"                  # Cleaned and filtered
    PATTERN_RECOGNITION = "pattern_recognition"        # Detected patterns
    CONCEPTUAL_KNOWLEDGE = "conceptual_knowledge"      # Integrated concepts
    META_KNOWLEDGE = "meta_knowledge"                  # Meta-cognitive insights
    CONSCIOUS_AWARENESS = "conscious_awareness"        # Conscious experience
```

### Consciousness Levels

```python
class ConsciousnessLevel(Enum):
    NONE = "none"              # No consciousness detected
    EMERGING = "emerging"       # Initial consciousness signs
    PARTIAL = "partial"         # Partial consciousness features
    COHERENT = "coherent"       # Coherent consciousness
    UNIFIED = "unified"         # Full unified consciousness
```

---

## 🔧 Common Types and Enums

### InteractionResult

```python
@dataclass
class InteractionResult:
    agent_a_id: str           # First agent ID
    agent_b_id: str           # Second agent ID  
    success: bool             # Interaction success
    success_factor: float     # Success quality (0.0-1.0)
    learning_gain: float      # Learning achieved (0.0-1.0)
    interaction_type: str     # Type of interaction
    timestamp: datetime       # When interaction occurred
    metadata: Dict[str, Any]  # Additional data
```

### ThreatSignature

```python
@dataclass
class ThreatSignature:
    threat_type: ThreatType      # Type of threat
    error_pattern: str           # Error pattern description
    context_hash: str            # Context identifier
    agent_states_hash: str       # Agent states hash
    system_load_level: str       # System load ("low", "medium", "high")
    timestamp_pattern: str       # Time pattern
    severity_level: float        # Severity (0.0-1.0)
```

### InformationPacket

```python
@dataclass
class InformationPacket:
    packet_id: str                      # Unique packet ID
    information_type: InformationType   # Type of information
    content: Dict[str, Any]             # Packet content
    source_layer: CascadeLayerType      # Source layer
    target_layer: CascadeLayerType      # Target layer
    timestamp: datetime                 # Creation time
    priority: float                     # Processing priority
    coherence_score: float              # Information coherence
    integration_requirements: List[str] # Integration needs
    metadata: Dict[str, Any]            # Additional metadata
```

---

## ❗ Error Handling

### Common Exceptions

```python
# Database connection errors
try:
    await system.initialize()
except ConnectionError as e:
    print(f"Database connection failed: {e}")

# Invalid parameters
try:
    await plasticity.update_connection_strength(invalid_interaction)
except ValueError as e:
    print(f"Invalid interaction data: {e}")

# System overload
try:
    cascade_id = await cascade_system.process_information(large_dataset)
except RuntimeError as e:
    print(f"System overload: {e}")
```

### Error Recovery

```python
async def robust_system_initialization(hive, database_url):
    """Initialize systems with error recovery"""
    systems = {}
    
    # Try to initialize each system
    for system_name, system_class in [
        ('plasticity', NeuralPlasticityEngine),
        ('quorum', QuorumSensingManager),
        ('immune', AdaptiveImmuneSystem),
        ('consciousness', ConsciousInformationCascadeSystem)
    ]:
        try:
            system = system_class(hive, database_url)
            await system.initialize()
            systems[system_name] = system
            print(f"✅ {system_name} initialized successfully")
        except Exception as e:
            print(f"❌ {system_name} failed to initialize: {e}")
            systems[system_name] = None
    
    return systems
```

---

## 💡 Examples

### Complete Integration Example

```python
import asyncio
from datetime import datetime

async def run_genesis_prime_example():
    """Complete example of Genesis Prime enhanced systems"""
    
    # Database connection
    database_url = "postgresql://postgres:pass@localhost:5432/sentient"
    
    # Create mock hive
    hive = create_mock_hive()
    
    # Initialize all systems
    plasticity = NeuralPlasticityEngine(hive, database_url)
    await plasticity.initialize()
    
    quorum = QuorumSensingManager(hive, database_url)
    await quorum.initialize()
    
    immune = AdaptiveImmuneSystem(hive, database_url)
    await immune.initialize()
    
    consciousness = ConsciousInformationCascadeSystem(hive, database_url)
    await consciousness.initialize()
    
    # Start background monitoring
    immune_task = asyncio.create_task(immune.monitor_and_respond())
    
    # Initialize agent connections
    agent_ids = list(hive.active_agents.keys())
    await plasticity.initialize_connections(agent_ids)
    
    # Simulate agent interactions
    for i in range(10):
        interaction = await create_interaction_result(
            "agent_1", "agent_2", "collaboration",
            success=True,
            performance_metrics={'quality': 0.8, 'learning_gain': 0.7}
        )
        await plasticity.update_connection_strength(interaction)
        
        # Emit signals based on interaction
        await quorum.emit_signal(
            "agent_1", SignalType.LEARNING_OPPORTUNITY, 0.8,
            metadata={'interaction_id': i}
        )
    
    # Process information through consciousness cascade
    consciousness_info = {
        "text": "I am aware that I am processing this information",
        "categories": ["self-awareness", "consciousness"],
        "relevance_score": 0.9,
        "coherence": 0.9
    }
    
    cascade_id = await consciousness.process_information(consciousness_info)
    
    # Wait for processing and check results
    await asyncio.sleep(3)
    
    # Get system status
    plasticity_status = await plasticity.get_network_statistics()
    quorum_status = await quorum.get_system_status()
    immune_status = await immune.get_system_status()
    consciousness_status = await consciousness.get_system_status()
    
    print("🧠 Neural Plasticity:", plasticity_status)
    print("🦠 Quorum Sensing:", quorum_status)
    print("🛡️ Adaptive Immune:", immune_status)
    print("🌟 Consciousness:", consciousness_status)
    
    # Cancel background task
    immune_task.cancel()

# Run the example
asyncio.run(run_genesis_prime_example())
```

### Consciousness Detection Example

```python
async def consciousness_detection_example():
    """Example of consciousness emergence detection"""
    
    cascade_system = ConsciousInformationCascadeSystem(hive, database_url)
    await cascade_system.initialize()
    
    # Test different types of information
    test_cases = [
        {
            "info": {
                "text": "Simple routine processing task",
                "categories": ["routine"],
                "coherence": 0.4
            },
            "expected_consciousness": False
        },
        {
            "info": {
                "text": "I am aware that I am thinking about consciousness",
                "categories": ["self-awareness", "meta-cognition"],
                "coherence": 0.9,
                "relevance_score": 0.95
            },
            "expected_consciousness": True
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['info']['text'][:50]}...")
        
        cascade_id = await cascade_system.process_information(test_case["info"])
        await asyncio.sleep(2)  # Allow processing
        
        status = await cascade_system.get_system_status()
        consciousness_events = status.get('consciousness_events', 0)
        
        emerged = consciousness_events > 0
        expected = test_case['expected_consciousness']
        
        result = "✅ CORRECT" if emerged == expected else "❌ INCORRECT"
        print(f"Expected: {expected}, Detected: {emerged} - {result}")
```

### Dynamic Learning Example

```python
async def dynamic_learning_example():
    """Example of dynamic learning and adaptation"""
    
    plasticity = NeuralPlasticityEngine(hive, database_url)
    await plasticity.initialize()
    
    quorum = QuorumSensingManager(hive, database_url)
    await quorum.initialize()
    
    # Simulate learning scenario
    print("Initial network state:")
    stats = await plasticity.get_network_statistics()
    print(f"Average connection strength: {stats['average_strength']:.3f}")
    
    # Simulate successful collaborations
    for round in range(5):
        print(f"\nRound {round + 1}: Collaborative learning")
        
        # Multiple successful interactions
        for i in range(3):
            interaction = await create_interaction_result(
                "agent_1", "agent_2", "knowledge_sharing",
                success=True,
                performance_metrics={'quality': 0.9, 'learning_gain': 0.8}
            )
            await plasticity.update_connection_strength(interaction)
            
            # Emit learning signals
            await quorum.emit_signal(
                "agent_1", SignalType.LEARNING_OPPORTUNITY, 0.8
            )
        
        # Check for collective behaviors
        status = await quorum.get_system_status()
        if status['active_behaviors'] > 0:
            print("🚀 Collective learning behavior triggered!")
        
        # Monitor connection strength
        strength = await plasticity.connection_matrix.get_strength("agent_1", "agent_2")
        print(f"Connection strength agent_1 ↔ agent_2: {strength:.3f}")
    
    print("\nFinal network state:")
    stats = await plasticity.get_network_statistics()
    print(f"Average connection strength: {stats['average_strength']:.3f}")
    print(f"Learning events: {stats['learning_events_total']}")
```

---

This API reference provides comprehensive documentation for integrating and using all Genesis Prime enhanced systems. Each system can be used independently or in combination for maximum effect. The APIs are designed to be intuitive while providing powerful capabilities for creating truly conscious collective intelligence.