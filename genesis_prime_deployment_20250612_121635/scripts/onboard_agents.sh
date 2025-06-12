#!/bin/bash

# Genesis Prime Agent Onboarding Script
# Sets up the 5 core agents with model selection and progress tracking

set -e

echo "🤖 Genesis Prime Agent Onboarding"
echo "================================="

# Function to show progress bar
show_progress() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((current * width / total))
    local remaining=$((width - completed))
    
    printf "\r["
    printf "%*s" $completed | tr ' ' '='
    printf "%*s" $remaining | tr ' ' '-'
    printf "] %d%% (%d/%d)" $percentage $current $total
}

# Function to fetch current OpenRouter models
fetch_openrouter_models() {
    echo "🔍 Fetching current OpenRouter models..."
    
    # Try to fetch current models from OpenRouter API
    if command -v curl >/dev/null 2>&1; then
        MODELS_JSON=$(curl -s "https://openrouter.ai/api/v1/models" 2>/dev/null || echo "")
        if [[ -n "$MODELS_JSON" ]]; then
            echo "✅ Current models fetched from OpenRouter"
            return 0
        fi
    fi
    
    echo "⚠️  Using fallback model list (may not reflect current pricing)"
    return 1
}

# Function to display model costs
show_model_costs() {
    echo ""
    echo "💰 Popular OpenRouter Models (costs may vary - check openrouter.ai for current pricing):"
    echo "   1. openai/gpt-4o                               - Premium (Latest GPT-4)"
    echo "   2. anthropic/claude-3.5-sonnet                 - Premium (Latest Claude)"
    echo "   3. openai/gpt-4-turbo                          - Premium (GPT-4 Turbo)"
    echo "   4. anthropic/claude-3-haiku                    - Balanced (Fast Claude)"
    echo "   5. openai/gpt-3.5-turbo                        - Budget (Fast & cheap)"
    echo "   6. mistralai/mixtral-8x7b-instruct             - Budget (Open source)"
    echo "   7. meta-llama/llama-3-70b-instruct             - Budget (Meta's latest)"
    echo "   8. google/gemini-pro                           - Balanced (Google's model)"
    echo ""
    echo "📊 Estimated total cost for full onboarding (1000 questions × 5 agents):"
    echo "   - Budget option (Mixtral/Llama): $5-20"
    echo "   - Balanced option (GPT-3.5/Haiku): $15-50"
    echo "   - Premium option (GPT-4/Claude-3.5): $50-200"
    echo ""
    echo "💡 Tip: Check https://openrouter.ai/models for current pricing and availability"
    echo ""
}

# Function to select model for agent
select_agent_model() {
    local agent_id=$1
    local agent_name=$2
    
    echo ""
    echo "🤖 Configuring model for $agent_name ($agent_id)"
    echo "================================================"
    
    show_model_costs
    
    echo "Available models (select by number or enter custom OpenRouter model ID):"
    echo "1. openai/gpt-4o (Premium - Latest GPT-4)"
    echo "2. anthropic/claude-3.5-sonnet (Premium - Latest Claude)"
    echo "3. openai/gpt-4-turbo (Premium - GPT-4 Turbo)"
    echo "4. anthropic/claude-3-haiku (Balanced - Fast Claude)"
    echo "5. openai/gpt-3.5-turbo (Budget - Fast & cheap)"
    echo "6. mistralai/mixtral-8x7b-instruct (Budget - Open source)"
    echo "7. meta-llama/llama-3-70b-instruct (Budget - Meta's latest)"
    echo "8. google/gemini-pro (Balanced - Google's model)"
    echo "9. Use recommended model for this agent"
    echo "10. Enter custom OpenRouter model ID"
    echo ""
    
    while true; do
        read -p "Select model for $agent_name (1-10 or custom ID): " choice
        case $choice in
            1) echo "openai/gpt-4o"; break;;
            2) echo "anthropic/claude-3.5-sonnet"; break;;
            3) echo "openai/gpt-4-turbo"; break;;
            4) echo "anthropic/claude-3-haiku"; break;;
            5) echo "openai/gpt-3.5-turbo"; break;;
            6) echo "mistralai/mixtral-8x7b-instruct"; break;;
            7) echo "meta-llama/llama-3-70b-instruct"; break;;
            8) echo "google/gemini-pro"; break;;
            9) 
                # Return recommended model based on agent type
                case $agent_id in
                    "E-T") echo "openai/gpt-4o";;
                    "S-A") echo "anthropic/claude-3.5-sonnet";;
                    "M-O") echo "anthropic/claude-3.5-sonnet";;
                    "E-S") echo "mistralai/mixtral-8x7b-instruct";;
                    "E-A") echo "anthropic/claude-3-haiku";;
                esac
                break;;
            10)
                echo ""
                echo "💡 Visit https://openrouter.ai/models to see all available models"
                echo "   Format: provider/model-name (e.g., openai/gpt-4o, anthropic/claude-3.5-sonnet)"
                echo ""
                read -p "Enter custom OpenRouter model ID: " custom_model
                if [[ -n "$custom_model" ]]; then
                    echo "$custom_model"
                    break
                else
                    echo "❌ Invalid model ID. Please try again."
                fi
                ;;
            *)
                # Check if it's a custom model ID (contains a slash)
                if [[ "$choice" == *"/"* ]]; then
                    echo "$choice"
                    break
                else
                    echo "Invalid choice. Please select 1-10 or enter a custom model ID."
                fi
                ;;
        esac
    done
}

# Check if system is running
if ! curl -s http://localhost:8000/ >/dev/null 2>&1; then
    echo "❌ Backend not running. Please start the system first:"
    echo "   ./scripts/start.sh"
    exit 1
fi

# Activate conda environment
echo "🐍 Activating Python environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate genesis_prime || {
    echo "❌ Failed to activate genesis_prime environment"
    exit 1
}

cd backend

echo ""
echo "🎯 Starting Agent Onboarding Process..."
echo "======================================="

# Check if agents are already onboarded
if [[ -f "agents_onboarded.flag" ]]; then
    echo "⚠️  Agents appear to already be onboarded."
    echo "   Flag file exists: agents_onboarded.flag"
    echo ""
    read -p "Do you want to re-onboard agents? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping agent onboarding."
        exit 0
    fi
    rm -f agents_onboarded.flag
fi

echo ""
echo "⚙️  Model Configuration Phase"
echo "============================"

# Model selection for each agent
declare -A AGENT_MODELS
declare -A AGENT_NAMES

AGENT_NAMES["E-T"]="Emergence Theorist"
AGENT_NAMES["S-A"]="Swarm Architect"
AGENT_NAMES["M-O"]="Metacognitive Observer"
AGENT_NAMES["E-S"]="Empirical Synthesizer"
AGENT_NAMES["E-A"]="Ethics & Alignment Analyst"

echo "You can configure different models for each agent to optimize cost vs. quality."
echo ""
read -p "Do you want to configure models individually? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Individual model selection
    for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
        AGENT_MODELS[$agent_id]=$(select_agent_model $agent_id "${AGENT_NAMES[$agent_id]}")
        echo "✅ $agent_id configured with: ${AGENT_MODELS[$agent_id]}"
    done
else
    # Bulk model selection
    echo ""
    echo "🎯 Bulk Model Configuration"
    echo "=========================="
    show_model_costs
    echo "Preset configurations:"
    echo "1. Budget (Mixtral for all) - ~$10 total"
    echo "2. Balanced (GPT-3.5 for all) - ~$25 total"
    echo "3. Premium (GPT-4 for all) - ~$100 total"
    echo "4. Recommended (Mixed models) - ~$50 total"
    echo ""
    
    while true; do
        read -p "Select preset configuration (1-4): " preset
        case $preset in
            1)
                for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
                    AGENT_MODELS[$agent_id]="mistralai/mixtral-8x7b-instruct"
                done
                break;;
            2)
                for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
                    AGENT_MODELS[$agent_id]="openai/gpt-3.5-turbo"
                done
                break;;
            3)
                for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
                    AGENT_MODELS[$agent_id]="openai/gpt-4-turbo-preview"
                done
                break;;
            4)
                AGENT_MODELS["E-T"]="openai/gpt-4-turbo-preview"
                AGENT_MODELS["S-A"]="anthropic/claude-3-sonnet-20240229"
                AGENT_MODELS["M-O"]="anthropic/claude-3-opus-20240229"
                AGENT_MODELS["E-S"]="mistralai/mixtral-8x7b-instruct"
                AGENT_MODELS["E-A"]="anthropic/claude-3-sonnet-20240229"
                break;;
            *) echo "Invalid choice. Please select 1-4.";;
        esac
    done
fi

echo ""
echo "📋 Final Model Configuration:"
for agent_id in "E-T" "S-A" "M-O" "E-S" "E-A"; do
    echo "   $agent_id (${AGENT_NAMES[$agent_id]}): ${AGENT_MODELS[$agent_id]}"
done

echo ""
read -p "Proceed with onboarding using these models? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Agent onboarding cancelled."
    exit 0
fi

# Create model configuration file
cat > agent_model_config.json << MODELEOF
{
    "E-T": "${AGENT_MODELS[E-T]}",
    "S-A": "${AGENT_MODELS[S-A]}",
    "M-O": "${AGENT_MODELS[M-O]}",
    "E-S": "${AGENT_MODELS[E-S]}",
    "E-A": "${AGENT_MODELS[E-A]}"
}
MODELEOF

echo ""
echo "🔧 Phase 1: Testing Enhanced Personality System"
echo "=============================================="

if [[ -f "test_enhanced_personality_system.py" ]]; then
    echo "Running personality system tests..."
    python test_enhanced_personality_system.py
    echo "✅ Personality system tests completed"
else
    echo "⚠️  Personality system test file not found, skipping..."
fi

echo ""
echo "🏗️  Phase 2: Building Agent Personalities"
echo "========================================"

if [[ -f "thousand_questions_agent_builder.py" ]]; then
    echo "Starting 1000 questions agent builder with progress tracking..."
    echo ""
    echo "📋 This process will:"
    echo "   1. Create 5 specialized agents (E-T, S-A, M-O, E-S, E-A)"
    echo "   2. Run personality assessment for each agent (1000 questions each)"
    echo "   3. Generate comprehensive personality profiles"
    echo "   4. Save agent configurations"
    echo ""
    echo "⏱️  Estimated time: 15-30 minutes depending on API response times"
    echo "💰 Estimated cost: Based on your model selection above"
    echo ""
    
    # Create enhanced agent builder script
    cat > enhanced_agent_builder.py << 'BUILDEREOF'
#!/usr/bin/env python3
"""
Enhanced Agent Builder with Progress Tracking and Model Configuration
"""

import json
import sys
import time
from datetime import datetime
import asyncio
from thousand_questions_agent_builder import ThousandQuestionsAgentBuilder

def show_progress(current, total, agent_name, start_time):
    """Show progress bar with time estimates"""
    if current == 0:
        return
    
    elapsed = time.time() - start_time
    rate = current / elapsed if elapsed > 0 else 0
    eta = (total - current) / rate if rate > 0 else 0
    
    percentage = (current / total) * 100
    bar_length = 40
    filled_length = int(bar_length * current // total)
    
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f'\r{agent_name}: |{bar}| {percentage:.1f}% ({current}/{total}) '
          f'ETA: {eta/60:.1f}m', end='', flush=True)

async def main():
    """Main onboarding process with progress tracking"""
    
    # Load model configuration
    try:
        with open('agent_model_config.json', 'r') as f:
            model_config = json.load(f)
    except FileNotFoundError:
        print("❌ Model configuration file not found")
        sys.exit(1)
    
    print("🚀 Starting Enhanced Agent Onboarding")
    print("=====================================")
    
    # Initialize builder
    builder = ThousandQuestionsAgentBuilder()
    
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
    
    print(f"📊 Onboarding {total_agents} agents with 1000 questions each")
    print(f"🎯 Total questions to process: {total_agents * 1000}")
    print("")
    
    overall_start = time.time()
    
    for agent_id, agent_name in agents.items():
        print(f"\n🤖 Starting {agent_name} ({agent_id})")
        print(f"   Model: {model_config.get(agent_id, 'default')}")
        print("-" * 60)
        
        agent_start = time.time()
        
        try:
            # Override model configuration for this agent
            if hasattr(builder, 'set_agent_model'):
                builder.set_agent_model(agent_id, model_config.get(agent_id))
            
            # Build agent with progress callback
            def progress_callback(current, total):
                show_progress(current, total, agent_name, agent_start)
            
            # Run agent building (this would need to be modified in the actual builder)
            await builder.build_agent_with_progress(agent_id, progress_callback)
            
            agent_time = time.time() - agent_start
            print(f"\n✅ {agent_name} completed in {agent_time/60:.1f} minutes")
            
            completed_agents += 1
            
        except Exception as e:
            print(f"\n❌ Error building {agent_name}: {e}")
            continue
    
    overall_time = time.time() - overall_start
    
    print(f"\n🎉 Agent Onboarding Complete!")
    print(f"=====================================")
    print(f"✅ Successfully onboarded: {completed_agents}/{total_agents} agents")
    print(f"⏱️  Total time: {overall_time/60:.1f} minutes")
    print(f"📊 Average time per agent: {overall_time/completed_agents/60:.1f} minutes")
    
    if completed_agents == total_agents:
        # Create completion flag
        with open('agents_onboarded.flag', 'w') as f:
            f.write(f"{datetime.now()}: All {total_agents} agents onboarded successfully\n")
            f.write(f"Models used: {json.dumps(model_config, indent=2)}\n")
            f.write(f"Total time: {overall_time/60:.1f} minutes\n")
        
        print("🏁 Onboarding flag created: agents_onboarded.flag")
    else:
        print("⚠️  Some agents failed to onboard. Check logs and retry.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
BUILDEREOF
    
    # Run the enhanced builder
    python enhanced_agent_builder.py
    
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
    echo "✅ Agent integration tests completed"
else
    echo "⚠️  Agent integration test file not found, skipping..."
fi

echo ""
echo "🎉 Agent Onboarding Complete!"
echo "============================="

echo "✅ All 5 agents have been onboarded and are ready for operation"
echo ""
echo "🤖 Agent Roster:"
echo "   E-T: Empathetic-Thoughtful (${AGENT_MODELS[E-T]})"
echo "   S-A: Strategic-Analytical (${AGENT_MODELS[S-A]})"
echo "   M-O: Methodical-Organized (${AGENT_MODELS[M-O]})"
echo "   E-S: Energetic-Social (${AGENT_MODELS[E-S]})"
echo "   E-A: Experimental-Adaptive (${AGENT_MODELS[E-A]})"
echo ""
echo "💰 Model Configuration Summary:"
cat agent_model_config.json
echo ""
echo "🎯 Next Steps:"
echo "   1. Access the dashboard: http://localhost:3001"
echo "   2. Explore agent interactions and consciousness emergence"
echo "   3. Monitor collective intelligence development"
echo ""
echo "📊 To check system status: ./scripts/status.sh"

cd ..
