#!/usr/bin/env python
"""
Neural Plasticity Engine for Genesis Prime
Implements dynamic connection management between agents based on Hebbian learning principles
"""

import asyncio
import json
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import psycopg
from psycopg.rows import dict_row

@dataclass
class ConnectionData:
    """Data structure for agent connections"""
    agent_a_id: str
    agent_b_id: str
    strength: float
    interaction_count: int
    success_count: int
    last_interaction: datetime
    creation_time: datetime
    learning_rate: float = 0.1
    decay_rate: float = 0.01

@dataclass
class InteractionResult:
    """Result of an agent interaction"""
    agent_a_id: str
    agent_b_id: str
    success: bool
    success_factor: float
    learning_gain: float
    interaction_type: str
    timestamp: datetime
    metadata: Dict[str, Any]

class ConnectionMatrix:
    """Manages the connection matrix between agents"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connections: Dict[str, ConnectionData] = {}
        self.metadata = {}
        
    def _get_connection_key(self, agent_a_id: str, agent_b_id: str) -> str:
        """Generate consistent connection key"""
        # Always order IDs consistently
        if agent_a_id < agent_b_id:
            return f"{agent_a_id}::{agent_b_id}"
        else:
            return f"{agent_b_id}::{agent_a_id}"
    
    async def initialize_from_database(self):
        """Load existing connections from database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url, row_factory=dict_row)
        
        try:
            # Create table if it doesn't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS neural_connections (
                    id SERIAL PRIMARY KEY,
                    connection_key VARCHAR(255) UNIQUE NOT NULL,
                    agent_a_id UUID NOT NULL,
                    agent_b_id UUID NOT NULL,
                    strength FLOAT NOT NULL DEFAULT 0.5,
                    interaction_count INTEGER NOT NULL DEFAULT 0,
                    success_count INTEGER NOT NULL DEFAULT 0,
                    last_interaction TIMESTAMP,
                    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
                    learning_rate FLOAT NOT NULL DEFAULT 0.1,
                    decay_rate FLOAT NOT NULL DEFAULT 0.01,
                    metadata JSONB
                )
            """)
            
            # Load existing connections
            rows = await conn.fetch("SELECT * FROM neural_connections")
            
            for row in rows:
                connection_key = row['connection_key']
                self.connections[connection_key] = ConnectionData(
                    agent_a_id=str(row['agent_a_id']),
                    agent_b_id=str(row['agent_b_id']),
                    strength=row['strength'],
                    interaction_count=row['interaction_count'],
                    success_count=row['success_count'],
                    last_interaction=row['last_interaction'],
                    creation_time=row['creation_time'],
                    learning_rate=row['learning_rate'],
                    decay_rate=row['decay_rate']
                )
                
        finally:
            await conn.close()
    
    async def set_strength(self, agent_a_id: str, agent_b_id: str, strength: float):
        """Set connection strength between two agents"""
        key = self._get_connection_key(agent_a_id, agent_b_id)
        
        if key in self.connections:
            self.connections[key].strength = max(0.0, min(1.0, strength))
            self.connections[key].last_interaction = datetime.utcnow()
        else:
            # Create new connection
            self.connections[key] = ConnectionData(
                agent_a_id=agent_a_id,
                agent_b_id=agent_b_id,
                strength=max(0.0, min(1.0, strength)),
                interaction_count=0,
                success_count=0,
                last_interaction=datetime.utcnow(),
                creation_time=datetime.utcnow()
            )
        
        # Persist to database
        await self._persist_connection(key)
    
    async def get_strength(self, agent_a_id: str, agent_b_id: str) -> float:
        """Get connection strength between two agents"""
        key = self._get_connection_key(agent_a_id, agent_b_id)
        if key in self.connections:
            return self.connections[key].strength
        return 0.5  # Default neutral strength
    
    async def get_strongest_connections(self, agent_id: str, limit: int = 5) -> List[Tuple[str, float]]:
        """Get strongest connections for an agent"""
        agent_connections = []
        
        for key, connection in self.connections.items():
            if agent_id in [connection.agent_a_id, connection.agent_b_id]:
                other_agent = connection.agent_b_id if connection.agent_a_id == agent_id else connection.agent_a_id
                agent_connections.append((other_agent, connection.strength))
        
        # Sort by strength and return top connections
        agent_connections.sort(key=lambda x: x[1], reverse=True)
        return agent_connections[:limit]
    
    async def get_connections_below_threshold(self, threshold: float) -> List[ConnectionData]:
        """Get connections below strength threshold"""
        weak_connections = []
        for connection in self.connections.values():
            if connection.strength < threshold:
                weak_connections.append(connection)
        return weak_connections
    
    async def remove_connection(self, agent_a_id: str, agent_b_id: str):
        """Remove a connection"""
        key = self._get_connection_key(agent_a_id, agent_b_id)
        if key in self.connections:
            del self.connections[key]
            
            # Remove from database
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            try:
                await conn.execute(
                    "DELETE FROM neural_connections WHERE connection_key = %s",
                    (key,)
                )
            finally:
                await conn.close()
    
    async def _persist_connection(self, connection_key: str):
        """Persist connection to database"""
        if connection_key not in self.connections:
            return
            
        connection = self.connections[connection_key]
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO neural_connections (
                    connection_key, agent_a_id, agent_b_id, strength, 
                    interaction_count, success_count, last_interaction,
                    creation_time, learning_rate, decay_rate
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (connection_key) DO UPDATE SET
                    strength = EXCLUDED.strength,
                    interaction_count = EXCLUDED.interaction_count,
                    success_count = EXCLUDED.success_count,
                    last_interaction = EXCLUDED.last_interaction,
                    learning_rate = EXCLUDED.learning_rate,
                    decay_rate = EXCLUDED.decay_rate
            """, (
                connection_key,
                connection.agent_a_id,
                connection.agent_b_id,
                connection.strength,
                connection.interaction_count,
                connection.success_count,
                connection.last_interaction,
                connection.creation_time,
                connection.learning_rate,
                connection.decay_rate
            ))
        finally:
            await conn.close()

class NeuralPlasticityEngine:
    """Core neural plasticity engine implementing Hebbian learning"""
    
    def __init__(self, hive, database_url: str):
        self.hive = hive
        self.database_url = database_url
        self.connection_matrix = ConnectionMatrix(database_url)
        self.learning_history: List[InteractionResult] = []
        self.plasticity_config = {
            'hebbian_learning_rate': 0.1,
            'decay_rate': 0.01,
            'pruning_threshold': 0.2,
            'max_connection_strength': 1.0,
            'min_connection_strength': 0.01
        }
        
    async def initialize(self):
        """Initialize the neural plasticity system"""
        await self.connection_matrix.initialize_from_database()
        print("🧠 Neural Plasticity Engine initialized")
    
    async def initialize_connections(self, agent_ids: List[str]):
        """Initialize connections between all agents"""
        print(f"🔗 Initializing connections for {len(agent_ids)} agents")
        
        for i, agent_a in enumerate(agent_ids):
            for j, agent_b in enumerate(agent_ids):
                if i < j:  # Avoid duplicate connections
                    initial_strength = await self._calculate_initial_strength(agent_a, agent_b)
                    await self.connection_matrix.set_strength(agent_a, agent_b, initial_strength)
        
        print(f"✅ Initialized {len(agent_ids) * (len(agent_ids) - 1) // 2} connections")
    
    async def _calculate_initial_strength(self, agent_a_id: str, agent_b_id: str) -> float:
        """Calculate initial connection strength based on agent compatibility"""
        # Get agent data from hive
        agent_a_data = self.hive.active_agents.get(agent_a_id, {})
        agent_b_data = self.hive.active_agents.get(agent_b_id, {})
        
        # Base strength
        base_strength = 0.5
        
        # Adjust based on personality compatibility
        if 'traits' in agent_a_data and 'traits' in agent_b_data:
            compatibility = self._calculate_personality_compatibility(
                agent_a_data['traits'], agent_b_data['traits']
            )
            base_strength += (compatibility - 0.5) * 0.2  # Adjust by ±0.1
        
        # Add small random factor for diversity
        base_strength += np.random.normal(0, 0.05)
        
        return max(0.1, min(0.9, base_strength))
    
    def _calculate_personality_compatibility(self, traits_a: Dict, traits_b: Dict) -> float:
        """Calculate personality compatibility between two agents"""
        # Simple compatibility based on trait similarity/complementarity
        compatibility_factors = []
        
        for trait in ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']:
            if trait in traits_a and trait in traits_b:
                diff = abs(traits_a[trait] - traits_b[trait])
                # Some traits work better with similarity, others with complementarity
                if trait in ['conscientiousness', 'agreeableness']:
                    # Similar values work better
                    compatibility_factors.append(1.0 - diff)
                else:
                    # Some complementarity is good
                    compatibility_factors.append(0.7 + 0.3 * diff)
        
        return np.mean(compatibility_factors) if compatibility_factors else 0.5
    
    async def update_connection_strength(self, interaction_result: InteractionResult):
        """Update connection strength based on interaction result"""
        current_strength = await self.connection_matrix.get_strength(
            interaction_result.agent_a_id, interaction_result.agent_b_id
        )
        
        if interaction_result.success:
            # Hebbian strengthening
            new_strength = await self._hebbian_strengthening(
                current_strength,
                interaction_result.success_factor,
                interaction_result.learning_gain
            )
        else:
            # Connection weakening
            new_strength = await self._connection_weakening(
                current_strength,
                1.0 - interaction_result.success_factor
            )
        
        await self.connection_matrix.set_strength(
            interaction_result.agent_a_id,
            interaction_result.agent_b_id,
            new_strength
        )
        
        # Record in learning history
        self.learning_history.append(interaction_result)
        await self._log_plasticity_event(interaction_result, current_strength, new_strength)
        
        return new_strength
    
    async def _hebbian_strengthening(self, current_strength: float, success_factor: float, learning_gain: float) -> float:
        """Implement Hebbian learning strengthening"""
        learning_rate = self.plasticity_config['hebbian_learning_rate']
        
        # "Neurons that fire together, wire together"
        # Strength increases based on success and learning
        strength_increase = learning_rate * success_factor * learning_gain * (1 - current_strength)
        
        new_strength = current_strength + strength_increase
        return min(self.plasticity_config['max_connection_strength'], new_strength)
    
    async def _connection_weakening(self, current_strength: float, failure_factor: float) -> float:
        """Weaken connection based on failure"""
        decay_rate = self.plasticity_config['decay_rate']
        
        # Connections weaken with lack of successful use
        strength_decrease = decay_rate * failure_factor * current_strength
        
        new_strength = current_strength - strength_decrease
        return max(self.plasticity_config['min_connection_strength'], new_strength)
    
    async def prune_connections(self):
        """Remove weak connections to prevent information overload"""
        threshold = self.plasticity_config['pruning_threshold']
        weak_connections = await self.connection_matrix.get_connections_below_threshold(threshold)
        
        pruned_count = 0
        for connection in weak_connections:
            # Only prune if connection hasn't been used recently
            time_since_interaction = datetime.utcnow() - connection.last_interaction
            
            if time_since_interaction > timedelta(hours=24):  # 24 hours of inactivity
                await self.connection_matrix.remove_connection(
                    connection.agent_a_id, connection.agent_b_id
                )
                pruned_count += 1
                await self._log_pruning_event(connection)
        
        print(f"🌿 Pruned {pruned_count} weak connections")
        return pruned_count
    
    async def get_interaction_priority(self, agent_a_id: str, agent_b_id: str) -> float:
        """Get priority for agent interaction based on connection strength"""
        strength = await self.connection_matrix.get_strength(agent_a_id, agent_b_id)
        
        # Higher strength = higher priority for interaction
        # But also add some randomness to explore new connections
        priority = 0.7 * strength + 0.3 * np.random.random()
        
        return priority
    
    async def suggest_optimal_interactions(self, agent_id: str, num_suggestions: int = 3) -> List[Tuple[str, float]]:
        """Suggest optimal interactions for an agent"""
        # Get current connections
        connections = await self.connection_matrix.get_strongest_connections(agent_id, limit=10)
        
        # Score interactions based on:
        # 1. Connection strength
        # 2. Time since last interaction
        # 3. Potential for learning
        
        scored_interactions = []
        for other_agent_id, strength in connections:
            # Calculate interaction score
            score = await self._calculate_interaction_score(agent_id, other_agent_id, strength)
            scored_interactions.append((other_agent_id, score))
        
        # Sort by score and return top suggestions
        scored_interactions.sort(key=lambda x: x[1], reverse=True)
        return scored_interactions[:num_suggestions]
    
    async def _calculate_interaction_score(self, agent_a_id: str, agent_b_id: str, strength: float) -> float:
        """Calculate interaction score for prioritization"""
        # Base score from connection strength
        score = strength
        
        # Boost score for agents that haven't interacted recently
        key = self.connection_matrix._get_connection_key(agent_a_id, agent_b_id)
        if key in self.connection_matrix.connections:
            connection = self.connection_matrix.connections[key]
            time_since_interaction = datetime.utcnow() - connection.last_interaction
            
            # Boost score for connections that haven't been used recently
            hours_since = time_since_interaction.total_seconds() / 3600
            recency_boost = min(0.3, hours_since / 24)  # Up to 0.3 boost for 24+ hours
            score += recency_boost
        
        # Add small random factor for exploration
        score += np.random.normal(0, 0.05)
        
        return max(0, min(1, score))
    
    async def get_network_statistics(self) -> Dict[str, Any]:
        """Get statistics about the neural network"""
        connections = list(self.connection_matrix.connections.values())
        
        if not connections:
            return {"error": "No connections found"}
        
        strengths = [c.strength for c in connections]
        interaction_counts = [c.interaction_count for c in connections]
        success_rates = [c.success_count / max(1, c.interaction_count) for c in connections]
        
        stats = {
            "total_connections": len(connections),
            "average_strength": np.mean(strengths),
            "strength_std": np.std(strengths),
            "min_strength": np.min(strengths),
            "max_strength": np.max(strengths),
            "average_interactions": np.mean(interaction_counts),
            "average_success_rate": np.mean(success_rates),
            "network_density": len(connections) / (len(self.hive.active_agents) * (len(self.hive.active_agents) - 1) / 2) if len(self.hive.active_agents) > 1 else 0,
            "learning_events_total": len(self.learning_history),
            "recent_learning_events": len([e for e in self.learning_history if (datetime.utcnow() - e.timestamp).days < 1])
        }
        
        return stats
    
    async def _log_plasticity_event(self, interaction: InteractionResult, old_strength: float, new_strength: float):
        """Log plasticity event for analysis"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS plasticity_events (
                    id SERIAL PRIMARY KEY,
                    agent_a_id UUID NOT NULL,
                    agent_b_id UUID NOT NULL,
                    interaction_type VARCHAR(100),
                    success BOOLEAN,
                    success_factor FLOAT,
                    learning_gain FLOAT,
                    old_strength FLOAT,
                    new_strength FLOAT,
                    strength_change FLOAT,
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    metadata JSONB
                )
            """)
            
            await conn.execute("""
                INSERT INTO plasticity_events (
                    agent_a_id, agent_b_id, interaction_type, success,
                    success_factor, learning_gain, old_strength, new_strength,
                    strength_change, timestamp, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                interaction.agent_a_id,
                interaction.agent_b_id,
                interaction.interaction_type,
                interaction.success,
                interaction.success_factor,
                interaction.learning_gain,
                old_strength,
                new_strength,
                new_strength - old_strength,
                interaction.timestamp,
                json.dumps(interaction.metadata)
            ))
        finally:
            await conn.close()
    
    async def _log_pruning_event(self, connection: ConnectionData):
        """Log connection pruning event"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS pruning_events (
                    id SERIAL PRIMARY KEY,
                    agent_a_id UUID NOT NULL,
                    agent_b_id UUID NOT NULL,
                    final_strength FLOAT,
                    interaction_count INTEGER,
                    success_count INTEGER,
                    last_interaction TIMESTAMP,
                    connection_age_hours FLOAT,
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            connection_age = (datetime.utcnow() - connection.creation_time).total_seconds() / 3600
            
            await conn.execute("""
                INSERT INTO pruning_events (
                    agent_a_id, agent_b_id, final_strength, interaction_count,
                    success_count, last_interaction, connection_age_hours
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                connection.agent_a_id,
                connection.agent_b_id,
                connection.strength,
                connection.interaction_count,
                connection.success_count,
                connection.last_interaction,
                connection_age
            ))
        finally:
            await conn.close()

# Helper functions for interaction processing
async def create_interaction_result(
    agent_a_id: str,
    agent_b_id: str,
    interaction_type: str,
    success: bool,
    performance_metrics: Dict[str, float],
    metadata: Dict[str, Any] = None
) -> InteractionResult:
    """Create an interaction result from interaction data"""
    
    # Calculate success factor (0.0 to 1.0)
    if success:
        success_factor = 0.7 + 0.3 * performance_metrics.get('quality', 0.5)
    else:
        success_factor = 0.1 + 0.4 * performance_metrics.get('partial_success', 0.0)
    
    # Calculate learning gain
    learning_gain = performance_metrics.get('learning_gain', 0.5)
    if 'novelty' in performance_metrics:
        learning_gain *= (0.8 + 0.4 * performance_metrics['novelty'])
    
    return InteractionResult(
        agent_a_id=agent_a_id,
        agent_b_id=agent_b_id,
        success=success,
        success_factor=success_factor,
        learning_gain=learning_gain,
        interaction_type=interaction_type,
        timestamp=datetime.utcnow(),
        metadata=metadata or {}
    )

# Testing and validation functions
async def test_neural_plasticity_system(hive, database_url: str):
    """Test the neural plasticity system"""
    print("🧪 Testing Neural Plasticity System...")
    
    # Initialize system
    plasticity_engine = NeuralPlasticityEngine(hive, database_url)
    await plasticity_engine.initialize()
    
    # Test with sample agents
    test_agent_ids = ["agent_1", "agent_2", "agent_3"]
    
    # Initialize connections
    await plasticity_engine.initialize_connections(test_agent_ids)
    
    # Simulate successful interactions
    for i in range(10):
        interaction = await create_interaction_result(
            "agent_1", "agent_2", "knowledge_sharing",
            success=True,
            performance_metrics={'quality': 0.8, 'learning_gain': 0.7, 'novelty': 0.6}
        )
        await plasticity_engine.update_connection_strength(interaction)
    
    # Simulate failed interactions
    for i in range(3):
        interaction = await create_interaction_result(
            "agent_1", "agent_3", "problem_solving",
            success=False,
            performance_metrics={'partial_success': 0.2}
        )
        await plasticity_engine.update_connection_strength(interaction)
    
    # Get network statistics
    stats = await plasticity_engine.get_network_statistics()
    print(f"📊 Network Statistics: {json.dumps(stats, indent=2, default=str)}")
    
    # Test connection pruning
    await plasticity_engine.prune_connections()
    
    # Test interaction suggestions
    suggestions = await plasticity_engine.suggest_optimal_interactions("agent_1")
    print(f"💡 Interaction suggestions for agent_1: {suggestions}")
    
    print("✅ Neural Plasticity System test complete!")
    return plasticity_engine

if __name__ == "__main__":
    # Quick test run
    import asyncio
    
    class MockHive:
        def __init__(self):
            self.active_agents = {
                "agent_1": {"traits": {"openness": 0.8, "conscientiousness": 0.6}},
                "agent_2": {"traits": {"openness": 0.7, "conscientiousness": 0.8}},
                "agent_3": {"traits": {"openness": 0.5, "conscientiousness": 0.4}}
            }
    
    async def main():
        hive = MockHive()
        database_url = "postgresql://postgres:pass@localhost:5432/sentient"
        await test_neural_plasticity_system(hive, database_url)
    
    asyncio.run(main())