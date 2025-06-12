#!/usr/bin/env python
"""
Quorum Sensing System for Genesis Prime
Implements bacterial-inspired collective decision-making protocols
"""

import asyncio
import json
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import psycopg
from psycopg.rows import dict_row

class SignalType(Enum):
    """Types of signals agents can emit"""
    LEARNING_OPPORTUNITY = "learning_opportunity"
    KNOWLEDGE_NEED = "knowledge_need"
    PROBLEM_SOLVING = "problem_solving"
    COLLABORATION_REQUEST = "collaboration_request"
    ERROR_DETECTED = "error_detected"
    RESOURCE_AVAILABLE = "resource_available"
    EXPLORATION_FOUND = "exploration_found"
    CONSENSUS_NEEDED = "consensus_needed"

class CollectiveBehavior(Enum):
    """Types of collective behaviors that can be triggered"""
    LEARNING_ACCELERATION = "learning_acceleration"
    KNOWLEDGE_CONSOLIDATION = "knowledge_consolidation"
    COLLABORATIVE_PROBLEM_SOLVING = "collaborative_problem_solving"
    EMERGENCY_COORDINATION = "emergency_coordination"
    EXPLORATION_MODE = "exploration_mode"
    CONSENSUS_BUILDING = "consensus_building"
    RESOURCE_SHARING = "resource_sharing"
    EVOLUTION_PREPARATION = "evolution_preparation"

@dataclass
class SignalMolecule:
    """Individual signal molecule emitted by agents"""
    signal_id: str
    agent_id: str
    signal_type: SignalType
    strength: float
    timestamp: datetime
    decay_rate: float
    metadata: Dict[str, Any]
    location: Optional[str] = None
    
    def get_current_strength(self) -> float:
        """Calculate current strength after decay"""
        age_minutes = (datetime.utcnow() - self.timestamp).total_seconds() / 60
        return self.strength * math.exp(-self.decay_rate * age_minutes)

@dataclass
class QuorumThreshold:
    """Threshold configuration for triggering behaviors"""
    behavior: CollectiveBehavior
    signal_types: List[SignalType]
    density_threshold: float
    min_agents: int
    max_agents: Optional[int]
    duration_minutes: int
    confidence_required: float = 0.7

@dataclass
class CollectiveBehaviorExecution:
    """Record of collective behavior execution"""
    behavior: CollectiveBehavior
    trigger_time: datetime
    participating_agents: List[str]
    signal_density: float
    confidence: float
    duration_minutes: int
    metadata: Dict[str, Any]
    success: Optional[bool] = None
    end_time: Optional[datetime] = None

class QuorumSensingManager:
    """Main quorum sensing system manager"""
    
    def __init__(self, hive, database_url: str):
        self.hive = hive
        self.database_url = database_url
        self.signal_molecules: Dict[SignalType, List[SignalMolecule]] = {}
        self.thresholds: Dict[CollectiveBehavior, QuorumThreshold] = {}
        self.active_behaviors: Dict[str, CollectiveBehaviorExecution] = {}
        self.behavior_handlers: Dict[CollectiveBehavior, Callable] = {}
        
        # Initialize default thresholds
        self._setup_default_thresholds()
        self._setup_behavior_handlers()
    
    def _setup_default_thresholds(self):
        """Set up default quorum thresholds"""
        self.thresholds = {
            CollectiveBehavior.LEARNING_ACCELERATION: QuorumThreshold(
                behavior=CollectiveBehavior.LEARNING_ACCELERATION,
                signal_types=[SignalType.LEARNING_OPPORTUNITY, SignalType.KNOWLEDGE_NEED],
                density_threshold=0.6,
                min_agents=3,
                max_agents=None,
                duration_minutes=120,
                confidence_required=0.7
            ),
            CollectiveBehavior.KNOWLEDGE_CONSOLIDATION: QuorumThreshold(
                behavior=CollectiveBehavior.KNOWLEDGE_CONSOLIDATION,
                signal_types=[SignalType.LEARNING_OPPORTUNITY],
                density_threshold=0.7,
                min_agents=4,
                max_agents=None,
                duration_minutes=60,
                confidence_required=0.8
            ),
            CollectiveBehavior.COLLABORATIVE_PROBLEM_SOLVING: QuorumThreshold(
                behavior=CollectiveBehavior.COLLABORATIVE_PROBLEM_SOLVING,
                signal_types=[SignalType.PROBLEM_SOLVING, SignalType.COLLABORATION_REQUEST],
                density_threshold=0.5,
                min_agents=2,
                max_agents=None,
                duration_minutes=90,
                confidence_required=0.6
            ),
            CollectiveBehavior.EMERGENCY_COORDINATION: QuorumThreshold(
                behavior=CollectiveBehavior.EMERGENCY_COORDINATION,
                signal_types=[SignalType.ERROR_DETECTED],
                density_threshold=0.8,
                min_agents=2,
                max_agents=None,
                duration_minutes=30,
                confidence_required=0.9
            ),
            CollectiveBehavior.EXPLORATION_MODE: QuorumThreshold(
                behavior=CollectiveBehavior.EXPLORATION_MODE,
                signal_types=[SignalType.EXPLORATION_FOUND],
                density_threshold=0.4,
                min_agents=2,
                max_agents=None,
                duration_minutes=180,
                confidence_required=0.5
            ),
            CollectiveBehavior.CONSENSUS_BUILDING: QuorumThreshold(
                behavior=CollectiveBehavior.CONSENSUS_BUILDING,
                signal_types=[SignalType.CONSENSUS_NEEDED],
                density_threshold=0.6,
                min_agents=3,
                max_agents=None,
                duration_minutes=45,
                confidence_required=0.7
            ),
            CollectiveBehavior.RESOURCE_SHARING: QuorumThreshold(
                behavior=CollectiveBehavior.RESOURCE_SHARING,
                signal_types=[SignalType.RESOURCE_AVAILABLE, SignalType.KNOWLEDGE_NEED],
                density_threshold=0.5,
                min_agents=2,
                max_agents=None,
                duration_minutes=90,
                confidence_required=0.6
            ),
            CollectiveBehavior.EVOLUTION_PREPARATION: QuorumThreshold(
                behavior=CollectiveBehavior.EVOLUTION_PREPARATION,
                signal_types=[SignalType.LEARNING_OPPORTUNITY, SignalType.KNOWLEDGE_NEED],
                density_threshold=0.8,
                min_agents=5,
                max_agents=None,
                duration_minutes=240,
                confidence_required=0.9
            )
        }
    
    def _setup_behavior_handlers(self):
        """Set up handlers for collective behaviors"""
        self.behavior_handlers = {
            CollectiveBehavior.LEARNING_ACCELERATION: self._handle_learning_acceleration,
            CollectiveBehavior.KNOWLEDGE_CONSOLIDATION: self._handle_knowledge_consolidation,
            CollectiveBehavior.COLLABORATIVE_PROBLEM_SOLVING: self._handle_collaborative_problem_solving,
            CollectiveBehavior.EMERGENCY_COORDINATION: self._handle_emergency_coordination,
            CollectiveBehavior.EXPLORATION_MODE: self._handle_exploration_mode,
            CollectiveBehavior.CONSENSUS_BUILDING: self._handle_consensus_building,
            CollectiveBehavior.RESOURCE_SHARING: self._handle_resource_sharing,
            CollectiveBehavior.EVOLUTION_PREPARATION: self._handle_evolution_preparation
        }
    
    async def initialize(self):
        """Initialize the quorum sensing system"""
        await self._create_database_tables()
        await self._load_signal_history()
        print("🦠 Quorum Sensing System initialized")
    
    async def _create_database_tables(self):
        """Create necessary database tables"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            # Signal molecules table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS signal_molecules (
                    signal_id VARCHAR(255) PRIMARY KEY,
                    agent_id UUID NOT NULL,
                    signal_type VARCHAR(100) NOT NULL,
                    strength FLOAT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    decay_rate FLOAT NOT NULL,
                    location VARCHAR(255),
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Collective behaviors table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS collective_behaviors (
                    behavior_id VARCHAR(255) PRIMARY KEY,
                    behavior_type VARCHAR(100) NOT NULL,
                    trigger_time TIMESTAMP NOT NULL,
                    participating_agents UUID[] NOT NULL,
                    signal_density FLOAT NOT NULL,
                    confidence FLOAT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    success BOOLEAN,
                    end_time TIMESTAMP,
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Quorum events table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS quorum_events (
                    event_id SERIAL PRIMARY KEY,
                    event_type VARCHAR(100) NOT NULL,
                    signal_type VARCHAR(100),
                    behavior_type VARCHAR(100),
                    density_value FLOAT,
                    threshold_value FLOAT,
                    agent_count INTEGER,
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    metadata JSONB
                )
            """)
            
        finally:
            await conn.close()
    
    async def _load_signal_history(self):
        """Load recent signal history from database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        try:
            # Load signals from last 24 hours
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            rows = await conn.fetch("""
                SELECT * FROM signal_molecules 
                WHERE timestamp > %s 
                ORDER BY timestamp DESC
            """, (cutoff_time,))
            
            for row in rows:
                signal = SignalMolecule(
                    signal_id=row['signal_id'],
                    agent_id=row['agent_id'],
                    signal_type=SignalType(row['signal_type']),
                    strength=row['strength'],
                    timestamp=row['timestamp'],
                    decay_rate=row['decay_rate'],
                    metadata=row['metadata'] or {},
                    location=row['location']
                )
                
                if signal.signal_type not in self.signal_molecules:
                    self.signal_molecules[signal.signal_type] = []
                
                self.signal_molecules[signal.signal_type].append(signal)
                
        finally:
            await conn.close()
    
    async def emit_signal(self, agent_id: str, signal_type: SignalType, strength: float, 
                         metadata: Dict[str, Any] = None, location: str = None) -> str:
        """Agent emits a signal molecule"""
        signal_id = f"{agent_id}_{signal_type.value}_{datetime.utcnow().timestamp()}"
        
        # Determine decay rate based on signal type
        decay_rate = self._get_decay_rate(signal_type)
        
        signal = SignalMolecule(
            signal_id=signal_id,
            agent_id=agent_id,
            signal_type=signal_type,
            strength=max(0.0, min(1.0, strength)),
            timestamp=datetime.utcnow(),
            decay_rate=decay_rate,
            metadata=metadata or {},
            location=location
        )
        
        # Add to signal collection
        if signal_type not in self.signal_molecules:
            self.signal_molecules[signal_type] = []
        
        self.signal_molecules[signal_type].append(signal)
        
        # Persist to database
        await self._persist_signal(signal)
        
        # Check for quorum thresholds
        await self._check_quorum_thresholds()
        
        print(f"📡 Agent {agent_id} emitted {signal_type.value} signal (strength: {strength:.2f})")
        return signal_id
    
    def _get_decay_rate(self, signal_type: SignalType) -> float:
        """Get decay rate for different signal types"""
        decay_rates = {
            SignalType.LEARNING_OPPORTUNITY: 0.02,  # Slower decay for learning
            SignalType.KNOWLEDGE_NEED: 0.03,
            SignalType.PROBLEM_SOLVING: 0.04,
            SignalType.COLLABORATION_REQUEST: 0.03,
            SignalType.ERROR_DETECTED: 0.08,  # Faster decay for urgent signals
            SignalType.RESOURCE_AVAILABLE: 0.05,
            SignalType.EXPLORATION_FOUND: 0.02,
            SignalType.CONSENSUS_NEEDED: 0.04
        }
        return decay_rates.get(signal_type, 0.03)
    
    async def calculate_signal_density(self, signal_type: SignalType, time_window_minutes: int = 30) -> float:
        """Calculate current signal density for a type"""
        if signal_type not in self.signal_molecules:
            return 0.0
        
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        recent_signals = [
            s for s in self.signal_molecules[signal_type]
            if s.timestamp > cutoff_time
        ]
        
        if not recent_signals:
            return 0.0
        
        # Calculate total effective strength (with decay)
        total_strength = sum(signal.get_current_strength() for signal in recent_signals)
        
        # Normalize by active agent count
        active_agent_count = len(self.hive.active_agents) if hasattr(self.hive, 'active_agents') else 1
        
        return total_strength / active_agent_count
    
    async def calculate_combined_signal_density(self, signal_types: List[SignalType], 
                                              time_window_minutes: int = 30) -> float:
        """Calculate combined density for multiple signal types"""
        densities = []
        for signal_type in signal_types:
            density = await self.calculate_signal_density(signal_type, time_window_minutes)
            densities.append(density)
        
        # Use weighted average (could be customized per behavior)
        return np.mean(densities) if densities else 0.0
    
    async def _check_quorum_thresholds(self):
        """Check if any collective behaviors should be triggered"""
        triggered_behaviors = []
        
        for behavior, threshold in self.thresholds.items():
            # Skip if behavior is already active
            if any(active.behavior == behavior for active in self.active_behaviors.values()):
                continue
            
            # Calculate combined signal density
            combined_density = await self.calculate_combined_signal_density(
                threshold.signal_types, time_window_minutes=15
            )
            
            # Check if threshold is met
            if combined_density >= threshold.density_threshold:
                # Check agent count requirements
                active_agent_count = len(self.hive.active_agents) if hasattr(self.hive, 'active_agents') else 0
                
                if active_agent_count >= threshold.min_agents:
                    if threshold.max_agents is None or active_agent_count <= threshold.max_agents:
                        confidence = min(1.0, combined_density / threshold.density_threshold)
                        
                        if confidence >= threshold.confidence_required:
                            triggered_behaviors.append({
                                'behavior': behavior,
                                'density': combined_density,
                                'confidence': confidence,
                                'threshold': threshold
                            })
        
        # Execute triggered behaviors
        for behavior_data in triggered_behaviors:
            await self._trigger_collective_behavior(behavior_data)
    
    async def _trigger_collective_behavior(self, behavior_data: Dict[str, Any]):
        """Execute collective behavior across the hive"""
        behavior = behavior_data['behavior']
        threshold = behavior_data['threshold']
        confidence = behavior_data['confidence']
        
        # Get participating agents
        participating_agents = list(self.hive.active_agents.keys()) if hasattr(self.hive, 'active_agents') else []
        
        # Create behavior execution record
        behavior_id = f"{behavior.value}_{datetime.utcnow().timestamp()}"
        execution = CollectiveBehaviorExecution(
            behavior=behavior,
            trigger_time=datetime.utcnow(),
            participating_agents=participating_agents,
            signal_density=behavior_data['density'],
            confidence=confidence,
            duration_minutes=threshold.duration_minutes,
            metadata={
                'trigger_signals': [st.value for st in threshold.signal_types],
                'threshold_value': threshold.density_threshold
            }
        )
        
        self.active_behaviors[behavior_id] = execution
        
        # Execute the behavior
        if behavior in self.behavior_handlers:
            try:
                await self.behavior_handlers[behavior](execution)
                execution.success = True
            except Exception as e:
                execution.success = False
                execution.metadata['error'] = str(e)
                print(f"❌ Error executing {behavior.value}: {e}")
        
        # Schedule behavior end
        asyncio.create_task(self._end_behavior_after_duration(behavior_id, threshold.duration_minutes))
        
        # Log the behavior execution
        await self._log_collective_behavior(execution)
        
        print(f"🚀 Triggered {behavior.value} (confidence: {confidence:.2f}, agents: {len(participating_agents)})")
    
    async def _end_behavior_after_duration(self, behavior_id: str, duration_minutes: int):
        """End behavior after specified duration"""
        await asyncio.sleep(duration_minutes * 60)  # Convert to seconds
        
        if behavior_id in self.active_behaviors:
            execution = self.active_behaviors[behavior_id]
            execution.end_time = datetime.utcnow()
            
            # Update database record
            await self._update_behavior_completion(execution)
            
            # Remove from active behaviors
            del self.active_behaviors[behavior_id]
            
            print(f"⏰ Ended {execution.behavior.value} after {duration_minutes} minutes")
    
    # Behavior handlers
    async def _handle_learning_acceleration(self, execution: CollectiveBehaviorExecution):
        """Handle learning acceleration behavior"""
        acceleration_factor = 1.0 + (execution.confidence * 0.5)  # Up to 50% acceleration
        
        # Apply acceleration to all agents
        if hasattr(self.hive, 'active_agents'):
            for agent_id in execution.participating_agents:
                # Increase learning rates (implementation depends on agent structure)
                await self._apply_learning_acceleration(agent_id, acceleration_factor)
        
        # Enable enhanced knowledge sharing
        if hasattr(self.hive, 'enable_enhanced_knowledge_sharing'):
            await self.hive.enable_enhanced_knowledge_sharing(duration=timedelta(minutes=execution.duration_minutes))
        
        execution.metadata['acceleration_factor'] = acceleration_factor
    
    async def _handle_knowledge_consolidation(self, execution: CollectiveBehaviorExecution):
        """Handle knowledge consolidation behavior"""
        # Trigger memory consolidation across agents
        if hasattr(self.hive, 'trigger_memory_consolidation'):
            await self.hive.trigger_memory_consolidation(execution.confidence)
        
        # Cross-pollinate knowledge between agents
        await self._facilitate_knowledge_cross_pollination(execution.participating_agents)
    
    async def _handle_collaborative_problem_solving(self, execution: CollectiveBehaviorExecution):
        """Handle collaborative problem solving behavior"""
        # Form problem-solving groups
        groups = self._form_problem_solving_groups(execution.participating_agents)
        
        for group in groups:
            await self._initiate_collaborative_session(group, execution)
    
    async def _handle_emergency_coordination(self, execution: CollectiveBehaviorExecution):
        """Handle emergency coordination behavior"""
        # Activate emergency protocols
        if hasattr(self.hive, 'activate_emergency_coordination'):
            await self.hive.activate_emergency_coordination(execution.confidence)
        
        # Increase communication frequency
        await self._increase_communication_frequency(execution.participating_agents, factor=2.0)
    
    async def _handle_exploration_mode(self, execution: CollectiveBehaviorExecution):
        """Handle exploration mode behavior"""
        # Increase exploration parameters
        exploration_boost = execution.confidence * 0.3
        
        for agent_id in execution.participating_agents:
            await self._boost_agent_exploration(agent_id, exploration_boost)
    
    async def _handle_consensus_building(self, execution: CollectiveBehaviorExecution):
        """Handle consensus building behavior"""
        # Initiate consensus protocols
        await self._initiate_consensus_protocol(execution.participating_agents, execution.metadata)
    
    async def _handle_resource_sharing(self, execution: CollectiveBehaviorExecution):
        """Handle resource sharing behavior"""
        # Facilitate resource redistribution
        await self._facilitate_resource_sharing(execution.participating_agents)
    
    async def _handle_evolution_preparation(self, execution: CollectiveBehaviorExecution):
        """Handle evolution preparation behavior"""
        # Prepare for hive evolution
        if hasattr(self.hive, 'prepare_for_evolution'):
            await self.hive.prepare_for_evolution(execution.confidence)
        
        execution.metadata['evolution_readiness'] = True
    
    # Helper methods for behavior implementations
    async def _apply_learning_acceleration(self, agent_id: str, factor: float):
        """Apply learning acceleration to an agent"""
        # Implementation depends on agent structure
        # This would modify agent learning parameters
        pass
    
    async def _facilitate_knowledge_cross_pollination(self, agent_ids: List[str]):
        """Facilitate knowledge sharing between agents"""
        # Implement cross-pollination logic
        for i, agent_a in enumerate(agent_ids):
            for agent_b in agent_ids[i+1:]:
                await self._cross_pollinate_agents(agent_a, agent_b)
    
    async def _cross_pollinate_agents(self, agent_a_id: str, agent_b_id: str):
        """Cross-pollinate knowledge between two agents"""
        # Implementation would transfer relevant knowledge
        pass
    
    def _form_problem_solving_groups(self, agent_ids: List[str]) -> List[List[str]]:
        """Form optimal problem-solving groups"""
        # Simple grouping - could be enhanced with compatibility analysis
        group_size = min(4, max(2, len(agent_ids) // 2))
        groups = []
        
        for i in range(0, len(agent_ids), group_size):
            group = agent_ids[i:i + group_size]
            if len(group) >= 2:  # Minimum group size
                groups.append(group)
        
        return groups
    
    async def _initiate_collaborative_session(self, group: List[str], execution: CollectiveBehaviorExecution):
        """Initiate collaborative session for a group"""
        # Implementation would start collaborative problem-solving
        pass
    
    async def _increase_communication_frequency(self, agent_ids: List[str], factor: float):
        """Increase communication frequency between agents"""
        # Implementation would modify communication parameters
        pass
    
    async def _boost_agent_exploration(self, agent_id: str, boost: float):
        """Boost exploration parameters for an agent"""
        # Implementation would modify agent exploration behavior
        pass
    
    async def _initiate_consensus_protocol(self, agent_ids: List[str], metadata: Dict[str, Any]):
        """Initiate consensus building protocol"""
        # Implementation would start consensus mechanism
        pass
    
    async def _facilitate_resource_sharing(self, agent_ids: List[str]):
        """Facilitate resource sharing between agents"""
        # Implementation would redistribute resources based on need
        pass
    
    # Database persistence methods
    async def _persist_signal(self, signal: SignalMolecule):
        """Persist signal to database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO signal_molecules (
                    signal_id, agent_id, signal_type, strength, timestamp,
                    decay_rate, location, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (signal_id) DO NOTHING
            """, (
                signal.signal_id,
                signal.agent_id,
                signal.signal_type.value,
                signal.strength,
                signal.timestamp,
                signal.decay_rate,
                signal.location,
                json.dumps(signal.metadata)
            ))
        finally:
            await conn.close()
    
    async def _log_collective_behavior(self, execution: CollectiveBehaviorExecution):
        """Log collective behavior execution"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            behavior_id = f"{execution.behavior.value}_{execution.trigger_time.timestamp()}"
            
            await conn.execute("""
                INSERT INTO collective_behaviors (
                    behavior_id, behavior_type, trigger_time, participating_agents,
                    signal_density, confidence, duration_minutes, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                behavior_id,
                execution.behavior.value,
                execution.trigger_time,
                execution.participating_agents,
                execution.signal_density,
                execution.confidence,
                execution.duration_minutes,
                json.dumps(execution.metadata)
            ))
        finally:
            await conn.close()
    
    async def _update_behavior_completion(self, execution: CollectiveBehaviorExecution):
        """Update behavior completion in database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            behavior_id = f"{execution.behavior.value}_{execution.trigger_time.timestamp()}"
            
            await conn.execute("""
                UPDATE collective_behaviors 
                SET success = %s, end_time = %s, metadata = %s
                WHERE behavior_id = %s
            """, (
                execution.success,
                execution.end_time,
                json.dumps(execution.metadata),
                behavior_id
            ))
        finally:
            await conn.close()
    
    # Analysis and monitoring methods
    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        status = {
            "active_behaviors": len(self.active_behaviors),
            "signal_types_active": len(self.signal_molecules),
            "total_signals": sum(len(signals) for signals in self.signal_molecules.values()),
            "signal_densities": {},
            "active_behavior_details": []
        }
        
        # Calculate current signal densities
        for signal_type in SignalType:
            density = await self.calculate_signal_density(signal_type)
            status["signal_densities"][signal_type.value] = density
        
        # Add active behavior details
        for behavior_id, execution in self.active_behaviors.items():
            status["active_behavior_details"].append({
                "behavior": execution.behavior.value,
                "confidence": execution.confidence,
                "participants": len(execution.participating_agents),
                "minutes_remaining": execution.duration_minutes - 
                    ((datetime.utcnow() - execution.trigger_time).total_seconds() / 60)
            })
        
        return status
    
    async def cleanup_old_signals(self, hours: int = 24):
        """Clean up old signals from memory and database"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Clean from memory
        for signal_type in list(self.signal_molecules.keys()):
            self.signal_molecules[signal_type] = [
                signal for signal in self.signal_molecules[signal_type]
                if signal.timestamp > cutoff_time
            ]
            
            # Remove empty signal type collections
            if not self.signal_molecules[signal_type]:
                del self.signal_molecules[signal_type]
        
        # Clean from database
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        try:
            result = await conn.execute(
                "DELETE FROM signal_molecules WHERE timestamp < %s",
                (cutoff_time,)
            )
            print(f"🧹 Cleaned up old signals (removed: database)")
        finally:
            await conn.close()

# Testing function
async def test_quorum_sensing_system(hive, database_url: str):
    """Test the quorum sensing system"""
    print("🧪 Testing Quorum Sensing System...")
    
    # Initialize system
    quorum_manager = QuorumSensingManager(hive, database_url)
    await quorum_manager.initialize()
    
    # Test signal emission
    await quorum_manager.emit_signal(
        "agent_1", SignalType.LEARNING_OPPORTUNITY, 0.8,
        metadata={"topic": "neural_networks", "urgency": "medium"}
    )
    
    await quorum_manager.emit_signal(
        "agent_2", SignalType.LEARNING_OPPORTUNITY, 0.7,
        metadata={"topic": "machine_learning", "urgency": "high"}
    )
    
    await quorum_manager.emit_signal(
        "agent_3", SignalType.KNOWLEDGE_NEED, 0.9,
        metadata={"topic": "optimization", "urgency": "high"}
    )
    
    # Test signal density calculation
    density = await quorum_manager.calculate_signal_density(SignalType.LEARNING_OPPORTUNITY)
    print(f"📊 Learning opportunity signal density: {density:.3f}")
    
    # Test system status
    status = await quorum_manager.get_system_status()
    print(f"📋 System status: {json.dumps(status, indent=2, default=str)}")
    
    # Wait a bit and emit more signals to potentially trigger behavior
    await asyncio.sleep(1)
    
    for i in range(3):
        await quorum_manager.emit_signal(
            f"agent_{i+1}", SignalType.LEARNING_OPPORTUNITY, 0.8
        )
    
    # Check status again
    status = await quorum_manager.get_system_status()
    print(f"📋 Updated system status: {json.dumps(status, indent=2, default=str)}")
    
    print("✅ Quorum Sensing System test complete!")
    return quorum_manager

if __name__ == "__main__":
    # Quick test run
    import asyncio
    
    class MockHive:
        def __init__(self):
            self.active_agents = {
                "agent_1": {"name": "Explorer"},
                "agent_2": {"name": "Philosopher"},
                "agent_3": {"name": "Caregiver"},
                "agent_4": {"name": "Innovator"}
            }
    
    async def main():
        hive = MockHive()
        database_url = "postgresql://postgres:pass@localhost:5432/sentient"
        await test_quorum_sensing_system(hive, database_url)
    
    asyncio.run(main())