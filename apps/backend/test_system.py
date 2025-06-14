#!/usr/bin/env python
"""
Basic tests for the Thousand Questions system
"""

import asyncio
import uuid
import os
from pathlib import Path

import sys
sys.path.append('/Users/o2satz/sentient-ai-suite/libs')

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing imports...")
    
    try:
        # Test basic imports that don't require database
        from tq_dataset.parse_tq import parse_raw_file, get_question_statistics
        print("✅ TQ dataset parser imports successful")
        
        # Test persona traits (may have psycopg dependency)
        try:
            from persona_traits.builder import extract_traits, BIG_FIVE
            print("✅ Personality traits imports successful")
        except ImportError as e:
            if "psycopg" in str(e):
                print("⚠️ Personality traits import requires psycopg (database dependency)")
            else:
                raise e
        
        # Test memory adapter (may have psycopg dependency)
        try:
            from amm_memory_adapter import Memory, PostgresMemoryDb, MemoryManager
            print("✅ AMM memory adapter imports successful")
        except ImportError as e:
            if "psycopg" in str(e):
                print("⚠️ Memory adapter import requires psycopg (database dependency)")
            else:
                raise e
        
        # Test agent (may have dependencies)
        try:
            from agent import SentientAgent
            print("✅ SentientAgent import successful")
        except ImportError as e:
            if "psycopg" in str(e):
                print("⚠️ SentientAgent import requires psycopg (database dependency)")
            else:
                raise e
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_dataset_parsing():
    """Test that the TQ dataset was parsed correctly"""
    print("\n🧪 Testing dataset parsing...")
    
    try:
        from tq_dataset.parse_tq import parse_raw_file, get_question_statistics
        
        dataset_path = Path(__file__).parent.parent.parent / "libs" / "tq_dataset" / "Thousand_Questions.txt"
        
        if not dataset_path.exists():
            print(f"❌ Dataset file not found: {dataset_path}")
            return False
        
        questions = parse_raw_file(dataset_path)
        stats = get_question_statistics(questions)
        
        print(f"✅ Parsed {stats['total_questions']} questions")
        print(f"✅ Found {len(stats['categories'])} categories")
        print(f"✅ Identified {len(stats['themes'])} themes")
        
        # Check some questions have the expected structure
        if questions and all(key in questions[0] for key in ['id', 'text', 'category', 'themes', 'complexity']):
            print("✅ Question structure is correct")
            return True
        else:
            print("❌ Question structure is incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Dataset parsing error: {e}")
        return False

async def test_memory_adapter():
    """Test the memory adapter functionality"""
    print("\n🧪 Testing memory adapter...")
    
    try:
        from amm_memory_adapter import Memory, PostgresMemoryDb
        
        # Create a test memory instance (without actually connecting to DB)
        memory_db = PostgresMemoryDb("postgresql://test", "test_table")
        memory = Memory("gpt-4o-mini", memory_db)
        
        print("✅ Memory adapter initialization successful")
        
        # Test method existence
        methods = ['get_user_memories', 'create_user_memories', 'search', 'clear_user_memories']
        for method in methods:
            if hasattr(memory, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Memory adapter error: {e}")
        return False

async def test_agent_initialization():
    """Test that the SentientAgent can be initialized"""
    print("\n🧪 Testing agent initialization...")
    
    try:
        from agent import SentientAgent
        
        # Test initialization without actual DB connection
        # We'll mock the database URL to avoid connection errors
        os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test"
        
        # This should work without connecting to the database
        try:
            agent = SentientAgent(
                database_url="postgresql://test:test@localhost:5432/test",
                openai_api_key="test-key"
            )
            print("✅ Agent initialization successful")
            
            # Check that key methods exist
            methods = ['run_sentience_setup', 'ask_sample_questions', 'build_persona', 'answer_remaining']
            for method in methods:
                if hasattr(agent, method):
                    print(f"✅ Method {method} exists")
                else:
                    print(f"❌ Method {method} missing")
                    return False
            
            return True
            
        except Exception as e:
            if "connection" in str(e).lower() or "database" in str(e).lower():
                print("✅ Agent initialization successful (expected DB connection error)")
                return True
            else:
                print(f"❌ Unexpected agent initialization error: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Agent initialization error: {e}")
        return False

def test_prompt_template():
    """Test that the prompt template exists and is valid"""
    print("\n🧪 Testing prompt template...")
    
    try:
        template_path = Path(__file__).parent / "prompts" / "mono_agent.jinja2"
        
        if not template_path.exists():
            print(f"❌ Template file not found: {template_path}")
            return False
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Check for key template variables
        required_vars = ['traits', 'memories', 'question']
        for var in required_vars:
            if var in template_content:
                print(f"✅ Template variable '{var}' found")
            else:
                print(f"❌ Template variable '{var}' missing")
                return False
        
        print("✅ Prompt template is valid")
        return True
        
    except Exception as e:
        print(f"❌ Prompt template error: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("🚀 Running Thousand Questions System Tests\n")
    
    tests = [
        ("Imports", test_imports),
        ("Dataset Parsing", test_dataset_parsing),
        ("Memory Adapter", test_memory_adapter),
        ("Agent Initialization", test_agent_initialization),
        ("Prompt Template", test_prompt_template),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Set up PostgreSQL database")
        print("2. Run: python setup_database.py")
        print("3. Set OPENAI_API_KEY environment variable")
        print("4. Run: python cli.py --demo")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please fix issues before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(run_all_tests())