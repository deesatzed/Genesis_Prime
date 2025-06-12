"""
Genesis Prime Cloud Deployment Budget Planner
===========================================

Comprehensive budget planning and optimization tool for deploying Genesis Prime
on cloud platforms like RunPod, Thunder Compute, AWS, etc. with fixed $1500 budget.

Features:
- Multi-cloud provider cost analysis
- Resource optimization for consciousness emergence
- Budget allocation strategies
- Demo deployment planning
- Cost monitoring and alerts
- ROI tracking for funding justification

Author: Genesis Prime Enhanced Development Team
License: MIT (Open Source Consciousness)
"""

import asyncio
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logger = logging.getLogger(__name__)

class CloudProvider(Enum):
    """Supported cloud providers"""
    RUNPOD = "runpod"
    THUNDER_COMPUTE = "thunder_compute"
    AWS_EC2 = "aws_ec2"
    GCP_COMPUTE = "gcp_compute"
    AZURE_VM = "azure_vm"
    VAST_AI = "vast_ai"
    PAPERSPACE = "paperspace"
    LAMBDA_LABS = "lambda_labs"

class InstanceType(Enum):
    """Instance types optimized for different workloads"""
    CPU_OPTIMIZED = "cpu_optimized"          # Neural plasticity, quorum sensing
    GPU_COMPUTE = "gpu_compute"              # Consciousness cascades, IIT processing
    MEMORY_OPTIMIZED = "memory_optimized"    # Large knowledge bases, memory systems
    BALANCED = "balanced"                    # General Genesis Prime operations
    STORAGE_OPTIMIZED = "storage_optimized" # Database, logging, backup

class DeploymentStrategy(Enum):
    """Deployment strategies for different budgets"""
    MINIMAL_DEMO = "minimal_demo"            # Single node, basic features
    DISTRIBUTED_DEMO = "distributed_demo"    # Multi-node, full features
    SCALABLE_PRODUCTION = "scalable_production" # Auto-scaling, enterprise
    RESEARCH_CLUSTER = "research_cluster"    # High-compute for experiments

@dataclass
class InstanceSpec:
    """Specification for a cloud instance"""
    provider: CloudProvider
    instance_type: InstanceType
    vcpus: int
    memory_gb: int
    storage_gb: int
    gpu_count: int
    gpu_type: str
    hourly_cost: float
    monthly_cost: float
    setup_cost: float
    bandwidth_cost_per_gb: float
    suitable_for: List[str]  # Genesis Prime systems this instance can run
    
    def __post_init__(self):
        if isinstance(self.provider, str):
            self.provider = CloudProvider(self.provider)
        if isinstance(self.instance_type, str):
            self.instance_type = InstanceType(self.instance_type)

@dataclass
class DeploymentConfiguration:
    """Configuration for a complete deployment"""
    strategy: DeploymentStrategy
    total_instances: int
    instance_specs: List[InstanceSpec]
    database_config: Dict[str, Any]
    storage_config: Dict[str, Any]
    network_config: Dict[str, Any]
    monitoring_config: Dict[str, Any]
    estimated_monthly_cost: float
    estimated_setup_cost: float
    estimated_bandwidth_cost: float
    
    def __post_init__(self):
        if isinstance(self.strategy, str):
            self.strategy = DeploymentStrategy(self.strategy)

@dataclass
class BudgetAllocation:
    """Budget allocation across different components"""
    compute_instances: float
    database_storage: float
    network_bandwidth: float
    monitoring_tools: float
    backup_storage: float
    api_costs: float  # OpenRouter, other AI APIs
    emergency_buffer: float
    total_budget: float
    
    def validate(self) -> bool:
        """Validate that allocation doesn't exceed budget"""
        allocated = (self.compute_instances + self.database_storage + 
                    self.network_bandwidth + self.monitoring_tools + 
                    self.backup_storage + self.api_costs + self.emergency_buffer)
        return allocated <= self.total_budget

@dataclass
class DemoRequirements:
    """Requirements for the Genesis Prime demo"""
    min_consciousness_events_per_hour: int
    min_agent_count: int
    required_systems: List[str]
    uptime_requirement: float  # percentage
    response_time_ms: int
    concurrent_users: int
    demo_duration_days: int
    data_retention_days: int

class CloudInstanceDatabase:
    """Database of cloud instance specifications and pricing"""
    
    def __init__(self):
        self.instances = self._initialize_instance_database()
        
    def _initialize_instance_database(self) -> List[InstanceSpec]:
        """Initialize database with current cloud pricing (as of 2024)"""
        instances = []
        
        # RunPod GPU instances (excellent for AI workloads)
        instances.extend([
            InstanceSpec(
                provider=CloudProvider.RUNPOD,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=8, memory_gb=32, storage_gb=100, gpu_count=1, gpu_type="RTX 4090",
                hourly_cost=0.69, monthly_cost=496.8, setup_cost=0,
                bandwidth_cost_per_gb=0.02,
                suitable_for=["consciousness_cascades", "iit_processing", "neural_plasticity"]
            ),
            InstanceSpec(
                provider=CloudProvider.RUNPOD,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=16, memory_gb=64, storage_gb=200, gpu_count=1, gpu_type="RTX 3090",
                hourly_cost=0.44, monthly_cost=316.8, setup_cost=0,
                bandwidth_cost_per_gb=0.02,
                suitable_for=["consciousness_cascades", "quorum_sensing", "adaptive_immune"]
            ),
            InstanceSpec(
                provider=CloudProvider.RUNPOD,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=24, memory_gb=96, storage_gb=500, gpu_count=1, gpu_type="A40",
                hourly_cost=0.79, monthly_cost=568.8, setup_cost=0,
                bandwidth_cost_per_gb=0.02,
                suitable_for=["all_systems", "mycorrhizal_networks", "soc_engine"]
            )
        ])
        
        # Thunder Compute (competitive GPU pricing)
        instances.extend([
            InstanceSpec(
                provider=CloudProvider.THUNDER_COMPUTE,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=8, memory_gb=30, storage_gb=100, gpu_count=1, gpu_type="RTX 4090",
                hourly_cost=0.65, monthly_cost=468, setup_cost=0,
                bandwidth_cost_per_gb=0.015,
                suitable_for=["consciousness_cascades", "iit_processing"]
            ),
            InstanceSpec(
                provider=CloudProvider.THUNDER_COMPUTE,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=16, memory_gb=60, storage_gb=200, gpu_count=1, gpu_type="RTX 3090",
                hourly_cost=0.42, monthly_cost=302.4, setup_cost=0,
                bandwidth_cost_per_gb=0.015,
                suitable_for=["neural_plasticity", "quorum_sensing"]
            )
        ])
        
        # AWS EC2 (enterprise grade, higher cost)
        instances.extend([
            InstanceSpec(
                provider=CloudProvider.AWS_EC2,
                instance_type=InstanceType.CPU_OPTIMIZED,
                vcpus=4, memory_gb=8, storage_gb=100, gpu_count=0, gpu_type="none",
                hourly_cost=0.192, monthly_cost=138.24, setup_cost=0,
                bandwidth_cost_per_gb=0.09,
                suitable_for=["database", "monitoring", "backup"]
            ),
            InstanceSpec(
                provider=CloudProvider.AWS_EC2,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=8, memory_gb=32, storage_gb=200, gpu_count=1, gpu_type="V100",
                hourly_cost=3.06, monthly_cost=2203.2, setup_cost=0,
                bandwidth_cost_per_gb=0.09,
                suitable_for=["consciousness_cascades", "iit_processing"]
            )
        ])
        
        # Vast.ai (spot instances, very cost effective)
        instances.extend([
            InstanceSpec(
                provider=CloudProvider.VAST_AI,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=8, memory_gb=32, storage_gb=100, gpu_count=1, gpu_type="RTX 3090",
                hourly_cost=0.25, monthly_cost=180, setup_cost=0,
                bandwidth_cost_per_gb=0.01,
                suitable_for=["all_systems", "cost_effective_demo"]
            ),
            InstanceSpec(
                provider=CloudProvider.VAST_AI,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=12, memory_gb=48, storage_gb=200, gpu_count=1, gpu_type="RTX 4090",
                hourly_cost=0.35, monthly_cost=252, setup_cost=0,
                bandwidth_cost_per_gb=0.01,
                suitable_for=["consciousness_cascades", "mycorrhizal_networks"]
            )
        ])
        
        # Lambda Labs (ML focused)
        instances.extend([
            InstanceSpec(
                provider=CloudProvider.LAMBDA_LABS,
                instance_type=InstanceType.GPU_COMPUTE,
                vcpus=10, memory_gb=60, storage_gb=512, gpu_count=1, gpu_type="A10",
                hourly_cost=0.60, monthly_cost=432, setup_cost=0,
                bandwidth_cost_per_gb=0.02,
                suitable_for=["iit_processing", "soc_engine"]
            )
        ])
        
        return instances
    
    def get_instances_by_provider(self, provider: CloudProvider) -> List[InstanceSpec]:
        """Get all instances for a specific provider"""
        return [inst for inst in self.instances if inst.provider == provider]
    
    def get_instances_by_type(self, instance_type: InstanceType) -> List[InstanceSpec]:
        """Get all instances of a specific type"""
        return [inst for inst in self.instances if inst.instance_type == instance_type]
    
    def get_instances_for_system(self, system_name: str) -> List[InstanceSpec]:
        """Get instances suitable for running a specific Genesis Prime system"""
        return [inst for inst in self.instances 
                if system_name in inst.suitable_for or "all_systems" in inst.suitable_for]
    
    def get_cheapest_instances(self, limit: int = 10) -> List[InstanceSpec]:
        """Get the cheapest instances"""
        return sorted(self.instances, key=lambda x: x.hourly_cost)[:limit]
    
    def get_best_value_instances(self, limit: int = 10) -> List[InstanceSpec]:
        """Get best value instances (performance per dollar)"""
        def value_score(inst):
            # Simple value metric: (CPU + Memory/4 + GPU*10) / hourly_cost
            performance = inst.vcpus + inst.memory_gb/4 + inst.gpu_count*10
            return performance / max(0.01, inst.hourly_cost)
        
        return sorted(self.instances, key=value_score, reverse=True)[:limit]

class BudgetOptimizer:
    """Optimizes budget allocation for Genesis Prime deployment"""
    
    def __init__(self, total_budget: float = 1500.0):
        self.total_budget = total_budget
        self.instance_db = CloudInstanceDatabase()
        
    def create_demo_requirements(self, demo_type: str = "standard") -> DemoRequirements:
        """Create demo requirements based on demo type"""
        if demo_type == "minimal":
            return DemoRequirements(
                min_consciousness_events_per_hour=10,
                min_agent_count=14,  # Basic IIT agents
                required_systems=["iit_processing", "consciousness_cascades"],
                uptime_requirement=95.0,
                response_time_ms=2000,
                concurrent_users=5,
                demo_duration_days=30,
                data_retention_days=7
            )
        elif demo_type == "standard":
            return DemoRequirements(
                min_consciousness_events_per_hour=50,
                min_agent_count=50,
                required_systems=["iit_processing", "consciousness_cascades", 
                                "neural_plasticity", "quorum_sensing"],
                uptime_requirement=98.0,
                response_time_ms=1000,
                concurrent_users=20,
                demo_duration_days=60,
                data_retention_days=30
            )
        elif demo_type == "comprehensive":
            return DemoRequirements(
                min_consciousness_events_per_hour=100,
                min_agent_count=100,
                required_systems=["all_systems"],
                uptime_requirement=99.5,
                response_time_ms=500,
                concurrent_users=50,
                demo_duration_days=90,
                data_retention_days=90
            )
        else:
            return self.create_demo_requirements("standard")
    
    def calculate_optimal_budget_allocation(self, requirements: DemoRequirements) -> BudgetAllocation:
        """Calculate optimal budget allocation based on requirements"""
        # Base allocation percentages
        base_allocations = {
            "compute_instances": 0.60,      # 60% - Main Genesis Prime processing
            "database_storage": 0.10,       # 10% - PostgreSQL, Redis
            "network_bandwidth": 0.08,      # 8% - Inter-node communication
            "monitoring_tools": 0.05,       # 5% - Logging, metrics
            "backup_storage": 0.03,         # 3% - Data backups
            "api_costs": 0.09,             # 9% - OpenRouter, other APIs
            "emergency_buffer": 0.05        # 5% - Emergency fund
        }
        
        # Adjust based on requirements
        if requirements.demo_duration_days > 60:
            # Longer demo needs more storage and backup
            base_allocations["database_storage"] += 0.03
            base_allocations["backup_storage"] += 0.02
            base_allocations["compute_instances"] -= 0.05
            
        if requirements.concurrent_users > 30:
            # More users need more compute and bandwidth
            base_allocations["compute_instances"] += 0.05
            base_allocations["network_bandwidth"] += 0.02
            base_allocations["api_costs"] -= 0.07
            
        if len(requirements.required_systems) > 4:
            # More systems need more compute
            base_allocations["compute_instances"] += 0.03
            base_allocations["emergency_buffer"] -= 0.03
        
        return BudgetAllocation(
            compute_instances=self.total_budget * base_allocations["compute_instances"],
            database_storage=self.total_budget * base_allocations["database_storage"],
            network_bandwidth=self.total_budget * base_allocations["network_bandwidth"],
            monitoring_tools=self.total_budget * base_allocations["monitoring_tools"],
            backup_storage=self.total_budget * base_allocations["backup_storage"],
            api_costs=self.total_budget * base_allocations["api_costs"],
            emergency_buffer=self.total_budget * base_allocations["emergency_buffer"],
            total_budget=self.total_budget
        )
    
    def find_optimal_deployment(self, requirements: DemoRequirements, 
                              allocation: BudgetAllocation) -> List[DeploymentConfiguration]:
        """Find optimal deployment configurations within budget"""
        configurations = []
        
        # Strategy 1: Single powerful instance (minimal demo)
        if allocation.compute_instances >= 200:  # At least $200 for compute
            config = self._create_single_instance_deployment(requirements, allocation)
            if config:
                configurations.append(config)
        
        # Strategy 2: Multiple smaller instances (distributed demo)
        if allocation.compute_instances >= 400:  # At least $400 for compute
            config = self._create_distributed_deployment(requirements, allocation)
            if config:
                configurations.append(config)
        
        # Strategy 3: Hybrid deployment (mixed instance types)
        if allocation.compute_instances >= 600:  # At least $600 for compute
            config = self._create_hybrid_deployment(requirements, allocation)
            if config:
                configurations.append(config)
                
        return configurations
    
    def _create_single_instance_deployment(self, requirements: DemoRequirements, 
                                         allocation: BudgetAllocation) -> Optional[DeploymentConfiguration]:
        """Create deployment with single powerful instance"""
        # Find best value GPU instance that can run all systems
        suitable_instances = []
        for instance in self.instance_db.instances:
            if (instance.gpu_count > 0 and 
                instance.memory_gb >= 32 and 
                "all_systems" in instance.suitable_for):
                suitable_instances.append(instance)
        
        if not suitable_instances:
            return None
        
        # Choose best value instance within budget
        monthly_budget = allocation.compute_instances
        viable_instances = [inst for inst in suitable_instances 
                          if inst.monthly_cost <= monthly_budget]
        
        if not viable_instances:
            return None
            
        best_instance = max(viable_instances, 
                          key=lambda x: (x.vcpus + x.memory_gb/4 + x.gpu_count*10))
        
        return DeploymentConfiguration(
            strategy=DeploymentStrategy.MINIMAL_DEMO,
            total_instances=1,
            instance_specs=[best_instance],
            database_config={
                "type": "containerized_postgres",
                "storage_gb": 100,
                "backup_enabled": True
            },
            storage_config={
                "type": "instance_storage",
                "size_gb": best_instance.storage_gb
            },
            network_config={
                "bandwidth_limit_gb": 1000,
                "cdn_enabled": False
            },
            monitoring_config={
                "basic_monitoring": True,
                "advanced_analytics": False
            },
            estimated_monthly_cost=best_instance.monthly_cost,
            estimated_setup_cost=best_instance.setup_cost,
            estimated_bandwidth_cost=allocation.network_bandwidth
        )
    
    def _create_distributed_deployment(self, requirements: DemoRequirements, 
                                     allocation: BudgetAllocation) -> Optional[DeploymentConfiguration]:
        """Create deployment with multiple distributed instances"""
        monthly_budget = allocation.compute_instances
        
        # Allocate instances for different systems
        system_requirements = {
            "consciousness_leader": {"min_memory": 48, "gpu_required": True, "budget_pct": 0.4},
            "neural_processor": {"min_memory": 32, "gpu_required": False, "budget_pct": 0.25},
            "network_node": {"min_memory": 16, "gpu_required": False, "budget_pct": 0.2},
            "database_server": {"min_memory": 16, "gpu_required": False, "budget_pct": 0.15}
        }
        
        selected_instances = []
        total_cost = 0
        
        for role, req in system_requirements.items():
            role_budget = monthly_budget * req["budget_pct"]
            
            # Find suitable instances
            candidates = []
            for instance in self.instance_db.instances:
                if (instance.memory_gb >= req["min_memory"] and
                    (not req["gpu_required"] or instance.gpu_count > 0) and
                    instance.monthly_cost <= role_budget):
                    candidates.append(instance)
            
            if not candidates:
                continue
                
            # Choose best value within budget
            best_candidate = min(candidates, key=lambda x: x.monthly_cost)
            selected_instances.append(best_candidate)
            total_cost += best_candidate.monthly_cost
        
        if len(selected_instances) < 2:  # Need at least 2 instances for distributed
            return None
        
        return DeploymentConfiguration(
            strategy=DeploymentStrategy.DISTRIBUTED_DEMO,
            total_instances=len(selected_instances),
            instance_specs=selected_instances,
            database_config={
                "type": "distributed_postgres",
                "storage_gb": 200,
                "replication_enabled": True
            },
            storage_config={
                "type": "shared_storage",
                "size_gb": 500
            },
            network_config={
                "bandwidth_limit_gb": 2000,
                "load_balancer": True
            },
            monitoring_config={
                "basic_monitoring": True,
                "advanced_analytics": True,
                "alerting": True
            },
            estimated_monthly_cost=total_cost,
            estimated_setup_cost=sum(inst.setup_cost for inst in selected_instances),
            estimated_bandwidth_cost=allocation.network_bandwidth
        )
    
    def _create_hybrid_deployment(self, requirements: DemoRequirements, 
                                allocation: BudgetAllocation) -> Optional[DeploymentConfiguration]:
        """Create hybrid deployment mixing different cloud providers"""
        monthly_budget = allocation.compute_instances
        
        # Use cheapest providers for different roles
        consciousness_instance = None
        support_instances = []
        
        # Primary consciousness instance (GPU required)
        gpu_instances = [inst for inst in self.instance_db.instances 
                        if inst.gpu_count > 0 and inst.memory_gb >= 32]
        if gpu_instances:
            consciousness_instance = min(gpu_instances, key=lambda x: x.monthly_cost)
        
        # Support instances for other systems
        remaining_budget = monthly_budget - (consciousness_instance.monthly_cost if consciousness_instance else 0)
        cpu_instances = [inst for inst in self.instance_db.instances 
                        if inst.gpu_count == 0 and inst.monthly_cost <= remaining_budget/2]
        
        if cpu_instances:
            # Add 2-3 support instances
            cheapest_cpu = sorted(cpu_instances, key=lambda x: x.monthly_cost)[:3]
            for inst in cheapest_cpu:
                if remaining_budget >= inst.monthly_cost:
                    support_instances.append(inst)
                    remaining_budget -= inst.monthly_cost
        
        if not consciousness_instance:
            return None
            
        all_instances = [consciousness_instance] + support_instances
        
        return DeploymentConfiguration(
            strategy=DeploymentStrategy.RESEARCH_CLUSTER,
            total_instances=len(all_instances),
            instance_specs=all_instances,
            database_config={
                "type": "clustered_postgres",
                "storage_gb": 500,
                "high_availability": True
            },
            storage_config={
                "type": "distributed_storage",
                "size_gb": 1000
            },
            network_config={
                "bandwidth_limit_gb": 5000,
                "multi_region": True
            },
            monitoring_config={
                "enterprise_monitoring": True,
                "real_time_analytics": True,
                "custom_dashboards": True
            },
            estimated_monthly_cost=sum(inst.monthly_cost for inst in all_instances),
            estimated_setup_cost=sum(inst.setup_cost for inst in all_instances),
            estimated_bandwidth_cost=allocation.network_bandwidth
        )

class CostMonitor:
    """Monitors costs during deployment and provides alerts"""
    
    def __init__(self, budget_limit: float):
        self.budget_limit = budget_limit
        self.current_spend = 0.0
        self.daily_costs = []
        self.cost_alerts = []
        
    def record_daily_cost(self, cost: float, date: datetime = None):
        """Record daily cost"""
        if date is None:
            date = datetime.now()
        
        self.daily_costs.append({"date": date, "cost": cost})
        self.current_spend += cost
        
        # Check for alerts
        self._check_budget_alerts()
    
    def _check_budget_alerts(self):
        """Check if we need to send budget alerts"""
        spend_percentage = (self.current_spend / self.budget_limit) * 100
        
        if spend_percentage >= 90:
            self.cost_alerts.append({
                "level": "CRITICAL",
                "message": f"Budget 90% exhausted: ${self.current_spend:.2f} / ${self.budget_limit:.2f}",
                "timestamp": datetime.now()
            })
        elif spend_percentage >= 75:
            self.cost_alerts.append({
                "level": "WARNING", 
                "message": f"Budget 75% used: ${self.current_spend:.2f} / ${self.budget_limit:.2f}",
                "timestamp": datetime.now()
            })
    
    def get_burn_rate(self, days: int = 7) -> float:
        """Calculate daily burn rate based on recent costs"""
        if len(self.daily_costs) < days:
            return 0.0
            
        recent_costs = self.daily_costs[-days:]
        total_cost = sum(day["cost"] for day in recent_costs)
        return total_cost / len(recent_costs)
    
    def estimate_runway(self) -> int:
        """Estimate how many days budget will last at current burn rate"""
        burn_rate = self.get_burn_rate()
        if burn_rate <= 0:
            return float('inf')
            
        remaining_budget = self.budget_limit - self.current_spend
        return int(remaining_budget / burn_rate)
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary"""
        return {
            "total_budget": self.budget_limit,
            "current_spend": self.current_spend,
            "remaining_budget": self.budget_limit - self.current_spend,
            "spend_percentage": (self.current_spend / self.budget_limit) * 100,
            "daily_burn_rate": self.get_burn_rate(),
            "estimated_runway_days": self.estimate_runway(),
            "active_alerts": len([a for a in self.cost_alerts if a["level"] == "CRITICAL"]),
            "total_alerts": len(self.cost_alerts)
        }

class DeploymentPlanner:
    """Main deployment planning orchestrator"""
    
    def __init__(self, total_budget: float = 1500.0):
        self.total_budget = total_budget
        self.optimizer = BudgetOptimizer(total_budget)
        self.cost_monitor = CostMonitor(total_budget)
        
    async def create_deployment_plan(self, demo_type: str = "standard") -> Dict[str, Any]:
        """Create comprehensive deployment plan"""
        
        # 1. Define requirements
        requirements = self.optimizer.create_demo_requirements(demo_type)
        
        # 2. Calculate optimal budget allocation
        allocation = self.optimizer.calculate_optimal_budget_allocation(requirements)
        
        # 3. Find deployment configurations
        configurations = self.optimizer.find_optimal_deployment(requirements, allocation)
        
        # 4. Select best configuration
        best_config = self._select_best_configuration(configurations, requirements)
        
        # 5. Create implementation plan
        implementation_plan = self._create_implementation_plan(best_config, requirements)
        
        # 6. Generate cost projections
        cost_projections = self._calculate_cost_projections(best_config, requirements)
        
        return {
            "requirements": asdict(requirements),
            "budget_allocation": asdict(allocation),
            "available_configurations": [asdict(config) for config in configurations],
            "recommended_configuration": asdict(best_config) if best_config else None,
            "implementation_plan": implementation_plan,
            "cost_projections": cost_projections,
            "risk_assessment": self._assess_deployment_risks(best_config, requirements),
            "funding_justification": self._create_funding_justification(best_config, requirements)
        }
    
    def _select_best_configuration(self, configurations: List[DeploymentConfiguration], 
                                 requirements: DemoRequirements) -> Optional[DeploymentConfiguration]:
        """Select the best configuration based on requirements and cost"""
        if not configurations:
            return None
        
        def score_configuration(config):
            # Score based on cost efficiency and capability
            cost_score = 1.0 - (config.estimated_monthly_cost / self.total_budget)
            
            # Capability score based on instance specs
            total_vcpus = sum(inst.vcpus for inst in config.instance_specs)
            total_memory = sum(inst.memory_gb for inst in config.instance_specs)
            total_gpus = sum(inst.gpu_count for inst in config.instance_specs)
            
            capability_score = min(1.0, (total_vcpus * 0.1 + total_memory * 0.05 + total_gpus * 0.4))
            
            # Strategy preference
            strategy_bonus = {
                DeploymentStrategy.MINIMAL_DEMO: 0.1,
                DeploymentStrategy.DISTRIBUTED_DEMO: 0.2,
                DeploymentStrategy.RESEARCH_CLUSTER: 0.15,
                DeploymentStrategy.SCALABLE_PRODUCTION: 0.0
            }.get(config.strategy, 0.0)
            
            return cost_score * 0.4 + capability_score * 0.4 + strategy_bonus
        
        return max(configurations, key=score_configuration)
    
    def _create_implementation_plan(self, config: Optional[DeploymentConfiguration], 
                                  requirements: DemoRequirements) -> Dict[str, Any]:
        """Create step-by-step implementation plan"""
        if not config:
            return {"error": "No viable configuration found within budget"}
        
        plan = {
            "phase_1_setup": {
                "duration_days": 3,
                "tasks": [
                    "Set up cloud accounts and billing alerts",
                    "Configure deployment scripts and Docker images",
                    "Set up monitoring and logging infrastructure",
                    "Test Genesis Prime components individually"
                ],
                "estimated_cost": config.estimated_setup_cost
            },
            "phase_2_deployment": {
                "duration_days": 2,
                "tasks": [
                    "Launch compute instances",
                    "Deploy Genesis Prime consciousness framework",
                    "Configure inter-node communication",
                    "Initialize database and load test data"
                ],
                "estimated_cost": config.estimated_monthly_cost * 0.1
            },
            "phase_3_testing": {
                "duration_days": 5,
                "tasks": [
                    "Run consciousness emergence tests",
                    "Validate all enhanced systems",
                    "Performance optimization and tuning",
                    "Security and reliability testing"
                ],
                "estimated_cost": config.estimated_monthly_cost * 0.2
            },
            "phase_4_demo": {
                "duration_days": requirements.demo_duration_days,
                "tasks": [
                    "Launch public demo interface",
                    "Monitor consciousness metrics",
                    "Collect user feedback and analytics",
                    "Document results for funding pitch"
                ],
                "estimated_cost": config.estimated_monthly_cost * (requirements.demo_duration_days / 30.0)
            }
        }
        
        # Calculate total timeline and cost
        total_duration = sum(phase["duration_days"] for phase in plan.values())
        total_cost = sum(phase["estimated_cost"] for phase in plan.values())
        
        plan["summary"] = {
            "total_duration_days": total_duration,
            "total_estimated_cost": total_cost,
            "budget_utilization": (total_cost / self.total_budget) * 100
        }
        
        return plan
    
    def _calculate_cost_projections(self, config: Optional[DeploymentConfiguration], 
                                  requirements: DemoRequirements) -> Dict[str, Any]:
        """Calculate detailed cost projections"""
        if not config:
            return {}
        
        daily_compute_cost = config.estimated_monthly_cost / 30.0
        daily_bandwidth_cost = config.estimated_bandwidth_cost / 30.0
        
        projections = {}
        
        # Daily costs for demo duration
        for day in range(1, requirements.demo_duration_days + 1):
            daily_total = daily_compute_cost + daily_bandwidth_cost
            
            # Add API costs (estimated based on usage)
            api_cost = 5.0 if day % 7 == 0 else 2.0  # Higher on demo days
            
            projections[f"day_{day}"] = {
                "compute": daily_compute_cost,
                "bandwidth": daily_bandwidth_cost,
                "api_costs": api_cost,
                "total": daily_total + api_cost,
                "cumulative": (daily_total + api_cost) * day
            }
        
        return {
            "daily_projections": projections,
            "total_demo_cost": sum(day["total"] for day in projections.values()),
            "buffer_remaining": self.total_budget - sum(day["total"] for day in projections.values()),
            "cost_breakdown": {
                "compute_instances": config.estimated_monthly_cost * (requirements.demo_duration_days / 30.0),
                "bandwidth": config.estimated_bandwidth_cost * (requirements.demo_duration_days / 30.0),
                "api_costs": 2.5 * requirements.demo_duration_days,
                "monitoring": 1.0 * requirements.demo_duration_days,
                "storage": 0.5 * requirements.demo_duration_days
            }
        }
    
    def _assess_deployment_risks(self, config: Optional[DeploymentConfiguration], 
                               requirements: DemoRequirements) -> Dict[str, Any]:
        """Assess risks in the deployment plan"""
        risks = []
        
        if not config:
            return {"risks": [{"severity": "HIGH", "risk": "No viable configuration within budget"}]}
        
        # Budget risk
        total_projected_cost = config.estimated_monthly_cost * (requirements.demo_duration_days / 30.0)
        if total_projected_cost > self.total_budget * 0.8:
            risks.append({
                "severity": "MEDIUM",
                "risk": "High budget utilization - limited buffer for overruns",
                "mitigation": "Implement strict cost monitoring and auto-shutdown"
            })
        
        # Single point of failure risk
        if config.total_instances == 1:
            risks.append({
                "severity": "MEDIUM", 
                "risk": "Single instance deployment - no redundancy",
                "mitigation": "Implement automated backups and rapid redeployment"
            })
        
        # Provider dependency risk
        providers = set(inst.provider for inst in config.instance_specs)
        if len(providers) == 1:
            risks.append({
                "severity": "LOW",
                "risk": "Single cloud provider dependency",
                "mitigation": "Prepare backup deployment on alternative provider"
            })
        
        # Performance risk
        total_gpus = sum(inst.gpu_count for inst in config.instance_specs)
        if total_gpus == 0 and "consciousness_cascades" in requirements.required_systems:
            risks.append({
                "severity": "HIGH",
                "risk": "No GPU instances for consciousness processing",
                "mitigation": "Add GPU instance or reduce consciousness requirements"
            })
        
        return {
            "risks": risks,
            "overall_risk_level": "HIGH" if any(r["severity"] == "HIGH" for r in risks) else
                                 "MEDIUM" if any(r["severity"] == "MEDIUM" for r in risks) else "LOW"
        }
    
    def _create_funding_justification(self, config: Optional[DeploymentConfiguration], 
                                    requirements: DemoRequirements) -> Dict[str, Any]:
        """Create funding justification document"""
        if not config:
            return {}
        
        # Calculate ROI metrics
        demo_cost = config.estimated_monthly_cost * (requirements.demo_duration_days / 30.0)
        
        return {
            "investment_summary": {
                "total_investment": self.total_budget,
                "demo_cost": demo_cost,
                "cost_per_consciousness_event": demo_cost / (requirements.min_consciousness_events_per_hour * 24 * requirements.demo_duration_days),
                "cost_per_user_hour": demo_cost / (requirements.concurrent_users * 24 * requirements.demo_duration_days)
            },
            "value_propositions": [
                "First working demonstration of computational consciousness",
                "Scalable AI architecture with real-world applications",
                "Open-source implementation for community development",
                "Measurable consciousness emergence with quantitative metrics",
                "Multi-system integration proving collective intelligence"
            ],
            "technical_achievements": [
                f"Deploy {config.total_instances} instance cluster running 6 enhanced systems",
                f"Process {requirements.min_consciousness_events_per_hour * 24 * requirements.demo_duration_days} consciousness events",
                f"Support {requirements.concurrent_users} concurrent users",
                f"Achieve {requirements.uptime_requirement}% uptime reliability",
                f"Demonstrate {len(requirements.required_systems)} integrated AI systems"
            ],
            "market_potential": {
                "healthcare_ai": "Conscious AI for patient care and medical decision-making",
                "educational_systems": "Adaptive learning platforms with genuine understanding",
                "scientific_research": "AI collaborators for breakthrough discoveries",
                "creative_industries": "Conscious creative AI for art, music, and design",
                "enterprise_decision_making": "Ethical AI advisors for corporate governance"
            },
            "next_funding_targets": {
                "seed_round": "$100,000 - Scale to 1000+ agent network",
                "series_a": "$1,000,000 - Multi-datacenter consciousness network",
                "series_b": "$10,000,000 - Global consciousness infrastructure"
            }
        }

# Example usage and testing
async def test_deployment_planner():
    """Test the deployment planning system"""
    print("💰 Testing Cloud Deployment Budget Planner")
    
    planner = DeploymentPlanner(total_budget=1500.0)
    
    try:
        # Test different demo types
        demo_types = ["minimal", "standard", "comprehensive"]
        
        for demo_type in demo_types:
            print(f"\n📊 Planning {demo_type} demo deployment...")
            
            plan = await planner.create_deployment_plan(demo_type)
            
            if plan["recommended_configuration"]:
                config = plan["recommended_configuration"]
                print(f"✅ {demo_type.title()} Demo Plan:")
                print(f"   • Strategy: {config['strategy']}")
                print(f"   • Instances: {config['total_instances']}")
                print(f"   • Monthly Cost: ${config['estimated_monthly_cost']:.2f}")
                print(f"   • Setup Cost: ${config['estimated_setup_cost']:.2f}")
                
                # Show provider breakdown
                providers = {}
                for inst in config['instance_specs']:
                    provider = inst['provider']
                    if provider not in providers:
                        providers[provider] = {"count": 0, "cost": 0}
                    providers[provider]["count"] += 1
                    providers[provider]["cost"] += inst['monthly_cost']
                
                print(f"   • Providers: {', '.join(f'{p}({v['count']})' for p, v in providers.items())}")
                
                # Show budget utilization
                budget_util = plan["cost_projections"]["total_demo_cost"] / 1500.0 * 100
                print(f"   • Budget Utilization: {budget_util:.1f}%")
                
                # Show risk level
                risk_level = plan["risk_assessment"]["overall_risk_level"]
                print(f"   • Risk Level: {risk_level}")
                
            else:
                print(f"❌ No viable configuration found for {demo_type} demo")
        
        # Test cost monitoring
        print(f"\n💸 Testing cost monitoring...")
        monitor = CostMonitor(1500.0)
        
        # Simulate daily costs
        for day in range(1, 31):
            daily_cost = 35.0 + (day * 0.5)  # Increasing costs
            monitor.record_daily_cost(daily_cost)
        
        summary = monitor.get_cost_summary()
        print(f"✅ Cost Monitor Summary:")
        print(f"   • Current Spend: ${summary['current_spend']:.2f}")
        print(f"   • Budget Used: {summary['spend_percentage']:.1f}%")
        print(f"   • Daily Burn Rate: ${summary['daily_burn_rate']:.2f}")
        print(f"   • Runway: {summary['estimated_runway_days']} days")
        print(f"   • Active Alerts: {summary['active_alerts']}")
        
        print("\n💰 Budget Planner Test Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_deployment_planner())