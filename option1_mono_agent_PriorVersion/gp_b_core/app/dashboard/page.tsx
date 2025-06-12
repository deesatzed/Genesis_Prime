"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Settings, Loader2, Users, Brain, Target, Activity, Zap, MessageSquare, Eye, BarChart3, Lightbulb, ShieldCheck, SlidersHorizontal, ShieldAlert, Play, Pause, Info, AlertTriangle, CheckCircle, XCircle, ChevronsUpDown, Send, PlusCircle, Maximize, Minimize } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet'; // Added Sheet imports
import { SwarmDashboard } from '@/components/swarm-dashboard';
import { InteractionControls } from '@/components/interaction-controls';
import { AgentConsciousnessPanel } from '@/components/agent-consciousness-panel';
import { SettingsPanel } from '@/components/settings-panel';
import { GenesisPrimePanel } from '@/components/genesis-prime-panel';
import { ActivityMonitor } from '@/components/activity-monitor';
import { ConfigurationService, ARCHETYPE_PROFILES } from '@/lib/config-service';
import { useToast } from '@/hooks/use-toast'; // Import useToast // Assuming this service exists for model list
import type { SwarmState, Agent, StimulusEvent, ConsciousnessEvent, ConfigurationState, ModelOption, AgentConfig, RealityFrame, EmotionalState, AgentPrediction, PredictiveRealityModel, MemorySystem, SelfModel, ConsciousnessState as ConsciousnessStateType, EmergentBehavior, SwarmMessage } from '@/lib/types'; // Added AgentConfig and other detailed types, aliased ConsciousnessState
import { AgentArchetype, PredictableSwarmEvent } from '@/lib/types'; 

// Store the original mock agents to use as a template for dynamic agent creation
const MOCK_AGENT_TEMPLATE = {
  // This is one full agent definition from the original initialSwarmState, to be used as a template
  // Ensure all nested structures are complete and valid according to Agent type
  id: 'template-agent',
  name: 'Template Agent',
  model: 'template/model',
  archetype: AgentArchetype.ANALYST,
  personality: 'Template Personality',
  consciousness_state: { 
    current_reality_frame: { 
      id: "frame-template", 
      agent_id: 'template-agent', 
      frame_content: "Template frame", 
      timestamp: new Date(), 
      emotional_coloring: { primary_emotion: 'neutral', intensity: 0.5, mood: 'calm', mood_intensity: 0.5, emotional_context: '', regulation_strategy: '', emotional_predictions: [] }, 
      narrative_context: 'template_context', 
      scene_description: 'template_scene', 
      sensory_predictions: {}, 
      confidence: 0.8, 
      coherence_markers: [] 
    }, 
    prediction_confidence: 0.75, 
    attention_focus: ["Template focus"], 
    emotional_state: { primary_emotion: 'neutral', intensity: 0.5, mood: 'calm', mood_intensity: 0.5, emotional_context: '', regulation_strategy: '', emotional_predictions: [] }, 
    meta_awareness: 0.6, 
    processing_depth: 'surface', 
    active_predictions: [] 
  },
  reality_model: { 
    world_state: { template_state: true }, 
    predictions: [], 
    coherence_level: 0.85, 
    uncertainty_map: {}, 
    temporal_context: { present_focus: 1, past_influence: 0, future_projection: 0, temporal_coherence: 1, time_perception: 'normal' } 
  },
  memory_system: { 
    episodic_memories: [], 
    semantic_patterns: [], 
    working_memory: { capacity_utilization: 0.3, current_focus: ['template_focus'], active_predictions: [], attention_buffer: [], processing_queue: [] }, 
    reconstruction_history: [] 
  },
  self_model: { 
    identity_core: { core_traits: ['template_trait'], values: ['template_value'], capabilities: ['template_capability'], limitations: [], uniqueness_markers: [] }, 
    self_boundaries: { physical_boundaries: [], cognitive_boundaries: [], emotional_boundaries: [], social_boundaries: [], temporal_boundaries: [] }, 
    agency_model: { action_capabilities: ['template_action'], influence_scope: [], decision_patterns: [], autonomy_level: 0.5, responsibility_awareness: [] }, 
    self_narrative: { current_story: 'Template story.', past_chapters: [], future_projections: [], narrative_coherence: 0.9, identity_evolution: [] }, 
    boundary_confidence: 0.8 
  },
  last_activity: new Date(),
  status: 'active',
  learning_rate: 0.1,
  reflection_trigger_threshold: 0.7,
  agent_interaction_profile: { trust_levels: {}, goal_proposal_success_rate: 0},
  long_term_memory: [],
} as Agent; // Type assertion for the template

// Initial Swarm State (agents will be populated dynamically)
const initialSwarmState: SwarmState = {
  swarm_consciousness_level: 0.65,
  shared_reality: {
    coherence_level: 0.78,
    consensus_elements: { global_task: 'observe_environment', current_phase: 'initialization' },
    divergent_perspectives: {},
    last_updated: new Date(),
    uncertainty_areas: ['Future external stimuli impact.'],
  },
  agents: [], // Initialize with an empty array, will be populated from configuration
  collective_memory: {
    shared_experiences: [],
    consensus_memories: [],
    divergent_realities: [],
    memory_coherence: 0.85,
    last_updated: new Date(),
  },
  communication_network: {
    message_history: [],
    network_topology: 'fully_connected',
    bandwidth_usage: 0.2,
    last_updated: new Date(),
  },
  stimulus_events: [],
  emergent_behaviors: []
};

const createAgentFromConfig = (agentConfig: AgentConfig, template: Agent, currentConfig: ConfigurationState | null): Agent => {
  const archetypeProfile = ARCHETYPE_PROFILES[agentConfig.archetype];
  const personality = archetypeProfile ? archetypeProfile.personality_tagline + " " + agentConfig.name : agentConfig.name; // Added space

  // Deep clone the template's nested objects to avoid shared references
  const consciousness_state: ConsciousnessStateType = JSON.parse(JSON.stringify(template.consciousness_state));
  if (consciousness_state.current_reality_frame) {
    consciousness_state.current_reality_frame.agent_id = agentConfig.id;
    consciousness_state.current_reality_frame.id = `frame-${agentConfig.id}-${Date.now()}`;
  }
  // Update other agent_id specific fields if necessary within consciousness_state

  const reality_model: PredictiveRealityModel = JSON.parse(JSON.stringify(template.reality_model));
  const memory_system: MemorySystem = JSON.parse(JSON.stringify(template.memory_system));
  const self_model: SelfModel = JSON.parse(JSON.stringify(template.self_model));

  return {
    ...template, // Spread the template first for all its defaults
    id: agentConfig.id,
    name: agentConfig.name,
    // Get the correct, up-to-date model from the configuration's agentModels map
    model: currentConfig?.openRouter?.agentModels?.[agentConfig.name] || agentConfig.model, // Fallback to agentConfig.model
    archetype: agentConfig.archetype,
    personality: personality,
    status: 'active', // Default status
    last_activity: new Date(),
    learning_rate: agentConfig.learning_rate ?? template.learning_rate ?? 0.1,
    reflection_trigger_threshold: agentConfig.reflection_trigger_threshold ?? template.reflection_trigger_threshold ?? 0.7,
    long_term_memory: [], // Start with empty LTM for new agents
    agent_interaction_profile: { trust_levels: {}, goal_proposal_success_rate: 0 }, // Default interaction profile
    // Assign the deep-cloned and potentially customized nested objects
    consciousness_state,
    reality_model,
    memory_system,
    self_model,
  };
};

export default function DashboardPage() {
  const router = useRouter();
  const { toast } = useToast();

  const [configuration, setConfiguration] = useState<ConfigurationState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSwarmRunning, setIsSwarmRunning] = useState(false);
  const [simulationIntervalId, setSimulationIntervalId] = useState<NodeJS.Timeout | null>(null);
  const [currentSimulationSpeedMs, setCurrentSimulationSpeedMs] = useState<number>(1000); // Default speed: 1 tick per second

  const [isSettingsPanelOpen, setIsSettingsPanelOpen] = useState(false); // Ensured this is declared correctly
  const [swarmState, setSwarmState] = useState<SwarmState>(initialSwarmState);
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'swarm' | 'genesis'>('swarm');

  useEffect(() => {
    console.log('[DashboardPage] Initializing: Fetching configuration...');
    const loadedConfig = ConfigurationService.getConfiguration();
    console.log('[DashboardPage] Initial config loaded:', loadedConfig);
    setConfiguration(loadedConfig);
  }, []);

  useEffect(() => {
    return () => {
      if (simulationIntervalId) {
        clearInterval(simulationIntervalId);
        console.log('[DashboardPage] Cleaned up simulation interval on unmount/change.');
      }
    };
  }, [simulationIntervalId]);

  useEffect(() => {
    console.log('[DashboardPage] useEffect[configuration] - Configuration changed, attempting to update swarmState. Current config (raw object):', configuration);
    console.log('[DashboardPage] useEffect[configuration] - configuration.openRouter.agentModels:', JSON.parse(JSON.stringify(configuration?.openRouter?.agentModels || {})));
    if (configuration?.agents) {
      const newAgents = configuration.agents.map(agentConfig => 
        createAgentFromConfig(agentConfig, MOCK_AGENT_TEMPLATE, configuration)
      );
      console.log('[DashboardPage] New agents created from config:', newAgents);
      setSwarmState(prevState => ({
        ...prevState,
        agents: newAgents,
      }));
      if (newAgents.length > 0 && !selectedAgentId) {
        setSelectedAgentId(newAgents[0].id);
      }
    }
    if (configuration) { 
      setIsLoading(false);
    }
  }, [configuration, selectedAgentId]);

  useEffect(() => {
    if (!swarmState.agents || swarmState.agents.length === 0) return;

    const newStatus = isSwarmRunning ? 'processing' : 'active';
    
    // Check if any agent status actually needs to change to prevent unnecessary updates
    const needsUpdate = swarmState.agents.some(agent => agent.status !== newStatus);

    if (needsUpdate) {
      setSwarmState(prevState => ({
        ...prevState,
        agents: prevState.agents.map(agent => ({
          ...agent,
          status: newStatus,
          last_activity: new Date(), // Also update last_activity
        })),
      }));
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSwarmRunning, swarmState.agents.length]);

  const selectedAgent = selectedAgentId ? swarmState.agents.find(agent => agent.id === selectedAgentId) : null;

  if (isLoading || !configuration) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-900">
        <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
      </div>
    );
  }

  // This specific check for !configuration might now be redundant due to the change above,
  // but we'll keep it for now to ensure no regressions. It can be cleaned up later if the primary loading works.
  if (!configuration) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-900">
        <p className="text-white">Configuration not loaded. Redirecting to setup...</p>
      </div>
    );
  }
  
  const handleSelectAgent = (agentId: string) => {
    setSelectedAgentId(agentId);
  };

  const handleIntroduceStimulus = (stimulus: StimulusEvent) => {
    console.log('Stimulus introduced to dashboard:', stimulus);
    setSwarmState(prevState => ({ ...prevState, stimulus_events: [...prevState.stimulus_events, stimulus] }));
    toast({ title: "Stimulus Introduced", description: `Event: ${stimulus.type}, Target: ${stimulus.target_agents?.join(', ') || 'all agents'}`, variant: "default" });
  };

  const handleStartSwarm = () => {
    if (simulationIntervalId) {
      clearInterval(simulationIntervalId);
    }
    setIsSwarmRunning(true);
    const newIntervalId = setInterval(runSwarmTick, currentSimulationSpeedMs);
    setSimulationIntervalId(newIntervalId);
    toast({ title: "Swarm Simulation Started", description: `Running at ${currentSimulationSpeedMs / 1000}s interval.`, variant: "default" });
  };

  const handleStopSwarm = () => {
    setIsSwarmRunning(false);
    if (simulationIntervalId) {
      clearInterval(simulationIntervalId);
      setSimulationIntervalId(null);
    }
    toast({ title: "Swarm Simulation Stopped", description: "Processing paused.", variant: "default" });
  };

  const handleSimulationSpeedChange = (newSpeed: number) => {
    setCurrentSimulationSpeedMs(newSpeed);
    if (isSwarmRunning) {
      if (simulationIntervalId) {
        clearInterval(simulationIntervalId);
      }
      const newIntervalId = setInterval(runSwarmTick, newSpeed);
      setSimulationIntervalId(newIntervalId);
      toast({ title: "Simulation Speed Updated", description: `Now running at ${newSpeed / 1000}s interval.`, variant: "default" });
    } else {
      toast({ title: "Simulation Speed Set", description: `Will run at ${newSpeed / 1000}s interval when started.`, variant: "default" });
    }
  };

  const handleIntroduceEmergentBehavior = (behaviorData: Omit<EmergentBehavior, "id" | "timestamp">) => {
    const newBehavior: EmergentBehavior = {
      ...behaviorData,
      id: `eb_manual_${Date.now()}`,
      timestamp: new Date(),
    };
    setSwarmState(prevState => ({
      ...prevState,
      emergent_behaviors: [...(prevState.emergent_behaviors || []), newBehavior],
    }));
    toast({ title: "Emergent Behavior Manually Added", description: `Type: ${newBehavior.behavior_type}`, variant: "default" });
  };

  const detectEmergentBehaviors = (currentSwarmState: SwarmState): EmergentBehavior[] => {
  const detectedBehaviors: EmergentBehavior[] = [];
  const { agents } = currentSwarmState;

  if (!agents || agents.length === 0) {
    return detectedBehaviors;
  }

  // Rule 1: High Collective Focus/Optimism
  const focusedOrOptimisticAgents = agents.filter(agent => 
    agent.emotional_state && 
    (agent.emotional_state.mood === 'optimistic' || agent.emotional_state.mood === 'focused') && 
    agent.emotional_state.mood_intensity > 0.7
  );

  const percentageFocusedOrOptimistic = (focusedOrOptimisticAgents.length / agents.length) * 100;

  if (percentageFocusedOrOptimistic > 75) {
    const behaviorId = `eb_hfo_${Date.now()}`;
    const existingBehavior = currentSwarmState.emergent_behaviors?.find(b => 
        b.behavior_type === 'High Collective Focus/Optimism' && 
        (new Date().getTime() - new Date(b.timestamp).getTime()) < 30000 // within last 30s
    );

    if (!existingBehavior) {
        detectedBehaviors.push({
            id: behaviorId,
            behavior_type: 'High Collective Focus/Optimism',
            description: `Over ${percentageFocusedOrOptimistic.toFixed(0)}% of agents are highly focused or optimistic.`,
            participating_agents: focusedOrOptimisticAgents.map(a => a.id),
            emergence_level: percentageFocusedOrOptimistic / 100,
            stability: 0.5, // Placeholder
            timestamp: new Date(),
        });
    }
  }
  // Add more detection rules here
  return detectedBehaviors;
};

const runSwarmTick = () => {
    setSwarmState(prevState => {
      const newMessages: SwarmMessage[] = [];
      
      // Check if there are recent stimuli (within last 30 seconds)
      const recentStimuli = (prevState.stimulus_events || []).filter(stimulus => 
        new Date().getTime() - new Date(stimulus.timestamp).getTime() < 30000
      );
      const hasRecentStimuli = recentStimuli.length > 0;
      
      const agentsWithUpdatedEmotions = prevState.agents.map(agent => {
        let newMood = agent.emotional_state?.mood || 'neutral';
        let newMoodIntensity = agent.emotional_state?.mood_intensity || 0.5;
        let shouldGenerateMessage = false;
        
        // Check if this agent is affected by recent stimuli
        const isAffectedByStimulus = recentStimuli.some(stimulus => 
          !stimulus.target_agents || 
          stimulus.target_agents.length === 0 || 
          stimulus.target_agents.includes(agent.id)
        );
        
        // Higher chance of mood change and message generation if affected by stimulus
        const moodChangeChance = isAffectedByStimulus ? 0.3 : 0.1; // 30% vs 10% chance
        const messageChance = isAffectedByStimulus ? 0.8 : 0.05; // 80% vs 5% chance
        
        // Placeholder: Randomly fluctuate mood for demonstration
        if (Math.random() < moodChangeChance) {
          const moods = ['optimistic', 'neutral', 'focused', 'irritable', 'pessimistic'];
          newMood = moods[Math.floor(Math.random() * moods.length)];
          newMoodIntensity = Math.random();
          shouldGenerateMessage = Math.random() < 0.7; // 70% chance to send message when mood changes
        } else if (Math.random() < messageChance) {
          shouldGenerateMessage = true;
        }

        let currentAction: string = "Observing";
        let currentActionIcon: string = "Eye";

        switch (newMood) {
          case 'optimistic':
            currentAction = "Planning Big Moves";
            currentActionIcon = "Lightbulb";
            break;
          case 'focused':
            currentAction = "Deep Analysis";
            currentActionIcon = "Brain";
            break;
          case 'irritable':
            currentAction = "Recalibrating...";
            currentActionIcon = "Zap";
            break;
          case 'pessimistic':
            currentAction = "Contemplating Risks";
            currentActionIcon = "ShieldAlert";
            break;
          default:
            currentAction = "Observing";
            currentActionIcon = "Eye";
            break;
        }

        // Generate message if conditions are met
        if (shouldGenerateMessage && prevState.agents.length > 1) {
          const messageTypes = ['reality_share', 'memory_query', 'consensus_request', 'self_model_update'];
          const messageType = messageTypes[Math.floor(Math.random() * messageTypes.length)];
          
          // Create context-aware message templates
          let messageTemplates = {
            reality_share: [
              `I'm experiencing ${newMood} patterns in my reality model. Current coherence at ${Math.round(agent.reality_model?.coherence_level * 100 || 80)}%.`,
              `Reality frame shifted to ${currentAction.toLowerCase()}. Observing new environmental patterns.`,
              `Sharing current reality state: ${newMood} with intensity ${Math.round(newMoodIntensity * 100)}%.`
            ],
            memory_query: [
              `Requesting collective memory access for pattern: ${currentAction.toLowerCase()}.`,
              `Querying shared experiences related to ${newMood} states.`,
              `Memory reconstruction needed for current ${currentAction.toLowerCase()} process.`
            ],
            consensus_request: [
              `Proposing consensus on current environmental assessment: ${newMood}.`,
              `Seeking agreement on ${currentAction.toLowerCase()} approach.`,
              `Collective decision needed regarding ${newMood} response patterns.`
            ],
            self_model_update: [
              `Updating self-model: identity boundaries shifting during ${currentAction.toLowerCase()}.`,
              `Self-awareness recalibration: ${newMood} state integration.`,
              `Identity coherence update: ${Math.round(newMoodIntensity * 100)}% confidence.`
            ]
          };

          // Add stimulus-specific messages if agent is affected by recent stimuli
          if (isAffectedByStimulus && recentStimuli.length > 0) {
            const latestStimulus = recentStimuli[recentStimuli.length - 1];
            const stimulusMessages = {
              reality_share: [
                `Responding to ${latestStimulus.type} stimulus: reality model adapting to new conditions.`,
                `${latestStimulus.description} - updating shared reality framework.`,
                `Stimulus integration: ${newMood} state emerging from ${latestStimulus.type} event.`
              ],
              memory_query: [
                `Accessing memories related to ${latestStimulus.type} events for pattern matching.`,
                `Historical analysis needed: how did we handle similar ${latestStimulus.description.slice(0, 30)}... before?`,
                `Memory search initiated for ${latestStimulus.type} response protocols.`
              ],
              consensus_request: [
                `Team consensus needed: how should we collectively respond to ${latestStimulus.type} stimulus?`,
                `Seeking agreement on unified response to: ${latestStimulus.description.slice(0, 40)}...`,
                `Coordination required for ${latestStimulus.type} event management.`
              ],
              self_model_update: [
                `Self-model adaptation in progress: integrating ${latestStimulus.type} stimulus effects.`,
                `Identity recalibration: how does ${latestStimulus.description.slice(0, 30)}... change who I am?`,
                `Personal boundaries shifting in response to ${latestStimulus.type} environment.`
              ]
            };
            // Mix stimulus-specific messages with regular ones
            Object.keys(messageTemplates).forEach(key => {
              messageTemplates[key as keyof typeof messageTemplates] = [
                ...messageTemplates[key as keyof typeof messageTemplates],
                ...stimulusMessages[key as keyof typeof stimulusMessages]
              ];
            });
          }
          
          const messageContent = messageTemplates[messageType as keyof typeof messageTemplates];
          const randomMessage = messageContent[Math.floor(Math.random() * messageContent.length)];
          
          const newMessage: SwarmMessage = {
            id: `msg_${Date.now()}_${agent.id}`,
            sender_id: agent.id,
            recipient_ids: [], // Broadcast to all
            message_type: messageType as any,
            content: {
              message: randomMessage,
              mood: newMood,
              action: currentAction,
              metadata: {
                consciousness_level: agent.consciousness_state.meta_awareness,
                reality_coherence: agent.reality_model?.coherence_level || 0.8
              }
            },
            timestamp: new Date(),
            confidence: 0.7 + Math.random() * 0.3, // Random confidence between 0.7-1.0
            priority: Math.random() < 0.3 ? 'high' : 'normal' // 30% chance of high priority
          };
          
          newMessages.push(newMessage);
        }

        return {
          ...agent,
          last_activity: new Date(), // Simulate activity by updating timestamp
          emotional_state: {
            ...(agent.emotional_state || {}),
            primary_emotion: agent.emotional_state?.primary_emotion || 'neutral',
            intensity: agent.emotional_state?.intensity || 0.5,
            emotional_context: 'tick_update',
            regulation_strategy: 'none',
            emotional_predictions: [],
            mood: newMood,
            mood_intensity: newMoodIntensity,
          } as EmotionalState,
          current_action: currentAction,
          current_action_icon: currentActionIcon,
        };
      });

      let detectedBehaviorsInTick: EmergentBehavior[] = [];
      if (agentsWithUpdatedEmotions && agentsWithUpdatedEmotions.length > 0) {
          detectedBehaviorsInTick = detectEmergentBehaviors({ ...prevState, agents: agentsWithUpdatedEmotions, emergent_behaviors: prevState.emergent_behaviors || [] });
      }

      const allEmergentBehaviors = [...(prevState.emergent_behaviors || [])];

      if (detectedBehaviorsInTick.length > 0) {
        detectedBehaviorsInTick.forEach(newBehavior => {
          if (!allEmergentBehaviors.find(eb => eb.id === newBehavior.id)) {
            allEmergentBehaviors.push(newBehavior);
            console.log(`[DashboardPage] New emergent behavior detected and added: ${newBehavior.behavior_type}`);
            toast({ title: "Emergent Behavior Added!", description: `Type: ${newBehavior.behavior_type} (Icon was: CheckCircle)`, variant: "default" });
          }
        });
      }

      // Update communication network with new messages
      const updatedCommunicationNetwork = {
        ...prevState.communication_network,
        message_history: [...prevState.communication_network.message_history, ...newMessages],
        bandwidth_usage: Math.min(1.0, prevState.communication_network.bandwidth_usage + (newMessages.length * 0.1)),
        last_updated: new Date(),
      };

      return { 
        ...prevState, 
        agents: agentsWithUpdatedEmotions, 
        emergent_behaviors: allEmergentBehaviors,
        communication_network: updatedCommunicationNetwork
      };
  });
};

  return (
    <div>
      <header className="flex items-center justify-between p-4 border-b border-slate-700/50 bg-slate-900 text-slate-100 sticky top-0 z-20">
  <div className="flex items-center">
    <Brain className="w-8 h-8 mr-3 text-purple-400" />
    <h1 className="text-xl font-semibold">AgnoSwarm Mission Control</h1>
  </div>
  <Button 
    variant="outline" 
    size="icon" 
    onClick={() => setIsSettingsPanelOpen(!isSettingsPanelOpen)}
    className="border-slate-600 hover:bg-slate-700 hover:text-slate-50"
    aria-label="Open settings panel"
  >
    <Settings className="h-5 w-5" />
  </Button>
</header>

      {/* Main Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */} 
        <aside className="w-72 p-4 space-y-4 border-r border-slate-700/50 overflow-y-auto bg-slate-800/60 shadow-md">
          <div className="sticky top-0 pt-2 pb-2 bg-slate-800/60 backdrop-blur-sm z-10 -mx-4 px-4 border-b border-slate-700/30">
            <h2 className="text-lg font-semibold text-slate-100 flex items-center"><Users className="w-5 h-5 mr-2 text-purple-400"/>Agent Roster</h2>
          </div>
          {swarmState.agents.map(agent => (
            <div 
              key={agent.id} 
              onClick={() => handleSelectAgent(agent.id)}
              className={`p-3 rounded-lg cursor-pointer transition-all duration-150 ease-in-out hover:bg-slate-700/70 hover:shadow-lg transform hover:scale-[1.02] active:scale-95
                          ${selectedAgentId === agent.id ? 'bg-gradient-to-r from-purple-600/50 to-blue-600/50 ring-2 ring-purple-400 shadow-xl' : 'bg-slate-700/40 border border-slate-600/50'}`}
            >
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-slate-50 text-md">{agent.name}</h3>
                <span className={`px-2 py-0.5 text-xs rounded-full ${agent.status === 'active' ? 'bg-green-500/20 text-green-300' : 'bg-yellow-500/20 text-yellow-300'}`}>
                  {agent.status}
                </span>
              </div>
               <p className="text-xs text-slate-400 mt-1">{(agent.archetype ?? AgentArchetype.ANALYST)} - <span className="italic">{agent.model.split('/').pop()}</span></p>
              {agent.current_action && (
                <div className="mt-2 flex items-center text-xs text-slate-300">
                  {/* Dynamically render icon based on agent.current_action_icon */}
                  {agent.current_action_icon === 'Eye' && <Eye className="w-3 h-3 mr-1.5 text-sky-400 flex-shrink-0" />}
                  {agent.current_action_icon === 'Lightbulb' && <Lightbulb className="w-3 h-3 mr-1.5 text-yellow-400 flex-shrink-0" />}
                  {agent.current_action_icon === 'Brain' && <Brain className="w-3 h-3 mr-1.5 text-pink-400 flex-shrink-0" />}
                  {agent.current_action_icon === 'Zap' && <Zap className="w-3 h-3 mr-1.5 text-red-400 flex-shrink-0" />}
                  {agent.current_action_icon === 'ShieldAlert' && <ShieldAlert className="w-3 h-3 mr-1.5 text-orange-400 flex-shrink-0" />}
                  <span>{agent.current_action}</span>
                </div>
              )}
            </div>
          ))}
        </aside>

        {/* Central Main Panel */} 
        <main className="flex-1 p-6 overflow-y-auto bg-black/20">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-100 flex items-center"><Activity className="w-7 h-7 mr-3 text-blue-400"/>Mission Control Dashboard</h2>
            <p className="text-sm text-slate-400">Real-time visualization of consciousness states and collective intelligence.</p>
          </div>

          <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as 'swarm' | 'genesis')} className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-6">
              <TabsTrigger value="swarm" className="flex items-center space-x-2">
                <Users className="w-4 h-4" />
                <span>Agent Swarm</span>
              </TabsTrigger>
              <TabsTrigger value="genesis" className="flex items-center space-x-2">
                <Brain className="w-4 h-4" />
                <span>Genesis Prime</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="swarm" className="space-y-6">
              {/* Activity Monitor - Shows real-time status and token tracking */}
              {(!isLoading && configuration && swarmState.agents) && (
                <ActivityMonitor 
                  swarmState={swarmState}
                  isSimulationRunning={isSwarmRunning}
                  className="mb-6"
                />
              )}

              {/* Interaction Controls should be placed here, above or alongside SwarmDashboard */}
              {/* We need to ensure configuration and agents are loaded before rendering InteractionControls */}
              {(!isLoading && configuration && swarmState.agents) && (
                <InteractionControls 
                  agents={swarmState.agents}
                  isSimulationRunning={isSwarmRunning}
                  onStartSimulation={handleStartSwarm}
                  onStopSimulation={handleStopSwarm}
                  onIntroduceStimulus={handleIntroduceStimulus}
                  onSimulationSpeedChange={handleSimulationSpeedChange}
                  onIntroduceEmergentBehavior={handleIntroduceEmergentBehavior}
                  className="mb-6" // Add some margin below the controls
                />
              )}

              <div className="bg-slate-800/50 p-1 rounded-xl border border-slate-700/50 shadow-2xl min-h-[400px] lg:min-h-[500px]">
                <SwarmDashboard 
                    swarmState={swarmState} 
                    messages={swarmState.communication_network.message_history || []} 
                    emergentBehaviors={swarmState.emergent_behaviors || []}
                />
               </div>
            </TabsContent>

            <TabsContent value="genesis" className="space-y-6">
              <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 shadow-2xl min-h-[400px] lg:min-h-[500px]">
                <GenesisPrimePanel />
              </div>
            </TabsContent>
          </Tabs>
        </main>
      </div> {/* Closes flex flex-1 overflow-hidden */}

      {/* Settings Panel */}
      <Sheet open={isSettingsPanelOpen} onOpenChange={setIsSettingsPanelOpen}>
        <SheetContent className="md:w-[600px] sm:w-[450px] w-full p-0 overflow-y-auto">
          <SheetHeader className="p-4 border-b border-slate-700">
            <SheetTitle className="sr-only">Settings Panel</SheetTitle>
            <SheetDescription className="sr-only">Configure swarm agents and OpenRouter API settings.</SheetDescription>
          </SheetHeader>
          {(!isLoading && configuration) && (
            <SettingsPanel 
              configuration={configuration!} // No '!' needed due to check
              onConfigurationChange={(newConfig) => {
                console.log('[DashboardPage] SettingsPanel onConfigurationChange called with:', newConfig);
                setConfiguration(newConfig);
              }} 
              onConfigurationSave={(newConfig) => {
                console.log('[DashboardPage] SettingsPanel onConfigurationSave called with (raw object):', newConfig);
    console.log('[DashboardPage] SettingsPanel onConfigurationSave - newConfig.openRouter.agentModels:', JSON.parse(JSON.stringify(newConfig.openRouter?.agentModels || {})));
                ConfigurationService.saveConfiguration(newConfig);
                console.log('[DashboardPage] Configuration supposedly saved by ConfigurationService. Updated dashboard configuration state will trigger agent recreation if models changed.');
                setConfiguration(newConfig); // This should trigger the useEffect to update swarmState.agents
                setIsSettingsPanelOpen(false); // Close panel on save
              }}
            />
          )}
        </SheetContent>
      </Sheet>
    </div>
  );
}
