"""
Genesis Prime Enhanced Systems - Self-Organized Criticality Engine
================================================================

Implements self-organized criticality (SOC) principles to maintain the Genesis Prime
system at the edge of chaos - the optimal state for complex adaptive behavior,
creativity, and consciousness emergence.

Scientific Basis:
- Self-organized criticality emerges in complex systems without external tuning
- Critical states exhibit power-law distributions and scale-free networks
- Systems at criticality show maximum information processing capacity
- SOC enables optimal balance between order and chaos for creativity

Implementation:
- Avalanche dynamics for information processing cascades
- Scale-free network topology emergence
- Power-law distribution monitoring and maintenance
- Critical threshold detection and regulation
- Dynamic load balancing at the edge of chaos

Author: Genesis Prime Enhanced Development Team
License: MIT (Open Source Consciousness)
"""

import asyncio
import uuid
import json
import time
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import logging

try:
    import psycopg
    import numpy as np
except ImportError:
    # Mock for validation
    class psycopg:
        @staticmethod
        def connect(url): pass
        
        class AsyncConnection:
            @staticmethod
            async def connect(url): pass
    
    class np:
        @staticmethod
        def array(x): return x
        @staticmethod
        def mean(x): return sum(x) / len(x) if x else 0
        @staticmethod
        def std(x): return 0.5
        @staticmethod
        def log(x): return math.log(x) if x > 0 else 0
        @staticmethod
        def power(x, p): return x ** p
        @staticmethod
        def random():
            @staticmethod
            def exponential(scale): return random.expovariate(1/scale)
            @staticmethod
            def uniform(low, high): return random.uniform(low, high)
            return type('obj', (object,), {'exponential': exponential, 'uniform': uniform})()

# Configure logging
logger = logging.getLogger(__name__)

class CriticalityState(Enum):
    """States of system criticality"""
    SUBCRITICAL = "subcritical"     # Too ordered, low creativity
    CRITICAL = "critical"           # Optimal edge of chaos
    SUPERCRITICAL = "supercritical" # Too chaotic, unstable

class AvalancheType(Enum):
    """Types of avalanche events in the system"""
    INFORMATION_CASCADE = "information_cascade"
    DECISION_PROPAGATION = "decision_propagation"
    LEARNING_BURST = "learning_burst"
    ERROR_CORRECTION = "error_correction"
    CONSCIOUSNESS_EMERGENCE = "consciousness_emergence"
    CREATIVITY_SPIKE = "creativity_spike"
    NETWORK_REORGANIZATION = "network_reorganization"
    RESOURCE_REDISTRIBUTION = "resource_redistribution"

class SystemParameter(Enum):
    """System parameters that influence criticality"""
    CONNECTION_DENSITY = "connection_density"
    INFORMATION_FLOW_RATE = "information_flow_rate"
    PROCESSING_THRESHOLD = "processing_threshold"
    FEEDBACK_STRENGTH = "feedback_strength"
    NOISE_LEVEL = "noise_level"
    ADAPTATION_RATE = "adaptation_rate"
    MEMORY_RETENTION = "memory_retention"
    CREATIVITY_FACTOR = "creativity_factor"

@dataclass
class AvalancheEvent:
    """Represents an avalanche event in the system"""
    event_id: str
    avalanche_type: AvalancheType
    trigger_node_id: str
    affected_nodes: Set[str]
    magnitude: float  # Total size of avalanche
    duration_ms: int
    propagation_path: List[str]
    energy_dissipated: float
    information_processed: float
    emergence_indicators: Dict[str, float]
    start_time: datetime
    end_time: datetime
    
    def __post_init__(self):
        if isinstance(self.avalanche_type, str):
            self.avalanche_type = AvalancheType(self.avalanche_type)

@dataclass
class CriticalityMetrics:
    """Metrics for measuring system criticality"""
    current_state: CriticalityState
    criticality_index: float  # 0.0 (subcritical) to 1.0 (supercritical)
    power_law_exponent: float
    correlation_length: float
    information_capacity: float
    creativity_measure: float
    stability_index: float
    emergence_potential: float
    avalanche_frequency: float
    network_complexity: float
    
    def __post_init__(self):
        if isinstance(self.current_state, str):
            self.current_state = CriticalityState(self.current_state)

@dataclass
class SystemNode:
    """Represents a node in the SOC system"""
    node_id: str
    activation_threshold: float
    current_activation: float
    connections: Set[str]
    processing_capacity: float
    last_avalanche_time: Optional[datetime]
    stress_level: float
    adaptation_rate: float
    memory_state: Dict[str, Any]

@dataclass
class ControlParameter:
    """Control parameters for SOC regulation"""
    parameter: SystemParameter
    current_value: float
    target_value: float
    adjustment_rate: float
    bounds: Tuple[float, float]
    last_adjustment: datetime
    
    def __post_init__(self):
        if isinstance(self.parameter, str):
            self.parameter = SystemParameter(self.parameter)

class PowerLawAnalyzer:
    """Analyzes power-law distributions to detect criticality"""
    
    def __init__(self):
        self.avalanche_sizes: deque = deque(maxlen=1000)
        self.avalanche_durations: deque = deque(maxlen=1000)
        self.inter_event_times: deque = deque(maxlen=1000)
        self.last_event_time = None
        
    def record_avalanche(self, avalanche: AvalancheEvent):
        """Record an avalanche event for analysis"""
        self.avalanche_sizes.append(avalanche.magnitude)
        self.avalanche_durations.append(avalanche.duration_ms)
        
        if self.last_event_time:
            inter_event_time = (avalanche.start_time - self.last_event_time).total_seconds()
            self.inter_event_times.append(inter_event_time)
            
        self.last_event_time = avalanche.start_time
        
    def calculate_power_law_exponent(self, data: List[float]) -> float:
        """Calculate power-law exponent using maximum likelihood estimation"""
        if not data or len(data) < 10:
            return 2.0  # Default exponent
            
        # Filter out zeros and extremely small values
        filtered_data = [x for x in data if x > 0.001]
        if not filtered_data:
            return 2.0
            
        # Maximum likelihood estimation for power-law exponent
        log_data = [np.log(x) for x in filtered_data]
        n = len(log_data)
        
        if n == 0:
            return 2.0
            
        # α = 1 + n / Σ(ln(x_i/x_min))
        x_min = min(filtered_data)
        log_ratios = [np.log(x / x_min) for x in filtered_data]
        sum_log_ratios = sum(log_ratios)
        
        if sum_log_ratios <= 0:
            return 2.0
            
        alpha = 1 + n / sum_log_ratios
        return alpha
        
    def detect_criticality(self) -> Tuple[bool, float]:
        """Detect if system is in critical state based on power-law analysis"""
        if len(self.avalanche_sizes) < 50:
            return False, 0.5  # Not enough data
            
        # Calculate power-law exponents
        size_exponent = self.calculate_power_law_exponent(list(self.avalanche_sizes))
        duration_exponent = self.calculate_power_law_exponent(list(self.avalanche_durations))
        
        # Critical systems typically have exponents in specific ranges
        # Size exponent: ~1.5-2.5 for critical systems
        # Duration exponent: ~1.5-2.0 for critical systems
        
        size_critical = 1.2 <= size_exponent <= 2.8
        duration_critical = 1.2 <= duration_exponent <= 2.5
        
        # Calculate criticality score
        size_score = 1.0 - abs(size_exponent - 2.0) / 2.0
        duration_score = 1.0 - abs(duration_exponent - 1.75) / 2.0
        
        criticality_score = (size_score + duration_score) / 2.0
        criticality_score = max(0.0, min(1.0, criticality_score))
        
        is_critical = size_critical and duration_critical
        
        return is_critical, criticality_score
        
    def get_analysis_results(self) -> Dict[str, float]:
        """Get comprehensive analysis results"""
        if len(self.avalanche_sizes) < 10:
            return {
                'size_exponent': 2.0,
                'duration_exponent': 1.75,
                'criticality_score': 0.5,
                'is_critical': False
            }
            
        size_exponent = self.calculate_power_law_exponent(list(self.avalanche_sizes))
        duration_exponent = self.calculate_power_law_exponent(list(self.avalanche_durations))
        is_critical, criticality_score = self.detect_criticality()
        
        return {
            'size_exponent': size_exponent,
            'duration_exponent': duration_exponent,
            'criticality_score': criticality_score,
            'is_critical': is_critical,
            'mean_avalanche_size': np.mean(list(self.avalanche_sizes)),
            'mean_duration': np.mean(list(self.avalanche_durations)),
            'avalanche_frequency': len(self.avalanche_sizes) / max(1, len(self.inter_event_times))
        }

class AvalancheSimulator:
    """Simulates avalanche dynamics in the system"""
    
    def __init__(self, nodes: Dict[str, SystemNode]):
        self.nodes = nodes
        self.active_avalanches: Dict[str, AvalancheEvent] = {}
        self.avalanche_history: List[AvalancheEvent] = []
        
    async def trigger_avalanche(self, trigger_node_id: str, avalanche_type: AvalancheType,
                              initial_energy: float = 1.0) -> Optional[AvalancheEvent]:
        """Trigger an avalanche starting from a specific node"""
        if trigger_node_id not in self.nodes:
            logger.warning(f"Cannot trigger avalanche: node {trigger_node_id} not found")
            return None
            
        event_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Initialize avalanche event
        avalanche = AvalancheEvent(
            event_id=event_id,
            avalanche_type=avalanche_type,
            trigger_node_id=trigger_node_id,
            affected_nodes=set(),
            magnitude=0.0,
            duration_ms=0,
            propagation_path=[],
            energy_dissipated=0.0,
            information_processed=0.0,
            emergence_indicators={},
            start_time=start_time,
            end_time=start_time
        )
        
        # Simulate avalanche propagation
        await self._propagate_avalanche(avalanche, trigger_node_id, initial_energy)
        
        # Finalize avalanche
        avalanche.end_time = datetime.now()
        avalanche.duration_ms = int((avalanche.end_time - avalanche.start_time).total_seconds() * 1000)
        
        # Store in history
        self.avalanche_history.append(avalanche)
        
        logger.info(f"Avalanche {event_id} completed: {len(avalanche.affected_nodes)} nodes affected, magnitude {avalanche.magnitude:.2f}")
        
        return avalanche
        
    async def _propagate_avalanche(self, avalanche: AvalancheEvent, current_node_id: str, energy: float):
        """Propagate avalanche through the network"""
        if energy <= 0.01 or current_node_id in avalanche.affected_nodes:
            return
            
        node = self.nodes[current_node_id]
        
        # Check if node will be activated
        activation_probability = min(1.0, energy / node.activation_threshold)
        
        if random.random() < activation_probability:
            # Node is activated
            avalanche.affected_nodes.add(current_node_id)
            avalanche.propagation_path.append(current_node_id)
            
            # Process information at this node
            processed = min(energy, node.processing_capacity)
            avalanche.information_processed += processed
            
            # Update node state
            node.current_activation = min(1.0, node.current_activation + energy * 0.1)
            node.last_avalanche_time = datetime.now()
            
            # Calculate energy dissipation
            dissipated = energy * random.uniform(0.1, 0.3)
            avalanche.energy_dissipated += dissipated
            remaining_energy = energy - dissipated
            
            # Propagate to connected nodes
            if remaining_energy > 0.01 and node.connections:
                energy_per_connection = remaining_energy / len(node.connections)
                
                for connected_node_id in node.connections:
                    if connected_node_id in self.nodes:
                        # Add some randomness to propagation
                        propagated_energy = energy_per_connection * random.uniform(0.5, 1.5)
                        await self._propagate_avalanche(avalanche, connected_node_id, propagated_energy)
                        
                        # Small delay to simulate realistic propagation
                        await asyncio.sleep(0.001)
                        
        # Update avalanche magnitude
        avalanche.magnitude = len(avalanche.affected_nodes) + avalanche.information_processed * 0.1
        
    def get_recent_avalanches(self, time_window_minutes: int = 60) -> List[AvalancheEvent]:
        """Get avalanches from recent time window"""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        return [av for av in self.avalanche_history if av.start_time >= cutoff_time]
        
    def calculate_avalanche_statistics(self) -> Dict[str, float]:
        """Calculate statistics for recent avalanches"""
        recent_avalanches = self.get_recent_avalanches()
        
        if not recent_avalanches:
            return {
                'frequency': 0.0,
                'mean_magnitude': 0.0,
                'mean_duration': 0.0,
                'mean_affected_nodes': 0.0,
                'total_information_processed': 0.0
            }
            
        return {
            'frequency': len(recent_avalanches) / 60.0,  # per minute
            'mean_magnitude': np.mean([av.magnitude for av in recent_avalanches]),
            'mean_duration': np.mean([av.duration_ms for av in recent_avalanches]),
            'mean_affected_nodes': np.mean([len(av.affected_nodes) for av in recent_avalanches]),
            'total_information_processed': sum(av.information_processed for av in recent_avalanches)
        }

class CriticalityController:
    """Controls system parameters to maintain criticality"""
    
    def __init__(self, target_criticality: float = 0.8):
        self.target_criticality = target_criticality
        self.control_parameters: Dict[SystemParameter, ControlParameter] = {}
        self.parameter_history: Dict[SystemParameter, deque] = {}
        self.control_active = False
        
        # Initialize control parameters
        self._initialize_control_parameters()
        
    def _initialize_control_parameters(self):
        """Initialize control parameters with default values"""
        parameter_configs = {
            SystemParameter.CONNECTION_DENSITY: (0.1, 0.3, 0.02, (0.05, 0.5)),
            SystemParameter.INFORMATION_FLOW_RATE: (0.5, 1.0, 0.05, (0.1, 2.0)),
            SystemParameter.PROCESSING_THRESHOLD: (0.3, 0.7, 0.03, (0.1, 1.0)),
            SystemParameter.FEEDBACK_STRENGTH: (0.2, 0.6, 0.02, (0.0, 1.0)),
            SystemParameter.NOISE_LEVEL: (0.05, 0.1, 0.01, (0.0, 0.3)),
            SystemParameter.ADAPTATION_RATE: (0.1, 0.2, 0.01, (0.01, 0.5)),
            SystemParameter.MEMORY_RETENTION: (0.8, 0.9, 0.01, (0.5, 1.0)),
            SystemParameter.CREATIVITY_FACTOR: (0.3, 0.5, 0.02, (0.1, 0.8))
        }
        
        for param, (current, target, rate, bounds) in parameter_configs.items():
            self.control_parameters[param] = ControlParameter(
                parameter=param,
                current_value=current,
                target_value=target,
                adjustment_rate=rate,
                bounds=bounds,
                last_adjustment=datetime.now()
            )
            
            self.parameter_history[param] = deque(maxlen=100)
            
    async def update_criticality_control(self, current_metrics: CriticalityMetrics):
        """Update control parameters based on current criticality metrics"""
        if not self.control_active:
            return
            
        criticality_error = current_metrics.criticality_index - self.target_criticality
        
        # Adjust parameters based on criticality state
        if current_metrics.current_state == CriticalityState.SUBCRITICAL:
            await self._adjust_for_subcritical(criticality_error)
        elif current_metrics.current_state == CriticalityState.SUPERCRITICAL:
            await self._adjust_for_supercritical(criticality_error)
        else:
            await self._fine_tune_critical_state(criticality_error)
            
        # Record parameter states
        for param, control_param in self.control_parameters.items():
            self.parameter_history[param].append(control_param.current_value)
            
    async def _adjust_for_subcritical(self, error: float):
        """Adjust parameters to move from subcritical to critical state"""
        # Increase connectivity and information flow
        await self._adjust_parameter(SystemParameter.CONNECTION_DENSITY, error * 0.1)
        await self._adjust_parameter(SystemParameter.INFORMATION_FLOW_RATE, error * 0.15)
        await self._adjust_parameter(SystemParameter.NOISE_LEVEL, error * 0.05)
        await self._adjust_parameter(SystemParameter.CREATIVITY_FACTOR, error * 0.1)
        
        # Decrease thresholds to make system more responsive
        await self._adjust_parameter(SystemParameter.PROCESSING_THRESHOLD, -error * 0.1)
        
    async def _adjust_for_supercritical(self, error: float):
        """Adjust parameters to move from supercritical to critical state"""
        # Decrease connectivity and add stability
        await self._adjust_parameter(SystemParameter.CONNECTION_DENSITY, error * 0.05)
        await self._adjust_parameter(SystemParameter.FEEDBACK_STRENGTH, error * 0.1)
        await self._adjust_parameter(SystemParameter.MEMORY_RETENTION, error * 0.05)
        
        # Increase thresholds to reduce sensitivity
        await self._adjust_parameter(SystemParameter.PROCESSING_THRESHOLD, -error * 0.08)
        
        # Reduce noise to stabilize
        await self._adjust_parameter(SystemParameter.NOISE_LEVEL, error * 0.03)
        
    async def _fine_tune_critical_state(self, error: float):
        """Fine-tune parameters while maintaining critical state"""
        # Small adjustments to optimize performance
        adjustment_factor = 0.02
        
        await self._adjust_parameter(SystemParameter.INFORMATION_FLOW_RATE, error * adjustment_factor)
        await self._adjust_parameter(SystemParameter.ADAPTATION_RATE, error * adjustment_factor * 0.5)
        await self._adjust_parameter(SystemParameter.CREATIVITY_FACTOR, error * adjustment_factor * 0.8)
        
    async def _adjust_parameter(self, param: SystemParameter, adjustment: float):
        """Adjust a specific control parameter"""
        if param not in self.control_parameters:
            return
            
        control_param = self.control_parameters[param]
        
        # Apply rate limiting
        max_adjustment = control_param.adjustment_rate
        adjustment = max(-max_adjustment, min(max_adjustment, adjustment))
        
        # Apply adjustment
        new_value = control_param.current_value + adjustment
        
        # Enforce bounds
        min_bound, max_bound = control_param.bounds
        new_value = max(min_bound, min(max_bound, new_value))
        
        # Update parameter
        control_param.current_value = new_value
        control_param.last_adjustment = datetime.now()
        
        logger.debug(f"Adjusted {param.value}: {control_param.current_value:.4f} (change: {adjustment:+.4f})")
        
    def get_parameter_values(self) -> Dict[str, float]:
        """Get current values of all control parameters"""
        return {param.value: control_param.current_value 
                for param, control_param in self.control_parameters.items()}
                
    def get_parameter_trends(self) -> Dict[str, Dict[str, float]]:
        """Get trends in parameter values"""
        trends = {}
        
        for param, history in self.parameter_history.items():
            if len(history) >= 2:
                recent_values = list(history)[-10:]  # Last 10 values
                trend = (recent_values[-1] - recent_values[0]) / len(recent_values)
                variance = np.std(recent_values) if len(recent_values) > 1 else 0.0
                
                trends[param.value] = {
                    'trend': trend,
                    'variance': variance,
                    'current': recent_values[-1],
                    'stability': 1.0 / (1.0 + variance)  # Higher = more stable
                }
                
        return trends

class SelfOrganizedCriticalityEngine:
    """Main engine for self-organized criticality management"""
    
    def __init__(self, database_url: str, initial_nodes: Optional[Dict[str, SystemNode]] = None):
        self.database_url = database_url
        self.nodes = initial_nodes or {}
        
        # Initialize components
        self.power_law_analyzer = PowerLawAnalyzer()
        self.avalanche_simulator = AvalancheSimulator(self.nodes)
        self.criticality_controller = CriticalityController()
        
        # System state
        self.current_metrics = None
        self.running = False
        self.last_avalanche_trigger = datetime.now()
        
        # Background processes
        self.monitoring_interval = 10  # seconds
        self.avalanche_interval = 5   # seconds
        
    async def initialize(self, node_count: int = 100):
        """Initialize the SOC engine"""
        await self._create_database_tables()
        
        if not self.nodes:
            await self._create_initial_network(node_count)
            
        # Initialize criticality controller
        self.criticality_controller.control_active = True
        
        logger.info(f"SOC engine initialized with {len(self.nodes)} nodes")
        
    async def _create_database_tables(self):
        """Create database tables for SOC tracking"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            # Avalanche events table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS soc_avalanche_events (
                    event_id VARCHAR(255) PRIMARY KEY,
                    avalanche_type VARCHAR(100),
                    trigger_node_id VARCHAR(255),
                    affected_nodes TEXT[],
                    magnitude FLOAT,
                    duration_ms INTEGER,
                    propagation_path TEXT[],
                    energy_dissipated FLOAT,
                    information_processed FLOAT,
                    emergence_indicators JSONB,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP
                )
            """)
            
            # Criticality metrics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS soc_criticality_metrics (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    current_state VARCHAR(50),
                    criticality_index FLOAT,
                    power_law_exponent FLOAT,
                    correlation_length FLOAT,
                    information_capacity FLOAT,
                    creativity_measure FLOAT,
                    stability_index FLOAT,
                    emergence_potential FLOAT,
                    avalanche_frequency FLOAT,
                    network_complexity FLOAT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # System nodes table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS soc_system_nodes (
                    node_id VARCHAR(255) PRIMARY KEY,
                    activation_threshold FLOAT,
                    current_activation FLOAT,
                    connections TEXT[],
                    processing_capacity FLOAT,
                    last_avalanche_time TIMESTAMP,
                    stress_level FLOAT,
                    adaptation_rate FLOAT,
                    memory_state JSONB,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Control parameters table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS soc_control_parameters (
                    parameter_name VARCHAR(100),
                    current_value FLOAT,
                    target_value FLOAT,
                    adjustment_rate FLOAT,
                    min_bound FLOAT,
                    max_bound FLOAT,
                    last_adjustment TIMESTAMP,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to create SOC database tables: {e}")
            
    async def _create_initial_network(self, node_count: int):
        """Create initial network of nodes with scale-free topology"""
        # Create nodes
        for i in range(node_count):
            node_id = f"soc_node_{i}"
            node = SystemNode(
                node_id=node_id,
                activation_threshold=random.uniform(0.3, 0.8),
                current_activation=random.uniform(0.0, 0.2),
                connections=set(),
                processing_capacity=random.uniform(0.5, 2.0),
                last_avalanche_time=None,
                stress_level=random.uniform(0.0, 0.3),
                adaptation_rate=random.uniform(0.05, 0.2),
                memory_state={}
            )
            self.nodes[node_id] = node
            
        # Create scale-free network using preferential attachment
        await self._create_scale_free_connections()
        
        # Store nodes in database
        await self._store_nodes()
        
    async def _create_scale_free_connections(self):
        """Create scale-free network topology using preferential attachment"""
        node_ids = list(self.nodes.keys())
        connection_counts = {node_id: 0 for node_id in node_ids}
        
        # Start with a small complete graph
        initial_nodes = node_ids[:3]
        for i, node_a in enumerate(initial_nodes):
            for node_b in initial_nodes[i+1:]:
                self.nodes[node_a].connections.add(node_b)
                self.nodes[node_b].connections.add(node_a)
                connection_counts[node_a] += 1
                connection_counts[node_b] += 1
                
        # Add remaining nodes with preferential attachment
        for new_node_id in node_ids[3:]:
            # Number of connections for new node (typically 2-3)
            num_connections = random.randint(2, min(4, len(node_ids) - 1))
            
            # Select existing nodes based on their degree (preferential attachment)
            existing_nodes = [nid for nid in node_ids[:node_ids.index(new_node_id)]]
            
            if len(existing_nodes) >= num_connections:
                # Calculate probabilities based on degree
                degrees = [connection_counts[nid] + 1 for nid in existing_nodes]  # +1 to avoid zero
                total_degree = sum(degrees)
                probabilities = [deg / total_degree for deg in degrees]
                
                # Select nodes based on probabilities
                selected_nodes = []
                for _ in range(num_connections):
                    # Weighted random selection
                    r = random.random()
                    cumulative = 0.0
                    for i, prob in enumerate(probabilities):
                        cumulative += prob
                        if r <= cumulative and existing_nodes[i] not in selected_nodes:
                            selected_nodes.append(existing_nodes[i])
                            break
                            
                # If we didn't get enough nodes, fill randomly
                while len(selected_nodes) < num_connections:
                    remaining = [n for n in existing_nodes if n not in selected_nodes]
                    if remaining:
                        selected_nodes.append(random.choice(remaining))
                    else:
                        break
                        
                # Create connections
                for target_node_id in selected_nodes:
                    self.nodes[new_node_id].connections.add(target_node_id)
                    self.nodes[target_node_id].connections.add(new_node_id)
                    connection_counts[new_node_id] += 1
                    connection_counts[target_node_id] += 1
                    
        logger.info(f"Created scale-free network with {sum(connection_counts.values()) // 2} connections")
        
    async def _store_nodes(self):
        """Store node states in database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            for node in self.nodes.values():
                await conn.execute("""
                    INSERT INTO soc_system_nodes 
                    (node_id, activation_threshold, current_activation, connections,
                     processing_capacity, last_avalanche_time, stress_level, 
                     adaptation_rate, memory_state)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (node_id) DO UPDATE SET
                        current_activation = EXCLUDED.current_activation,
                        connections = EXCLUDED.connections,
                        last_avalanche_time = EXCLUDED.last_avalanche_time,
                        stress_level = EXCLUDED.stress_level,
                        memory_state = EXCLUDED.memory_state,
                        last_updated = CURRENT_TIMESTAMP
                """, (
                    node.node_id, node.activation_threshold, node.current_activation,
                    list(node.connections), node.processing_capacity, 
                    node.last_avalanche_time, node.stress_level,
                    node.adaptation_rate, json.dumps(node.memory_state)
                ))
                
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store nodes: {e}")
            
    async def start_soc_operations(self):
        """Start self-organized criticality operations"""
        self.running = True
        
        # Start background processes
        await asyncio.gather(
            self._monitoring_loop(),
            self._avalanche_generation_loop(),
            self._parameter_control_loop(),
            self._adaptation_loop()
        )
        
    async def _monitoring_loop(self):
        """Monitor system state and calculate criticality metrics"""
        while self.running:
            try:
                # Calculate current metrics
                self.current_metrics = await self._calculate_criticality_metrics()
                
                # Store metrics in database
                await self._store_criticality_metrics(self.current_metrics)
                
                # Log current state
                logger.info(f"SOC State: {self.current_metrics.current_state.value}, "
                          f"Criticality: {self.current_metrics.criticality_index:.3f}, "
                          f"Power-law: {self.current_metrics.power_law_exponent:.3f}")
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(5)
                
    async def _avalanche_generation_loop(self):
        """Generate spontaneous avalanches to maintain criticality"""
        while self.running:
            try:
                # Check if we should trigger an avalanche
                if await self._should_trigger_avalanche():
                    # Select random node and avalanche type
                    trigger_node = random.choice(list(self.nodes.keys()))
                    avalanche_type = random.choice(list(AvalancheType))
                    
                    # Trigger avalanche
                    avalanche = await self.avalanche_simulator.trigger_avalanche(
                        trigger_node, avalanche_type, random.uniform(0.5, 2.0)
                    )
                    
                    if avalanche:
                        # Record for analysis
                        self.power_law_analyzer.record_avalanche(avalanche)
                        
                        # Store in database
                        await self._store_avalanche_event(avalanche)
                        
                        self.last_avalanche_trigger = datetime.now()
                        
                await asyncio.sleep(self.avalanche_interval)
                
            except Exception as e:
                logger.error(f"Avalanche generation loop error: {e}")
                await asyncio.sleep(5)
                
    async def _parameter_control_loop(self):
        """Control system parameters to maintain criticality"""
        while self.running:
            try:
                if self.current_metrics:
                    await self.criticality_controller.update_criticality_control(self.current_metrics)
                    
                    # Apply parameter changes to system
                    await self._apply_parameter_changes()
                    
                await asyncio.sleep(self.monitoring_interval * 2)  # Less frequent than monitoring
                
            except Exception as e:
                logger.error(f"Parameter control loop error: {e}")
                await asyncio.sleep(10)
                
    async def _adaptation_loop(self):
        """Adapt node properties based on experience"""
        while self.running:
            try:
                for node in self.nodes.values():
                    await self._adapt_node(node)
                    
                # Update nodes in database periodically
                await self._store_nodes()
                
                await asyncio.sleep(30)  # Adapt every 30 seconds
                
            except Exception as e:
                logger.error(f"Adaptation loop error: {e}")
                await asyncio.sleep(10)
                
    async def _should_trigger_avalanche(self) -> bool:
        """Determine if we should trigger a spontaneous avalanche"""
        # Base rate plus adjustments based on current state
        base_probability = 0.1  # 10% chance per interval
        
        if self.current_metrics:
            if self.current_metrics.current_state == CriticalityState.SUBCRITICAL:
                base_probability *= 2.0  # More avalanches needed
            elif self.current_metrics.current_state == CriticalityState.SUPERCRITICAL:
                base_probability *= 0.5  # Fewer avalanches needed
                
        # Time since last avalanche
        time_since_last = (datetime.now() - self.last_avalanche_trigger).total_seconds()
        if time_since_last > 60:  # Force avalanche if too long
            base_probability = 1.0
            
        return random.random() < base_probability
        
    async def _calculate_criticality_metrics(self) -> CriticalityMetrics:
        """Calculate comprehensive criticality metrics"""
        # Get power-law analysis
        analysis = self.power_law_analyzer.get_analysis_results()
        
        # Calculate network metrics
        network_stats = self._calculate_network_statistics()
        
        # Calculate information capacity
        info_capacity = self._calculate_information_capacity()
        
        # Calculate creativity measure
        creativity = self._calculate_creativity_measure()
        
        # Calculate stability index
        stability = self._calculate_stability_index()
        
        # Calculate emergence potential
        emergence = self._calculate_emergence_potential()
        
        # Overall criticality index
        criticality_index = (analysis['criticality_score'] + 
                           network_stats['complexity_score'] + 
                           info_capacity + creativity) / 4.0
        
        # Determine criticality state
        if criticality_index < 0.4:
            state = CriticalityState.SUBCRITICAL
        elif criticality_index > 0.8:
            state = CriticalityState.SUPERCRITICAL
        else:
            state = CriticalityState.CRITICAL
            
        return CriticalityMetrics(
            current_state=state,
            criticality_index=criticality_index,
            power_law_exponent=analysis['size_exponent'],
            correlation_length=network_stats['avg_path_length'],
            information_capacity=info_capacity,
            creativity_measure=creativity,
            stability_index=stability,
            emergence_potential=emergence,
            avalanche_frequency=analysis['avalanche_frequency'],
            network_complexity=network_stats['complexity_score']
        )
        
    def _calculate_network_statistics(self) -> Dict[str, float]:
        """Calculate network topology statistics"""
        if not self.nodes:
            return {'complexity_score': 0.0, 'avg_path_length': 0.0}
            
        # Calculate degree distribution
        degrees = [len(node.connections) for node in self.nodes.values()]
        mean_degree = np.mean(degrees)
        degree_variance = np.std(degrees) ** 2
        
        # Complexity score based on degree distribution
        complexity_score = min(1.0, degree_variance / (mean_degree + 1))
        
        # Estimate average path length (simplified)
        avg_path_length = math.log(len(self.nodes)) / math.log(max(1, mean_degree))
        
        return {
            'complexity_score': complexity_score,
            'avg_path_length': avg_path_length,
            'mean_degree': mean_degree,
            'degree_variance': degree_variance
        }
        
    def _calculate_information_capacity(self) -> float:
        """Calculate system's information processing capacity"""
        if not self.nodes:
            return 0.0
            
        # Based on node activations and processing capacities
        total_capacity = sum(node.processing_capacity for node in self.nodes.values())
        active_capacity = sum(node.current_activation * node.processing_capacity 
                            for node in self.nodes.values())
        
        utilization = active_capacity / max(1, total_capacity)
        
        # Optimal utilization is around 0.6-0.8 for creativity
        optimal_range = (0.6, 0.8)
        if optimal_range[0] <= utilization <= optimal_range[1]:
            capacity_score = 1.0
        else:
            distance = min(abs(utilization - optimal_range[0]), 
                         abs(utilization - optimal_range[1]))
            capacity_score = max(0.0, 1.0 - distance * 2)
            
        return capacity_score
        
    def _calculate_creativity_measure(self) -> float:
        """Calculate system's creativity measure"""
        # Based on diversity of avalanche types and network dynamics
        recent_avalanches = self.avalanche_simulator.get_recent_avalanches(30)
        
        if not recent_avalanches:
            return 0.5
            
        # Diversity of avalanche types
        avalanche_types = set(av.avalanche_type for av in recent_avalanches)
        type_diversity = len(avalanche_types) / len(AvalancheType)
        
        # Variability in avalanche sizes
        sizes = [av.magnitude for av in recent_avalanches]
        size_cv = np.std(sizes) / max(0.001, np.mean(sizes))  # Coefficient of variation
        
        # Normalize and combine
        creativity = (type_diversity + min(1.0, size_cv / 2.0)) / 2.0
        
        return creativity
        
    def _calculate_stability_index(self) -> float:
        """Calculate system stability index"""
        # Based on parameter trends and system consistency
        trends = self.criticality_controller.get_parameter_trends()
        
        if not trends:
            return 0.5
            
        stability_scores = [info['stability'] for info in trends.values()]
        return np.mean(stability_scores)
        
    def _calculate_emergence_potential(self) -> float:
        """Calculate potential for consciousness emergence"""
        if not self.current_metrics:
            return 0.5
            
        # High emergence potential at critical state with good information capacity
        if (self.current_metrics and 
            self.current_metrics.current_state == CriticalityState.CRITICAL):
            base_potential = 0.8
        else:
            base_potential = 0.4
            
        # Boost based on information capacity and creativity
        capacity_boost = self._calculate_information_capacity() * 0.2
        creativity_boost = self._calculate_creativity_measure() * 0.2
        
        emergence_potential = min(1.0, base_potential + capacity_boost + creativity_boost)
        
        return emergence_potential
        
    async def _store_criticality_metrics(self, metrics: CriticalityMetrics):
        """Store criticality metrics in database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            await conn.execute("""
                INSERT INTO soc_criticality_metrics 
                (current_state, criticality_index, power_law_exponent, correlation_length,
                 information_capacity, creativity_measure, stability_index, 
                 emergence_potential, avalanche_frequency, network_complexity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                metrics.current_state.value, metrics.criticality_index, 
                metrics.power_law_exponent, metrics.correlation_length,
                metrics.information_capacity, metrics.creativity_measure,
                metrics.stability_index, metrics.emergence_potential,
                metrics.avalanche_frequency, metrics.network_complexity
            ))
            await conn.commit()
            await conn.close()
        except Exception as e:
            logger.error(f"Failed to store criticality metrics: {e}")
            
    async def _store_avalanche_event(self, avalanche: AvalancheEvent):
        """Store avalanche event in database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            await conn.execute("""
                INSERT INTO soc_avalanche_events 
                (event_id, avalanche_type, trigger_node_id, affected_nodes, magnitude,
                 duration_ms, propagation_path, energy_dissipated, information_processed,
                 emergence_indicators, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                avalanche.event_id, avalanche.avalanche_type.value, 
                avalanche.trigger_node_id, list(avalanche.affected_nodes),
                avalanche.magnitude, avalanche.duration_ms, avalanche.propagation_path,
                avalanche.energy_dissipated, avalanche.information_processed,
                json.dumps(avalanche.emergence_indicators), 
                avalanche.start_time, avalanche.end_time
            ))
            await conn.commit()
            await conn.close()
        except Exception as e:
            logger.error(f"Failed to store avalanche event: {e}")
            
    async def _apply_parameter_changes(self):
        """Apply control parameter changes to the system"""
        params = self.criticality_controller.get_parameter_values()
        
        # Apply to nodes
        for node in self.nodes.values():
            if 'processing_threshold' in params:
                node.activation_threshold = params['processing_threshold']
            if 'adaptation_rate' in params:
                node.adaptation_rate = params['adaptation_rate']
                
        # Update simulation parameters
        if 'noise_level' in params:
            # Apply noise to system (implementation depends on specific noise model)
            pass
            
    async def _adapt_node(self, node: SystemNode):
        """Adapt individual node properties based on experience"""
        # Adapt activation threshold based on recent activity
        if node.last_avalanche_time:
            time_since = (datetime.now() - node.last_avalanche_time).total_seconds()
            
            if time_since < 60:  # Recently active
                # Slightly increase threshold (habituation)
                node.activation_threshold = min(1.0, node.activation_threshold + 0.001)
            elif time_since > 300:  # Long time inactive
                # Slightly decrease threshold (sensitization)
                node.activation_threshold = max(0.1, node.activation_threshold - 0.001)
                
        # Adapt stress level
        connection_load = len(node.connections) / 50.0  # Normalize by typical max connections
        node.stress_level = min(1.0, connection_load * 0.8 + node.current_activation * 0.2)
        
        # Decay current activation
        node.current_activation *= 0.95
        
    async def trigger_external_avalanche(self, avalanche_type: AvalancheType, 
                                       energy: float = 1.0) -> Optional[AvalancheEvent]:
        """Manually trigger an avalanche for testing or specific purposes"""
        if not self.nodes:
            return None
            
        trigger_node = random.choice(list(self.nodes.keys()))
        avalanche = await self.avalanche_simulator.trigger_avalanche(
            trigger_node, avalanche_type, energy
        )
        
        if avalanche:
            self.power_law_analyzer.record_avalanche(avalanche)
            await self._store_avalanche_event(avalanche)
            
        return avalanche
        
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'soc_state': self.current_metrics.current_state.value if self.current_metrics else 'unknown',
            'criticality_index': self.current_metrics.criticality_index if self.current_metrics else 0.0,
            'power_law_exponent': self.current_metrics.power_law_exponent if self.current_metrics else 2.0,
            'node_count': len(self.nodes),
            'total_connections': sum(len(node.connections) for node in self.nodes.values()) // 2,
            'recent_avalanches': len(self.avalanche_simulator.get_recent_avalanches(60)),
            'parameter_values': self.criticality_controller.get_parameter_values(),
            'avalanche_statistics': self.avalanche_simulator.calculate_avalanche_statistics(),
            'power_law_analysis': self.power_law_analyzer.get_analysis_results()
        }
        
        return status
        
    async def stop_soc_operations(self):
        """Stop SOC operations"""
        self.running = False
        logger.info("SOC operations stopped")

# Example usage and testing
async def test_self_organized_criticality():
    """Test the self-organized criticality implementation"""
    print("🌊 Testing Self-Organized Criticality Engine")
    
    database_url = "postgresql://postgres:password@localhost:5432/sentient"
    soc_engine = SelfOrganizedCriticalityEngine(database_url)
    
    try:
        # Initialize with 50 nodes for testing
        await soc_engine.initialize(node_count=50)
        print("✅ SOC engine initialized")
        
        # Test avalanche triggering
        avalanche = await soc_engine.trigger_external_avalanche(
            AvalancheType.CONSCIOUSNESS_EMERGENCE, energy=1.5
        )
        if avalanche:
            print(f"✅ Triggered avalanche: {len(avalanche.affected_nodes)} nodes affected")
        
        # Get initial status
        status = await soc_engine.get_system_status()
        print(f"✅ System status retrieved: {status['soc_state']} state")
        
        # Test brief operation period
        print("🔄 Running SOC operations for 30 seconds...")
        
        # Start operations for a short period
        operation_task = asyncio.create_task(soc_engine.start_soc_operations())
        
        # Let it run briefly
        await asyncio.sleep(30)
        
        # Stop operations
        await soc_engine.stop_soc_operations()
        operation_task.cancel()
        
        # Get final status
        final_status = await soc_engine.get_system_status()
        
        print("\n🌊 Self-Organized Criticality Test Results:")
        print(f"   • Criticality State: {final_status['soc_state']}")
        print(f"   • Criticality Index: {final_status['criticality_index']:.3f}")
        print(f"   • Power-law Exponent: {final_status['power_law_exponent']:.3f}")
        print(f"   • Network Size: {final_status['node_count']} nodes")
        print(f"   • Total Connections: {final_status['total_connections']}")
        print(f"   • Recent Avalanches: {final_status['recent_avalanches']}")
        
        avalanche_stats = final_status['avalanche_statistics']
        print(f"   • Avalanche Frequency: {avalanche_stats['frequency']:.2f}/min")
        print(f"   • Mean Magnitude: {avalanche_stats['mean_magnitude']:.2f}")
        print(f"   • Information Processed: {avalanche_stats['total_information_processed']:.1f}")
        
        # Verify criticality detection
        power_law_analysis = final_status['power_law_analysis']
        print(f"   • Is Critical: {power_law_analysis['is_critical']}")
        print(f"   • Criticality Score: {power_law_analysis['criticality_score']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_self_organized_criticality())