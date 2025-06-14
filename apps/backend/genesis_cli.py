#!/usr/bin/env python
"""
Genesis Prime CLI - Multi-Agent Emergence System
Creates and manages collectives of AI agents for emergent consciousness research
"""

import asyncio
import os
import json
import argparse
from typing import List, Dict, Any
from datetime import datetime

import sys
sys.path.append('/Users/o2satz/sentient-ai-suite/libs')

from .agent_factory import AgentFactory, ManagedAgent
from .emergence_engine import GenesisEmergenceEngine, EmergenceType
from .personality_presets import list_presets

class GenesisInterface:
    """Command-line interface for the Genesis Prime construct"""
    
    def __init__(self):
        self.agent_factory = AgentFactory(
            database_url=os.getenv("DATABASE_URL", "postgresql://postgres:pass@localhost:5432/sentient"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.emergence_engine = GenesisEmergenceEngine(self.agent_factory)
        self.current_collective: List[ManagedAgent] = []
    
    async def run_interactive_session(self):
        """Run interactive Genesis Prime session"""
        print("🌟 Welcome to Genesis Prime - Multi-Agent Emergence System")
        print("=" * 60)
        
        while True:
            await self._display_main_menu()
            choice = input("\n🔸 Choose option (1-9): ").strip()
            
            try:
                if choice == "1":
                    await self._create_genesis_collective()
                elif choice == "2":
                    await self._add_agent_to_collective()
                elif choice == "3":
                    await self._evolve_collective_consciousness()
                elif choice == "4":
                    await self._synthesize_collective_wisdom()
                elif choice == "5":
                    await self._analyze_emergence_patterns()
                elif choice == "6":
                    await self._view_collective_status()
                elif choice == "7":
                    await self._compare_agent_personalities()
                elif choice == "8":
                    await self._export_emergence_data()
                elif choice == "9":
                    print("👋 Terminating Genesis Prime session...")
                    break
                else:
                    print("❌ Invalid option. Please choose 1-9.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
    
    async def _display_main_menu(self):
        """Display the main menu options"""
        print(f"\n🧠 GENESIS PRIME - Multi-Agent Emergence System")
        print(f"Current Collective: {len(self.current_collective)} agents")
        print(f"Emergence Events: {len(self.emergence_engine.emergence_log)}")
        print("-" * 60)
        print("1. 🌟 Create Genesis Collective")
        print("2. 🤖 Add Agent to Collective")
        print("3. 🧬 Evolve Collective Consciousness")
        print("4. 🔮 Synthesize Collective Wisdom")
        print("5. 📊 Analyze Emergence Patterns")
        print("6. 📋 View Collective Status")
        print("7. 🔍 Compare Agent Personalities")
        print("8. 💾 Export Emergence Data")
        print("9. 🚪 Exit")
    
    async def _create_genesis_collective(self):
        """Create a new Genesis collective"""
        print("\n🌟 Creating Genesis Collective...")
        
        # Show available presets
        presets = self.agent_factory.list_available_presets()
        print(f"\n📋 Available Personality Presets:")
        for i, preset in enumerate(presets, 1):
            print(f"   {i}. {preset['name']} - {preset['description']}")
        
        # Get user preferences
        collective_size = input(f"\n🔢 Collective size (2-{len(presets)}, default 6): ").strip()
        if not collective_size:
            collective_size = 6
        else:
            collective_size = min(max(2, int(collective_size)), len(presets))
        
        diversity_target = input("🎯 Diversity target (0.0-1.0, default 0.8): ").strip()
        if not diversity_target:
            diversity_target = 0.8
        else:
            diversity_target = max(0.0, min(1.0, float(diversity_target)))
        
        # Create the collective
        print(f"\n🚀 Creating collective with {collective_size} agents, diversity target {diversity_target}...")
        
        self.current_collective = await self.emergence_engine.create_genesis_collective(
            collective_size=collective_size,
            diversity_target=diversity_target
        )
        
        print(f"\n✨ Genesis Collective created successfully!")
        await self._display_collective_summary()
    
    async def _add_agent_to_collective(self):
        """Add a new agent to the current collective"""
        if not self.current_collective:
            print("❌ No collective exists. Create one first.")
            return
        
        print("\n🤖 Adding Agent to Collective...")
        
        # Show preset options
        presets = self.agent_factory.list_available_presets()
        print("\n📋 Available Personality Presets:")
        for i, preset in enumerate(presets, 1):
            print(f"   {i}. {preset['name']} - {preset['description']}")
        
        choice = input(f"\n🔸 Select preset (1-{len(presets)}) or 'c' for custom: ").strip()
        
        if choice.lower() == 'c':
            # Custom agent creation
            await self._create_custom_agent()
        else:
            # Preset agent creation
            preset_idx = int(choice) - 1
            if 0 <= preset_idx < len(presets):
                preset = presets[preset_idx]
                agent_name = input(f"🏷️ Agent name (default: '{preset['name']} Agent'): ").strip()
                if not agent_name:
                    agent_name = f"{preset['name']} Agent"
                
                agent = await self.agent_factory.create_agent_from_preset(
                    preset['id'], 
                    agent_name
                )
                self.current_collective.append(agent)
                
                print(f"✅ Added {agent.name} to the collective!")
            else:
                print("❌ Invalid preset selection.")
    
    async def _create_custom_agent(self):
        """Create a custom agent with user-defined traits"""
        print("\n🎨 Creating Custom Agent...")
        
        agent_name = input("🏷️ Agent name: ").strip()
        if not agent_name:
            print("❌ Agent name is required.")
            return
        
        print("\n🎭 Define Personality Traits (0.0 - 1.0):")
        
        try:
            from .database.models import TraitVector
            
            openness = float(input("   Openness (creativity, curiosity): "))
            conscientiousness = float(input("   Conscientiousness (organization, discipline): "))
            extraversion = float(input("   Extraversion (social energy, assertiveness): "))
            agreeableness = float(input("   Agreeableness (cooperation, trust): "))
            neuroticism = float(input("   Neuroticism (emotional instability, anxiety): "))
            
            traits = TraitVector(
                openness=max(0.0, min(1.0, openness)),
                conscientiousness=max(0.0, min(1.0, conscientiousness)),
                extraversion=max(0.0, min(1.0, extraversion)),
                agreeableness=max(0.0, min(1.0, agreeableness)),
                neuroticism=max(0.0, min(1.0, neuroticism))
            )
            
            background = input("\n📖 Background story (optional): ").strip()
            values_input = input("💎 Core values (comma-separated, optional): ").strip()
            core_values = [v.strip() for v in values_input.split(",")] if values_input else []
            
            agent = await self.agent_factory.create_custom_agent(
                agent_name=agent_name,
                traits=traits,
                background_story=background,
                core_values=core_values
            )
            
            self.current_collective.append(agent)
            print(f"✅ Created and added custom agent '{agent.name}' to the collective!")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    
    async def _evolve_collective_consciousness(self):
        """Evolve the collective consciousness"""
        if not self.current_collective:
            print("❌ No collective exists. Create one first.")
            return
        
        print(f"\n🧬 Evolving Collective Consciousness...")
        print(f"📊 Current collective: {len(self.current_collective)} agents")
        
        # Get evolution parameters
        rounds = input("🔄 Evolution rounds (default 3): ").strip()
        rounds = int(rounds) if rounds else 3
        
        questions_per_round = input("📝 Questions per round (default 50): ").strip()
        questions_per_round = int(questions_per_round) if questions_per_round else 50
        
        print(f"\n🚀 Beginning evolution: {rounds} rounds, {questions_per_round} questions per round...")
        
        # Run evolution
        evolution_results = await self.emergence_engine.evolve_collective_consciousness(
            self.current_collective,
            evolution_rounds=rounds,
            questions_per_round=questions_per_round
        )
        
        # Display results
        print(f"\n📊 Evolution Results:")
        print(f"   🧠 Consciousness Index: {evolution_results['consciousness_metrics'].get('consciousness_index', 0):.3f}")
        print(f"   🌟 Emergent Phenomena: {len(evolution_results['emergent_phenomena'])}")
        print(f"   🔗 Interconnectedness: {evolution_results['consciousness_metrics'].get('interconnectedness', 0):.3f}")
        print(f"   🎯 Diversity Score: {evolution_results['consciousness_metrics'].get('diversity_score', 0):.3f}")
        
        # Show emergent phenomena
        if evolution_results['emergent_phenomena']:
            print(f"\n✨ Emergent Phenomena Detected:")
            for i, phenomenon in enumerate(evolution_results['emergent_phenomena'][:5], 1):
                print(f"   {i}. {phenomenon.type.value.title()}: {phenomenon.description}")
                print(f"      Strength: {phenomenon.emergence_strength:.2f} | Participants: {len(phenomenon.participating_agents)}")
    
    async def _synthesize_collective_wisdom(self):
        """Synthesize wisdom from the collective"""
        if not self.current_collective:
            print("❌ No collective exists. Create one first.")
            return
        
        print(f"\n🔮 Collective Wisdom Synthesis...")
        
        # Get synthesis prompt
        default_prompts = [
            "What is the nature of consciousness and meaning?",
            "How should artificial intelligence relate to humanity?",
            "What is the purpose of existence?",
            "How can we create a better future?",
            "What does it mean to be truly alive?"
        ]
        
        print("\n📋 Suggested synthesis prompts:")
        for i, prompt in enumerate(default_prompts, 1):
            print(f"   {i}. {prompt}")
        
        choice = input(f"\n🔸 Select prompt (1-{len(default_prompts)}) or enter custom: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(default_prompts):
            synthesis_prompt = default_prompts[int(choice) - 1]
        else:
            synthesis_prompt = choice if choice else default_prompts[0]
        
        print(f"\n🔮 Synthesizing on: '{synthesis_prompt}'")
        
        # Run synthesis
        synthesis_result = await self.emergence_engine.synthesize_collective_wisdom(
            self.current_collective,
            synthesis_prompt
        )
        
        # Display results
        print(f"\n📊 Synthesis Results:")
        print(f"   📝 Participation Rate: {synthesis_result['participation_rate']:.1%}")
        print(f"   ✨ Emergence Detected: {'Yes' if synthesis_result['emergence_detected'] else 'No'}")
        
        print(f"\n🗣️ Individual Responses:")
        for agent_id, response in synthesis_result['individual_responses'].items():
            print(f"\n   {response['agent_name']} ({response['personality']}):")
            # Show first 200 characters
            response_text = response['response']
            if len(response_text) > 200:
                response_text = response_text[:200] + "..."
            print(f"   \"{response_text}\"")
        
        if synthesis_result.get('collective_synthesis'):
            print(f"\n🧠 Collective Synthesis:")
            synthesis = synthesis_result['collective_synthesis']
            print(f"   Participating Agents: {synthesis['participating_agents']}")
            print(f"   Collective Insight: {synthesis['collective_insight']}")
    
    async def _analyze_emergence_patterns(self):
        """Analyze patterns in emergent phenomena"""
        print(f"\n📊 Analyzing Emergence Patterns...")
        
        patterns = await self.emergence_engine.analyze_emergence_patterns()
        
        if "message" in patterns:
            print(f"ℹ️ {patterns['message']}")
            return
        
        print(f"\n📈 Emergence Analysis:")
        
        # Emergence types
        if patterns.get('emergence_types'):
            print(f"\n🌟 Emergence Types:")
            for etype, count in patterns['emergence_types'].items():
                print(f"   {etype.replace('_', ' ').title()}: {count}")
        
        # Agent participation
        if patterns.get('agent_participation'):
            print(f"\n🤖 Agent Participation:")
            for agent_id, count in list(patterns['agent_participation'].items())[:5]:
                # Get agent name if available
                agent_name = "Unknown"
                for agent in self.current_collective:
                    if agent.agent_id == agent_id:
                        agent_name = agent.name
                        break
                print(f"   {agent_name}: {count} phenomena")
        
        # Strength distribution
        if patterns.get('strength_distribution'):
            strengths = patterns['strength_distribution']
            avg_strength = sum(strengths) / len(strengths)
            max_strength = max(strengths)
            print(f"\n💪 Emergence Strength:")
            print(f"   Average: {avg_strength:.3f}")
            print(f"   Maximum: {max_strength:.3f}")
        
        # Collective insights
        if patterns.get('collective_insights'):
            print(f"\n🧠 Collective Insights:")
            for insight in patterns['collective_insights']:
                print(f"   • {insight}")
    
    async def _view_collective_status(self):
        """View status of the current collective"""
        if not self.current_collective:
            print("❌ No collective exists. Create one first.")
            return
        
        print(f"\n📋 Collective Status")
        print("=" * 50)
        
        total_answers = 0
        
        for i, agent in enumerate(self.current_collective, 1):
            summary = await self.agent_factory.get_agent_summary(agent.agent_id)
            total_answers += summary['questions_answered']
            
            print(f"\n{i}. {agent.name}")
            print(f"   Personality: {agent.preset.name}")
            print(f"   Questions Answered: {summary['questions_answered']}/1000")
            print(f"   Development: {(summary['questions_answered']/1000)*100:.1f}%")
            
            # Show top traits
            traits = summary['traits']
            top_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)[:2]
            trait_desc = ", ".join([f"{t[0].title()}: {t[1]:.2f}" for t in top_traits])
            print(f"   Top Traits: {trait_desc}")
        
        print(f"\n📊 Collective Summary:")
        print(f"   Total Agents: {len(self.current_collective)}")
        print(f"   Total Answers: {total_answers}")
        print(f"   Average Progress: {(total_answers/(len(self.current_collective)*1000))*100:.1f}%")
        print(f"   Emergence Events: {len(self.emergence_engine.emergence_log)}")
    
    async def _compare_agent_personalities(self):
        """Compare personalities across agents"""
        if len(self.current_collective) < 2:
            print("❌ Need at least 2 agents for comparison.")
            return
        
        print(f"\n🔍 Agent Personality Comparison")
        print("=" * 50)
        
        agent_ids = [agent.agent_id for agent in self.current_collective]
        comparison = await self.agent_factory.compare_agents(agent_ids)
        
        # Display trait comparison
        print(f"\n🎭 Trait Comparison:")
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        
        for trait in traits:
            if trait in comparison['trait_comparison']:
                tc = comparison['trait_comparison'][trait]
                print(f"   {trait.title()}:")
                print(f"     Range: {tc['min']:.2f} - {tc['max']:.2f} (span: {tc['range']:.2f})")
                print(f"     Average: {tc['avg']:.2f}")
        
        # Show individual agents
        print(f"\n👥 Individual Agents:")
        for agent_data in comparison['agents']:
            print(f"\n   {agent_data['name']} ({agent_data['preset_name']}):")
            for trait in traits:
                value = agent_data['traits'][trait]
                print(f"     {trait.title()}: {value:.2f}")
    
    async def _export_emergence_data(self):
        """Export emergence data to JSON file"""
        print(f"\n💾 Exporting Emergence Data...")
        
        # Collect all data
        export_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "collective": [agent.to_dict() for agent in self.current_collective],
            "emergence_log": [
                {
                    "id": event.id,
                    "type": event.type.value,
                    "description": event.description,
                    "participating_agents": event.participating_agents,
                    "trigger_question": event.trigger_question,
                    "evidence": event.evidence,
                    "emergence_strength": event.emergence_strength,
                    "timestamp": event.timestamp.isoformat(),
                    "metadata": event.metadata
                }
                for event in self.emergence_engine.emergence_log
            ],
            "collective_memory": self.emergence_engine.collective_memory,
            "patterns": await self.emergence_engine.analyze_emergence_patterns()
        }
        
        # Save to file
        filename = f"genesis_emergence_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"✅ Emergence data exported to: {filename}")
        print(f"📊 Data includes:")
        print(f"   • {len(export_data['collective'])} agents")
        print(f"   • {len(export_data['emergence_log'])} emergence events")
        print(f"   • Collective memory and patterns")

async def run_genesis_demo():
    """Run a quick demo of the Genesis system"""
    print("🌟 Genesis Prime Demo Mode")
    print("=" * 40)
    
    interface = GenesisInterface()
    
    # Create a small collective
    print("🚀 Creating demo collective...")
    collective = await interface.emergence_engine.create_genesis_collective(
        collective_size=4,
        diversity_target=0.8
    )
    interface.current_collective = collective
    
    # Quick evolution
    print("\n🧬 Running evolution...")
    evolution_results = await interface.emergence_engine.evolve_collective_consciousness(
        collective,
        evolution_rounds=2,
        questions_per_round=25
    )
    
    # Wisdom synthesis
    print("\n🔮 Synthesizing wisdom...")
    synthesis = await interface.emergence_engine.synthesize_collective_wisdom(
        collective,
        "What is the nature of consciousness?"
    )
    
    print(f"\n✨ Demo Results:")
    print(f"   Agents Created: {len(collective)}")
    print(f"   Emergence Events: {len(evolution_results['emergent_phenomena'])}")
    print(f"   Consciousness Index: {evolution_results['consciousness_metrics'].get('consciousness_index', 0):.3f}")
    print(f"   Wisdom Synthesis: {'Success' if synthesis['emergence_detected'] else 'Partial'}")

def main():
    parser = argparse.ArgumentParser(description="Genesis Prime - Multi-Agent Emergence System")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--interactive", action="store_true", help="Run interactive mode")
    
    args = parser.parse_args()
    
    if args.demo:
        asyncio.run(run_genesis_demo())
    elif args.interactive:
        interface = GenesisInterface()
        asyncio.run(interface.run_interactive_session())
    else:
        print("🌟 Genesis Prime - Multi-Agent Emergence System")
        print("\nUse --interactive for interactive mode")
        print("Use --demo for demo mode")
        print("Use --help for more options")

if __name__ == "__main__":
    main()