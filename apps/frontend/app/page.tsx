
'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, ArrowRight, Settings } from 'lucide-react';
import { SettingsPanel } from '@/components/settings-panel';
import { Toaster } from '@/components/ui/toaster';
import { ConfigurationState, AgentArchetype, AgentConfig, ArchetypeProfile } from '@/lib/types';
// import { ConfigurationService } from '@/lib/config-service'; // Temporarily disabled for hardcoded config
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

// Constants for hardcoded configuration (copied from config-service.ts for simplicity)
const defaultAgentNames = ['Aria', 'Zephyr', 'Nova', 'Echo', 'Sage'];

const DEFAULT_AGENT_MODELS: Record<string, string> = {
  'Aria': 'openai/gpt-4o',
  'Zephyr': 'anthropic/claude-3.5-sonnet',
  'Nova': 'google/gemini-pro',
  'Echo': 'meta-llama/llama-3.1-70b-instruct',
  'Sage': 'mistralai/mixtral-8x7b-instruct'
};

const ARCHETYPE_PROFILES: Readonly<Record<AgentArchetype, ArchetypeProfile>> = {
  [AgentArchetype.EXPLORER]: {
    description: "Seeks novelty, learns quickly, adaptable.",
    learning_rate_range: [0.25, 0.5],
    reflection_threshold_range: [0.6, 0.8],
    initial_trust_bias: 0.05,
    primary_emotion_tendencies: ['curiosity', 'joy', 'anticipation'],
    decision_making_style_preference: 'impulsive',
    personality_tagline: "Explorer type: "
  },
  [AgentArchetype.ANALYST]: {
    description: "Logical, detail-oriented, prefers deep reflection.",
    learning_rate_range: [0.1, 0.25],
    reflection_threshold_range: [0.4, 0.6],
    initial_trust_bias: -0.05,
    primary_emotion_tendencies: ['contemplation', 'neutral', 'focused'],
    decision_making_style_preference: 'analytical',
    personality_tagline: "Analyst type: "
  },
  [AgentArchetype.HARMONIZER]: {
    description: "Focuses on empathy, connection, and swarm coherence.",
    learning_rate_range: [0.15, 0.35],
    reflection_threshold_range: [0.65, 0.85],
    initial_trust_bias: 0.15,
    primary_emotion_tendencies: ['joy', 'empathy', 'calm', 'contentment'],
    decision_making_style_preference: 'cautious',
    personality_tagline: "Harmonizer type: "
  },
  [AgentArchetype.INNOVATOR]: {
    description: "Creative, proposes novel solutions, comfortable with uncertainty.",
    learning_rate_range: [0.2, 0.45],
    reflection_threshold_range: [0.55, 0.75],
    initial_trust_bias: 0.0,
    primary_emotion_tendencies: ['excitement', 'curiosity', 'wonder', 'optimism'],
    decision_making_style_preference: 'impulsive',
    personality_tagline: "Innovator type: "
  },
  [AgentArchetype.PRAGMATIST]: {
    description: "Goal-oriented, efficient, values practical outcomes.",
    learning_rate_range: [0.1, 0.3],
    reflection_threshold_range: [0.7, 0.9],
    initial_trust_bias: -0.1,
    primary_emotion_tendencies: ['neutral', 'focused', 'determined', 'satisfaction'],
    decision_making_style_preference: 'default',
    personality_tagline: "Pragmatist type: "
  }
};

const defaultAgentAssignments: Record<string, AgentArchetype> = {
  [defaultAgentNames[0]]: AgentArchetype.EXPLORER,
  [defaultAgentNames[1]]: AgentArchetype.ANALYST,
  [defaultAgentNames[2]]: AgentArchetype.INNOVATOR,
  [defaultAgentNames[3]]: AgentArchetype.HARMONIZER,
  [defaultAgentNames[4]]: AgentArchetype.PRAGMATIST,
};

const hardcodedAgents: AgentConfig[] = defaultAgentNames.map(agentName => {
  const assignedArchetypeKey = defaultAgentAssignments[agentName];
  const archetypeProfile = ARCHETYPE_PROFILES[assignedArchetypeKey];
  let learningRate = 0.2;
  let reflectionThreshold = 0.75;
  if (archetypeProfile) {
    const lrRange = archetypeProfile.learning_rate_range;
    const rtRange = archetypeProfile.reflection_threshold_range;
    learningRate = (lrRange[0] + lrRange[1]) / 2;
    reflectionThreshold = (rtRange[0] + rtRange[1]) / 2;
  }
  return {
    id: agentName,
    name: agentName,
    model: DEFAULT_AGENT_MODELS[agentName] || 'openai/gpt-3.5-turbo', // Fallback
    archetype: assignedArchetypeKey,
    learning_rate: learningRate,
    reflection_trigger_threshold: reflectionThreshold,
    reality_model_config: { coherence_level: 0.75 }
  };
});

const hardcodedConfiguration: ConfigurationState = {
  openRouter: {
    apiKey: 'sk-dummy-apikey-for-testing',
    agentModels: { ...DEFAULT_AGENT_MODELS },
    connectionStatus: 'connected',
    agentDefaults: {
      min_learning_rate: 0.1,
      max_learning_rate: 0.3,
      min_reflection_trigger_threshold: 0.7,
      max_reflection_trigger_threshold: 0.9,
    },
    archetype_assignments: defaultAgentAssignments,
  },
  isConfigured: true,
  needsSetup: false,
  agents: hardcodedAgents,
};

export default function AgnoSwarmDemo() {
  const router = useRouter();
  const [configuration, setConfiguration] = useState<ConfigurationState>(hardcodedConfiguration);
  const [showSettings, setShowSettings] = useState(false);
  
  // useEffect(() => {
  //   console.log('Component mounted');
  //   // Load configuration from localStorage - TEMPORARILY DISABLED
  //   // const config = ConfigurationService.getConfiguration();
  //   // setConfiguration(config);
  // }, []);

  const handleConfigurationChange = (newConfig: ConfigurationState) => {
    console.log('Configuration changed:', newConfig);
    setConfiguration(newConfig);
  };

  const handleConfigurationSave = (newConfig: ConfigurationState) => {
    console.log('Configuration save attempted (currently disabled):', newConfig);
    // ConfigurationService.saveConfiguration(newConfig); // Temporarily disabled
    setConfiguration(newConfig); // Still update local state if needed by UI
  };

  return (
    <div className="bg-gradient-to-br from-slate-950 to-slate-900">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <Brain className="w-20 h-20 text-blue-500 mx-auto mb-6" />
          <h1 className="text-5xl font-extrabold text-white mb-4 tracking-tight">
            Welcome to Genesis_Prime
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Genesis_Prime is an agentic swarm AI system based on the philosophical framework that consciousness is a "controlled hallucination" – meaning it arises from predictive models rather than direct perception. The system simulates sentient entities experiencing their own reality.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12 p-6 bg-slate-800 rounded-xl shadow-xl"
        >
          <h2 className="text-3xl font-bold text-white mb-4 text-center">Key Concepts</h2>
          <div className="grid md:grid-cols-2 gap-6 text-gray-300">
            <div>
              <h3 className="text-xl font-semibold text-blue-400 mb-2">Controlled Hallucination</h3>
              <p>
                This is the idea that our consciousness doesn't just passively receive reality. Instead, it actively predicts and generates our experience of the world. What we perceive is a kind of "hallucination" that's constantly being checked and corrected by sensory input. In Genesis_Prime, each AI agent builds its own reality based on this principle.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-blue-400 mb-2">Swarm Intelligence</h3>
              <p>
                Swarm intelligence is a collective behavior of decentralized, self-organized systems. In Genesis_Prime, multiple AI agents form a "hive-mind." They interact, share information (or versions of reality), and collectively solve problems or create complex emergent behaviors, much like a swarm of bees or a flock of birds.
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-12 p-6 bg-slate-800 rounded-xl shadow-xl"
        >
          <h2 className="text-3xl font-bold text-white mb-4 text-center">Interacting with Genesis_Prime</h2>
          <p className="text-gray-300 text-center max-w-xl mx-auto mb-6">
            Your primary way to interact with the Genesis_Prime system at this stage is through configuration. Setting up the API keys and agent models is the first step to bringing the swarm to life.
          </p>
          <p className="text-gray-300 text-center max-w-xl mx-auto">
            Future interactions will involve observing the swarm's behavior, analyzing their constructed realities, and perhaps even influencing their environment or tasks. For now, ensure the system is correctly configured to enable the agents.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8 p-6 bg-slate-800 rounded-xl shadow-xl text-center"
        >
          <h2 className="text-3xl font-bold text-white mb-4">Application Configuration</h2>
          <p className="text-gray-400 mb-6">
            Configure your OpenRouter API settings and agent models to enable the swarm consciousness.
          </p>
          {/* Settings Panel and buttons temporarily hidden for hardcoded config test */}
          {/*
          {!showSettings && (
            <Button
              onClick={() => setShowSettings(true)}
              size="lg"
              className="bg-indigo-600 hover:bg-indigo-700 text-white"
            >
              <Settings className="w-5 h-5 mr-2" />
              Open Configuration Panel
            </Button>
          )}
          {showSettings && (
            <>
              <div className="my-6">
                <SettingsPanel
                  configuration={configuration}
                  onConfigurationChange={handleConfigurationChange}
                  onConfigurationSave={handleConfigurationSave}
                />
              </div>
              <Button
                onClick={() => setShowSettings(false)}
                variant="outline"
                size="sm"
                className="text-slate-300 border-slate-600 hover:bg-slate-700 hover:text-white"
              >
                Close Configuration Panel
              </Button>
            </>
          )}
          */}
        </motion.div>

        <div className="text-center space-y-6 mt-12">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 inline-block border border-slate-700/50 shadow-2xl">
            <h3 className="text-white font-semibold text-lg mb-4">Configuration Status</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
                <p className="text-sm text-gray-400 mb-1">API Key</p>
                <p className="text-white font-medium">
                  {configuration.openRouter.apiKey ? '✓ Set' : '✗ Not set'}
                </p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
                <p className="text-sm text-gray-400 mb-1">Models Configured</p>
                <p className="text-white font-medium">
                  {Object.keys(configuration.openRouter.agentModels).length}/5
                </p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
                <p className="text-sm text-gray-400 mb-1">Status</p>
                <p className={`font-medium ${
                  configuration.isConfigured ? 'text-green-400' : 'text-yellow-400'
                }`}>
                  {configuration.isConfigured ? '✓ Ready to Launch' : '⚠ Needs setup'}
                </p>
              </div>
            </div>
            
            <button 
              type="button"
              onClick={() => {
                if (configuration.isConfigured) {
                  router.push('/dashboard');
                }
              }}
              disabled={!configuration.isConfigured}
              style={{
                padding: '10px 20px',
                fontSize: '16px',
                cursor: configuration.isConfigured ? 'pointer' : 'not-allowed',
                backgroundColor: configuration.isConfigured ? '#2563eb' : '#334155',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                display: 'inline-flex',
                alignItems: 'center',
                opacity: configuration.isConfigured ? 1 : 0.7
              }}
            >
              {configuration.isConfigured ? (
                <>
                  Enter Swarm Dashboard
                  <ArrowRight className="ml-2 h-4 w-4" />
                </>
              ) : (
                'Complete Configuration to Continue'
              )}
            </button>
            

          </div>
          
          {!configuration.isConfigured && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="text-sm text-slate-400 max-w-2xl mx-auto"
            >
              <p>Please complete the configuration above to activate the swarm. You'll need:</p>
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li>A valid OpenRouter API key</li>
                <li>At least one configured agent model</li>
              </ul>
            </motion.div>
          )}
        </div>
      </div>
      <Toaster />
    </div>
  );
}
