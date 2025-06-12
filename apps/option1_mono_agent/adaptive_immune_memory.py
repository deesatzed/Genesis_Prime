#!/usr/bin/env python
"""
Adaptive Immune Memory System for Genesis Prime
Implements biological immune system-inspired error detection, prevention, and rapid response mechanisms
"""

import asyncio
import json
import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import psycopg
from psycopg.rows import dict_row

class ThreatType(Enum):
    """Types of threats the immune system can detect"""
    LOGIC_ERROR = "logic_error"
    MEMORY_CORRUPTION = "memory_corruption"
    COMMUNICATION_FAILURE = "communication_failure"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    INFINITE_LOOP = "infinite_loop"
    DATA_INCONSISTENCY = "data_inconsistency"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SECURITY_BREACH = "security_breach"

class ResponseType(Enum):
    """Types of immune responses"""
    ERROR_CORRECTION = "error_correction"
    AGENT_ISOLATION = "agent_isolation"
    MEMORY_CLEANUP = "memory_cleanup"
    CONNECTION_REPAIR = "connection_repair"
    RESOURCE_REALLOCATION = "resource_reallocation"
    SYSTEM_RESTART = "system_restart"
    ROLLBACK_OPERATION = "rollback_operation"
    PREVENTIVE_MEASURE = "preventive_measure"

@dataclass
class ThreatSignature:
    """Unique signature for identifying threat patterns"""
    threat_type: ThreatType
    error_pattern: str
    context_hash: str
    agent_states_hash: str
    system_load_level: str
    timestamp_pattern: str
    severity_level: float
    
    def to_hash(self) -> str:
        """Generate unique hash for this threat signature"""
        signature_str = f"{self.threat_type.value}:{self.error_pattern}:{self.context_hash}:{self.agent_states_hash}:{self.system_load_level}"
        return hashlib.sha256(signature_str.encode()).hexdigest()

@dataclass
class ImmuneMemory:
    """Memory of past threats and successful responses"""
    threat_signature: ThreatSignature
    response_pattern: ResponseType
    success_count: int
    failure_count: int
    last_encountered: datetime
    creation_time: datetime
    response_time_avg: float
    effectiveness_score: float
    metadata: Dict[str, Any]
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0
    
    def update_effectiveness(self, success: bool, response_time: float):
        """Update memory effectiveness based on response outcome"""
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        # Update average response time
        total_responses = self.success_count + self.failure_count
        self.response_time_avg = ((self.response_time_avg * (total_responses - 1)) + response_time) / total_responses
        
        # Calculate effectiveness score (combines success rate and speed)
        self.effectiveness_score = self.success_rate * (1.0 / max(0.1, self.response_time_avg))
        self.last_encountered = datetime.utcnow()

@dataclass
class AntibodyAgent:
    """Specialized agent for detecting and responding to specific threats"""
    agent_id: str
    specialized_threats: List[ThreatType]
    detection_patterns: List[str]
    response_capabilities: List[ResponseType]
    activation_count: int
    success_rate: float
    learning_rate: float = 0.1
    creation_time: datetime = None
    
    def __post_init__(self):
        if self.creation_time is None:
            self.creation_time = datetime.utcnow()
    
    def can_handle_threat(self, threat_type: ThreatType) -> bool:
        """Check if this antibody can handle the given threat type"""
        return threat_type in self.specialized_threats
    
    def calculate_threat_similarity(self, threat_signature: ThreatSignature) -> float:
        """Calculate similarity between threat and what this antibody can handle"""
        if not self.can_handle_threat(threat_signature.threat_type):
            return 0.0
        
        # Calculate pattern similarity
        pattern_similarities = []
        for pattern in self.detection_patterns:
            similarity = self._calculate_pattern_similarity(pattern, threat_signature.error_pattern)
            pattern_similarities.append(similarity)
        
        return max(pattern_similarities) if pattern_similarities else 0.0
    
    def _calculate_pattern_similarity(self, pattern1: str, pattern2: str) -> float:
        """Calculate similarity between two patterns"""
        # Simple similarity based on common substrings
        words1 = set(pattern1.lower().split())
        words2 = set(pattern2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)

class ThreatDetector:
    """Detects various types of threats in the hive system"""
    
    def __init__(self):
        self.detection_thresholds = {
            ThreatType.LOGIC_ERROR: 0.7,
            ThreatType.MEMORY_CORRUPTION: 0.8,
            ThreatType.COMMUNICATION_FAILURE: 0.6,
            ThreatType.RESOURCE_EXHAUSTION: 0.9,
            ThreatType.INFINITE_LOOP: 0.95,
            ThreatType.DATA_INCONSISTENCY: 0.7,
            ThreatType.PERFORMANCE_DEGRADATION: 0.5,
            ThreatType.SECURITY_BREACH: 0.9
        }
        self.threat_history = []
    
    async def detect_threats(self, hive) -> List[ThreatSignature]:
        """Detect current threats in the hive system"""
        detected_threats = []
        
        # Check for logic errors
        logic_threats = await self._detect_logic_errors(hive)
        detected_threats.extend(logic_threats)
        
        # Check for memory corruption
        memory_threats = await self._detect_memory_corruption(hive)
        detected_threats.extend(memory_threats)
        
        # Check for communication failures
        comm_threats = await self._detect_communication_failures(hive)
        detected_threats.extend(comm_threats)
        
        # Check for resource exhaustion
        resource_threats = await self._detect_resource_exhaustion(hive)
        detected_threats.extend(resource_threats)
        
        # Check for infinite loops
        loop_threats = await self._detect_infinite_loops(hive)
        detected_threats.extend(loop_threats)
        
        # Check for data inconsistencies
        data_threats = await self._detect_data_inconsistencies(hive)
        detected_threats.extend(data_threats)
        
        # Check for performance degradation
        perf_threats = await self._detect_performance_degradation(hive)
        detected_threats.extend(perf_threats)
        
        return detected_threats
    
    async def _detect_logic_errors(self, hive) -> List[ThreatSignature]:
        """Detect logic errors in agent operations"""
        threats = []
        
        for agent_id, agent in hive.active_agents.items():
            try:
                # Check for inconsistent outputs
                recent_outputs = getattr(agent, 'recent_outputs', [])
                if len(recent_outputs) >= 3:
                    consistency_score = self._calculate_output_consistency(recent_outputs)
                    
                    if consistency_score < self.detection_thresholds[ThreatType.LOGIC_ERROR]:
                        threat = ThreatSignature(
                            threat_type=ThreatType.LOGIC_ERROR,
                            error_pattern=f"inconsistent_outputs_{agent_id}",
                            context_hash=self._hash_context(agent),
                            agent_states_hash=self._hash_agent_states(hive),
                            system_load_level=self._get_load_level(hive),
                            timestamp_pattern=self._get_timestamp_pattern(),
                            severity_level=1.0 - consistency_score
                        )
                        threats.append(threat)
            except Exception as e:
                # Error checking for errors - meta-threat detection
                threat = ThreatSignature(
                    threat_type=ThreatType.LOGIC_ERROR,
                    error_pattern=f"meta_error_{str(e)}",
                    context_hash=self._hash_context(agent),
                    agent_states_hash=self._hash_agent_states(hive),
                    system_load_level=self._get_load_level(hive),
                    timestamp_pattern=self._get_timestamp_pattern(),
                    severity_level=0.8
                )
                threats.append(threat)
        
        return threats
    
    async def _detect_memory_corruption(self, hive) -> List[ThreatSignature]:
        """Detect memory corruption issues"""
        threats = []
        
        # Check for memory inconsistencies
        if hasattr(hive, 'memory_system'):
            memory_integrity = await self._check_memory_integrity(hive.memory_system)
            
            if memory_integrity < self.detection_thresholds[ThreatType.MEMORY_CORRUPTION]:
                threat = ThreatSignature(
                    threat_type=ThreatType.MEMORY_CORRUPTION,
                    error_pattern="memory_integrity_failure",
                    context_hash=self._hash_context(hive.memory_system),
                    agent_states_hash=self._hash_agent_states(hive),
                    system_load_level=self._get_load_level(hive),
                    timestamp_pattern=self._get_timestamp_pattern(),
                    severity_level=1.0 - memory_integrity
                )
                threats.append(threat)
        
        return threats
    
    async def _detect_communication_failures(self, hive) -> List[ThreatSignature]:
        """Detect communication failures between agents"""
        threats = []
        
        # Check for communication timeouts and failures
        if hasattr(hive, 'communication_stats'):
            failure_rate = hive.communication_stats.get('failure_rate', 0.0)
            
            if failure_rate > (1.0 - self.detection_thresholds[ThreatType.COMMUNICATION_FAILURE]):
                threat = ThreatSignature(
                    threat_type=ThreatType.COMMUNICATION_FAILURE,
                    error_pattern=f"high_failure_rate_{failure_rate}",
                    context_hash=self._hash_context(hive.communication_stats),
                    agent_states_hash=self._hash_agent_states(hive),
                    system_load_level=self._get_load_level(hive),
                    timestamp_pattern=self._get_timestamp_pattern(),
                    severity_level=failure_rate
                )
                threats.append(threat)
        
        return threats
    
    async def _detect_resource_exhaustion(self, hive) -> List[ThreatSignature]:
        """Detect resource exhaustion issues"""
        threats = []
        
        # Check memory usage
        memory_usage = self._get_memory_usage(hive)
        if memory_usage > self.detection_thresholds[ThreatType.RESOURCE_EXHAUSTION]:
            threat = ThreatSignature(
                threat_type=ThreatType.RESOURCE_EXHAUSTION,
                error_pattern=f"memory_exhaustion_{memory_usage}",
                context_hash=self._hash_context({'memory_usage': memory_usage}),
                agent_states_hash=self._hash_agent_states(hive),
                system_load_level=self._get_load_level(hive),
                timestamp_pattern=self._get_timestamp_pattern(),
                severity_level=memory_usage
            )
            threats.append(threat)
        
        # Check CPU usage
        cpu_usage = self._get_cpu_usage(hive)
        if cpu_usage > self.detection_thresholds[ThreatType.RESOURCE_EXHAUSTION]:
            threat = ThreatSignature(
                threat_type=ThreatType.RESOURCE_EXHAUSTION,
                error_pattern=f"cpu_exhaustion_{cpu_usage}",
                context_hash=self._hash_context({'cpu_usage': cpu_usage}),
                agent_states_hash=self._hash_agent_states(hive),
                system_load_level=self._get_load_level(hive),
                timestamp_pattern=self._get_timestamp_pattern(),
                severity_level=cpu_usage
            )
            threats.append(threat)
        
        return threats
    
    async def _detect_infinite_loops(self, hive) -> List[ThreatSignature]:
        """Detect infinite loops in agent execution"""
        threats = []
        
        for agent_id, agent in hive.active_agents.items():
            # Check for repeated identical operations
            if hasattr(agent, 'operation_history'):
                loop_detected = self._detect_operation_loops(agent.operation_history)
                
                if loop_detected:
                    threat = ThreatSignature(
                        threat_type=ThreatType.INFINITE_LOOP,
                        error_pattern=f"infinite_loop_{agent_id}",
                        context_hash=self._hash_context(agent),
                        agent_states_hash=self._hash_agent_states(hive),
                        system_load_level=self._get_load_level(hive),
                        timestamp_pattern=self._get_timestamp_pattern(),
                        severity_level=0.95
                    )
                    threats.append(threat)
        
        return threats
    
    async def _detect_data_inconsistencies(self, hive) -> List[ThreatSignature]:
        """Detect data inconsistencies across the hive"""
        threats = []
        
        # Check for inconsistent agent states
        inconsistency_score = self._calculate_state_consistency(hive)
        
        if inconsistency_score > (1.0 - self.detection_thresholds[ThreatType.DATA_INCONSISTENCY]):
            threat = ThreatSignature(
                threat_type=ThreatType.DATA_INCONSISTENCY,
                error_pattern=f"state_inconsistency_{inconsistency_score}",
                context_hash=self._hash_context(hive),
                agent_states_hash=self._hash_agent_states(hive),
                system_load_level=self._get_load_level(hive),
                timestamp_pattern=self._get_timestamp_pattern(),
                severity_level=inconsistency_score
            )
            threats.append(threat)
        
        return threats
    
    async def _detect_performance_degradation(self, hive) -> List[ThreatSignature]:
        """Detect performance degradation"""
        threats = []
        
        # Compare current performance to baseline
        current_performance = self._measure_current_performance(hive)
        baseline_performance = getattr(hive, 'baseline_performance', 1.0)
        
        performance_ratio = current_performance / baseline_performance
        
        if performance_ratio < self.detection_thresholds[ThreatType.PERFORMANCE_DEGRADATION]:
            threat = ThreatSignature(
                threat_type=ThreatType.PERFORMANCE_DEGRADATION,
                error_pattern=f"performance_drop_{performance_ratio}",
                context_hash=self._hash_context({'performance': current_performance}),
                agent_states_hash=self._hash_agent_states(hive),
                system_load_level=self._get_load_level(hive),
                timestamp_pattern=self._get_timestamp_pattern(),
                severity_level=1.0 - performance_ratio
            )
            threats.append(threat)
        
        return threats
    
    # Helper methods
    def _calculate_output_consistency(self, outputs: List) -> float:
        """Calculate consistency score for outputs"""
        if len(outputs) < 2:
            return 1.0
        
        similarities = []
        for i in range(len(outputs) - 1):
            for j in range(i + 1, len(outputs)):
                similarity = self._calculate_similarity(outputs[i], outputs[j])
                similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 1.0
    
    def _calculate_similarity(self, obj1, obj2) -> float:
        """Calculate similarity between two objects"""
        try:
            str1 = str(obj1)
            str2 = str(obj2)
            
            if str1 == str2:
                return 1.0
            
            # Simple character-based similarity
            common_chars = sum(1 for a, b in zip(str1, str2) if a == b)
            max_length = max(len(str1), len(str2))
            
            return common_chars / max_length if max_length > 0 else 0.0
        except:
            return 0.0
    
    async def _check_memory_integrity(self, memory_system) -> float:
        """Check integrity of memory system"""
        try:
            # Perform integrity checks
            if hasattr(memory_system, 'verify_integrity'):
                return await memory_system.verify_integrity()
            else:
                # Basic check - assume good if no obvious errors
                return 0.9
        except:
            return 0.3
    
    def _hash_context(self, obj) -> str:
        """Generate hash for object context"""
        try:
            return hashlib.md5(str(obj).encode()).hexdigest()[:16]
        except:
            return "unknown_context"
    
    def _hash_agent_states(self, hive) -> str:
        """Generate hash for current agent states"""
        try:
            states_str = str(sorted(hive.active_agents.keys()))
            return hashlib.md5(states_str.encode()).hexdigest()[:16]
        except:
            return "unknown_states"
    
    def _get_load_level(self, hive) -> str:
        """Get current system load level"""
        try:
            agent_count = len(hive.active_agents)
            if agent_count < 5:
                return "low"
            elif agent_count < 20:
                return "medium"
            else:
                return "high"
        except:
            return "unknown"
    
    def _get_timestamp_pattern(self) -> str:
        """Get timestamp pattern for trend analysis"""
        now = datetime.utcnow()
        return f"{now.hour:02d}_{now.minute//10}"
    
    def _get_memory_usage(self, hive) -> float:
        """Get current memory usage (0.0-1.0)"""
        # Simplified - would use actual system metrics in production
        agent_count = len(hive.active_agents) if hasattr(hive, 'active_agents') else 0
        return min(1.0, agent_count / 100.0)
    
    def _get_cpu_usage(self, hive) -> float:
        """Get current CPU usage (0.0-1.0)"""
        # Simplified - would use actual system metrics in production
        return min(1.0, np.random.random() * 0.3)  # Random low usage for testing
    
    def _detect_operation_loops(self, history: List) -> bool:
        """Detect loops in operation history"""
        if len(history) < 10:
            return False
        
        # Check for repeated patterns in recent history
        recent = history[-10:]
        for i in range(len(recent) - 2):
            for j in range(i + 2, len(recent)):
                if recent[i] == recent[j]:
                    # Found potential loop
                    pattern_length = j - i
                    if pattern_length < 5:  # Short patterns are suspicious
                        return True
        
        return False
    
    def _calculate_state_consistency(self, hive) -> float:
        """Calculate consistency of agent states"""
        if not hasattr(hive, 'active_agents') or len(hive.active_agents) < 2:
            return 0.0
        
        # Check for state inconsistencies
        states = []
        for agent in hive.active_agents.values():
            if hasattr(agent, 'state'):
                states.append(str(agent.state))
        
        if len(states) < 2:
            return 0.0
        
        # Calculate inconsistency as variation in states
        unique_states = len(set(states))
        total_states = len(states)
        
        return unique_states / total_states  # Higher = more inconsistent
    
    def _measure_current_performance(self, hive) -> float:
        """Measure current system performance"""
        # Simplified performance metric
        if hasattr(hive, 'performance_metrics'):
            return hive.performance_metrics.get('current_score', 1.0)
        else:
            # Default reasonable performance
            return 0.8

class AdaptiveImmuneSystem:
    """Main adaptive immune system manager"""
    
    def __init__(self, hive, database_url: str):
        self.hive = hive
        self.database_url = database_url
        self.threat_detector = ThreatDetector()
        self.immune_memory: Dict[str, ImmuneMemory] = {}
        self.antibody_agents: Dict[str, AntibodyAgent] = {}
        self.active_responses: Dict[str, Any] = {}
        
        # Initialize default antibody agents
        self._create_default_antibodies()
    
    def _create_default_antibodies(self):
        """Create default antibody agents for common threats"""
        antibodies = [
            AntibodyAgent(
                agent_id="antibody_logic_error",
                specialized_threats=[ThreatType.LOGIC_ERROR],
                detection_patterns=["inconsistent_outputs", "logic_failure", "invalid_state"],
                response_capabilities=[ResponseType.ERROR_CORRECTION, ResponseType.AGENT_ISOLATION],
                activation_count=0,
                success_rate=0.5
            ),
            AntibodyAgent(
                agent_id="antibody_memory_corruption",
                specialized_threats=[ThreatType.MEMORY_CORRUPTION],
                detection_patterns=["memory_integrity", "corruption", "invalid_data"],
                response_capabilities=[ResponseType.MEMORY_CLEANUP, ResponseType.ROLLBACK_OPERATION],
                activation_count=0,
                success_rate=0.5
            ),
            AntibodyAgent(
                agent_id="antibody_communication",
                specialized_threats=[ThreatType.COMMUNICATION_FAILURE],
                detection_patterns=["timeout", "failure_rate", "connection_lost"],
                response_capabilities=[ResponseType.CONNECTION_REPAIR, ResponseType.PREVENTIVE_MEASURE],
                activation_count=0,
                success_rate=0.5
            ),
            AntibodyAgent(
                agent_id="antibody_resource_exhaustion",
                specialized_threats=[ThreatType.RESOURCE_EXHAUSTION],
                detection_patterns=["memory_exhaustion", "cpu_exhaustion", "resource_limit"],
                response_capabilities=[ResponseType.RESOURCE_REALLOCATION, ResponseType.AGENT_ISOLATION],
                activation_count=0,
                success_rate=0.5
            )
        ]
        
        for antibody in antibodies:
            self.antibody_agents[antibody.agent_id] = antibody
    
    async def initialize(self):
        """Initialize the adaptive immune system"""
        await self._create_database_tables()
        await self._load_immune_memory()
        print("🛡️ Adaptive Immune System initialized")
    
    async def _create_database_tables(self):
        """Create necessary database tables"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            # Immune memory table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS immune_memory (
                    memory_id VARCHAR(255) PRIMARY KEY,
                    threat_signature JSONB NOT NULL,
                    response_pattern VARCHAR(100) NOT NULL,
                    success_count INTEGER NOT NULL DEFAULT 0,
                    failure_count INTEGER NOT NULL DEFAULT 0,
                    last_encountered TIMESTAMP NOT NULL,
                    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
                    response_time_avg FLOAT NOT NULL DEFAULT 1.0,
                    effectiveness_score FLOAT NOT NULL DEFAULT 0.5,
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Antibody agents table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS antibody_agents (
                    agent_id VARCHAR(255) PRIMARY KEY,
                    specialized_threats TEXT[] NOT NULL,
                    detection_patterns TEXT[] NOT NULL,
                    response_capabilities TEXT[] NOT NULL,
                    activation_count INTEGER NOT NULL DEFAULT 0,
                    success_rate FLOAT NOT NULL DEFAULT 0.5,
                    learning_rate FLOAT NOT NULL DEFAULT 0.1,
                    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Threat incidents table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS threat_incidents (
                    incident_id SERIAL PRIMARY KEY,
                    threat_signature_hash VARCHAR(255) NOT NULL,
                    threat_type VARCHAR(100) NOT NULL,
                    severity_level FLOAT NOT NULL,
                    detection_time TIMESTAMP NOT NULL,
                    response_time TIMESTAMP,
                    resolution_time TIMESTAMP,
                    antibody_agent_id VARCHAR(255),
                    response_type VARCHAR(100),
                    success BOOLEAN,
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
        finally:
            await conn.close()
    
    async def _load_immune_memory(self):
        """Load existing immune memory from database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        try:
            rows = await conn.fetch("SELECT * FROM immune_memory")
            
            for row in rows:
                threat_sig_data = row['threat_signature']
                threat_signature = ThreatSignature(
                    threat_type=ThreatType(threat_sig_data['threat_type']),
                    error_pattern=threat_sig_data['error_pattern'],
                    context_hash=threat_sig_data['context_hash'],
                    agent_states_hash=threat_sig_data['agent_states_hash'],
                    system_load_level=threat_sig_data['system_load_level'],
                    timestamp_pattern=threat_sig_data['timestamp_pattern'],
                    severity_level=threat_sig_data['severity_level']
                )
                
                memory = ImmuneMemory(
                    threat_signature=threat_signature,
                    response_pattern=ResponseType(row['response_pattern']),
                    success_count=row['success_count'],
                    failure_count=row['failure_count'],
                    last_encountered=row['last_encountered'],
                    creation_time=row['creation_time'],
                    response_time_avg=row['response_time_avg'],
                    effectiveness_score=row['effectiveness_score'],
                    metadata=row['metadata'] or {}
                )
                
                self.immune_memory[row['memory_id']] = memory
            
            # Load antibody agents
            rows = await conn.fetch("SELECT * FROM antibody_agents")
            
            for row in rows:
                antibody = AntibodyAgent(
                    agent_id=row['agent_id'],
                    specialized_threats=[ThreatType(t) for t in row['specialized_threats']],
                    detection_patterns=row['detection_patterns'],
                    response_capabilities=[ResponseType(r) for r in row['response_capabilities']],
                    activation_count=row['activation_count'],
                    success_rate=row['success_rate'],
                    learning_rate=row['learning_rate'],
                    creation_time=row['creation_time']
                )
                
                self.antibody_agents[antibody.agent_id] = antibody
                
        finally:
            await conn.close()
    
    async def monitor_and_respond(self):
        """Main monitoring loop for threat detection and response"""
        while True:
            try:
                # Detect current threats
                threats = await self.threat_detector.detect_threats(self.hive)
                
                for threat in threats:
                    await self._handle_threat(threat)
                
                # Clean up old responses
                await self._cleanup_old_responses()
                
                # Update antibody performance
                await self._update_antibody_performance()
                
                # Wait before next scan
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"❌ Error in immune system monitoring: {e}")
                await asyncio.sleep(10)  # Wait longer on error
    
    async def _handle_threat(self, threat_signature: ThreatSignature):
        """Handle a detected threat"""
        threat_hash = threat_signature.to_hash()
        
        # Check if already handling this threat
        if threat_hash in self.active_responses:
            return
        
        detection_time = datetime.utcnow()
        
        # Look for existing immune memory
        matching_memory = await self._find_matching_memory(threat_signature)
        
        if matching_memory:
            # Known threat - mount rapid response
            await self._mount_rapid_response(threat_signature, matching_memory, detection_time)
        else:
            # Novel threat - create new response
            await self._create_new_immune_response(threat_signature, detection_time)
    
    async def _find_matching_memory(self, threat_signature: ThreatSignature) -> Optional[ImmuneMemory]:
        """Find matching immune memory for threat"""
        best_match = None
        best_similarity = 0.0
        
        for memory in self.immune_memory.values():
            similarity = self._calculate_threat_similarity(threat_signature, memory.threat_signature)
            
            if similarity > best_similarity and similarity > 0.7:  # Threshold for match
                best_similarity = similarity
                best_match = memory
        
        return best_match
    
    def _calculate_threat_similarity(self, threat1: ThreatSignature, threat2: ThreatSignature) -> float:
        """Calculate similarity between two threat signatures"""
        if threat1.threat_type != threat2.threat_type:
            return 0.0
        
        # Calculate pattern similarity
        pattern_sim = self._calculate_string_similarity(threat1.error_pattern, threat2.error_pattern)
        
        # Calculate context similarity
        context_sim = 1.0 if threat1.context_hash == threat2.context_hash else 0.0
        
        # Calculate load similarity
        load_sim = 1.0 if threat1.system_load_level == threat2.system_load_level else 0.5
        
        # Calculate severity similarity
        severity_sim = 1.0 - abs(threat1.severity_level - threat2.severity_level)
        
        # Weighted average
        return (pattern_sim * 0.4 + context_sim * 0.2 + load_sim * 0.2 + severity_sim * 0.2)
    
    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        words1 = set(str1.lower().split('_'))
        words2 = set(str2.lower().split('_'))
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    async def _mount_rapid_response(self, threat_signature: ThreatSignature, memory: ImmuneMemory, detection_time: datetime):
        """Mount rapid response based on immune memory"""
        threat_hash = threat_signature.to_hash()
        
        # Find best antibody agent for this response
        best_antibody = await self._find_best_antibody(threat_signature, memory.response_pattern)
        
        if not best_antibody:
            # No suitable antibody - create new one
            best_antibody = await self._create_specialized_antibody(threat_signature, memory.response_pattern)
        
        # Record response start
        self.active_responses[threat_hash] = {
            'threat_signature': threat_signature,
            'memory': memory,
            'antibody': best_antibody,
            'detection_time': detection_time,
            'response_start_time': datetime.utcnow(),
            'status': 'responding'
        }
        
        # Execute response
        try:
            success = await self._execute_immune_response(threat_signature, memory.response_pattern, best_antibody)
            response_time = (datetime.utcnow() - detection_time).total_seconds()
            
            # Update memory effectiveness
            memory.update_effectiveness(success, response_time)
            
            # Update antibody performance
            best_antibody.activation_count += 1
            if success:
                best_antibody.success_rate = (best_antibody.success_rate * (best_antibody.activation_count - 1) + 1.0) / best_antibody.activation_count
            else:
                best_antibody.success_rate = (best_antibody.success_rate * (best_antibody.activation_count - 1)) / best_antibody.activation_count
            
            # Log incident
            await self._log_threat_incident(threat_signature, best_antibody, memory.response_pattern, detection_time, success)
            
            # Update response status
            self.active_responses[threat_hash]['status'] = 'completed'
            self.active_responses[threat_hash]['success'] = success
            
            print(f"🛡️ Rapid immune response: {threat_signature.threat_type.value} - {'✅ Success' if success else '❌ Failed'}")
            
        except Exception as e:
            print(f"❌ Error in rapid immune response: {e}")
            self.active_responses[threat_hash]['status'] = 'failed'
            self.active_responses[threat_hash]['error'] = str(e)
    
    async def _create_new_immune_response(self, threat_signature: ThreatSignature, detection_time: datetime):
        """Create new immune response for novel threat"""
        threat_hash = threat_signature.to_hash()
        
        # Analyze threat to determine best response
        response_type = await self._analyze_optimal_response(threat_signature)
        
        # Find or create antibody for this response
        antibody = await self._find_best_antibody(threat_signature, response_type)
        if not antibody:
            antibody = await self._create_specialized_antibody(threat_signature, response_type)
        
        # Record response start
        self.active_responses[threat_hash] = {
            'threat_signature': threat_signature,
            'antibody': antibody,
            'detection_time': detection_time,
            'response_start_time': datetime.utcnow(),
            'response_type': response_type,
            'status': 'learning'
        }
        
        # Execute response
        try:
            success = await self._execute_immune_response(threat_signature, response_type, antibody)
            response_time = (datetime.utcnow() - detection_time).total_seconds()
            
            # Create new immune memory
            memory_id = f"memory_{threat_hash}_{int(datetime.utcnow().timestamp())}"
            new_memory = ImmuneMemory(
                threat_signature=threat_signature,
                response_pattern=response_type,
                success_count=1 if success else 0,
                failure_count=0 if success else 1,
                last_encountered=datetime.utcnow(),
                creation_time=datetime.utcnow(),
                response_time_avg=response_time,
                effectiveness_score=1.0 if success else 0.0,
                metadata={'creation_context': 'novel_threat_response'}
            )
            
            self.immune_memory[memory_id] = new_memory
            
            # Persist to database
            await self._persist_immune_memory(memory_id, new_memory)
            
            # Update antibody performance
            antibody.activation_count += 1
            if success:
                antibody.success_rate = (antibody.success_rate * (antibody.activation_count - 1) + 1.0) / antibody.activation_count
            else:
                antibody.success_rate = (antibody.success_rate * (antibody.activation_count - 1)) / antibody.activation_count
            
            # Log incident
            await self._log_threat_incident(threat_signature, antibody, response_type, detection_time, success)
            
            # Update response status
            self.active_responses[threat_hash]['status'] = 'completed'
            self.active_responses[threat_hash]['success'] = success
            self.active_responses[threat_hash]['memory_id'] = memory_id
            
            print(f"🛡️ New immune response: {threat_signature.threat_type.value} - {'✅ Success' if success else '❌ Failed'}")
            
        except Exception as e:
            print(f"❌ Error in new immune response: {e}")
            self.active_responses[threat_hash]['status'] = 'failed'
            self.active_responses[threat_hash]['error'] = str(e)
    
    async def _analyze_optimal_response(self, threat_signature: ThreatSignature) -> ResponseType:
        """Analyze threat to determine optimal response type"""
        threat_type = threat_signature.threat_type
        
        # Default response mappings
        response_map = {
            ThreatType.LOGIC_ERROR: ResponseType.ERROR_CORRECTION,
            ThreatType.MEMORY_CORRUPTION: ResponseType.MEMORY_CLEANUP,
            ThreatType.COMMUNICATION_FAILURE: ResponseType.CONNECTION_REPAIR,
            ThreatType.RESOURCE_EXHAUSTION: ResponseType.RESOURCE_REALLOCATION,
            ThreatType.INFINITE_LOOP: ResponseType.AGENT_ISOLATION,
            ThreatType.DATA_INCONSISTENCY: ResponseType.ROLLBACK_OPERATION,
            ThreatType.PERFORMANCE_DEGRADATION: ResponseType.PREVENTIVE_MEASURE,
            ThreatType.SECURITY_BREACH: ResponseType.SYSTEM_RESTART
        }
        
        base_response = response_map.get(threat_type, ResponseType.ERROR_CORRECTION)
        
        # Adjust based on severity
        if threat_signature.severity_level > 0.9:
            # High severity threats might need more drastic measures
            if base_response == ResponseType.ERROR_CORRECTION:
                return ResponseType.AGENT_ISOLATION
            elif base_response == ResponseType.MEMORY_CLEANUP:
                return ResponseType.ROLLBACK_OPERATION
        
        return base_response
    
    async def _find_best_antibody(self, threat_signature: ThreatSignature, response_type: ResponseType) -> Optional[AntibodyAgent]:
        """Find best antibody agent for handling this threat"""
        best_antibody = None
        best_score = 0.0
        
        for antibody in self.antibody_agents.values():
            # Check if antibody can handle this threat type
            if not antibody.can_handle_threat(threat_signature.threat_type):
                continue
            
            # Check if antibody has required response capability
            if response_type not in antibody.response_capabilities:
                continue
            
            # Calculate suitability score
            threat_similarity = antibody.calculate_threat_similarity(threat_signature)
            success_weight = antibody.success_rate
            
            score = threat_similarity * 0.6 + success_weight * 0.4
            
            if score > best_score:
                best_score = score
                best_antibody = antibody
        
        return best_antibody if best_score > 0.5 else None
    
    async def _create_specialized_antibody(self, threat_signature: ThreatSignature, response_type: ResponseType) -> AntibodyAgent:
        """Create specialized antibody agent for specific threat"""
        antibody_id = f"antibody_{threat_signature.threat_type.value}_{int(datetime.utcnow().timestamp())}"
        
        # Extract patterns from threat signature
        detection_patterns = [threat_signature.error_pattern]
        if '_' in threat_signature.error_pattern:
            detection_patterns.extend(threat_signature.error_pattern.split('_'))
        
        # Determine response capabilities based on threat type
        response_capabilities = [response_type]
        
        # Add complementary response types
        if response_type == ResponseType.ERROR_CORRECTION:
            response_capabilities.append(ResponseType.PREVENTIVE_MEASURE)
        elif response_type == ResponseType.MEMORY_CLEANUP:
            response_capabilities.append(ResponseType.ROLLBACK_OPERATION)
        elif response_type == ResponseType.AGENT_ISOLATION:
            response_capabilities.append(ResponseType.SYSTEM_RESTART)
        
        antibody = AntibodyAgent(
            agent_id=antibody_id,
            specialized_threats=[threat_signature.threat_type],
            detection_patterns=detection_patterns,
            response_capabilities=response_capabilities,
            activation_count=0,
            success_rate=0.5
        )
        
        self.antibody_agents[antibody_id] = antibody
        
        # Persist to database
        await self._persist_antibody_agent(antibody)
        
        print(f"🦠 Created specialized antibody: {antibody_id} for {threat_signature.threat_type.value}")
        
        return antibody
    
    async def _execute_immune_response(self, threat_signature: ThreatSignature, response_type: ResponseType, antibody: AntibodyAgent) -> bool:
        """Execute immune response"""
        try:
            if response_type == ResponseType.ERROR_CORRECTION:
                return await self._execute_error_correction(threat_signature)
            elif response_type == ResponseType.AGENT_ISOLATION:
                return await self._execute_agent_isolation(threat_signature)
            elif response_type == ResponseType.MEMORY_CLEANUP:
                return await self._execute_memory_cleanup(threat_signature)
            elif response_type == ResponseType.CONNECTION_REPAIR:
                return await self._execute_connection_repair(threat_signature)
            elif response_type == ResponseType.RESOURCE_REALLOCATION:
                return await self._execute_resource_reallocation(threat_signature)
            elif response_type == ResponseType.ROLLBACK_OPERATION:
                return await self._execute_rollback_operation(threat_signature)
            elif response_type == ResponseType.PREVENTIVE_MEASURE:
                return await self._execute_preventive_measure(threat_signature)
            elif response_type == ResponseType.SYSTEM_RESTART:
                return await self._execute_system_restart(threat_signature)
            else:
                print(f"⚠️ Unknown response type: {response_type}")
                return False
                
        except Exception as e:
            print(f"❌ Error executing immune response {response_type}: {e}")
            return False
    
    # Response execution methods
    async def _execute_error_correction(self, threat_signature: ThreatSignature) -> bool:
        """Execute error correction response"""
        try:
            # Identify problematic agent from error pattern
            if 'agent_' in threat_signature.error_pattern:
                agent_id = threat_signature.error_pattern.split('_')[1]
                if agent_id in self.hive.active_agents:
                    agent = self.hive.active_agents[agent_id]
                    
                    # Reset agent state if possible
                    if hasattr(agent, 'reset_state'):
                        agent.reset_state()
                    
                    # Clear recent outputs that caused inconsistency
                    if hasattr(agent, 'recent_outputs'):
                        agent.recent_outputs = []
                    
                    return True
            
            return False
        except Exception:
            return False
    
    async def _execute_agent_isolation(self, threat_signature: ThreatSignature) -> bool:
        """Execute agent isolation response"""
        try:
            # Temporarily disable problematic agent
            if 'agent_' in threat_signature.error_pattern:
                agent_id = threat_signature.error_pattern.split('_')[1]
                if agent_id in self.hive.active_agents:
                    # Mark agent as isolated
                    agent = self.hive.active_agents[agent_id]
                    agent.isolated = True
                    agent.isolation_time = datetime.utcnow()
                    
                    print(f"🚫 Isolated agent {agent_id} due to threat")
                    return True
            
            return False
        except Exception:
            return False
    
    async def _execute_memory_cleanup(self, threat_signature: ThreatSignature) -> bool:
        """Execute memory cleanup response"""
        try:
            if hasattr(self.hive, 'memory_system'):
                # Perform memory integrity check and cleanup
                if hasattr(self.hive.memory_system, 'cleanup_corrupted'):
                    await self.hive.memory_system.cleanup_corrupted()
                
                # Force memory consolidation
                if hasattr(self.hive.memory_system, 'force_consolidation'):
                    await self.hive.memory_system.force_consolidation()
                
                return True
            
            return False
        except Exception:
            return False
    
    async def _execute_connection_repair(self, threat_signature: ThreatSignature) -> bool:
        """Execute connection repair response"""
        try:
            # Reset communication statistics
            if hasattr(self.hive, 'communication_stats'):
                self.hive.communication_stats.reset()
            
            # Reinitialize connections between agents
            if hasattr(self.hive, 'reinitialize_connections'):
                await self.hive.reinitialize_connections()
            
            return True
        except Exception:
            return False
    
    async def _execute_resource_reallocation(self, threat_signature: ThreatSignature) -> bool:
        """Execute resource reallocation response"""
        try:
            # Reduce resource usage by scaling down non-essential operations
            for agent in self.hive.active_agents.values():
                if hasattr(agent, 'reduce_resource_usage'):
                    agent.reduce_resource_usage(0.2)  # 20% reduction
            
            # Force garbage collection if possible
            import gc
            gc.collect()
            
            return True
        except Exception:
            return False
    
    async def _execute_rollback_operation(self, threat_signature: ThreatSignature) -> bool:
        """Execute rollback operation response"""
        try:
            # Rollback to last known good state
            if hasattr(self.hive, 'rollback_to_checkpoint'):
                await self.hive.rollback_to_checkpoint()
                return True
            
            # Alternative: reset problematic components
            if hasattr(self.hive, 'reset_to_defaults'):
                self.hive.reset_to_defaults()
                return True
            
            return False
        except Exception:
            return False
    
    async def _execute_preventive_measure(self, threat_signature: ThreatSignature) -> bool:
        """Execute preventive measure response"""
        try:
            # Increase monitoring frequency
            if hasattr(self.hive, 'monitoring_frequency'):
                self.hive.monitoring_frequency *= 2
            
            # Enable additional safety checks
            if hasattr(self.hive, 'enable_safety_mode'):
                self.hive.enable_safety_mode()
            
            return True
        except Exception:
            return False
    
    async def _execute_system_restart(self, threat_signature: ThreatSignature) -> bool:
        """Execute system restart response"""
        try:
            # Graceful restart of affected subsystems
            if hasattr(self.hive, 'restart_subsystem'):
                await self.hive.restart_subsystem('communication')
                await self.hive.restart_subsystem('memory')
                return True
            
            return False
        except Exception:
            return False
    
    # Database persistence methods
    async def _persist_immune_memory(self, memory_id: str, memory: ImmuneMemory):
        """Persist immune memory to database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO immune_memory (
                    memory_id, threat_signature, response_pattern, success_count,
                    failure_count, last_encountered, creation_time, response_time_avg,
                    effectiveness_score, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (memory_id) DO UPDATE SET
                    success_count = EXCLUDED.success_count,
                    failure_count = EXCLUDED.failure_count,
                    last_encountered = EXCLUDED.last_encountered,
                    response_time_avg = EXCLUDED.response_time_avg,
                    effectiveness_score = EXCLUDED.effectiveness_score,
                    metadata = EXCLUDED.metadata
            """, (
                memory_id,
                json.dumps(asdict(memory.threat_signature)),
                memory.response_pattern.value,
                memory.success_count,
                memory.failure_count,
                memory.last_encountered,
                memory.creation_time,
                memory.response_time_avg,
                memory.effectiveness_score,
                json.dumps(memory.metadata)
            ))
        finally:
            await conn.close()
    
    async def _persist_antibody_agent(self, antibody: AntibodyAgent):
        """Persist antibody agent to database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO antibody_agents (
                    agent_id, specialized_threats, detection_patterns, response_capabilities,
                    activation_count, success_rate, learning_rate, creation_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (agent_id) DO UPDATE SET
                    activation_count = EXCLUDED.activation_count,
                    success_rate = EXCLUDED.success_rate,
                    learning_rate = EXCLUDED.learning_rate
            """, (
                antibody.agent_id,
                [t.value for t in antibody.specialized_threats],
                antibody.detection_patterns,
                [r.value for r in antibody.response_capabilities],
                antibody.activation_count,
                antibody.success_rate,
                antibody.learning_rate,
                antibody.creation_time
            ))
        finally:
            await conn.close()
    
    async def _log_threat_incident(self, threat_signature: ThreatSignature, antibody: AntibodyAgent, 
                                 response_type: ResponseType, detection_time: datetime, success: bool):
        """Log threat incident to database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO threat_incidents (
                    threat_signature_hash, threat_type, severity_level, detection_time,
                    response_time, resolution_time, antibody_agent_id, response_type, success, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                threat_signature.to_hash(),
                threat_signature.threat_type.value,
                threat_signature.severity_level,
                detection_time,
                datetime.utcnow(),
                datetime.utcnow(),
                antibody.agent_id,
                response_type.value,
                success,
                json.dumps({
                    'error_pattern': threat_signature.error_pattern,
                    'context_hash': threat_signature.context_hash,
                    'system_load': threat_signature.system_load_level
                })
            ))
        finally:
            await conn.close()
    
    # Maintenance methods
    async def _cleanup_old_responses(self):
        """Clean up old active responses"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=30)
        
        completed_responses = []
        for threat_hash, response in self.active_responses.items():
            if response.get('status') in ['completed', 'failed'] and response.get('response_start_time', datetime.utcnow()) < cutoff_time:
                completed_responses.append(threat_hash)
        
        for threat_hash in completed_responses:
            del self.active_responses[threat_hash]
    
    async def _update_antibody_performance(self):
        """Update antibody agent performance metrics"""
        for antibody in self.antibody_agents.values():
            # Persist updated antibody data
            await self._persist_antibody_agent(antibody)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get immune system status"""
        status = {
            "immune_memories": len(self.immune_memory),
            "antibody_agents": len(self.antibody_agents),
            "active_responses": len(self.active_responses),
            "memory_effectiveness": {},
            "antibody_performance": {},
            "recent_incidents": []
        }
        
        # Calculate memory effectiveness
        for memory_id, memory in list(self.immune_memory.items())[:10]:  # Top 10
            status["memory_effectiveness"][memory.threat_signature.threat_type.value] = {
                "success_rate": memory.success_rate,
                "effectiveness_score": memory.effectiveness_score,
                "response_time_avg": memory.response_time_avg
            }
        
        # Calculate antibody performance
        for antibody_id, antibody in list(self.antibody_agents.items())[:10]:  # Top 10
            status["antibody_performance"][antibody_id] = {
                "activation_count": antibody.activation_count,
                "success_rate": antibody.success_rate,
                "specialized_threats": [t.value for t in antibody.specialized_threats]
            }
        
        # Get recent incidents
        for response in list(self.active_responses.values())[:5]:  # Recent 5
            status["recent_incidents"].append({
                "threat_type": response["threat_signature"].threat_type.value,
                "status": response["status"],
                "detection_time": response["detection_time"].isoformat() if response["detection_time"] else None
            })
        
        return status

# Testing function
async def test_adaptive_immune_system(hive, database_url: str):
    """Test the adaptive immune system"""
    print("🧪 Testing Adaptive Immune System...")
    
    # Initialize system
    immune_system = AdaptiveImmuneSystem(hive, database_url)
    await immune_system.initialize()
    
    # Simulate a threat
    test_threat = ThreatSignature(
        threat_type=ThreatType.LOGIC_ERROR,
        error_pattern="test_inconsistent_outputs_agent_1",
        context_hash="test_context_123",
        agent_states_hash="test_states_456", 
        system_load_level="medium",
        timestamp_pattern="14_3",
        severity_level=0.8
    )
    
    # Handle the threat
    await immune_system._handle_threat(test_threat)
    
    # Wait for response to complete
    await asyncio.sleep(2)
    
    # Test status
    status = await immune_system.get_system_status()
    print(f"📊 Immune System Status: {json.dumps(status, indent=2, default=str)}")
    
    # Test multiple threats to trigger memory creation
    for i in range(3):
        threat = ThreatSignature(
            threat_type=ThreatType.COMMUNICATION_FAILURE,
            error_pattern=f"test_timeout_agent_{i}",
            context_hash=f"test_context_{i}",
            agent_states_hash="test_states_789",
            system_load_level="high",
            timestamp_pattern="15_2", 
            severity_level=0.7
        )
        await immune_system._handle_threat(threat)
        await asyncio.sleep(1)
    
    # Check final status
    final_status = await immune_system.get_system_status()
    print(f"📋 Final Status: {json.dumps(final_status, indent=2, default=str)}")
    
    print("✅ Adaptive Immune System test complete!")
    return immune_system

if __name__ == "__main__":
    # Quick test run
    import asyncio
    
    class MockHive:
        def __init__(self):
            self.active_agents = {
                "agent_1": type('Agent', (), {
                    'recent_outputs': ['output1', 'output2', 'different_output'],
                    'state': 'active',
                    'isolated': False
                })(),
                "agent_2": type('Agent', (), {
                    'recent_outputs': ['consistent', 'consistent', 'consistent'],
                    'state': 'active', 
                    'isolated': False
                })()
            }
            self.communication_stats = {'failure_rate': 0.1}
            self.baseline_performance = 1.0
            self.performance_metrics = {'current_score': 0.6}
    
    async def main():
        hive = MockHive()
        database_url = "postgresql://postgres:pass@localhost:5432/sentient"
        await test_adaptive_immune_system(hive, database_url)
    
    asyncio.run(main())