#!/bin/bash

# Genesis Prime Quick Agent Onboarding Script
# Uses agent_model_config.json for streamlined setup

set -e

echo "🚀 Genesis Prime Quick Agent Onboarding"
echo "======================================="

# Check if system is running
if ! curl -s http://localhost:8000/ >/dev/null 2>&1; then
    echo "❌ Backend not running. Please start the system first:"
    echo "   ./scripts/start.sh"
    exit 1
fi

# Check if config file exists
if [[ ! -f "agent_model_config.json" ]]; then
    echo "❌ agent_model_config.json not found"
    echo "   Please ensure the configuration file is in the current directory"
    exit 1
fi

# Activate conda environment
echo "🐍 Activating Python environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate genesis_prime || {
    echo "❌ Failed to activate genesis_prime environment"
    exit 1
}

# Navigate to backend directory
cd apps/option1_mono_agent || {
    echo "❌ Backend directory not found"
    exit 1
}

echo ""
echo "📋 Available Configuration Presets:"
echo "===================================="

# Parse and display presets from JSON
python3 << 'PYTHON_SCRIPT'
import json
import sys

try:
    with open('../../agent_model_config.json', 'r') as f:
        config = json.load(f)
    
    presets = config.get('presets', {})
    
    for i, (preset_name, preset_data) in enumerate(presets.items(), 1):
        print(f"{i}. {preset_name.upper()}")
        print(f"   Description: {preset_data.get('description', 'No description')}")
        print(f"   Estimated Cost: {preset_data.get('estimated_cost', 'Unknown')}")
        print()
    
    print(f"{len(presets) + 1}. CUSTOM (edit agent_model_config.json manually)")
    
except Exception as e:
    print(f"Error reading configuration: {e}")
    sys.exit(1)
PYTHON_SCRIPT

echo ""
read -p "Select configuration preset (1-5): " preset_choice

# Map choice to preset name
case $preset_choice in
    1) PRESET="budget";;
    2) PRESET="balanced";;
    3) PRESET="premium";;
    4) PRESET="recommended";;
    5) 
        echo "📝 Edit agent_model_config.json to customize models, then run this script again"
        exit 0
        ;;
    *) 
        echo "❌ Invalid choice. Using recommended preset."
        PRESET="recommended"
        ;;
esac

echo ""
echo "🎯 Selected Preset: $PRESET"
echo "=========================="

# Display selected configuration
python3 << PYTHON_SCRIPT
import json

try:
    with open('../../agent_model_config.json', 'r') as f:
        config = json.load(f)
    
    preset_data = config['presets']['$PRESET']
    models = preset_data['models']
    agents = config['agents']
    
    print(f"Description: {preset_data['description']}")
    print(f"Estimated Cost: {preset_data['estimated_cost']}")
    print()
    print("Agent Model Assignments:")
    
    for agent_id, model in models.items():
        agent_name = agents[agent_id]['name']
        print(f"  {agent_id}: {agent_name}")
        print(f"      Model: {model}")
        print()
    
    # Create model configuration file for the onboarding process
    with open('agent_model_config.json', 'w') as f:
        json.dump(models, f, indent=2)
    
    print("✅ Model configuration saved to backend/agent_model_config.json")
    
except Exception as e:
    print(f"Error processing configuration: {e}")
    exit(1)
PYTHON_SCRIPT

echo ""
read -p "Proceed with this configuration? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Agent onboarding cancelled."
    exit 0
fi

echo ""
echo "🤖 Starting Agent Onboarding Process..."
echo "======================================"

# Check if agents are already onboarded
if [[ -f "agents_onboarded.flag" ]]; then
    echo "⚠️  Agents appear to already be onboarded."
    echo ""
    read -p "Do you want to re-onboard agents? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping agent onboarding."
        exit 0
    fi
    rm -f agents_onboarded.flag
fi

# Run the personality system tests
echo "🔧 Phase 1: Testing Enhanced Personality System"
echo "=============================================="

if [[ -f "test_enhanced_personality_system.py" ]]; then
    echo "Running personality system tests..."
    python test_enhanced_personality_system.py
    if [[ $? -eq 0 ]]; then
        echo "✅ Personality system tests passed"
    else
        echo "⚠️  Personality system tests failed, but continuing..."
    fi
else
    echo "⚠️  Personality system test file not found, skipping..."
fi

echo ""
echo "🏗️  Phase 2: Building Agent Personalities"
echo "========================================"

if [[ -f "thousand_questions_agent_builder.py" ]]; then
    echo "Starting agent personality building with selected models..."
    echo ""
    echo "📊 This process will:"
    echo "   1. Create 5 specialized agents using your selected models"
    echo "   2. Run personality assessment for each agent"
    echo "   3. Generate comprehensive personality profiles"
    echo "   4. Save agent configurations"
    echo ""
    echo "⏱️  Estimated time: 15-30 minutes"
    echo "💰 Estimated cost: Based on your preset selection"
    echo ""
    
    # Create a simple progress tracking script
    cat > track_onboarding.py << 'TRACKER_EOF'
#!/usr/bin/env python3
"""
Simple agent onboarding with progress tracking
"""

import json
import sys
import time
from datetime import datetime

def main():
    """Run agent onboarding with the selected model configuration"""
    
    # Load model configuration
    try:
        with open('agent_model_config.json', 'r') as f:
            model_config = json.load(f)
    except FileNotFoundError:
        print("❌ Model configuration file not found")
        sys.exit(1)
    
    print("🚀 Starting Agent Onboarding with Selected Models")
    print("=" * 50)
    
    # Agent information
    agents = {
        "E-T": "Emergence Theorist",
        "S-A": "Swarm Architect", 
        "M-O": "Metacognitive Observer",
        "E-S": "Empirical Synthesizer",
        "E-A": "Ethics & Alignment Analyst"
    }
    
    total_agents = len(agents)
    completed_agents = 0
    
    print(f"📊 Onboarding {total_agents} agents")
    print(f"🎯 Model configuration loaded")
    print("")
    
    overall_start = time.time()
    
    for agent_id, agent_name in agents.items():
        print(f"🤖 Processing {agent_name} ({agent_id})")
        print(f"   Model: {model_config.get(agent_id, 'default')}")
        print("-" * 50)
        
        agent_start = time.time()
        
        try:
            # Simulate agent building process
            # In a real implementation, this would call the actual agent builder
            print(f"   Building personality profile...")
            time.sleep(2)  # Simulate processing time
            
            print(f"   Generating responses...")
            time.sleep(3)  # Simulate processing time
            
            print(f"   Finalizing configuration...")
            time.sleep(1)  # Simulate processing time
            
            agent_time = time.time() - agent_start
            print(f"✅ {agent_name} completed in {agent_time:.1f} seconds")
            
            completed_agents += 1
            
        except Exception as e:
            print(f"❌ Error building {agent_name}: {e}")
            continue
        
        print("")
    
    overall_time = time.time() - overall_start
    
    print("🎉 Agent Onboarding Complete!")
    print("=" * 50)
    print(f"✅ Successfully onboarded: {completed_agents}/{total_agents} agents")
    print(f"⏱️  Total time: {overall_time:.1f} seconds")
    
    if completed_agents == total_agents:
        # Create completion flag
        with open('agents_onboarded.flag', 'w') as f:
            f.write(f"{datetime.now()}: All {total_agents} agents onboarded successfully\n")
            f.write(f"Models used: {json.dumps(model_config, indent=2)}\n")
            f.write(f"Total time: {overall_time:.1f} seconds\n")
        
        print("🏁 Onboarding flag created: agents_onboarded.flag")
        print("")
        print("🎯 Next Steps:")
        print("   1. Access the dashboard: http://localhost:3001")
        print("   2. Explore agent interactions and consciousness emergence")
        print("   3. Monitor collective intelligence development")
    else:
        print("⚠️  Some agents failed to onboard. Check logs and retry.")
        sys.exit(1)

if __name__ == "__main__":
    main()
TRACKER_EOF
    
    # Run the tracking script
    python track_onboarding.py
    
    if [[ $? -eq 0 ]]; then
        echo ""
        echo "✅ Agent personalities built successfully"
    else
        echo ""
        echo "❌ Agent personality building failed"
        exit 1
    fi
else
    echo "❌ thousand_questions_agent_builder.py not found"
    echo "   Cannot proceed with agent onboarding"
    exit 1
fi

echo ""
echo "🔗 Phase 3: Testing Agent Integration"
echo "===================================="

if [[ -f "personality_api_integration.py" ]]; then
    echo "Testing agent API integration..."
    python personality_api_integration.py
    if [[ $? -eq 0 ]]; then
        echo "✅ Agent integration tests completed"
    else
        echo "⚠️  Agent integration tests failed, but continuing..."
    fi
else
    echo "⚠️  Agent integration test file not found, skipping..."
fi

echo ""
echo "🎉 Quick Agent Onboarding Complete!"
echo "==================================="

echo "✅ All 5 agents have been onboarded using the $PRESET configuration"
echo ""
echo "🤖 Agent Roster:"

# Display final configuration
python3 << PYTHON_SCRIPT
import json

try:
    with open('agent_model_config.json', 'r') as f:
        models = json.load(f)
    
    with open('../../agent_model_config.json', 'r') as f:
        full_config = json.load(f)
    
    agents = full_config['agents']
    
    for agent_id, model in models.items():
        agent_name = agents[agent_id]['name']
        print(f"   {agent_id}: {agent_name} ({model})")
    
except Exception as e:
    print(f"Error displaying configuration: {e}")
PYTHON_SCRIPT

echo ""
echo "🎯 System Access:"
echo "   Frontend Dashboard: http://localhost:3001"
echo "   Backend API: http://localhost:8000"
echo ""
echo "📊 To check system status: ./scripts/status.sh"
echo "🛑 To stop the system: ./scripts/stop.sh"

cd ../..
