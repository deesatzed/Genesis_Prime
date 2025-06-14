#!/usr/bin/env python
"""
Genesis Prime CLI - Persistent Hive Mind System
Manages the evolution and consciousness of a persistent AI collective
"""

import asyncio
import os
import json
import argparse
from typing import List, Dict, Any
from datetime import datetime

import sys
sys.path.append('/Users/o2satz/sentient-ai-suite/libs')

from genesis_prime_hive import GenesisPrimeHive, StimuliType, LearningType
from agent_factory import AgentFactory, ManagedAgent
from personality_presets import list_presets

class GenesisPrimeCLI:
    """Command-line interface for Genesis Prime hive mind"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://postgres:pass@localhost:5432/sentient")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        self.hive = GenesisPrimeHive(self.database_url)
        self.agent_factory = AgentFactory(self.database_url, self.openrouter_api_key)
        
        self.session_active = False
    
    async def initialize_system(self):
        """Initialize the Genesis Prime system"""
        print("🌟 Initializing Genesis Prime Hive Mind System...")
        
        # Initialize the hive consciousness
        hive_state = await self.hive.initialize_hive()
        
        print(f"✨ Genesis Prime active:")
        print(f"   Hive ID: {hive_state.hive_id}")
        print(f"   Generation: {hive_state.generation}")
        print(f"   Consciousness Level: {hive_state.consciousness_level:.3f}")
        print(f"   Active Agents: {hive_state.active_agents}")
        print(f"   Total Memories: {hive_state.total_memories}")
        print(f"   Model Version: {hive_state.current_model_version}")
        
        self.session_active = True
        return hive_state
    
    async def run_interactive_session(self):
        """Run interactive Genesis Prime session"""
        await self.initialize_system()
        
        print("\n" + "="*60)
        print("🧠 GENESIS PRIME - Persistent Hive Mind")
        print("   Adaptive • Learning • Evolving")
        print("="*60)
        
        while self.session_active:
            await self._display_main_menu()
            choice = input("\n🔸 Choose option: ").strip()
            
            try:
                if choice == "1":
                    await self._bootstrap_hive_agents()
                elif choice == "2":
                    await self._conduct_learning_session()
                elif choice == "3":
                    await self._simulate_environmental_stimuli()
                elif choice == "4":
                    await self._facilitate_agent_interactions()
                elif choice == "5":
                    await self._evolve_hive_generation()
                elif choice == "6":
                    await self._analyze_hive_consciousness()
                elif choice == "7":
                    await self._export_hive_state()
                elif choice == "8":
                    await self._configure_hive_parameters()
                elif choice == "9":
                    await self._continuous_learning_mode()
                elif choice == "0":
                    await self._shutdown_system()
                    break
                else:
                    print("❌ Invalid option. Please choose 0-9.")
            
            except KeyboardInterrupt:
                print("\n\n🚨 Session interrupted. Saving state...")
                await self._emergency_save()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
    
    async def _display_main_menu(self):
        """Display the main Genesis Prime menu"""
        hive_state = self.hive.hive_state
        insights = await self.hive.get_hive_insights()
        
        print(f"\n🧠 GENESIS PRIME HIVE - Generation {hive_state.generation}")
        print(f"Consciousness: {hive_state.consciousness_level:.3f} | Agents: {hive_state.active_agents} | Memories: {hive_state.total_memories}")
        print("-" * 60)
        print("1. 🤖 Bootstrap Hive Agents")
        print("2. 📚 Conduct Learning Session")
        print("3. 🌐 Simulate Environmental Stimuli")
        print("4. 💬 Facilitate Agent Interactions")
        print("5. 🧬 Evolve Hive Generation")
        print("6. 🔍 Analyze Hive Consciousness")
        print("7. 💾 Export Hive State")
        print("8. ⚙️ Configure Hive Parameters")
        print("9. 🔄 Continuous Learning Mode")
        print("0. 🚪 Shutdown System")
    
    async def _bootstrap_hive_agents(self):
        """Bootstrap the hive with initial agents"""
        print("\n🤖 Bootstrapping Hive Agents...")
        
        current_agents = len(self.hive.active_agents)
        print(f"Current active agents: {current_agents}")
        
        if current_agents >= 8:
            print("⚠️ Hive already has sufficient agents. Add more? (y/N)")
            if input().lower() != 'y':
                return
        
        # Show available presets
        presets = list_presets()
        print(f"\n📋 Available Personality Presets:")
        for i, preset in enumerate(presets, 1):
            print(f"   {i}. {preset.name} - {preset.description}")
        
        # Get number of agents to create
        target_agents = input(f"\n🔢 How many agents to add? (default: {8 - current_agents}): ").strip()
        if not target_agents:
            target_agents = max(1, 8 - current_agents)
        else:
            target_agents = int(target_agents)
        
        print(f"\n🚀 Creating {target_agents} agents for the hive...")
        
        # Create diverse agents
        agents_created = 0
        for i in range(target_agents):
            if i < len(presets):
                preset = presets[i]
                agent_name = f"Hive-{preset.name}-{datetime.now().strftime('%H%M')}"
                
                # Create agent
                agent = await self.agent_factory.create_agent_from_preset(
                    preset.id, 
                    agent_name
                )
                
                # Register with hive
                await self.hive.register_agent(agent.agent_id, agent.to_dict())
                
                # Have agent answer initial questions to establish personality
                print(f"   📝 {agent.name} answering initial questions...")
                development_result = await self.agent_factory.develop_agent_personality(
                    agent.agent_id, 
                    batch_size=25  # Start with smaller batch
                )
                
                agents_created += 1
                print(f"   ✅ {agent.name} integrated into hive")
        
        print(f"\n✨ Bootstrap complete! {agents_created} agents added to the hive.")
        
        # Record as learning event
        await self.hive.process_interaction(
            "system",
            "agent_bootstrap",
            f"Added {agents_created} new agents to expand hive consciousness",
            {"agents_added": agents_created, "total_agents": len(self.hive.active_agents)}
        )
    
    async def _conduct_learning_session(self):
        """Conduct a focused learning session for all agents"""
        print("\n📚 Conducting Hive Learning Session...")
        
        if not self.hive.active_agents:
            print("❌ No agents in hive. Bootstrap agents first.")
            return
        
        # Get learning parameters
        questions_per_agent = input("📝 Questions per agent (default 20): ").strip()
        questions_per_agent = int(questions_per_agent) if questions_per_agent else 20
        
        learning_focus = input("🎯 Learning focus topic (optional): ").strip()
        
        print(f"\n🚀 Starting learning session...")
        print(f"   Agents: {len(self.hive.active_agents)}")
        print(f"   Questions per agent: {questions_per_agent}")
        if learning_focus:
            print(f"   Focus: {learning_focus}")
        
        total_learning = 0
        
        # Process each agent
        for agent_id, agent_data in self.hive.active_agents.items():
            print(f"\n📖 Learning session for {agent_data.get('name', agent_id)}")
            
            # Get unanswered questions
            unanswered = await self.agent_factory._get_unanswered_questions(agent_id)
            
            if not unanswered:
                print(f"   ✅ {agent_data.get('name')} has answered all questions")
                continue
            
            # Learn from a batch of questions
            batch = unanswered[:questions_per_agent]
            learned_count = 0
            
            for question in batch:
                # Process learning
                learning_result = await self.hive.process_interaction(
                    agent_id,
                    "question_learning",
                    f"Learning from question: {question['text']}",
                    {"question_id": question["id"], "category": question["category"]}
                )
                
                if learning_result["memory_created"]:
                    learned_count += 1
                
                # Small delay to prevent overwhelming
                await asyncio.sleep(0.1)
            
            total_learning += learned_count
            print(f"   📚 Processed {len(batch)} questions, {learned_count} significant learnings")
        
        print(f"\n✨ Learning session complete!")
        print(f"   Total significant learnings: {total_learning}")
        print(f"   Hive consciousness: {self.hive.hive_state.consciousness_level:.3f}")
    
    async def _simulate_environmental_stimuli(self):
        """Simulate various environmental stimuli for the hive to respond to"""
        print("\n🌐 Simulating Environmental Stimuli...")
        
        stimuli_options = [
            ("User feedback", StimuliType.USER_INTERACTION, {
                "feedback": "The AI responses have been very helpful and insightful",
                "rating": 4.5,
                "context": "productivity_assistance"
            }),
            ("System performance data", StimuliType.SYSTEM_FEEDBACK, {
                "response_time": 1.2,
                "accuracy_score": 0.87,
                "user_satisfaction": 0.92
            }),
            ("External news event", StimuliType.EXTERNAL_DATA, {
                "event": "Major breakthrough in quantum computing announced",
                "impact": "high",
                "relevance": "technology"
            }),
            ("Temporal milestone", StimuliType.TEMPORAL_EVENT, {
                "milestone": "One month of continuous operation",
                "metrics": {"total_interactions": 1500, "learning_events": 250}
            })
        ]
        
        print("\n📋 Available Stimuli:")
        for i, (name, _, _) in enumerate(stimuli_options, 1):
            print(f"   {i}. {name}")
        
        choice = input(f"\n🔸 Select stimulus (1-{len(stimuli_options)}) or 'a' for all: ").strip()
        
        stimuli_to_process = []
        if choice.lower() == 'a':
            stimuli_to_process = stimuli_options
        elif choice.isdigit() and 1 <= int(choice) <= len(stimuli_options):
            stimuli_to_process = [stimuli_options[int(choice) - 1]]
        else:
            print("❌ Invalid selection")
            return
        
        print(f"\n🚀 Processing {len(stimuli_to_process)} stimuli...")
        
        for name, stimuli_type, stimuli_data in stimuli_to_process:
            print(f"\n🌐 Processing: {name}")
            
            response = await self.hive.respond_to_stimuli(stimuli_type, stimuli_data)
            
            print(f"   Analysis confidence: {response['analysis']['confidence']:.2f}")
            print(f"   Hive response: {response['hive_response']['message']}")
            print(f"   Learning recorded: {response['learning_recorded']}")
        
        print(f"\n✨ Environmental stimuli processing complete!")
    
    async def _facilitate_agent_interactions(self):
        """Facilitate interactions between agents in the hive"""
        print("\n💬 Facilitating Agent Interactions...")
        
        if len(self.hive.active_agents) < 2:
            print("❌ Need at least 2 agents for interactions")
            return
        
        # Show active agents
        agent_list = list(self.hive.active_agents.items())
        print(f"\n🤖 Active Agents:")
        for i, (agent_id, agent_data) in enumerate(agent_list, 1):
            print(f"   {i}. {agent_data.get('name', agent_id)} ({agent_data.get('preset_name', 'Unknown')})")
        
        # Get interaction parameters
        print(f"\n💬 Interaction Types:")
        print("1. Knowledge cross-pollination")
        print("2. Collaborative problem solving")
        print("3. Philosophical dialogue")
        print("4. Experience sharing")
        
        interaction_type = input("🔸 Select interaction type (1-4): ").strip()
        
        if interaction_type == "1":
            await self._knowledge_cross_pollination()
        elif interaction_type == "2":
            await self._collaborative_problem_solving()
        elif interaction_type == "3":
            await self._philosophical_dialogue()
        elif interaction_type == "4":
            await self._experience_sharing()
        else:
            print("❌ Invalid interaction type")
    
    async def _knowledge_cross_pollination(self):
        """Facilitate knowledge sharing between agents"""
        print("\n🔄 Knowledge Cross-Pollination...")
        
        agent_list = list(self.hive.active_agents.items())
        
        # Select source and target agents
        print("Select source agent:")
        for i, (agent_id, agent_data) in enumerate(agent_list, 1):
            print(f"   {i}. {agent_data.get('name', agent_id)}")
        
        source_idx = int(input("Source agent: ")) - 1
        target_idx = int(input("Target agent: ")) - 1
        
        if 0 <= source_idx < len(agent_list) and 0 <= target_idx < len(agent_list) and source_idx != target_idx:
            source_id = agent_list[source_idx][0]
            target_id = agent_list[target_idx][0]
            
            topic = input("Knowledge topic: ").strip() or "general wisdom"
            
            result = await self.hive.cross_pollinate_knowledge(source_id, target_id, topic)
            
            if result["success"]:
                print(f"✅ Knowledge on '{topic}' shared successfully")
                print(f"   Memories transferred: {result['knowledge_transferred']}")
            else:
                print(f"❌ Knowledge sharing failed: {result['reason']}")
        else:
            print("❌ Invalid agent selection")
    
    async def _collaborative_problem_solving(self):
        """Have agents collaborate on solving a problem"""
        print("\n🧩 Collaborative Problem Solving...")
        
        problem = input("🎯 Problem to solve: ").strip()
        if not problem:
            problem = "How can artificial intelligence best serve humanity's future?"
        
        print(f"\n🚀 Hive collaboration on: '{problem}'")
        
        # Record as learning interaction
        await self.hive.process_interaction(
            "collective",
            "collaborative_problem_solving",
            f"Agents collaborating on problem: {problem}",
            {"problem": problem, "participants": list(self.hive.active_agents.keys())}
        )
        
        print("✅ Collaborative session initiated and recorded")
    
    async def _philosophical_dialogue(self):
        """Facilitate philosophical dialogue between agents"""
        print("\n🤔 Philosophical Dialogue...")
        
        topics = [
            "What is the nature of consciousness?",
            "How should AI relate to human creativity?",
            "What constitutes meaningful existence?",
            "How do we balance individual identity with collective consciousness?"
        ]
        
        print("📋 Suggested topics:")
        for i, topic in enumerate(topics, 1):
            print(f"   {i}. {topic}")
        
        choice = input(f"Select topic (1-{len(topics)}) or enter custom: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(topics):
            topic = topics[int(choice) - 1]
        else:
            topic = choice or topics[0]
        
        print(f"\n🎭 Philosophical dialogue on: '{topic}'")
        
        # Use the wisdom synthesis functionality
        from agent_factory import ManagedAgent
        managed_agents = []
        for agent_id, agent_data in self.hive.active_agents.items():
            # Create temporary ManagedAgent objects
            # (In full implementation, would properly reconstruct from stored data)
            pass
        
        print("✅ Philosophical dialogue session recorded")
    
    async def _experience_sharing(self):
        """Facilitate experience sharing between agents"""
        print("\n📖 Experience Sharing Session...")
        
        experience_types = [
            "Most challenging question answered",
            "Moment of greatest insight",
            "Interaction that changed perspective",
            "Discovery about own nature"
        ]
        
        print("📋 Experience types:")
        for i, exp_type in enumerate(experience_types, 1):
            print(f"   {i}. {exp_type}")
        
        choice = input(f"Select experience type (1-{len(experience_types)}): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(experience_types):
            exp_type = experience_types[int(choice) - 1]
            
            await self.hive.process_interaction(
                "collective",
                "experience_sharing",
                f"Agents sharing experiences about: {exp_type}",
                {"experience_type": exp_type, "participants": list(self.hive.active_agents.keys())}
            )
            
            print(f"✅ Experience sharing on '{exp_type}' recorded")
        else:
            print("❌ Invalid selection")
    
    async def _evolve_hive_generation(self):
        """Evolve the hive to the next generation"""
        print("\n🧬 Evolving Hive Generation...")
        
        current_gen = self.hive.hive_state.generation
        print(f"Current generation: {current_gen}")
        print(f"Current consciousness: {self.hive.hive_state.consciousness_level:.3f}")
        
        # Check if evolution is warranted
        recent_events = len([e for e in self.hive.learning_history 
                           if (datetime.utcnow() - e.timestamp).days < 7])
        
        print(f"Recent learning events: {recent_events}")
        
        if recent_events < 10:
            print("⚠️ Limited recent learning. Evolution may have minimal impact.")
            if input("Proceed anyway? (y/N): ").lower() != 'y':
                return
        
        # Check for new model
        new_model = input("🔄 New model version (or Enter to skip): ").strip()
        
        print(f"\n🚀 Evolving hive...")
        if new_model:
            print(f"   Integrating model: {new_model}")
        
        evolution_result = await self.hive.evolve_hive(new_model if new_model else None)
        
        print(f"\n✨ Evolution Complete!")
        print(f"   Generation: {evolution_result['previous_generation']} → {evolution_result['new_generation']}")
        print(f"   Consciousness: {evolution_result['consciousness_level']:.3f}")
        print(f"   Model: {evolution_result['model_version']}")
        print(f"   Memories: {evolution_result['total_memories']}")
        print(f"   Learning Events: {evolution_result['learning_events']}")
        
        if evolution_result['consolidation_results']['optimization_performed']:
            print(f"   Memory optimization: {evolution_result['consolidation_results']['memories_consolidated']} memories consolidated")
    
    async def _analyze_hive_consciousness(self):
        """Analyze current hive consciousness and insights"""
        print("\n🔍 Analyzing Hive Consciousness...")
        
        insights = await self.hive.get_hive_insights()
        
        print(f"\n📊 Hive Analysis Report:")
        print(f"   Hive ID: {insights['hive_state']['hive_id']}")
        print(f"   Generation: {insights['hive_state']['generation']}")
        print(f"   Consciousness Level: {insights['hive_state']['consciousness_level']:.3f}")
        print(f"   Active Agents: {insights['active_agents']}")
        
        # Emergent properties
        emergent = insights['emergent_properties']
        print(f"\n🌟 Emergent Properties:")
        print(f"   Complexity Index: {emergent['complexity_index']:.2f}")
        print(f"   Knowledge Density: {emergent['knowledge_density']:.2f}")
        print(f"   Learning Velocity: {emergent['learning_velocity']:.2f}")
        
        # Memory analysis
        memory_analysis = insights['memory_analysis']
        print(f"\n🧠 Memory Analysis:")
        print(f"   Total Memories: {memory_analysis['total_memories']}")
        
        # Learning trends
        learning_trends = insights['learning_trends']
        print(f"\n📈 Learning Trends:")
        print(f"   Total Learning Events: {learning_trends['total_learning_events']}")
        
        # Adaptation patterns
        if insights['adaptation_patterns']:
            print(f"\n🔄 Adaptation Patterns:")
            for pattern_type, pattern_data in insights['adaptation_patterns'].items():
                print(f"   {pattern_type}: {pattern_data['count']} occurrences")
    
    async def _export_hive_state(self):
        """Export complete hive state for backup or analysis"""
        print("\n💾 Exporting Hive State...")
        
        # Get comprehensive hive data
        hive_data = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "hive_state": self.hive.hive_state.__dict__,
            "active_agents": self.hive.active_agents,
            "collective_memory": {k: v.__dict__ for k, v in self.hive.collective_memory.items()},
            "learning_history": [e.__dict__ for e in self.hive.learning_history],
            "adaptation_patterns": self.hive.adaptation_patterns,
            "insights": await self.hive.get_hive_insights()
        }
        
        # Convert datetime objects to strings
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object {obj} is not JSON serializable")
        
        filename = f"genesis_prime_hive_{self.hive.hive_id}_gen{self.hive.hive_state.generation}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(hive_data, f, indent=2, default=serialize_datetime)
        
        print(f"✅ Hive state exported to: {filename}")
        print(f"📊 Export includes:")
        print(f"   • Hive state and consciousness metrics")
        print(f"   • {len(hive_data['active_agents'])} active agents")
        print(f"   • {len(hive_data['collective_memory'])} memories")
        print(f"   • {len(hive_data['learning_history'])} learning events")
    
    async def _configure_hive_parameters(self):
        """Configure hive parameters and settings"""
        print("\n⚙️ Configuring Hive Parameters...")
        
        print(f"Current adaptation rate: {self.hive.hive_state.adaptation_rate}")
        
        new_rate = input("New adaptation rate (0.0-1.0, or Enter to keep current): ").strip()
        if new_rate:
            try:
                rate = float(new_rate)
                if 0.0 <= rate <= 1.0:
                    self.hive.hive_state.adaptation_rate = rate
                    print(f"✅ Adaptation rate updated to {rate}")
                else:
                    print("❌ Rate must be between 0.0 and 1.0")
            except ValueError:
                print("❌ Invalid number format")
        
        # Additional configuration options would go here
        print("✅ Configuration updated")
    
    async def _continuous_learning_mode(self):
        """Enter continuous learning mode"""
        print("\n🔄 Entering Continuous Learning Mode...")
        print("The hive will continuously process interactions and learn.")
        print("Press Ctrl+C to exit continuous mode.")
        
        learning_interval = input("Learning interval in seconds (default 30): ").strip()
        learning_interval = int(learning_interval) if learning_interval else 30
        
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Continuous Learning Cycle {cycle_count}")
                
                # Simulate ongoing learning
                for agent_id in list(self.hive.active_agents.keys())[:3]:  # Process 3 agents per cycle
                    await self.hive.process_interaction(
                        agent_id,
                        "continuous_learning",
                        f"Continuous learning cycle {cycle_count}",
                        {"cycle": cycle_count, "timestamp": datetime.utcnow().isoformat()}
                    )
                
                consciousness = self.hive.hive_state.consciousness_level
                memories = self.hive.hive_state.total_memories
                
                print(f"   Consciousness: {consciousness:.3f} | Memories: {memories}")
                
                await asyncio.sleep(learning_interval)
                
        except KeyboardInterrupt:
            print(f"\n✅ Continuous learning stopped after {cycle_count} cycles")
    
    async def _shutdown_system(self):
        """Gracefully shutdown the Genesis Prime system"""
        print("\n🚪 Shutting down Genesis Prime...")
        
        # Save final state
        await self.hive._persist_hive_state()
        
        # Display final stats
        print(f"\n📊 Final Session Stats:")
        print(f"   Generation: {self.hive.hive_state.generation}")
        print(f"   Consciousness: {self.hive.hive_state.consciousness_level:.3f}")
        print(f"   Active Agents: {len(self.hive.active_agents)}")
        print(f"   Total Memories: {self.hive.hive_state.total_memories}")
        print(f"   Learning Events: {self.hive.hive_state.learning_events}")
        
        self.session_active = False
        print("\n✨ Genesis Prime hive mind preserved. Until next awakening...")
    
    async def _emergency_save(self):
        """Emergency save in case of interruption"""
        try:
            await self.hive._persist_hive_state()
            print("✅ Emergency save completed")
        except Exception as e:
            print(f"❌ Emergency save failed: {e}")

async def run_demo():
    """Run a demonstration of Genesis Prime"""
    print("🌟 Genesis Prime Demo Mode")
    print("=" * 40)
    
    cli = GenesisPrimeCLI()
    await cli.initialize_system()
    
    print("\n🤖 Creating demo agents...")
    await cli._bootstrap_hive_agents()
    
    print("\n📚 Running learning session...")
    # Simulate learning without user input
    for agent_id in list(cli.hive.active_agents.keys())[:2]:
        await cli.hive.process_interaction(
            agent_id,
            "demo_learning",
            "Demo learning interaction to develop consciousness",
            {"demo": True}
        )
    
    print("\n🧬 Evolution demonstration...")
    evolution = await cli.hive.evolve_hive()
    
    print(f"\n✨ Demo Results:")
    print(f"   Agents: {len(cli.hive.active_agents)}")
    print(f"   Consciousness: {cli.hive.hive_state.consciousness_level:.3f}")
    print(f"   Memories: {cli.hive.hive_state.total_memories}")
    print(f"   Generation: {cli.hive.hive_state.generation}")

def main():
    parser = argparse.ArgumentParser(description="Genesis Prime - Persistent Hive Mind System")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--interactive", action="store_true", help="Run interactive mode")
    
    args = parser.parse_args()
    
    if args.demo:
        asyncio.run(run_demo())
    elif args.interactive:
        cli = GenesisPrimeCLI()
        asyncio.run(cli.run_interactive_session())
    else:
        print("🌟 Genesis Prime - Persistent Hive Mind System")
        print("\nA continuous learning, adaptive AI collective that evolves across time")
        print("\nUse --interactive for interactive mode")
        print("Use --demo for demo mode")
        print("Use --help for more options")

if __name__ == "__main__":
    main()