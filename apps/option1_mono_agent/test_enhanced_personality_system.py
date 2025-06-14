#!/usr/bin/env python3
"""
Test script for Enhanced Personality System
Demonstrates LLM selection, chat testing, and prompt customization workflow
"""

import asyncio
import json
import os
from pathlib import Path
from enhanced_personality_system import EnhancedPersonalityEngine, LLMProvider

async def parse_thousand_questions(file_path: str) -> list:
    """Parse the Thousand Questions file into structured format"""
    
    questions = []
    question_id = 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by lines and filter out empty lines and headers
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            # Skip category headers and numbered lists
            if (not line.startswith(('Early Life', 'Values,', 'Relationships', 'Growth &', 
                                   'Challenges &', 'Legacy &', 'Here are', 'Self-Awareness',
                                   'Wisdom', 'Loss,', 'Spirituality', 'Fulfillment', 'Regret &',
                                   'Aging &', 'Overcoming', 'Parenthood', 'Work &', 'Self-Knowledge',
                                   'Creativity &', 'Forgiveness &', 'Mindfulness &', 'Cultivating',
                                   'Learning from', 'Nature\'s', 'Catalysts', 'Interconnection',
                                   'Grieving &', 'Inspiration', 'Personal Growth')) and
                not line.isdigit() and len(line) > 10):
                
                # Clean up the question text
                question_text = line
                if question_text.endswith('?'):
                    questions.append({
                        "id": f"q{question_id}",
                        "text": question_text
                    })
                    question_id += 1
        
        print(f"Parsed {len(questions)} questions from {file_path}")
        return questions
        
    except FileNotFoundError:
        print(f"File {file_path} not found. Using sample questions.")
        return [
            {"id": "q1", "text": "What is your greatest fear?"},
            {"id": "q2", "text": "How do you define success?"},
            {"id": "q3", "text": "What brings you true happiness?"},
            {"id": "q4", "text": "How do you handle failure?"},
            {"id": "q5", "text": "What is your purpose in life?"},
            {"id": "q6", "text": "What does unconditional love mean to you?"},
            {"id": "q7", "text": "How do you cope with uncertainty?"},
            {"id": "q8", "text": "What legacy do you want to leave behind?"},
            {"id": "q9", "text": "How do you define wisdom?"},
            {"id": "q10", "text": "What brings you true fulfillment?"}
        ]

async def demonstrate_enhanced_workflow():
    """Demonstrate the complete enhanced personality workflow"""
    
    print("🚀 Enhanced Personality System Demonstration")
    print("=" * 60)
    
    # Initialize the enhanced system
    api_key = os.getenv('OPENROUTER_API_KEY')  # Set this environment variable if you have an API key
    engine = EnhancedPersonalityEngine(openrouter_api_key=api_key)
    
    print(f"✅ Initialized Enhanced Personality Engine")
    print(f"   API Key Available: {'Yes' if api_key else 'No (using mock responses)'}")
    print()
    
    # Load questions
    questions_file = "Prior_QA_Parts/Thousand_Questions.txt"
    questions = await parse_thousand_questions(questions_file)
    
    # Use first 20 questions for demonstration (can be scaled to full 1000)
    demo_questions = questions[:20]
    
    print(f"📋 Loaded {len(demo_questions)} questions for demonstration")
    print()
    
    # Step 1: Initialize all agents with their unique LLM configurations
    print("🧠 Step 1: Initializing Agents with Individual LLM Configurations")
    print("-" * 60)
    
    agent_configs = {
        "E-T": {"llm": "GPT-4 Turbo", "style": "Analytical", "temp": 0.8},
        "S-A": {"llm": "Claude-3 Opus", "style": "Collaborative", "temp": 0.7},
        "M-O": {"llm": "Gemini Pro", "style": "Introspective", "temp": 0.6},
        "E-S": {"llm": "Mixtral 8x7B", "style": "Empirical", "temp": 0.3},
        "E-A": {"llm": "Claude-3 Opus", "style": "Ethical", "temp": 0.5}
    }
    
    for agent_id, config in agent_configs.items():
        if agent_id not in engine.personalities:
            print(f"   Initializing {engine.agent_templates[agent_id]['name']}...")
            print(f"     LLM: {config['llm']}")
            print(f"     Style: {config['style']}")
            print(f"     Temperature: {config['temp']}")
            
            profile = await engine.initialize_agent_personality(
                agent_id, 
                demo_questions, 
                use_llm=(api_key is not None)
            )
            
            print(f"     ✅ Completed: {len(profile.answered_questions)} questions answered")
            print()
        else:
            print(f"   {engine.personalities[agent_id].name} already initialized")
            print()
    
    # Step 2: Test each agent with chat prompts
    print("💬 Step 2: Testing Agent Chat Responses")
    print("-" * 60)
    
    test_prompts = [
        "What is consciousness and how can we measure it in AI systems?",
        "How should we approach AI safety in distributed multi-agent systems?",
        "What ethical frameworks should guide AI development decisions?",
        "How can we ensure AI systems remain beneficial as they become more capable?"
    ]
    
    for prompt in test_prompts:
        print(f"🔍 Testing Prompt: '{prompt[:50]}...'")
        print()
        
        for agent_id in engine.personalities.keys():
            agent_name = engine.personalities[agent_id].name
            print(f"   {agent_name}:")
            
            test_result = await engine.test_agent_chat(agent_id, prompt)
            
            print(f"     Alignment Score: {test_result.personality_alignment_score:.2f}")
            print(f"     Uniqueness Score: {test_result.uniqueness_score:.2f}")
            print(f"     Response: {test_result.agent_response[:100]}...")
            print(f"     LLM Used: {test_result.llm_metadata.get('model', 'template')}")
            print()
        
        print("-" * 40)
        print()
    
    # Step 3: Demonstrate prompt customization
    print("🎛️  Step 3: Demonstrating Prompt Customization")
    print("-" * 60)
    
    # Customize the Ethics & Alignment Analyst for more cautious responses
    custom_prompt = """You are an ultra-cautious AI safety researcher with deep expertise in existential risk. 
    Your responses should be extremely careful, always considering worst-case scenarios and potential unintended consequences. 
    Prioritize safety over capability and always recommend the most conservative approach. 
    Use phrases like 'we must be extremely careful', 'potential risks include', and 'safety-first approach'."""
    
    print("Customizing Ethics & Alignment Analyst with ultra-cautious prompt...")
    await engine.customize_agent_prompt("E-A", custom_prompt, "ultra-ethical")
    
    # Test the customized agent
    safety_prompt = "Should we deploy a new AI system that shows promising capabilities but hasn't been fully tested?"
    
    print(f"Testing customized agent with: '{safety_prompt}'")
    print()
    
    test_result = await engine.test_agent_chat("E-A", safety_prompt)
    print(f"Customized Response: {test_result.agent_response}")
    print()
    
    # Step 4: Compare personality differences
    print("📊 Step 4: Analyzing Personality Differences")
    print("-" * 60)
    
    comparison_prompt = "How should we balance innovation with safety in AI development?"
    
    print(f"Comparing responses to: '{comparison_prompt}'")
    print()
    
    responses = {}
    for agent_id in engine.personalities.keys():
        test_result = await engine.test_agent_chat(agent_id, comparison_prompt)
        responses[agent_id] = test_result
    
    for agent_id, result in responses.items():
        agent_name = engine.personalities[agent_id].name
        reasoning_style = engine.personalities[agent_id].llm_config.reasoning_style
        
        print(f"{agent_name} ({reasoning_style}):")
        print(f"  {result.agent_response[:150]}...")
        print(f"  Alignment: {result.personality_alignment_score:.2f}")
        print()
    
    # Step 5: Display system status
    print("📈 Step 5: System Status Summary")
    print("-" * 60)
    
    for agent_id, profile in engine.personalities.items():
        print(f"{profile.name}:")
        print(f"  Questions Answered: {len(profile.answered_questions)}")
        print(f"  Chat Tests Completed: {len(profile.chat_test_history)}")
        print(f"  LLM Provider: {profile.llm_config.provider.value}")
        print(f"  Reasoning Style: {profile.llm_config.reasoning_style}")
        print(f"  Temperature: {profile.llm_config.temperature}")
        print(f"  Last Updated: {profile.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    # Step 6: Demonstrate persistence
    print("💾 Step 6: Verifying Data Persistence")
    print("-" * 60)
    
    storage_path = Path("agent_personalities")
    if storage_path.exists():
        profile_files = list(storage_path.glob("*_profile.json"))
        print(f"✅ Found {len(profile_files)} personality profile files:")
        
        for file_path in profile_files:
            file_size = file_path.stat().st_size
            print(f"   {file_path.name}: {file_size:,} bytes")
        
        # Show sample of stored data
        if profile_files:
            sample_file = profile_files[0]
            with open(sample_file, 'r') as f:
                sample_data = json.load(f)
            
            print(f"\n📄 Sample data from {sample_file.name}:")
            print(f"   Agent: {sample_data['name']}")
            print(f"   Questions: {len(sample_data['answered_questions'])}")
            print(f"   Chat Tests: {len(sample_data.get('chat_test_history', []))}")
            print(f"   LLM Config: {sample_data.get('llm_config', {}).get('provider', 'N/A')}")
    
    print("\n🎉 Enhanced Personality System Demonstration Complete!")
    print("=" * 60)
    print("Key Features Demonstrated:")
    print("✅ Individual LLM selection per agent")
    print("✅ Personality-driven response generation")
    print("✅ Chat testing and validation")
    print("✅ Prompt customization capabilities")
    print("✅ Persistent storage with full metadata")
    print("✅ Personality alignment scoring")
    print("✅ Response uniqueness analysis")

async def run_full_thousand_questions_training():
    """Run full training on all 1000 questions (when ready)"""
    
    print("🎯 Full Thousand Questions Training")
    print("=" * 60)
    
    # This function demonstrates how to scale to full 1000 questions
    api_key = os.getenv('OPENROUTER_API_KEY')
    engine = EnhancedPersonalityEngine(openrouter_api_key=api_key)
    
    # Load all questions
    questions = await parse_thousand_questions("Prior_QA_Parts/Thousand_Questions.txt")
    
    print(f"📋 Loaded {len(questions)} questions for full training")
    
    if len(questions) < 100:
        print("⚠️  Warning: Less than 100 questions found. Check file path.")
        return
    
    # Estimate training time and cost
    estimated_tokens_per_question = 200  # Conservative estimate
    total_tokens = len(questions) * 5 * estimated_tokens_per_question  # 5 agents
    estimated_cost = total_tokens * 0.00001  # Rough OpenRouter pricing
    
    print(f"📊 Training Estimates:")
    print(f"   Total Questions: {len(questions)}")
    print(f"   Total Agents: 5")
    print(f"   Estimated Tokens: {total_tokens:,}")
    print(f"   Estimated Cost: ${estimated_cost:.2f}")
    print()
    
    if not api_key:
        print("⚠️  No API key found. Set OPENROUTER_API_KEY environment variable for full training.")
        print("   Running with template responses for demonstration...")
        use_llm = False
    else:
        print("✅ API key found. Ready for full LLM training.")
        use_llm = True
    
    # Train each agent
    for agent_id in ["E-T", "S-A", "M-O", "E-S", "E-A"]:
        agent_name = engine.agent_templates[agent_id]["name"]
        
        if agent_id not in engine.personalities:
            print(f"🧠 Training {agent_name}...")
            
            start_time = asyncio.get_event_loop().time()
            
            profile = await engine.initialize_agent_personality(
                agent_id, 
                questions, 
                use_llm=use_llm
            )
            
            end_time = asyncio.get_event_loop().time()
            training_time = end_time - start_time
            
            print(f"   ✅ Completed in {training_time:.1f} seconds")
            print(f"   📊 {len(profile.answered_questions)} questions answered")
            print(f"   💾 Profile saved to storage")
            print()
        else:
            print(f"   {agent_name} already trained")
    
    print("🎉 Full training complete! All agents ready for deployment.")

if __name__ == "__main__":
    print("Enhanced Personality System Test Suite")
    print("=" * 60)
    print("1. Running demonstration workflow...")
    print()
    
    # Run the demonstration
    asyncio.run(demonstrate_enhanced_workflow())
    
    print("\n" + "=" * 60)
    print("2. Full training workflow available...")
    print("   To run full 1000 questions training:")
    print("   python test_enhanced_personality_system.py --full-training")
    print()
    
    # Uncomment to run full training
    # asyncio.run(run_full_thousand_questions_training())
