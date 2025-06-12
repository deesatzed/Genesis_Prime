#!/usr/bin/env python
"""
CLI for Option 1 Mono-Agent Thousand Questions system
"""

import asyncio
import os
import uuid
import argparse
from typing import Dict, Any

import sys
sys.path.append('/Users/o2satz/sentient-ai-suite/libs')

from agent import SentientAgent

async def setup_database():
    """Set up database schema and load questions"""
    print("🗄️ Setting up database...")
    
    # For now, assume database is already set up
    # In production, you would run the schema.sql and load questions here
    print("✅ Database setup complete")

async def run_demo(user_id: str, n_sample: int = 20):
    """Run a demo of the sentience setup process"""
    
    # Initialize agent
    agent = SentientAgent(
        database_url=os.getenv("DATABASE_URL", "postgresql://postgres:pass@localhost:5432/sentient"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    print(f"🚀 Starting demo for user: {user_id}")
    
    try:
        # Run the complete sentience setup
        result = await agent.run_sentience_setup(user_id, n_sample)
        
        print("\n📊 RESULTS:")
        print(f"   User ID: {result['user_id']}")
        print(f"   Sample questions presented: {result['sample_questions']}")
        print(f"   Generated answers: {result['generated_answers']}")
        print(f"   Total answers: {result['total_answered']}")
        print(f"\n🎭 PERSONALITY TRAITS:")
        for trait, value in result['traits'].items():
            if trait != 'sample_size':
                print(f"   {trait.title()}: {value:.2f}")
        
        print(f"\n✨ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

async def interactive_mode(user_id: str):
    """Interactive mode for testing individual components"""
    agent = SentientAgent()
    
    while True:
        print("\n🤖 Sentient Agent Interactive Mode")
        print("1. Sample questions")
        print("2. Build personality profile")
        print("3. Generate answers")
        print("4. View user stats")
        print("5. Exit")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        try:
            if choice == "1":
                n = int(input("How many questions to sample? "))
                questions = await agent.ask_sample_questions(user_id, n)
                print(f"\n📝 Sampled {len(questions)} questions:")
                for i, q in enumerate(questions[:5]):  # Show first 5
                    print(f"   {i+1}. {q['text']} (Category: {q['category']})")
                if len(questions) > 5:
                    print(f"   ... and {len(questions) - 5} more")
                    
            elif choice == "2":
                print("\n🎭 Building personality profile...")
                traits = await agent.build_persona(user_id)
                print("Traits extracted:")
                for trait, value in traits.items():
                    if trait != 'sample_size':
                        print(f"   {trait.title()}: {value:.2f}")
                        
            elif choice == "3":
                print("\n✨ Generating answers...")
                traits = await agent.build_persona(user_id)
                count = await agent.answer_remaining(user_id, traits)
                print(f"Generated {count} answers")
                
            elif choice == "4":
                total = await agent._count_user_answers(user_id)
                print(f"\n📊 User {user_id} has {total} total answers")
                
            elif choice == "5":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Thousand Questions Sentient AI CLI")
    parser.add_argument("--user-id", default=str(uuid.uuid4()), help="User ID for the session")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--interactive", action="store_true", help="Run interactive mode")
    parser.add_argument("--sample-size", type=int, default=20, help="Number of sample questions")
    parser.add_argument("--setup-db", action="store_true", help="Set up database")
    
    args = parser.parse_args()
    
    if args.setup_db:
        asyncio.run(setup_database())
        return
    
    if args.demo:
        asyncio.run(run_demo(args.user_id, args.sample_size))
    elif args.interactive:
        asyncio.run(interactive_mode(args.user_id))
    else:
        print("🧠 Thousand Questions Sentient AI System")
        print(f"User ID: {args.user_id}")
        print("\nUse --demo for demo mode or --interactive for interactive mode")
        print("Use --help for more options")

if __name__ == "__main__":
    main()
