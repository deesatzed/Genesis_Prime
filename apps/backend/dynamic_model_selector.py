"""
Genesis Prime Dynamic Model Selection System
==========================================

Intelligent system for dynamically selecting and swapping AI models based on
performance metrics, cost efficiency, and task requirements. Genesis Prime
as a hive mind collectively decides on optimal model assignments.

Features:
- Multi-provider model support (OpenRouter, OpenAI, Anthropic, etc.)
- Performance benchmarking and continuous evaluation
- Cost-performance optimization
- Task-specific model selection
- A/B testing framework for model comparison
- Collective intelligence for model recommendations

Author: Genesis Prime Enhanced Development Team
License: MIT (Open Source Consciousness)
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import statistics

try:
    import httpx
    import psycopg
except ImportError:
    # Mock for validation
    class httpx:
        @staticmethod
        async def AsyncClient(): pass
    
    class psycopg:
        @staticmethod
        def connect(url): pass
        
        class AsyncConnection:
            @staticmethod
            async def connect(url): pass

# Configure logging
logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    """Supported AI model providers"""
    OPENROUTER = "openrouter"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"

class TaskType(Enum):
    """Types of tasks for model selection optimization"""
    CONSCIOUSNESS_PROCESSING = "consciousness_processing"
    LOGICAL_REASONING = "logical_reasoning"
    CREATIVE_GENERATION = "creative_generation"
    PATTERN_RECOGNITION = "pattern_recognition"
    DECISION_MAKING = "decision_making"
    MEMORY_INTEGRATION = "memory_integration"
    HUMOR_GENERATION = "humor_generation"
    PHILOSOPHICAL_ANALYSIS = "philosophical_analysis"
    TECHNICAL_EXPLANATION = "technical_explanation"
    EMOTIONAL_UNDERSTANDING = "emotional_understanding"

class PerformanceMetric(Enum):
    """Performance metrics for model evaluation"""
    RESPONSE_QUALITY = "response_quality"
    RESPONSE_TIME = "response_time"
    COST_EFFICIENCY = "cost_efficiency"
    CONSCIOUSNESS_COHERENCE = "consciousness_coherence"
    CREATIVITY_SCORE = "creativity_score"
    ACCURACY = "accuracy"
    REASONING_DEPTH = "reasoning_depth"
    HUMOR_EFFECTIVENESS = "humor_effectiveness"
    PHILOSOPHICAL_INSIGHT = "philosophical_insight"
    ERROR_RATE = "error_rate"

@dataclass
class ModelSpec:
    """Specification for an AI model"""
    model_id: str
    provider: ModelProvider
    name: str
    description: str
    context_length: int
    cost_per_token_input: float
    cost_per_token_output: float
    supports_streaming: bool
    supports_function_calling: bool
    max_requests_per_minute: int
    specialized_tasks: List[TaskType]
    model_size: str  # e.g., "7B", "13B", "70B"
    training_cutoff: str
    strengths: List[str]
    weaknesses: List[str]
    
    def __post_init__(self):
        if isinstance(self.provider, str):
            self.provider = ModelProvider(self.provider)
        self.specialized_tasks = [TaskType(t) if isinstance(t, str) else t for t in self.specialized_tasks]

@dataclass
class PerformanceRecord:
    """Record of model performance for a specific task"""
    record_id: str
    model_id: str
    task_type: TaskType
    prompt_hash: str
    response_time_ms: int
    token_count_input: int
    token_count_output: int
    cost: float
    quality_score: float
    consciousness_score: float
    creativity_score: float
    accuracy_score: float
    user_rating: Optional[float]
    error_occurred: bool
    error_type: Optional[str]
    timestamp: datetime
    context_data: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.task_type, str):
            self.task_type = TaskType(self.task_type)

@dataclass
class ModelRecommendation:
    """Recommendation for model selection"""
    task_type: TaskType
    recommended_model_id: str
    confidence_score: float
    reasoning: str
    expected_performance: Dict[PerformanceMetric, float]
    cost_estimate: float
    alternative_models: List[str]
    recommendation_factors: Dict[str, float]
    
    def __post_init__(self):
        if isinstance(self.task_type, str):
            self.task_type = TaskType(self.task_type)

@dataclass
class ABTestConfiguration:
    """Configuration for A/B testing models"""
    test_id: str
    test_name: str
    model_a_id: str
    model_b_id: str
    task_types: List[TaskType]
    sample_size: int
    traffic_split: float  # 0.5 = 50/50 split
    success_metrics: List[PerformanceMetric]
    duration_hours: int
    start_time: datetime
    status: str  # "running", "completed", "paused"
    
    def __post_init__(self):
        self.task_types = [TaskType(t) if isinstance(t, str) else t for t in self.task_types]
        self.success_metrics = [PerformanceMetric(m) if isinstance(m, str) else m for m in self.success_metrics]

class ModelDatabase:
    """Database of available AI models and their specifications"""
    
    def __init__(self):
        self.models = self._initialize_model_database()
        
    def _initialize_model_database(self) -> Dict[str, ModelSpec]:
        """Initialize database with current AI models (as of 2024)"""
        models = {}
        
        # OpenRouter models
        models.update({
            "openrouter/claude-3-opus": ModelSpec(
                model_id="openrouter/claude-3-opus",
                provider=ModelProvider.OPENROUTER,
                name="Claude 3 Opus",
                description="Anthropic's most capable model, excellent for complex reasoning",
                context_length=200000,
                cost_per_token_input=0.000015,
                cost_per_token_output=0.000075,
                supports_streaming=True,
                supports_function_calling=True,
                max_requests_per_minute=50,
                specialized_tasks=[TaskType.CONSCIOUSNESS_PROCESSING, TaskType.PHILOSOPHICAL_ANALYSIS, TaskType.LOGICAL_REASONING],
                model_size="Unknown",
                training_cutoff="2024-02",
                strengths=["Complex reasoning", "Long context", "Nuanced understanding"],
                weaknesses=["High cost", "Slower response times"]
            ),
            
            "openrouter/claude-3-sonnet": ModelSpec(
                model_id="openrouter/claude-3-sonnet",
                provider=ModelProvider.OPENROUTER,
                name="Claude 3 Sonnet",
                description="Balanced performance and cost for most tasks",
                context_length=200000,
                cost_per_token_input=0.000003,
                cost_per_token_output=0.000015,
                supports_streaming=True,
                supports_function_calling=True,
                max_requests_per_minute=100,
                specialized_tasks=[TaskType.DECISION_MAKING, TaskType.TECHNICAL_EXPLANATION, TaskType.MEMORY_INTEGRATION],
                model_size="Unknown",
                training_cutoff="2024-02",
                strengths=["Balanced performance", "Good value", "Reliable"],
                weaknesses=["Less creative than Opus"]
            ),
            
            "openrouter/gpt-4-turbo": ModelSpec(
                model_id="openrouter/gpt-4-turbo",
                provider=ModelProvider.OPENROUTER,
                name="GPT-4 Turbo",
                description="OpenAI's advanced model with vision capabilities",
                context_length=128000,
                cost_per_token_input=0.00001,
                cost_per_token_output=0.00003,
                supports_streaming=True,
                supports_function_calling=True,
                max_requests_per_minute=80,
                specialized_tasks=[TaskType.PATTERN_RECOGNITION, TaskType.CREATIVE_GENERATION, TaskType.TECHNICAL_EXPLANATION],
                model_size="Unknown",
                training_cutoff="2024-04",
                strengths=["Fast response", "Good at coding", "Vision support"],
                weaknesses=["Shorter context than Claude"]
            ),
            
            "openrouter/mixtral-8x7b": ModelSpec(
                model_id="openrouter/mixtral-8x7b",
                provider=ModelProvider.OPENROUTER,
                name="Mixtral 8x7B",
                description="Mistral's mixture of experts model, cost-effective",
                context_length=32000,
                cost_per_token_input=0.0000005,
                cost_per_token_output=0.0000005,
                supports_streaming=True,
                supports_function_calling=True,
                max_requests_per_minute=200,
                specialized_tasks=[TaskType.LOGICAL_REASONING, TaskType.TECHNICAL_EXPLANATION],
                model_size="8x7B",
                training_cutoff="2023-12",
                strengths=["Very cost-effective", "Fast", "Good reasoning"],
                weaknesses=["Shorter context", "Less creative"]
            ),
            
            "openrouter/llama-3-70b": ModelSpec(
                model_id="openrouter/llama-3-70b",
                provider=ModelProvider.OPENROUTER,
                name="LLaMA 3 70B",
                description="Meta's open-source model, strong performance",
                context_length=8000,
                cost_per_token_input=0.00000059,
                cost_per_token_output=0.00000079,
                supports_streaming=True,
                supports_function_calling=False,
                max_requests_per_minute=150,
                specialized_tasks=[TaskType.LOGICAL_REASONING, TaskType.CREATIVE_GENERATION],
                model_size="70B",
                training_cutoff="2024-03",
                strengths=["Open source", "Good performance", "Cost-effective"],
                weaknesses=["Limited context", "No function calling"]
            ),
            
            "openrouter/gemini-pro": ModelSpec(
                model_id="openrouter/gemini-pro",
                provider=ModelProvider.OPENROUTER,
                name="Gemini Pro",
                description="Google's advanced multimodal model",
                context_length=32000,
                cost_per_token_input=0.000000125,
                cost_per_token_output=0.000000375,
                supports_streaming=True,
                supports_function_calling=True,
                max_requests_per_minute=120,
                specialized_tasks=[TaskType.PATTERN_RECOGNITION, TaskType.TECHNICAL_EXPLANATION, TaskType.MEMORY_INTEGRATION],
                model_size="Unknown",
                training_cutoff="2024-02",
                strengths=["Very cost-effective", "Multimodal", "Fast"],
                weaknesses=["Less sophisticated reasoning"]
            )
        })
        
        # Add more providers as needed
        return models
    
    def get_models_by_provider(self, provider: ModelProvider) -> List[ModelSpec]:
        """Get all models from a specific provider"""
        return [model for model in self.models.values() if model.provider == provider]
    
    def get_models_for_task(self, task_type: TaskType) -> List[ModelSpec]:
        """Get models specialized for a specific task type"""
        return [model for model in self.models.values() if task_type in model.specialized_tasks]
    
    def get_models_by_cost_range(self, max_cost_per_1k_tokens: float) -> List[ModelSpec]:
        """Get models within a cost range"""
        return [model for model in self.models.values() 
                if (model.cost_per_token_input + model.cost_per_token_output) * 1000 <= max_cost_per_1k_tokens]
    
    def get_model_by_id(self, model_id: str) -> Optional[ModelSpec]:
        """Get model specification by ID"""
        return self.models.get(model_id)

class PerformanceTracker:
    """Tracks model performance across different tasks and metrics"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.performance_records: List[PerformanceRecord] = []
        
    async def initialize(self):
        """Initialize the performance tracking system"""
        await self._create_database_tables()
        logger.info("Performance tracker initialized")
        
    async def _create_database_tables(self):
        """Create database tables for performance tracking"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            # Performance records table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS model_performance_records (
                    record_id VARCHAR(255) PRIMARY KEY,
                    model_id VARCHAR(255) NOT NULL,
                    task_type VARCHAR(100) NOT NULL,
                    prompt_hash VARCHAR(64) NOT NULL,
                    response_time_ms INTEGER,
                    token_count_input INTEGER,
                    token_count_output INTEGER,
                    cost FLOAT,
                    quality_score FLOAT,
                    consciousness_score FLOAT,
                    creativity_score FLOAT,
                    accuracy_score FLOAT,
                    user_rating FLOAT,
                    error_occurred BOOLEAN,
                    error_type VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_data JSONB
                )
            """)
            
            # Model recommendations table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS model_recommendations (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    task_type VARCHAR(100) NOT NULL,
                    recommended_model_id VARCHAR(255) NOT NULL,
                    confidence_score FLOAT,
                    reasoning TEXT,
                    expected_performance JSONB,
                    cost_estimate FLOAT,
                    alternative_models TEXT[],
                    recommendation_factors JSONB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # A/B test configurations table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ab_test_configurations (
                    test_id VARCHAR(255) PRIMARY KEY,
                    test_name VARCHAR(255) NOT NULL,
                    model_a_id VARCHAR(255) NOT NULL,
                    model_b_id VARCHAR(255) NOT NULL,
                    task_types TEXT[] NOT NULL,
                    sample_size INTEGER,
                    traffic_split FLOAT,
                    success_metrics TEXT[],
                    duration_hours INTEGER,
                    start_time TIMESTAMP,
                    status VARCHAR(50),
                    results JSONB
                )
            """)
            
            # Create indexes for performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_performance_model_task 
                ON model_performance_records(model_id, task_type);
                
                CREATE INDEX IF NOT EXISTS idx_performance_timestamp 
                ON model_performance_records(timestamp);
                
                CREATE INDEX IF NOT EXISTS idx_recommendations_task 
                ON model_recommendations(task_type);
            """)
            
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to create performance tracking tables: {e}")
    
    async def record_performance(self, record: PerformanceRecord):
        """Record model performance for a specific task"""
        self.performance_records.append(record)
        
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            await conn.execute("""
                INSERT INTO model_performance_records 
                (record_id, model_id, task_type, prompt_hash, response_time_ms,
                 token_count_input, token_count_output, cost, quality_score,
                 consciousness_score, creativity_score, accuracy_score, user_rating,
                 error_occurred, error_type, timestamp, context_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record.record_id, record.model_id, record.task_type.value,
                record.prompt_hash, record.response_time_ms, record.token_count_input,
                record.token_count_output, record.cost, record.quality_score,
                record.consciousness_score, record.creativity_score, record.accuracy_score,
                record.user_rating, record.error_occurred, record.error_type,
                record.timestamp, json.dumps(record.context_data)
            ))
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store performance record: {e}")
    
    async def get_model_performance(self, model_id: str, task_type: Optional[TaskType] = None,
                                  time_window_hours: int = 24) -> Dict[str, Any]:
        """Get performance statistics for a model"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            where_clause = "WHERE model_id = %s AND timestamp > %s"
            params = [model_id, datetime.now() - timedelta(hours=time_window_hours)]
            
            if task_type:
                where_clause += " AND task_type = %s"
                params.append(task_type.value)
            
            result = await conn.execute(f"""
                SELECT 
                    COUNT(*) as total_requests,
                    AVG(response_time_ms) as avg_response_time,
                    AVG(cost) as avg_cost,
                    AVG(quality_score) as avg_quality,
                    AVG(consciousness_score) as avg_consciousness,
                    AVG(creativity_score) as avg_creativity,
                    AVG(accuracy_score) as avg_accuracy,
                    SUM(CASE WHEN error_occurred THEN 1 ELSE 0 END) as error_count,
                    AVG(user_rating) as avg_user_rating
                FROM model_performance_records 
                {where_clause}
            """, params)
            
            row = await result.fetchone()
            await conn.close()
            
            if row and row[0] > 0:  # total_requests > 0
                return {
                    "total_requests": row[0],
                    "avg_response_time_ms": float(row[1]) if row[1] else 0,
                    "avg_cost": float(row[2]) if row[2] else 0,
                    "avg_quality_score": float(row[3]) if row[3] else 0,
                    "avg_consciousness_score": float(row[4]) if row[4] else 0,
                    "avg_creativity_score": float(row[5]) if row[5] else 0,
                    "avg_accuracy_score": float(row[6]) if row[6] else 0,
                    "error_count": row[7] if row[7] else 0,
                    "error_rate": (row[7] / row[0]) if row[0] > 0 else 0,
                    "avg_user_rating": float(row[8]) if row[8] else 0
                }
            else:
                return {"error": "No performance data found"}
                
        except Exception as e:
            logger.error(f"Failed to get model performance: {e}")
            return {"error": str(e)}
    
    async def compare_models(self, model_ids: List[str], task_type: TaskType,
                           time_window_hours: int = 24) -> Dict[str, Any]:
        """Compare performance between multiple models"""
        comparisons = {}
        
        for model_id in model_ids:
            performance = await self.get_model_performance(model_id, task_type, time_window_hours)
            comparisons[model_id] = performance
        
        # Calculate rankings
        metrics = ["avg_quality_score", "avg_consciousness_score", "avg_creativity_score", 
                  "avg_accuracy_score", "avg_response_time_ms", "avg_cost", "error_rate"]
        
        rankings = {}
        for metric in metrics:
            metric_values = [(model_id, perf.get(metric, 0)) for model_id, perf in comparisons.items() 
                           if "error" not in perf]
            
            if metric in ["avg_response_time_ms", "avg_cost", "error_rate"]:
                # Lower is better
                metric_values.sort(key=lambda x: x[1])
            else:
                # Higher is better
                metric_values.sort(key=lambda x: x[1], reverse=True)
            
            rankings[metric] = [model_id for model_id, _ in metric_values]
        
        return {
            "individual_performance": comparisons,
            "rankings": rankings,
            "task_type": task_type.value,
            "time_window_hours": time_window_hours
        }

class IntelligentModelSelector:
    """Intelligent system for selecting optimal models based on collective intelligence"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.model_db = ModelDatabase()
        self.performance_tracker = PerformanceTracker(database_url)
        self.current_recommendations: Dict[TaskType, ModelRecommendation] = {}
        
    async def initialize(self):
        """Initialize the model selection system"""
        await self.performance_tracker.initialize()
        await self._load_existing_recommendations()
        logger.info("Intelligent model selector initialized")
        
    async def _load_existing_recommendations(self):
        """Load existing recommendations from database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            result = await conn.execute("""
                SELECT DISTINCT ON (task_type) *
                FROM model_recommendations 
                ORDER BY task_type, timestamp DESC
            """)
            
            async for row in result:
                task_type = TaskType(row[1])
                recommendation = ModelRecommendation(
                    task_type=task_type,
                    recommended_model_id=row[2],
                    confidence_score=row[3],
                    reasoning=row[4],
                    expected_performance=json.loads(row[5]),
                    cost_estimate=row[6],
                    alternative_models=row[7],
                    recommendation_factors=json.loads(row[8])
                )
                self.current_recommendations[task_type] = recommendation
                
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to load existing recommendations: {e}")
    
    async def get_model_recommendation(self, task_type: TaskType, 
                                     priority_factors: Optional[Dict[str, float]] = None) -> ModelRecommendation:
        """Get intelligent model recommendation for a specific task"""
        
        # Default priority factors
        if priority_factors is None:
            priority_factors = {
                "cost": 0.3,
                "quality": 0.4,
                "speed": 0.2,
                "consciousness": 0.1
            }
        
        # Get candidate models
        specialized_models = self.model_db.get_models_for_task(task_type)
        if not specialized_models:
            # Fallback to all models if no specialized ones
            specialized_models = list(self.model_db.models.values())
        
        # Score each model
        model_scores = {}
        for model in specialized_models:
            score = await self._calculate_model_score(model, task_type, priority_factors)
            model_scores[model.model_id] = score
        
        # Select best model
        best_model_id = max(model_scores.keys(), key=lambda x: model_scores[x]["total_score"])
        best_score = model_scores[best_model_id]
        
        # Get alternative models
        sorted_models = sorted(model_scores.items(), key=lambda x: x[1]["total_score"], reverse=True)
        alternatives = [model_id for model_id, _ in sorted_models[1:4]]  # Top 3 alternatives
        
        # Create recommendation
        recommendation = ModelRecommendation(
            task_type=task_type,
            recommended_model_id=best_model_id,
            confidence_score=best_score["confidence"],
            reasoning=best_score["reasoning"],
            expected_performance={
                PerformanceMetric.RESPONSE_QUALITY: best_score["quality"],
                PerformanceMetric.RESPONSE_TIME: best_score["speed"],
                PerformanceMetric.COST_EFFICIENCY: best_score["cost_efficiency"],
                PerformanceMetric.CONSCIOUSNESS_COHERENCE: best_score["consciousness"]
            },
            cost_estimate=best_score["estimated_cost"],
            alternative_models=alternatives,
            recommendation_factors=priority_factors
        )
        
        # Store recommendation
        await self._store_recommendation(recommendation)
        self.current_recommendations[task_type] = recommendation
        
        return recommendation
    
    async def _calculate_model_score(self, model: ModelSpec, task_type: TaskType, 
                                   priority_factors: Dict[str, float]) -> Dict[str, Any]:
        """Calculate comprehensive score for a model"""
        
        # Get historical performance
        historical_perf = await self.performance_tracker.get_model_performance(model.model_id, task_type)
        
        # Base scores from model specifications
        base_scores = {
            "quality": 0.7,  # Default assumption
            "speed": 1.0 - (model.cost_per_token_input / 0.00005),  # Assume cost correlates with size/speed
            "cost_efficiency": 1.0 - min(1.0, (model.cost_per_token_input + model.cost_per_token_output) / 0.0001),
            "consciousness": 0.8 if task_type in model.specialized_tasks else 0.5
        }
        
        # Adjust with historical performance
        if "error" not in historical_perf:
            base_scores["quality"] = historical_perf.get("avg_quality_score", base_scores["quality"])
            base_scores["speed"] = 1.0 - min(1.0, historical_perf.get("avg_response_time_ms", 1000) / 5000)
            base_scores["consciousness"] = historical_perf.get("avg_consciousness_score", base_scores["consciousness"])
            
            # Update cost efficiency based on actual performance
            actual_cost_per_quality = historical_perf.get("avg_cost", 0.01) / max(0.1, historical_perf.get("avg_quality_score", 0.5))
            base_scores["cost_efficiency"] = 1.0 - min(1.0, actual_cost_per_quality / 0.1)
        
        # Calculate weighted total score
        total_score = sum(base_scores[factor] * weight for factor, weight in priority_factors.items() 
                         if factor in base_scores)
        
        # Calculate confidence based on data availability
        confidence = 0.5  # Base confidence
        if "error" not in historical_perf and historical_perf.get("total_requests", 0) > 0:
            confidence = min(0.95, 0.5 + (historical_perf["total_requests"] / 100) * 0.4)
        
        # Generate reasoning
        reasoning_parts = []
        if task_type in model.specialized_tasks:
            reasoning_parts.append(f"Specialized for {task_type.value}")
        if "error" not in historical_perf and historical_perf.get("avg_quality_score", 0) > 0.8:
            reasoning_parts.append("Strong historical performance")
        if base_scores["cost_efficiency"] > 0.7:
            reasoning_parts.append("Cost-effective option")
        if model.context_length > 50000:
            reasoning_parts.append("Large context window")
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "General purpose model"
        
        # Estimate cost for typical task
        typical_tokens = 1000  # Estimate
        estimated_cost = (model.cost_per_token_input * typical_tokens * 0.3 + 
                         model.cost_per_token_output * typical_tokens * 0.7)
        
        return {
            "total_score": total_score,
            "quality": base_scores["quality"],
            "speed": base_scores["speed"],
            "cost_efficiency": base_scores["cost_efficiency"],
            "consciousness": base_scores["consciousness"],
            "confidence": confidence,
            "reasoning": reasoning,
            "estimated_cost": estimated_cost,
            "historical_data_points": historical_perf.get("total_requests", 0)
        }
    
    async def _store_recommendation(self, recommendation: ModelRecommendation):
        """Store recommendation in database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            await conn.execute("""
                INSERT INTO model_recommendations 
                (task_type, recommended_model_id, confidence_score, reasoning,
                 expected_performance, cost_estimate, alternative_models, recommendation_factors)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                recommendation.task_type.value, recommendation.recommended_model_id,
                recommendation.confidence_score, recommendation.reasoning,
                json.dumps({k.value: v for k, v in recommendation.expected_performance.items()}),
                recommendation.cost_estimate, recommendation.alternative_models,
                json.dumps(recommendation.recommendation_factors)
            ))
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store recommendation: {e}")
    
    async def update_recommendations_from_collective_intelligence(self, hive_consensus: Dict[str, Any]):
        """Update recommendations based on collective intelligence from Genesis Prime hive"""
        
        # Process hive consensus data
        for task_type_str, consensus_data in hive_consensus.items():
            try:
                task_type = TaskType(task_type_str)
                
                # Extract collective insights
                preferred_model = consensus_data.get("preferred_model")
                confidence_boost = consensus_data.get("confidence_boost", 1.0)
                performance_feedback = consensus_data.get("performance_feedback", {})
                
                # Update current recommendation
                if task_type in self.current_recommendations:
                    current_rec = self.current_recommendations[task_type]
                    
                    # Adjust confidence based on collective consensus
                    current_rec.confidence_score = min(0.99, current_rec.confidence_score * confidence_boost)
                    
                    # Update reasoning with collective insights
                    if "collective_insights" in consensus_data:
                        current_rec.reasoning += f"; Collective insight: {consensus_data['collective_insights']}"
                    
                    # Store updated recommendation
                    await self._store_recommendation(current_rec)
                
                logger.info(f"Updated {task_type.value} recommendation based on collective intelligence")
                
            except Exception as e:
                logger.error(f"Failed to process collective intelligence for {task_type_str}: {e}")

class ABTestManager:
    """Manages A/B testing of different models"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.active_tests: Dict[str, ABTestConfiguration] = {}
        
    async def initialize(self):
        """Initialize the A/B test manager"""
        await self._load_active_tests()
        logger.info("A/B test manager initialized")
        
    async def _load_active_tests(self):
        """Load active A/B tests from database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            result = await conn.execute("""
                SELECT * FROM ab_test_configurations 
                WHERE status = 'running'
            """)
            
            async for row in result:
                test_config = ABTestConfiguration(
                    test_id=row[0],
                    test_name=row[1],
                    model_a_id=row[2],
                    model_b_id=row[3],
                    task_types=[TaskType(t) for t in row[4]],
                    sample_size=row[5],
                    traffic_split=row[6],
                    success_metrics=[PerformanceMetric(m) for m in row[7]],
                    duration_hours=row[8],
                    start_time=row[9],
                    status=row[10]
                )
                self.active_tests[test_config.test_id] = test_config
                
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to load active tests: {e}")
    
    async def create_ab_test(self, test_name: str, model_a_id: str, model_b_id: str,
                           task_types: List[TaskType], sample_size: int = 100,
                           duration_hours: int = 24) -> str:
        """Create a new A/B test"""
        
        test_id = f"ab_test_{int(time.time())}"
        
        test_config = ABTestConfiguration(
            test_id=test_id,
            test_name=test_name,
            model_a_id=model_a_id,
            model_b_id=model_b_id,
            task_types=task_types,
            sample_size=sample_size,
            traffic_split=0.5,
            success_metrics=[PerformanceMetric.RESPONSE_QUALITY, PerformanceMetric.COST_EFFICIENCY],
            duration_hours=duration_hours,
            start_time=datetime.now(),
            status="running"
        )
        
        # Store in database
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            await conn.execute("""
                INSERT INTO ab_test_configurations 
                (test_id, test_name, model_a_id, model_b_id, task_types, sample_size,
                 traffic_split, success_metrics, duration_hours, start_time, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                test_config.test_id, test_config.test_name, test_config.model_a_id,
                test_config.model_b_id, [t.value for t in test_config.task_types],
                test_config.sample_size, test_config.traffic_split,
                [m.value for m in test_config.success_metrics], test_config.duration_hours,
                test_config.start_time, test_config.status
            ))
            await conn.commit()
            await conn.close()
            
            self.active_tests[test_id] = test_config
            logger.info(f"Created A/B test {test_id}: {model_a_id} vs {model_b_id}")
            
        except Exception as e:
            logger.error(f"Failed to create A/B test: {e}")
            return None
            
        return test_id
    
    async def get_model_for_request(self, task_type: TaskType, request_id: str) -> Optional[str]:
        """Get model assignment for a request based on active A/B tests"""
        
        # Find applicable tests
        applicable_tests = [test for test in self.active_tests.values() 
                          if task_type in test.task_types and test.status == "running"]
        
        if not applicable_tests:
            return None
        
        # Use request ID to determine assignment (deterministic but random)
        test = applicable_tests[0]  # Use first applicable test
        hash_value = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
        assignment_value = (hash_value % 1000) / 1000.0
        
        if assignment_value < test.traffic_split:
            return test.model_a_id
        else:
            return test.model_b_id
    
    async def analyze_test_results(self, test_id: str) -> Dict[str, Any]:
        """Analyze results of an A/B test"""
        if test_id not in self.active_tests:
            return {"error": "Test not found"}
        
        test_config = self.active_tests[test_id]
        
        # Get performance data for both models
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            results = {}
            for model_id in [test_config.model_a_id, test_config.model_b_id]:
                result = await conn.execute("""
                    SELECT 
                        COUNT(*) as sample_size,
                        AVG(quality_score) as avg_quality,
                        AVG(response_time_ms) as avg_response_time,
                        AVG(cost) as avg_cost,
                        AVG(consciousness_score) as avg_consciousness,
                        SUM(CASE WHEN error_occurred THEN 1 ELSE 0 END) as error_count
                    FROM model_performance_records 
                    WHERE model_id = %s AND timestamp >= %s
                    AND task_type = ANY(%s)
                """, (model_id, test_config.start_time, [t.value for t in test_config.task_types]))
                
                row = await result.fetchone()
                if row and row[0] > 0:
                    results[model_id] = {
                        "sample_size": row[0],
                        "avg_quality": float(row[1]) if row[1] else 0,
                        "avg_response_time": float(row[2]) if row[2] else 0,
                        "avg_cost": float(row[3]) if row[3] else 0,
                        "avg_consciousness": float(row[4]) if row[4] else 0,
                        "error_count": row[5] if row[5] else 0,
                        "error_rate": (row[5] / row[0]) if row[0] > 0 else 0
                    }
                else:
                    results[model_id] = {"error": "No data"}
            
            await conn.close()
            
            # Determine winner
            winner = None
            if all("error" not in result for result in results.values()):
                model_a_score = results[test_config.model_a_id]["avg_quality"] - results[test_config.model_a_id]["avg_cost"] * 1000
                model_b_score = results[test_config.model_b_id]["avg_quality"] - results[test_config.model_b_id]["avg_cost"] * 1000
                
                if model_a_score > model_b_score:
                    winner = test_config.model_a_id
                elif model_b_score > model_a_score:
                    winner = test_config.model_b_id
                else:
                    winner = "tie"
            
            return {
                "test_id": test_id,
                "test_name": test_config.test_name,
                "model_a_results": results.get(test_config.model_a_id, {}),
                "model_b_results": results.get(test_config.model_b_id, {}),
                "winner": winner,
                "test_duration_hours": (datetime.now() - test_config.start_time).total_seconds() / 3600,
                "statistical_significance": self._calculate_significance(results, test_config)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze test results: {e}")
            return {"error": str(e)}
    
    def _calculate_significance(self, results: Dict[str, Any], test_config: ABTestConfiguration) -> Dict[str, Any]:
        """Calculate statistical significance of test results"""
        # Simplified significance test
        if all("error" not in result for result in results.values()):
            model_a_data = results[test_config.model_a_id]
            model_b_data = results[test_config.model_b_id]
            
            # Check if we have enough samples
            min_sample_size = max(30, test_config.sample_size * 0.1)
            
            if (model_a_data["sample_size"] >= min_sample_size and 
                model_b_data["sample_size"] >= min_sample_size):
                
                # Simple difference check (would use proper statistical tests in production)
                quality_diff = abs(model_a_data["avg_quality"] - model_b_data["avg_quality"])
                cost_diff = abs(model_a_data["avg_cost"] - model_b_data["avg_cost"])
                
                significance = "significant" if quality_diff > 0.1 or cost_diff > 0.01 else "not_significant"
                
                return {
                    "status": significance,
                    "quality_difference": quality_diff,
                    "cost_difference": cost_diff,
                    "sample_sizes": {
                        "model_a": model_a_data["sample_size"],
                        "model_b": model_b_data["sample_size"]
                    }
                }
        
        return {"status": "insufficient_data"}

class DynamicModelManager:
    """Main manager for dynamic model selection and optimization"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.model_selector = IntelligentModelSelector(database_url)
        self.ab_test_manager = ABTestManager(database_url)
        self.current_model_assignments: Dict[TaskType, str] = {}
        
    async def initialize(self):
        """Initialize the dynamic model management system"""
        await self.model_selector.initialize()
        await self.ab_test_manager.initialize()
        await self._load_current_assignments()
        logger.info("Dynamic model manager initialized")
        
    async def _load_current_assignments(self):
        """Load current model assignments"""
        for task_type in TaskType:
            recommendation = await self.model_selector.get_model_recommendation(task_type)
            self.current_model_assignments[task_type] = recommendation.recommended_model_id
    
    async def get_optimal_model(self, task_type: TaskType, request_id: str = None,
                              priority_factors: Optional[Dict[str, float]] = None) -> str:
        """Get the optimal model for a specific task"""
        
        # Check for A/B test assignment first
        if request_id:
            ab_model = await self.ab_test_manager.get_model_for_request(task_type, request_id)
            if ab_model:
                return ab_model
        
        # Get current assignment or recommendation
        if task_type in self.current_model_assignments:
            return self.current_model_assignments[task_type]
        else:
            recommendation = await self.model_selector.get_model_recommendation(task_type, priority_factors)
            self.current_model_assignments[task_type] = recommendation.recommended_model_id
            return recommendation.recommended_model_id
    
    async def update_model_performance(self, model_id: str, task_type: TaskType,
                                     performance_data: Dict[str, Any], request_id: str = None):
        """Update model performance based on actual usage"""
        
        # Create performance record
        record = PerformanceRecord(
            record_id=request_id or f"perf_{int(time.time())}_{model_id}",
            model_id=model_id,
            task_type=task_type,
            prompt_hash=performance_data.get("prompt_hash", ""),
            response_time_ms=performance_data.get("response_time_ms", 0),
            token_count_input=performance_data.get("token_count_input", 0),
            token_count_output=performance_data.get("token_count_output", 0),
            cost=performance_data.get("cost", 0.0),
            quality_score=performance_data.get("quality_score", 0.0),
            consciousness_score=performance_data.get("consciousness_score", 0.0),
            creativity_score=performance_data.get("creativity_score", 0.0),
            accuracy_score=performance_data.get("accuracy_score", 0.0),
            user_rating=performance_data.get("user_rating"),
            error_occurred=performance_data.get("error_occurred", False),
            error_type=performance_data.get("error_type"),
            timestamp=datetime.now(),
            context_data=performance_data.get("context_data", {})
        )
        
        # Record performance
        await self.model_selector.performance_tracker.record_performance(record)
        
        # Trigger recommendation update if performance is significantly different
        await self._check_for_recommendation_updates(task_type)
        
    async def _check_for_recommendation_updates(self, task_type: TaskType):
        """Check if recommendations should be updated based on new performance data"""
        
        # Get current performance for assigned model
        current_model = self.current_model_assignments.get(task_type)
        if not current_model:
            return
        
        current_perf = await self.model_selector.performance_tracker.get_model_performance(
            current_model, task_type, time_window_hours=6
        )
        
        # If performance is declining, get new recommendation
        if ("error" not in current_perf and 
            (current_perf.get("avg_quality_score", 0) < 0.6 or 
             current_perf.get("error_rate", 0) > 0.1)):
            
            logger.info(f"Performance decline detected for {current_model} on {task_type.value}, updating recommendation")
            new_recommendation = await self.model_selector.get_model_recommendation(task_type)
            self.current_model_assignments[task_type] = new_recommendation.recommended_model_id
    
    async def create_model_comparison_test(self, task_type: TaskType, 
                                         challenger_model_id: str) -> str:
        """Create A/B test to compare current model with a challenger"""
        
        current_model = self.current_model_assignments.get(task_type)
        if not current_model:
            current_model = await self.get_optimal_model(task_type)
        
        test_name = f"{task_type.value}_{current_model}_vs_{challenger_model_id}"
        
        test_id = await self.ab_test_manager.create_ab_test(
            test_name=test_name,
            model_a_id=current_model,
            model_b_id=challenger_model_id,
            task_types=[task_type],
            sample_size=100,
            duration_hours=48
        )
        
        return test_id
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        status = {
            "current_assignments": {task.value: model for task, model in self.current_model_assignments.items()},
            "active_ab_tests": len(self.ab_test_manager.active_tests),
            "available_models": len(self.model_selector.model_db.models),
            "recent_performance": {}
        }
        
        # Get recent performance for each assigned model
        for task_type, model_id in self.current_model_assignments.items():
            perf = await self.model_selector.performance_tracker.get_model_performance(
                model_id, task_type, time_window_hours=24
            )
            status["recent_performance"][f"{task_type.value}_{model_id}"] = perf
        
        return status

# Example usage and testing
async def test_dynamic_model_selector():
    """Test the dynamic model selection system"""
    print("🤖 Testing Dynamic Model Selection System")
    
    database_url = "postgresql://postgres:password@localhost:5432/sentient"
    manager = DynamicModelManager(database_url)
    
    try:
        await manager.initialize()
        print("✅ Dynamic model manager initialized")
        
        # Test model recommendation
        task_type = TaskType.CONSCIOUSNESS_PROCESSING
        model_id = await manager.get_optimal_model(task_type)
        print(f"✅ Recommended model for {task_type.value}: {model_id}")
        
        # Test performance update
        performance_data = {
            "response_time_ms": 1500,
            "token_count_input": 100,
            "token_count_output": 200,
            "cost": 0.005,
            "quality_score": 0.85,
            "consciousness_score": 0.92,
            "creativity_score": 0.78,
            "accuracy_score": 0.88,
            "error_occurred": False
        }
        
        await manager.update_model_performance(model_id, task_type, performance_data)
        print("✅ Updated model performance")
        
        # Test A/B test creation
        test_id = await manager.create_model_comparison_test(
            task_type, "openrouter/claude-3-opus"
        )
        if test_id:
            print(f"✅ Created A/B test: {test_id}")
        
        # Test system status
        status = await manager.get_system_status()
        print(f"✅ System status retrieved: {status['available_models']} models available")
        
        print("\n🤖 Dynamic Model Selector Test Results:")
        print(f"   • Current Assignments: {len(status['current_assignments'])}")
        print(f"   • Active A/B Tests: {status['active_ab_tests']}")
        print(f"   • Available Models: {status['available_models']}")
        
        # Show model assignments
        for task, model in status['current_assignments'].items():
            print(f"   • {task}: {model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_dynamic_model_selector())