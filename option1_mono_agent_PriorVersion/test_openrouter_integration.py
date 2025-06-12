#!/usr/bin/env python
"""
Test script to verify OpenRouter integration for Genesis Prime
"""

import os
import sys
import asyncio
from datetime import datetime

# Add the libs path for imports
sys.path.append('/Users/o2satz/sentient-ai-suite/libs')

def test_environment_variables():
    """Test that required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = [
        "OPENROUTER_API_KEY",
        "DATABASE_URL"
    ]
    
    optional_vars = [
        "OPENROUTER_SITE_URL",
        "OPENROUTER_SITE_NAME"
    ]
    
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
        else:
            print(f"   ✅ {var}: Set")
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"   ✅ {var}: {os.getenv(var)}")
        else:
            print(f"   ⚠️ {var}: Not set (using default)")
    
    if missing_required:
        print(f"   ❌ Missing required variables: {', '.join(missing_required)}")
        return False
    
    print("   ✅ Environment variables check passed")
    return True

async def test_openrouter_connection():
    """Test basic OpenRouter API connection"""
    print("\n🌐 Testing OpenRouter Connection...")
    
    try:
        import openai
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("   ❌ No OpenRouter API key found")
            return False
        
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:3000"),
                "X-Title": os.getenv("OPENROUTER_SITE_NAME", "Genesis Prime Test"),
            }
        )
        
        # Test simple completion
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello! Please respond with 'OpenRouter test successful'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"   ✅ OpenRouter API response: {result}")
        return True
        
    except Exception as e:
        print(f"   ❌ OpenRouter connection failed: {e}")
        return False

async def test_agent_creation():
    """Test creating a SentientAgent with OpenRouter"""
    print("\n🤖 Testing Agent Creation...")
    
    try:
        from agent import SentientAgent
        
        # Create agent with OpenRouter
        agent = SentientAgent(
            database_url=os.getenv("DATABASE_URL"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
        )
        
        print("   ✅ SentientAgent created successfully with OpenRouter")
        return True
        
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        return False

async def test_agent_factory():
    """Test creating AgentFactory with OpenRouter"""
    print("\n🏭 Testing Agent Factory...")
    
    try:
        from agent_factory import AgentFactory
        
        # Create factory with OpenRouter
        factory = AgentFactory(
            database_url=os.getenv("DATABASE_URL"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
        )
        
        print("   ✅ AgentFactory created successfully with OpenRouter")
        return True
        
    except Exception as e:
        print(f"   ❌ AgentFactory creation failed: {e}")
        return False

async def test_genesis_prime_cli():
    """Test Genesis Prime CLI initialization"""
    print("\n🧠 Testing Genesis Prime CLI...")
    
    try:
        from genesis_prime_cli import GenesisPrimeCLI
        
        # Set environment variables for test
        os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "test-key")
        os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
        
        cli = GenesisPrimeCLI()
        
        print("   ✅ Genesis Prime CLI initialized successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Genesis Prime CLI initialization failed: {e}")
        return False

async def main():
    """Run all OpenRouter integration tests"""
    print("🌟 OpenRouter Integration Test Suite")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Environment Variables", test_environment_variables()),
        ("OpenRouter Connection", test_openrouter_connection()),
        ("Agent Creation", test_agent_creation()),
        ("Agent Factory", test_agent_factory()),
        ("Genesis Prime CLI", test_genesis_prime_cli())
    ]
    
    results = []
    for name, test_coro in tests:
        if asyncio.iscoroutine(test_coro):
            result = await test_coro
        else:
            result = test_coro
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All OpenRouter integration tests PASSED!")
        print("Genesis Prime is ready to use with OpenRouter!")
    else:
        print("⚠️ Some tests failed. Please check configuration and environment.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)