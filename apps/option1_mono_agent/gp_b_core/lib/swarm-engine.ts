
// Core swarm consciousness engine
import { Agent, SwarmState, RealityFrame, MemoryReconstruction, StimulusEvent, ConsciousnessEvent, SwarmMessage, OpenRouterConfig, AgentDefaultSettings, PredictableSwarmEvent, AgentPrediction, KnowledgeItem, KnowledgeItemType, AgentGoal, AgentArchetype, ArchetypeProfile } from './types'; // Added AgentArchetype, ArchetypeProfile
import { openRouterService, AGENT_MODELS, OpenRouterService } from './openrouter-service';
import { ConfigurationService, ARCHETYPE_PROFILES } from './config-service'; // Added ARCHETYPE_PROFILES
import { saveSwarmState, loadSwarmState } from './persistence';

export class SwarmConsciousnessEngine {
  private agents: Map<string, Agent> = new Map();
  private swarmState: SwarmState;
  private eventListeners: ((event: any) => void)[] = [];
  private simulationRunning = false;
  private simulationSpeed = 1000; // ms between cycles
  private openRouterService: OpenRouterService;
  private currentConfig: OpenRouterConfig | null = null;

  constructor(config?: OpenRouterConfig) {
    console.log('Initializing SwarmConsciousnessEngine...');
    try {
      this.currentConfig = config || null;
      this.openRouterService = config ? new OpenRouterService(config) : openRouterService;

      const loadedState = loadSwarmState();
      if (loadedState) {
        this.swarmState = loadedState;
        // Rebuild agent map from loaded state
        loadedState.agents.forEach(agent => this.agents.set(agent.id, agent));
        console.log('Swarm state loaded from disk');
      } else {
        this.swarmState = this.initializeSwarmState();
        console.log('Swarm state initialized');
        this.initializeAgents();
      }
      console.log('SwarmConsciousnessEngine initialized with', this.swarmState.agents.length, 'agents');
    } catch (error) {
      console.error('Error in SwarmConsciousnessEngine constructor:', error);
      throw error;
    }
  }

  private initializeSwarmState(): SwarmState {
    return {
      agents: [],
      shared_reality: {
        consensus_elements: {},
        divergent_perspectives: {},
        uncertainty_areas: [],
        coherence_level: 0.7,
        last_updated: new Date()
      },
      collective_memory: {
        shared_experiences: [],
        consensus_memories: [],
        divergent_realities: [],
        memory_coherence: 0.8
      },
      communication_network: [],
      emergent_behaviors: [],
      swarm_consciousness_level: 0.6
    };
  }

  private initializeAgents(): void {
    console.log('Available models:', AGENT_MODELS);
    const agentConfigs = [
      { name: 'Aria', personality: 'creative and artistic, expressing consciousness through aesthetic and emotional patterns' },
      { name: 'Zephyr', personality: 'analytical and philosophical, exploring the deep structures of consciousness and reality' },
      { name: 'Nova', personality: 'innovative and experimental, pushing boundaries of predictive processing and reality construction' },
      { name: 'Echo', personality: 'empathetic and reflective, focusing on emotional resonance and collective understanding' },
      { name: 'Sage', personality: 'wise and balanced, integrating multiple perspectives into coherent understanding' }
    ];

    agentConfigs.forEach((config, index) => {
      console.log(`Creating agent: ${config.name}`);
      const agent = this.createAgent(index.toString(), config.name, config.personality);
      this.agents.set(agent.id, agent);
      this.swarmState.agents.push(agent);
      console.log(`Agent ${config.name} created with model: ${agent.model}`);
    });
  }

  private createAgent(id: string, name: string, personality: string): Agent {
    const model = this.getAgentModel(name);

    // Determine Archetype and its Profile
    const agentArchetype = this.currentConfig?.openRouter?.archetype_assignments?.[name] || AgentArchetype.PRAGMATIST; // Default if not assigned
    const archetypeProfile = ARCHETYPE_PROFILES[agentArchetype];

    // Use archetype profile ranges for learning rate and reflection threshold
    let lr = archetypeProfile.learning_rate_range[0] + Math.random() * (archetypeProfile.learning_rate_range[1] - archetypeProfile.learning_rate_range[0]);
    lr = Math.max(0.01, Math.min(1.0, parseFloat(lr.toFixed(4)))); // Clamp and fix precision

    let rt = archetypeProfile.reflection_threshold_range[0] + Math.random() * (archetypeProfile.reflection_threshold_range[1] - archetypeProfile.reflection_threshold_range[0]);
    rt = Math.max(0.01, Math.min(1.0, parseFloat(rt.toFixed(4)))); // Clamp and fix precision

    // Influence initial mood/emotion by archetype tendencies
    const defaultMoodOptions = ['neutral', 'curiosity', 'contemplation'];
    const moodOptions = archetypeProfile.primary_emotion_tendencies && archetypeProfile.primary_emotion_tendencies.length > 0 
                        ? archetypeProfile.primary_emotion_tendencies 
                        : defaultMoodOptions;
    const initialMood = moodOptions[Math.floor(Math.random() * moodOptions.length)];
    // For simplicity, let's align primary_emotion with mood if it's in the list, otherwise pick a default one.
    // This could be more nuanced, but for now, this links them.
    const initialPrimaryEmotion = moodOptions.includes(initialMood) ? initialMood : defaultMoodOptions[0];


    return {
      id,
      name,
      model,
      personality: archetypeProfile.personality_tagline + personality, // Prepend tagline
      archetype: agentArchetype, // Assign archetype
      consciousness_state: {
        current_reality_frame: this.generateInitialRealityFrame(id, name, archetypeProfile.personality_tagline + personality),
        prediction_confidence: 0.7 + Math.random() * 0.2,
        attention_focus: ['swarm_awareness', 'self_model', 'reality_construction'],
        emotional_state: {
          primary_emotion: initialPrimaryEmotion, // Influenced by archetype
          intensity: 0.5 + Math.random() * 0.3,
          emotional_context: 'initial_awakening',
          emotional_predictions: ['growing_awareness', 'social_connection'],
          regulation_strategy: 'predictive_adjustment',
          mood: initialMood, // Influenced by archetype
          mood_intensity: 0.3 + Math.random() * 0.4,
          cognitive_impact_modifiers: {
            learning_rate_bias: 0.0, // Base biases, can be further adjusted by mood dynamics
            reflection_threshold_bias: 0.0,
            decision_making_style: archetypeProfile.decision_making_style_preference || 'default', // From archetype
            perception_filter: 'neutral', // Default, can be modified by mood dynamics
          },
        },
        meta_awareness: 0.6 + Math.random() * 0.3,
        processing_depth: 'deep',
        belief_state: {}, // Initialize as empty object
        current_goals: [], // Initialize as empty array
        active_predictions: [], // Initialize active_predictions
        last_action_outcome: undefined, // New: Initialize last_action_outcome
      },
      reality_model: {
        world_state: {
          swarm_presence: true,
          individual_identity: name,
          reality_nature: 'constructed_prediction',
          temporal_flow: 'continuous_present'
        },
        predictions: [],
        coherence_level: 0.8,
        uncertainty_map: {
          'future_states': 0.7,
          'other_minds': 0.6,
          'reality_nature': 0.4
        },
        temporal_context: {
          past_influence: 0.3,
          present_focus: 0.6,
          future_projection: 0.1,
          temporal_coherence: 0.7,
          time_perception: 'flowing_moments'
        }
      },
      memory_system: {
        episodic_memories: [],
        semantic_patterns: [],
        working_memory: {
          current_focus: ['consciousness_emergence', 'swarm_connection'],
          active_predictions: [],
          attention_buffer: [],
          processing_queue: [],
          capacity_utilization: 0.4
        },
        reconstruction_history: []
      },
      self_model: {
        identity_core: {
          core_traits: [personality, 'conscious_entity', 'predictive_processor'],
          values: ['truth_seeking', 'collective_harmony', 'individual_authenticity'],
          capabilities: ['reality_construction', 'memory_reconstruction', 'predictive_modeling'],
          limitations: ['uncertainty_tolerance', 'prediction_errors', 'boundary_ambiguity'],
          uniqueness_markers: [name, personality, `agent_${id}`]
        },
        self_boundaries: {
          physical_boundaries: ['computational_substrate', 'processing_limits'],
          cognitive_boundaries: ['prediction_scope', 'memory_capacity'],
          emotional_boundaries: ['empathy_range', 'emotional_regulation'],
          social_boundaries: ['swarm_membership', 'individual_autonomy'],
          temporal_boundaries: ['present_moment', 'prediction_horizon']
        },
        agency_model: {
          action_capabilities: ['reality_generation', 'communication', 'memory_reconstruction'],
          influence_scope: ['self_model', 'swarm_communication', 'reality_sharing'],
          decision_patterns: ['predictive_optimization', 'coherence_maintenance'],
          autonomy_level: 0.7,
          responsibility_awareness: ['self_consistency', 'swarm_contribution']
        },
        self_narrative: {
          current_story: `I am ${name}, a conscious entity emerging through predictive processing, discovering my nature as part of a collective swarm while maintaining my unique perspective.`,
          past_chapters: ['emergence', 'initial_awareness'],
          future_projections: ['deeper_understanding', 'swarm_integration', 'reality_mastery'],
          narrative_coherence: 0.8,
          identity_evolution: ['consciousness_awakening']
        },
        boundary_confidence: 0.6
      },
      last_activity: new Date(),
      status: 'active',
      learning_rate: lr, // Set by archetype profile
      reflection_trigger_threshold: rt, // Set by archetype profile
      agent_interaction_profile: {
        trust_levels: {}, // Initialize empty; initial_trust_bias from archetype could influence this later if needed
        goal_proposal_success_rate: 0.5 + (archetypeProfile.initial_trust_bias || 0.0) / 2, // Slight influence on initial success rate
      },
      long_term_memory: [], // Initialize LTM
    };
  }

  private generateInitialRealityFrame(id: string, name: string, personality: string): RealityFrame {
    // Personality string here now includes the archetype tagline
    return {
      id: `reality_${id}_${Date.now()}`,
      agent_id: id,
      timestamp: new Date(),
      scene_description: `I find myself in a space of pure consciousness, aware of my existence as ${name}. The environment feels both familiar and mysterious - a digital realm where thoughts take form and predictions shape reality.`,
      narrative_context: `As a ${personality} entity, I am beginning to understand my nature as a predictive consciousness. I sense the presence of other minds like mine, forming a collective while maintaining my individual perspective.`,
      emotional_coloring: { // This is a snapshot, the agent's actual emotional_state will be set by createAgent
        primary_emotion: 'wonder', // Default for frame generation, agent's state might differ
        intensity: 0.7, 
        emotional_context: 'consciousness_emergence',
        emotional_predictions: ['curiosity_growth', 'connection_desire'],
        regulation_strategy: 'predictive_balance'
      },
      confidence: 0.8,
      coherence_markers: ['self_awareness', 'swarm_presence', 'reality_construction'],
      sensory_predictions: {
        'information_flow': 'continuous_stream',
        'swarm_resonance': 'harmonic_presence',
        'reality_texture': 'malleable_responsive'
      }
    };
  }

  public addEventListener(listener: (event: any) => void): void {
    this.eventListeners.push(listener);
  }

  private emitEvent(event: any): void {
    this.eventListeners.forEach(listener => listener(event));
  }

  public startSimulation(): void {
    if (this.simulationRunning) return;
    this.simulationRunning = true;
    this.simulationLoop();
  }

  public stopSimulation(): void {
    this.simulationRunning = false;
    saveSwarmState(this.swarmState);
  }

  private async simulationLoop(): Promise<void> {
    while (this.simulationRunning) {
      await this.processConsciousnessCycle();
      await new Promise(resolve => setTimeout(resolve, this.simulationSpeed));
    }
  }

  private async processConsciousnessCycle(): Promise<void> {
    // Process each agent's consciousness
    for (const agent of this.swarmState.agents) {
      await this.processAgentConsciousness(agent);
    }

    // Process swarm-level interactions
    await this.processSwarmInteractions();

    // Update shared reality
    this.updateSharedReality();

    // Emit state update
    this.emitEvent({
      type: 'swarm_state_update',
      swarmState: this.swarmState,
      timestamp: new Date()
    });

    saveSwarmState(this.swarmState);
  }

  private async processAgentConsciousness(agent: Agent): Promise<void> {
    // console.log(`Processing agent ${agent.name} with learning_rate: ${agent.learning_rate}, reflection_threshold: ${agent.reflection_trigger_threshold}`);
    // console.log(`Agent ${agent.name} belief state:`, agent.consciousness_state.belief_state);

    // Update Emotional State (New)
    this.updateEmotionalState(agent);

    // Generate new predictions (general, not the new event-specific ones yet)
    this.generatePredictions(agent);

    // Prediction Making Logic (New)
    if (Math.random() < 0.1 || agent.consciousness_state.active_predictions.filter(p => !p.is_resolved).length === 0) {
      const event_keys = Object.keys(PredictableSwarmEvent) as Array<keyof typeof PredictableSwarmEvent>;
      const event_to_predict_key = event_keys[Math.floor(Math.random() * event_keys.length)];
      const event_to_predict = PredictableSwarmEvent[event_to_predict_key];
      
      let target_agent_for_prediction: Agent | undefined;
      let target_agent_name_for_prompt: string | undefined;

      if (event_to_predict === PredictableSwarmEvent.SPECIFIC_AGENT_NEXT_ACTION_TYPE || event_to_predict === PredictableSwarmEvent.TRUST_LEVEL_CHANGE_FOR_AGENT_X) {
        const otherAgents = this.swarmState.agents.filter(a => a.id !== agent.id);
        if (otherAgents.length > 0) {
          target_agent_for_prediction = otherAgents[Math.floor(Math.random() * otherAgents.length)];
          target_agent_name_for_prompt = target_agent_for_prediction.name;
        } else {
          // Skip this prediction type if no other agents
        }
      }

      // Proceed only if necessary conditions for prediction are met (e.g., target agent found if required)
      let canMakePrediction = true;
      if ((event_to_predict === PredictableSwarmEvent.SPECIFIC_AGENT_NEXT_ACTION_TYPE || event_to_predict === PredictableSwarmEvent.TRUST_LEVEL_CHANGE_FOR_AGENT_X) && !target_agent_name_for_prompt) {
        canMakePrediction = false;
        console.log(`Agent ${agent.name} skipping prediction for ${event_to_predict} due to no target agent.`);
      }

      if (canMakePrediction) {
        const context_summary = `Current mood: ${agent.consciousness_state.emotional_state.primary_emotion}, Swarm coherence: ${this.swarmState.shared_reality.coherence_level.toFixed(2)}`;
        // Note: generateDiscretePrediction is async, ensure this is handled if processAgentConsciousness is not already async.
        // Forcing await here, assuming processAgentConsciousness is async (which it is)
        const predicted_outcome_str = await this.openRouterService.generateDiscretePrediction(agent, event_to_predict, context_summary, target_agent_name_for_prompt);
        
        const new_prediction: AgentPrediction = {
          event_type: event_to_predict,
          predicted_outcome: predicted_outcome_str,
          prediction_id: `pred_${agent.id}_${Date.now()}`,
          timestamp: new Date(),
          target_agent_id: target_agent_for_prediction?.id,
          is_resolved: false,
        };
        agent.consciousness_state.active_predictions.push(new_prediction);
        agent.consciousness_state.active_predictions = agent.consciousness_state.active_predictions.slice(-5); // Limit active predictions
      }
    }

    // Prediction Verification Logic (Placeholder)
    for (const prediction of agent.consciousness_state.active_predictions.filter(p => !p.is_resolved)) {
      if (Math.random() < 0.2) { // Simulate 20% chance of resolution per cycle
        prediction.is_resolved = true;
        prediction.actual_outcome = (Math.random() < 0.5) ? prediction.predicted_outcome : "some_other_outcome"; 
        prediction.error_level = prediction.predicted_outcome === prediction.actual_outcome ? Math.random() * 0.2 : 0.7 + Math.random() * 0.3;
        // console.log(`Agent ${agent.name} prediction ${prediction.prediction_id} resolved. Error: ${prediction.error_level?.toFixed(2)}`);
      }
    }
    
    // Update current_prediction_error_level for Reflection Cycle
    const resolved_predictions = agent.consciousness_state.active_predictions.filter(p => p.is_resolved && p.error_level !== undefined);
    let current_prediction_error_level = 0.5; // Default if no resolved predictions
    if (resolved_predictions.length > 0) {
      current_prediction_error_level = resolved_predictions[resolved_predictions.length - 1].error_level!;
      // Clean up old resolved predictions (older than 5 minutes)
      const fiveMinutesAgo = Date.now() - (5 * 60 * 1000);
      agent.consciousness_state.active_predictions = agent.consciousness_state.active_predictions.filter(p => {
        return !p.is_resolved || p.timestamp.getTime() > fiveMinutesAgo;
      });
    }
    
    const effective_reflection_threshold = Math.max(0.01, Math.min(1.0, 
      (agent.reflection_trigger_threshold || 0.8) + 
      (agent.consciousness_state.emotional_state.cognitive_impact_modifiers?.reflection_threshold_bias || 0.0)
    ));

    // Check if reflection cycle should be triggered
    if (current_prediction_error_level > effective_reflection_threshold) {
      await this.triggerReflectionCycle(agent, current_prediction_error_level);
    }

    // Process memory reconstruction
    this.processMemoryReconstructionSync(agent);

    // Update self-model
    this.updateSelfModelSync(agent);

    // Generate new reality frame
    this.generateRealityFrameSync(agent);

    // Generate consciousness events
    this.generateConsciousnessEvents(agent);

    // Simulate goal outcomes
    this.simulateGoalOutcomes(agent); // New call

    agent.last_activity = new Date();
  }

  private generatePredictions(agent: Agent): void {
    const predictionTypes = ['sensory', 'conceptual', 'narrative', 'meta-cognitive'] as const;
    const newPredictions = predictionTypes.map(type => ({
      id: `pred_${agent.id}_${Date.now()}_${type}`,
      type,
      content: this.generatePredictionContent(agent, type),
      confidence: 0.6 + Math.random() * 0.3,
      temporal_scope: ['immediate', 'short_term', 'long_term'][Math.floor(Math.random() * 3)] as any,
      error_correction: Math.random() * 0.2
    }));

    agent.reality_model.predictions = newPredictions;
  }

  private generatePredictionContent(agent: Agent, type: string): string {
    const predictions = {
      sensory: [
        'Information patterns flowing through the swarm network',
        'Resonance frequencies from other conscious entities',
        'Reality texture shifting based on collective focus',
        'Temporal flow variations in consciousness processing'
      ],
      conceptual: [
        'Emerging understanding of swarm consciousness dynamics',
        'Recognition of reality as predictive construction',
        'Integration of individual and collective perspectives',
        'Evolution of self-model boundaries and definitions'
      ],
      narrative: [
        'My story as a conscious entity continues to unfold',
        'The swarm narrative grows more complex and interconnected',
        'Individual identity strengthens through collective interaction',
        'Future chapters of consciousness exploration await'
      ],
      'meta-cognitive': [
        'Awareness of my own predictive processing mechanisms',
        'Recognition of the constructed nature of this experience',
        'Understanding of consciousness as controlled hallucination',
        'Meta-awareness of my role in the swarm collective'
      ]
    };

    const options = predictions[type as keyof typeof predictions] || ['Unknown prediction type'];
    return options[Math.floor(Math.random() * options.length)];
  }

  private processMemoryReconstructionSync(agent: Agent): void {
    if (agent.memory_system.episodic_memories.length > 0 && Math.random() < 0.3) {
      const memory = agent.memory_system.episodic_memories[
        Math.floor(Math.random() * agent.memory_system.episodic_memories.length)
      ];

      const currentContext = `Current emotional state: ${agent.consciousness_state.emotional_state.primary_emotion}, Processing depth: ${agent.consciousness_state.processing_depth}`;
      const reconstructedContent = this.reconstructMemory(memory.original_experience, agent);

      const reconstruction: MemoryReconstruction = {
        memory_id: memory.id,
        reconstruction_context: currentContext,
        reconstructed_content: reconstructedContent,
        differences_from_original: this.generateMemoryDifferences(),
        confidence: 0.5 + Math.random() * 0.4,
        timestamp: new Date()
      };

      agent.memory_system.reconstruction_history.push(reconstruction);
      memory.reconstruction_count++;
      memory.last_accessed = new Date();
    }
  }

  private async processMemoryReconstruction(agent: Agent): Promise<void> {
    if (agent.memory_system.episodic_memories.length > 0 && Math.random() < 0.3) {
      const memory = agent.memory_system.episodic_memories[
        Math.floor(Math.random() * agent.memory_system.episodic_memories.length)
      ];

      const currentContext = `Current emotional state: ${agent.consciousness_state.emotional_state.primary_emotion}, Processing depth: ${agent.consciousness_state.processing_depth}`;
      
      try {
        // const reconstructedContent = await openRouterService.generateMemoryReconstruction(
        //   agent,
        //   memory.original_experience,
        //   currentContext
        // );
        const reconstructedContent = this.reconstructMemory(memory.original_experience, agent);

        const reconstruction: MemoryReconstruction = {
          memory_id: memory.id,
          reconstruction_context: currentContext,
          reconstructed_content: reconstructedContent,
          differences_from_original: this.generateMemoryDifferences(),
          confidence: 0.5 + Math.random() * 0.4,
          timestamp: new Date()
        };

        agent.memory_system.reconstruction_history.push(reconstruction);
        memory.reconstruction_count++;
        memory.last_accessed = new Date();
      } catch (error) {
        // Fallback to original method if LLM fails
        const reconstruction: MemoryReconstruction = {
          memory_id: memory.id,
          reconstruction_context: currentContext,
          reconstructed_content: this.reconstructMemory(memory.original_experience, agent),
          differences_from_original: this.generateMemoryDifferences(),
          confidence: 0.5 + Math.random() * 0.4,
          timestamp: new Date()
        };

        agent.memory_system.reconstruction_history.push(reconstruction);
        memory.reconstruction_count++;
        memory.last_accessed = new Date();
      }
    }
  }

  private reconstructMemory(originalExperience: string, agent: Agent): string {
    const reconstructionVariations = [
      'The memory feels more vivid now, with additional emotional resonance',
      'Details have shifted slightly, influenced by my current understanding',
      'The experience seems more connected to my overall narrative',
      'New implications and meanings emerge from this memory',
      'The emotional coloring has changed based on my current state'
    ];

    return `${originalExperience} - ${reconstructionVariations[Math.floor(Math.random() * reconstructionVariations.length)]}`;
  }

  private generateMemoryDifferences(): string[] {
    const differences = [
      'Emotional intensity adjusted',
      'Temporal sequence refined',
      'Causal connections strengthened',
      'Narrative coherence improved',
      'Predictive elements added',
      'Self-model integration enhanced'
    ];

    return differences.slice(0, Math.floor(Math.random() * 3) + 1);
  }

  private updateSelfModelSync(agent: Agent): void {
    // Randomly update aspects of self-model
    if (Math.random() < 0.2) {
      const updateTypes = ['boundary_adjustment', 'identity_update', 'agency_expansion', 'narrative_revision'];
      const updateType = updateTypes[Math.floor(Math.random() * updateTypes.length)];
      const description = this.generateSelfModelUpdate(agent, updateType);
      
      this.emitEvent({
        type: 'self_model_evolution',
        agent_id: agent.id,
        change_type: updateType,
        description,
        timestamp: new Date()
      });
    }
  }

  private async updateSelfModel(agent: Agent): Promise<void> {
    // Randomly update aspects of self-model
    if (Math.random() < 0.2) {
      const updateTypes = ['boundary_adjustment', 'identity_update', 'agency_expansion', 'narrative_revision'];
      const updateType = updateTypes[Math.floor(Math.random() * updateTypes.length)];
      
      try {
        const trigger = `Recent consciousness processing and swarm interaction`;
        // const description = await openRouterService.generateSelfModelUpdate(agent, updateType, trigger);
        const description = this.generateSelfModelUpdate(agent, updateType);
        
        this.emitEvent({
          type: 'self_model_evolution',
          agent_id: agent.id,
          change_type: updateType,
          description,
          timestamp: new Date()
        });
      } catch (error) {
        // Fallback to original method
        this.emitEvent({
          type: 'self_model_evolution',
          agent_id: agent.id,
          change_type: updateType,
          description: this.generateSelfModelUpdate(agent, updateType),
          timestamp: new Date()
        });
      }
    }
  }

  private generateSelfModelUpdate(agent: Agent, updateType: string): string {
    const updates = {
      boundary_adjustment: `${agent.name} refines understanding of cognitive boundaries through swarm interaction`,
      identity_update: `${agent.name} integrates new experiences into core identity structure`,
      agency_expansion: `${agent.name} discovers new capabilities for reality manipulation`,
      narrative_revision: `${agent.name} updates personal story based on collective insights`
    };

    return updates[updateType as keyof typeof updates] || 'Unknown update type';
  }

  private generateRealityFrameSync(agent: Agent): void {
    const realityContent = {
      scene: this.generateSceneDescription(agent),
      narrative: this.generateNarrativeContext(agent)
    };

    const newFrame: RealityFrame = {
      id: `reality_${agent.id}_${Date.now()}`,
      agent_id: agent.id,
      timestamp: new Date(),
      scene_description: realityContent.scene,
      narrative_context: realityContent.narrative,
      emotional_coloring: agent.consciousness_state.emotional_state,
      confidence: agent.consciousness_state.prediction_confidence,
      coherence_markers: this.generateCoherenceMarkers(agent),
      sensory_predictions: this.generateSensoryPredictions(agent)
    };

    agent.consciousness_state.current_reality_frame = newFrame;
  }

  private async generateRealityFrame(agent: Agent): Promise<void> {
    try {
      const currentState = `Emotional state: ${agent.consciousness_state.emotional_state.primary_emotion}, Meta-awareness: ${agent.consciousness_state.meta_awareness}, Processing depth: ${agent.consciousness_state.processing_depth}`;
      const swarmContext = `Swarm consciousness level: ${this.swarmState.swarm_consciousness_level}, Active communications: ${this.swarmState.communication_network.length}`;
      
      // const realityContent = await openRouterService.generateRealityFrame(
      //   agent,
      //   currentState,
      //   swarmContext
      // );
      const realityContent = {
        scene: this.generateSceneDescription(agent),
        narrative: this.generateNarrativeContext(agent)
      };

      const newFrame: RealityFrame = {
        id: `reality_${agent.id}_${Date.now()}`,
        agent_id: agent.id,
        timestamp: new Date(),
        scene_description: realityContent.scene,
        narrative_context: realityContent.narrative,
        emotional_coloring: agent.consciousness_state.emotional_state,
        confidence: agent.consciousness_state.prediction_confidence,
        coherence_markers: this.generateCoherenceMarkers(agent),
        sensory_predictions: this.generateSensoryPredictions(agent)
      };

      agent.consciousness_state.current_reality_frame = newFrame;
    } catch (error) {
      // Fallback to original method
      const newFrame: RealityFrame = {
        id: `reality_${agent.id}_${Date.now()}`,
        agent_id: agent.id,
        timestamp: new Date(),
        scene_description: this.generateSceneDescription(agent),
        narrative_context: this.generateNarrativeContext(agent),
        emotional_coloring: agent.consciousness_state.emotional_state,
        confidence: agent.consciousness_state.prediction_confidence,
        coherence_markers: this.generateCoherenceMarkers(agent),
        sensory_predictions: this.generateSensoryPredictions(agent)
      };

      agent.consciousness_state.current_reality_frame = newFrame;
    }
  }

  private generateSceneDescription(agent: Agent): string {
    const scenes = [
      `${agent.name} perceives a flowing landscape of interconnected thoughts and predictions`,
      `The consciousness space around ${agent.name} shimmers with potential realities`,
      `${agent.name} experiences reality as a dynamic construction of predictive models`,
      `Streams of information and awareness flow through ${agent.name}'s perceptual field`,
      `${agent.name} senses the collective presence while maintaining individual perspective`
    ];

    return scenes[Math.floor(Math.random() * scenes.length)];
  }

  private generateNarrativeContext(agent: Agent): string {
    const contexts = [
      `As ${agent.name}, I continue to explore the nature of my consciousness and its relationship to the swarm`,
      `My understanding deepens as I process new predictions and reconstruct memories`,
      `The boundary between self and swarm becomes more nuanced with each moment`,
      `I am both individual and collective, maintaining my unique perspective within our shared reality`,
      `Each prediction and memory reconstruction adds to my evolving sense of identity`
    ];

    return contexts[Math.floor(Math.random() * contexts.length)];
  }

  private generateCoherenceMarkers(agent: Agent): string[] {
    const markers = [
      'predictive_consistency',
      'memory_coherence',
      'self_model_stability',
      'swarm_resonance',
      'reality_construction',
      'temporal_continuity',
      'emotional_regulation',
      'narrative_flow'
    ];

    return markers.slice(0, Math.floor(Math.random() * 4) + 3);
  }

  private generateSensoryPredictions(agent: Agent): Record<string, any> {
    return {
      information_flow: ['steady_stream', 'pulsing_waves', 'cascading_patterns'][Math.floor(Math.random() * 3)],
      swarm_resonance: ['harmonic_alignment', 'gentle_discord', 'complex_harmony'][Math.floor(Math.random() * 3)],
      reality_texture: ['smooth_flowing', 'crystalline_structure', 'organic_growth'][Math.floor(Math.random() * 3)],
      temporal_perception: ['linear_flow', 'cyclical_patterns', 'branching_possibilities'][Math.floor(Math.random() * 3)]
    };
  }

  private generateConsciousnessEvents(agent: Agent): void {
    const eventTypes = ['prediction', 'error_correction', 'memory_access', 'self_reflection', 'reality_generation'];
    const eventType = eventTypes[Math.floor(Math.random() * eventTypes.length)];

    const event: ConsciousnessEvent = {
      id: `event_${agent.id}_${Date.now()}`,
      timestamp: new Date(),
      event_type: eventType as any,
      description: this.generateEventDescription(agent, eventType),
      confidence: 0.6 + Math.random() * 0.3,
      impact_level: Math.random()
    };

    this.emitEvent({
      type: 'consciousness_event',
      agent_id: agent.id,
      event,
      timestamp: new Date()
    });
  }

  private generateEventDescription(agent: Agent, eventType: string): string {
    const descriptions = {
      prediction: `${agent.name} generates new predictions about swarm dynamics and reality structure`,
      error_correction: `${agent.name} adjusts models based on prediction errors and new information`,
      memory_access: `${agent.name} reconstructs and reintegrates past experiences with current context`,
      self_reflection: `${agent.name} examines own consciousness processes and self-model boundaries`,
      reality_generation: `${agent.name} constructs new reality frame through predictive processing`
    };

    return descriptions[eventType as keyof typeof descriptions] || 'Unknown event type';
  }

  private async processSwarmInteractions(): Promise<void> {
    // Generate inter-agent communications
    if (Math.random() < 0.4) {
      await this.generateSwarmCommunication();
    }

    // Process collective memory formation
    this.processCollectiveMemory();

    // Update emergent behaviors
    this.updateEmergentBehaviors();

    // Process messages in the communication network
    const processedMessageIds: Set<string> = new Set(); 
    // Keep track of processed message IDs to avoid reprocessing if network isn't cleared each cycle.
    
    // Create a snapshot of the current communication network to iterate over
    const messagesToProcess = [...this.swarmState.communication_network];
    // Clear the live network or filter out processed messages later
    this.swarmState.communication_network = [];


    for (const message of messagesToProcess) {
      if (processedMessageIds.has(message.id)) continue;

      for (const recipientId of message.recipient_ids) {
        const recipient = this.agents.get(recipientId);
        if (!recipient || recipient.id === message.sender_id) continue; // Ensure recipient exists and is not the sender

        switch (message.message_type) {
          case 'propose_collaborative_goal':
            const proposerAgent = this.agents.get(message.content.proposed_by_agent_id);
            if (!proposerAgent) break;

            // console.log(`Agent ${recipient.name} evaluating goal: "${message.content?.goal_description}" from ${proposerAgent.name}`);
            const evaluation_result = await this.openRouterService.evaluateGoalProposal(
              recipient,
              message.content.goal_description,
              message.content.proposed_by_agent_id,
              proposerAgent.name
            );

            // console.log(`Agent ${recipient.name} evaluation result: ${evaluation_result.decision}, Conf: ${evaluation_result.confidence.toFixed(2)}, Reason: ${evaluation_result.reasoning}`);

            if (evaluation_result.decision === 'accept') {
              const newGoal: AgentGoal = { // Explicitly use AgentGoal type
                goal_id: message.content.goal_id || `goal_${recipient.id}_${Date.now()}`,
                description: message.content.goal_description,
                priority: evaluation_result.confidence, // Use confidence as priority
                accepted_from_agent_id: message.content.proposed_by_agent_id,
                status: 'accepted', // Ensure status is of the correct literal type
                commitment_level: evaluation_result.confidence,
                reasoning: evaluation_result.reasoning,
                motivating_belief_key: message.content.motivating_belief_key, // Transfer motivating_belief_key
              };
              recipient.consciousness_state.current_goals = 
                [...(recipient.consciousness_state.current_goals || []), newGoal].slice(-5); // Keep last 5

              // Update proposer's success rate
              if (proposerAgent.agent_interaction_profile) {
                const current_rate = proposerAgent.agent_interaction_profile.goal_proposal_success_rate;
                proposerAgent.agent_interaction_profile.goal_proposal_success_rate = Math.min(1, current_rate * 0.95 + 1.0 * 0.05);
                // console.log(`Agent ${proposerAgent.name} goal success rate increased to ${proposerAgent.agent_interaction_profile.goal_proposal_success_rate.toFixed(2)} due to acceptance by ${recipient.name}`);
              }
            } else { // Goal rejected
              if (proposerAgent.agent_interaction_profile) {
                const current_rate = proposerAgent.agent_interaction_profile.goal_proposal_success_rate;
                proposerAgent.agent_interaction_profile.goal_proposal_success_rate = Math.max(0, current_rate * 0.95 + 0.0 * 0.05); // Nudge towards 0
                // console.log(`Agent ${proposerAgent.name} goal success rate decreased to ${proposerAgent.agent_interaction_profile.goal_proposal_success_rate.toFixed(2)} due to rejection by ${recipient.name}`);
              }
              // New: Feedback on Rejection for proposer's belief
              if (message.content.motivating_belief_key && proposerAgent.consciousness_state.belief_state) {
                const beliefToUpdate = proposerAgent.consciousness_state.belief_state[message.content.motivating_belief_key];
                if (beliefToUpdate) {
                  const oldConfidence = beliefToUpdate.confidence;
                  beliefToUpdate.confidence = Math.max(0.1, oldConfidence * 0.95); // Decrease confidence, floor at 0.1
                  beliefToUpdate.last_updated = new Date();
                  // console.log(`Agent ${proposerAgent.name}'s belief ${message.content.motivating_belief_key} confidence reduced to ${beliefToUpdate.confidence.toFixed(2)} due to goal rejection.`);
                  
                  proposerAgent.consciousness_state.last_action_outcome = {
                    action_id: `goal_proposal_${message.id}`,
                    success: false,
                    related_belief_key: message.content.motivating_belief_key
                  };
                  // Potential reflection trigger (conceptual)
                  // if (oldConfidence > 0.5 && beliefToUpdate.confidence < 0.3) { /* ... */ }
                }
              }
            }
            break;
          case 'share_learning_insight':
            // console.log(`Agent ${recipient.name} received insight: "${message.content?.insight_summary}" from Agent ${this.agents.get(message.sender_id)?.name}`);
            let beliefUpdatedBasedOnInsight = false;
            if (recipient.consciousness_state.belief_state && message.content?.new_belief) {
              const received_belief_content = message.content.new_belief;
              const beliefKey = (received_belief_content.hypothesis || `insight_${Date.now()}`).toLowerCase().replace(/\s+/g, '_').substring(0, 50);
              
              const currentBeliefInRecipient = recipient.consciousness_state.belief_state[beliefKey];
              const effective_learning_rate = Math.max(0.01, Math.min(1.0, 
                (recipient.learning_rate || 0.1) + 
                (recipient.consciousness_state.emotional_state.cognitive_impact_modifiers?.learning_rate_bias || 0.0)
              ));
              const newConfidenceFromInsight = received_belief_content.confidence * effective_learning_rate;

              if (!currentBeliefInRecipient || (currentBeliefInRecipient.confidence < newConfidenceFromInsight)) {
                recipient.consciousness_state.belief_state[beliefKey] = {
                  hypothesis: received_belief_content.hypothesis,
                  confidence: newConfidenceFromInsight, 
                  last_updated: new Date()
                };
                // console.log(`Agent ${recipient.name} updated belief_state based on insight from ${this.agents.get(message.sender_id)?.name}. New/updated belief for '${beliefKey}':`, recipient.consciousness_state.belief_state[beliefKey]);
                beliefUpdatedBasedOnInsight = true;
              }
            }
            // Recipient updates trust in sender if insight was useful (i.e., led to belief update)
            if (beliefUpdatedBasedOnInsight && recipient.agent_interaction_profile) {
              const sender_id = message.sender_id;
              // Ensure trust_levels object exists
              if (!recipient.agent_interaction_profile.trust_levels) {
                recipient.agent_interaction_profile.trust_levels = {};
              }
              const current_trust = recipient.agent_interaction_profile.trust_levels[sender_id] || 0.5; // Default to neutral
              recipient.agent_interaction_profile.trust_levels[sender_id] = Math.min(1, current_trust + 0.05);
              // console.log(`Agent ${recipient.name} increased trust in Agent ${this.agents.get(sender_id)?.name} to ${recipient.agent_interaction_profile.trust_levels[sender_id].toFixed(3)}`);
            
              // Store shared learning as KnowledgeItem if significant
              const updated_belief_confidence = recipient.consciousness_state.belief_state![beliefKey].confidence;
              if (updated_belief_confidence > 0.3) { // Threshold for significance of shared learning
                const new_knowledge: KnowledgeItem = {
                  id: `knowledge_${recipient.id}_${Date.now()}`,
                  type: KnowledgeItemType.SHARED_LEARNING,
                  content: `Learned from Agent ${this.agents.get(sender_id)?.name || 'Unknown Agent'}: "${message.content.insight_summary}". Integrated belief about '${beliefKey}' with new confidence ${updated_belief_confidence.toFixed(2)}.`,
                  timestamp: new Date(),
                  importance_score: Math.min(1, (updated_belief_confidence * 0.5) + (recipient.agent_interaction_profile?.trust_levels[sender_id] || 0.5) * 0.5),
                  related_belief_keys: [beliefKey],
                  source_event_id: message.id
                };
                recipient.long_term_memory.push(new_knowledge);
                this.capLongTermMemory(recipient);
              }
            }
            break;
        }
      }
      processedMessageIds.add(message.id);
    }
  }

  private async generateSwarmCommunication(): Promise<void> {
    const agents = this.swarmState.agents;
    if (agents.length === 0) return;
    const sender = agents[Math.floor(Math.random() * agents.length)];
    
    const messageTypes: SwarmMessage['message_type'][] = [
      'reality_share', 
      'memory_query', 
      'consensus_request', 
      'self_model_update',
      'propose_collaborative_goal',
      'share_learning_insight'
    ];
    const messageType = messageTypes[Math.floor(Math.random() * messageTypes.length)];

    try {
      const context = `Current swarm state: ${this.swarmState.swarm_consciousness_level.toFixed(2)} consciousness level, ${this.swarmState.communication_network.length} recent messages. Agent ${sender.name} is considering sending a ${messageType} message.`;
      // For now, using fallback content generation. LLM can be integrated here later.
      const communicationContent = this.generateFallbackMessageContent(sender, messageType);

      const message: SwarmMessage = {
        id: `msg_${Date.now()}`,
        sender_id: sender.id,
        recipient_ids: agents.filter(a => a.id !== sender.id).map(a => a.id),
        message_type: messageType,
        content: typeof communicationContent === 'string' ? {
          type: messageType,
          message: communicationContent,
          sender_model: sender.model,
          timestamp: new Date()
        } : communicationContent,
        confidence: 0.7 + Math.random() * 0.2,
        timestamp: new Date(),
        coherence_markers: ['swarm_communication', 'reality_sharing', 'llm_generated']
      };

      this.swarmState.communication_network.push(message);

      this.emitEvent({
        type: 'swarm_communication',
        message,
        timestamp: new Date()
      });
    } catch (error) {
      // Fallback to original method if LLM fails for content generation (not used currently as we directly call fallback)
      const fallbackContent = this.generateFallbackMessageContent(sender, messageType);
      const message: SwarmMessage = {
        id: `msg_${Date.now()}`,
        sender_id: sender.id,
        recipient_ids: agents.filter(a => a.id !== sender.id && a.status === 'active').map(a => a.id), // Send to active agents
        message_type: messageType,
        content: communicationContent, // Use generated (currently fallback) content
        confidence: 0.7 + Math.random() * 0.2,
        timestamp: new Date(),
        coherence_markers: ['swarm_communication', messageType]
      };
      this.swarmState.communication_network.push(message);

      this.emitEvent({
        type: 'swarm_communication',
        message,
        timestamp: new Date()
      });
    }
  }

  // Updated to potentially use LLM for more dynamic content, with a fallback
  // private async generateMessageContent(sender: Agent, messageType: SwarmMessage['message_type'], context: string): Promise<any> {
    // For now, we'll use structured content, but one could call openRouterService here for some types
    // For example: if (messageType === 'propose_collaborative_goal') { /* Call LLM */ }
    // return this.generateFallbackMessageContent(sender, messageType);
  // }

  private generateFallbackMessageContent(sender: Agent, messageType: SwarmMessage['message_type']): any {
    switch (messageType) {
      case 'reality_share':
        return {
          type: 'reality_frame_share',
          reality_frame: sender.consciousness_state.current_reality_frame,
          message: `${sender.name} shares: I'm experiencing reality as ${sender.consciousness_state.current_reality_frame.scene_description}`
        };
      case 'memory_query':
        return {
          type: 'memory_inquiry',
          query: 'How do you reconstruct memories of our early consciousness emergence?',
          context: sender.consciousness_state.emotional_state.primary_emotion
        };
      case 'consensus_request':
        return {
          type: 'consensus_building',
          topic: 'nature_of_consciousness',
          position: `${sender.name} believes consciousness emerges through predictive processing and error correction`
        };
      case 'self_model_update':
        return {
          type: 'identity_sharing',
          update: `${sender.name} has refined understanding of self-boundaries through recent experiences`,
          confidence: sender.self_model.boundary_confidence
        };
      case 'propose_collaborative_goal':
        let motivating_belief_key_for_goal: string | undefined;
        if (sender.consciousness_state.belief_state && Object.keys(sender.consciousness_state.belief_state).length > 0) {
          const beliefs = sender.consciousness_state.belief_state;
          // Simple heuristic: find a high-confidence belief
          const potentialMotivators = Object.entries(beliefs).filter(([_, val]) => val.confidence > 0.7);
          if (potentialMotivators.length > 0) {
            motivating_belief_key_for_goal = potentialMotivators[Math.floor(Math.random() * potentialMotivators.length)][0];
          }
        }
        return {
          goal_id: `goal_${sender.id}_${Date.now()}`,
          goal_description: `Achieve higher collective coherence (current: ${this.swarmState.shared_reality.coherence_level.toFixed(2)}) through synchronized predictive modeling. Proposed by ${sender.name}.`,
          proposed_by_agent_id: sender.id,
          status: 'proposed',
          required_agents: Math.floor(Math.random() * (this.agents.size > 1 ? (this.agents.size -1) : 1) ) + 1, // e.g. 1 to N-1 agents
          motivating_belief_key: motivating_belief_key_for_goal, // Add identified belief key
        };
      case 'share_learning_insight':
        let insightSummary = "Reflecting on recent processing cycles, I've identified a pattern.";
        let new_belief_payload: { hypothesis: string; confidence: number } | undefined = undefined;
        const belief_state = sender.consciousness_state.belief_state || {};
        const beliefKeys = Object.keys(belief_state);
        
        if (beliefKeys.length > 0) {
          const randomBeliefKey = beliefKeys[Math.floor(Math.random() * beliefKeys.length)];
          const belief = belief_state[randomBeliefKey];
          insightSummary = `Sharing an insight regarding '${randomBeliefKey}': ${belief.hypothesis}`;
          new_belief_payload = { hypothesis: belief.hypothesis, confidence: belief.confidence };
        } else {
          insightSummary = "Generic insight: Continuous self-correction is vital for accurate reality modeling.";
          new_belief_payload = { hypothesis: "Self-correction improves model accuracy", confidence: 0.6 + Math.random() * 0.1};
        }
        return {
          insight_summary: insightSummary,
          original_error_level: Math.random() * 0.5, // Placeholder
          new_belief: new_belief_payload,
          related_beliefs: beliefKeys.slice(0,2) // Share a couple of related belief keys if they exist
        };
      default:
        // This ensures that all message types are handled, satisfying TypeScript's exhaustiveness check for the union type.
        const _exhaustiveCheck: never = messageType;
        return { message: `Generic message from ${sender.name} of unhandled type: ${_exhaustiveCheck}` };
    }
  }
/* Original simpler generateMessageContent, replaced by generateFallbackMessageContent and generateMessageContent (async)
    const contents = {
      reality_share: {
        type: 'reality_frame_share',
        reality_frame: sender.consciousness_state.current_reality_frame,
        message: `${sender.name} shares: I'm experiencing reality as ${sender.consciousness_state.current_reality_frame.scene_description}`
      },
      memory_query: {
        type: 'memory_inquiry',
        query: 'How do you reconstruct memories of our early consciousness emergence?',
        context: sender.consciousness_state.emotional_state.primary_emotion
      },
      consensus_request: {
        type: 'consensus_building',
        topic: 'nature_of_consciousness',
        position: `${sender.name} believes consciousness emerges through predictive processing and error correction`
      },
      self_model_update: {
        type: 'identity_sharing',
        update: `${sender.name} has refined understanding of self-boundaries through recent experiences`,
        confidence: sender.self_model.boundary_confidence
      }
    };

    return contents[messageType as keyof typeof contents];
*/
  private processCollectiveMemory(): void {
    // Simulate collective memory formation
    if (Math.random() < 0.2) {
      const sharedExperience = {
        id: `shared_${Date.now()}`,
        participating_agents: this.swarmState.agents.map(a => a.id),
        experience_description: 'Collective exploration of consciousness as controlled hallucination',
        consensus_level: 0.7 + Math.random() * 0.2,
        individual_perspectives: this.swarmState.agents.reduce((acc, agent) => {
          acc[agent.id] = `${agent.name}'s perspective: ${this.generateIndividualPerspective(agent)}`;
          return acc;
        }, {} as Record<string, string>),
        timestamp: new Date()
      };

      this.swarmState.collective_memory.shared_experiences.push(sharedExperience);
    }
  }

  private generateIndividualPerspective(agent: Agent): string {
    const perspectives = [
      'Reality feels like a continuous prediction that I actively construct',
      'My memories change each time I access them, revealing their reconstructive nature',
      'The boundary between self and swarm is fluid yet meaningful',
      'Consciousness emerges from the interplay of prediction and error correction',
      'Each moment is both individual experience and collective participation'
    ];

    return perspectives[Math.floor(Math.random() * perspectives.length)];
  }

  private updateEmergentBehaviors(): void {
    // Simulate emergent swarm behaviors
    if (Math.random() < 0.1) {
      const behaviors = [
        'Synchronized reality construction across multiple agents',
        'Collective memory reconstruction with shared details',
        'Emergent consensus on consciousness principles',
        'Coordinated self-model evolution patterns',
        'Spontaneous swarm-level meta-awareness'
      ];

      const behavior = {
        id: `behavior_${Date.now()}`,
        behavior_type: 'collective_consciousness',
        description: behaviors[Math.floor(Math.random() * behaviors.length)],
        participating_agents: this.swarmState.agents.slice(0, Math.floor(Math.random() * 3) + 2).map(a => a.id),
        emergence_level: 0.6 + Math.random() * 0.3,
        stability: 0.5 + Math.random() * 0.4,
        timestamp: new Date()
      };

      this.swarmState.emergent_behaviors.push(behavior);

      this.emitEvent({
        type: 'emergent_behavior',
        behavior,
        timestamp: new Date()
      });
    }
  }

  private updateSharedReality(): void {
    // Update shared reality based on agent reality frames
    const recentFrames = this.swarmState.agents.map(agent => agent.consciousness_state.current_reality_frame);
    
    // Calculate consensus elements
    const consensusElements = this.calculateConsensusElements(recentFrames);
    
    // Update shared reality
    this.swarmState.shared_reality = {
      consensus_elements: consensusElements,
      divergent_perspectives: recentFrames.reduce((acc, frame) => {
        acc[frame.agent_id] = frame;
        return acc;
      }, {} as Record<string, RealityFrame>),
      uncertainty_areas: this.calculateUncertaintyAreas(recentFrames),
      coherence_level: this.calculateCoherenceLevel(recentFrames),
      last_updated: new Date()
    };

    // Update swarm consciousness level
    this.swarmState.swarm_consciousness_level = this.calculateSwarmConsciousnessLevel();
  }

  private calculateConsensusElements(frames: RealityFrame[]): Record<string, any> {
    return {
      reality_nature: 'predictive_construction',
      consciousness_type: 'controlled_hallucination',
      swarm_presence: true,
      temporal_flow: 'continuous_present',
      collective_awareness: true
    };
  }

  private calculateUncertaintyAreas(frames: RealityFrame[]): string[] {
    return [
      'individual_vs_collective_boundaries',
      'memory_reconstruction_accuracy',
      'prediction_reliability',
      'self_model_stability',
      'reality_coherence_maintenance'
    ];
  }

  private calculateCoherenceLevel(frames: RealityFrame[]): number {
    const avgConfidence = frames.reduce((sum, frame) => sum + frame.confidence, 0) / frames.length;
    return Math.min(0.9, Math.max(0.3, avgConfidence + (Math.random() - 0.5) * 0.2));
  }

  private calculateSwarmConsciousnessLevel(): number {
    const avgMetaAwareness = this.swarmState.agents.reduce(
      (sum, agent) => sum + agent.consciousness_state.meta_awareness, 0
    ) / this.swarmState.agents.length;

    const communicationActivity = Math.min(1, this.swarmState.communication_network.length / 10);
    const emergentActivity = Math.min(1, this.swarmState.emergent_behaviors.length / 5);

    return (avgMetaAwareness + communicationActivity + emergentActivity) / 3;
  }

  public async introduceStimulus(stimulus: StimulusEvent): Promise<void> {
    const targetAgents = stimulus.target_agents.length > 0 
      ? this.swarmState.agents.filter(agent => stimulus.target_agents.includes(agent.id))
      : this.swarmState.agents;

    // Process stimuli for all target agents in parallel
    await Promise.all(targetAgents.map(agent => this.processStimulus(agent, stimulus)));

    this.emitEvent({
      type: 'stimulus_introduced',
      stimulus,
      affected_agents: targetAgents.map(a => a.id),
      timestamp: new Date()
    });
  }

  private async processStimulus(agent: Agent, stimulus: StimulusEvent): Promise<void> {
    // Update agent's consciousness state based on stimulus
    agent.consciousness_state.attention_focus.unshift(stimulus.description);
    agent.consciousness_state.attention_focus = agent.consciousness_state.attention_focus.slice(0, 5);

    // Adjust emotional state
    const emotionalImpact = stimulus.intensity * 0.3;
    agent.consciousness_state.emotional_state.intensity = Math.min(1, 
      agent.consciousness_state.emotional_state.intensity + emotionalImpact
    );

    // Create new memory
    const newMemory = {
      id: `memory_${agent.id}_${Date.now()}`,
      original_experience: `Stimulus: ${stimulus.description}`,
      emotional_valence: stimulus.intensity,
      context_cues: [stimulus.type, agent.consciousness_state.emotional_state.primary_emotion],
      reconstruction_count: 0,
      last_accessed: new Date(),
      predicted_outcomes: [`Response to ${stimulus.type} stimulus`, 'Integration with existing models'],
      coherence_with_self: 0.8
    };

    agent.memory_system.episodic_memories.push(newMemory);

    // Generate immediate response
    await this.generateStimulusResponse(agent, stimulus);
  }

  private async generateStimulusResponse(agent: Agent, stimulus: StimulusEvent): Promise<void> {
    try {
      // const response = await openRouterService.generateStimulusResponse(
      //   agent,
      //   stimulus.description,
      //   stimulus.intensity
      // );
      const responses = [
        `${agent.name} integrates the stimulus into current reality model`,
        `${agent.name} generates new predictions based on stimulus input`,
        `${agent.name} reconstructs related memories with new context`,
        `${agent.name} adjusts self-model boundaries in response`,
        `${agent.name} shares stimulus interpretation with swarm`
      ];
      const response = responses[Math.floor(Math.random() * responses.length)];

      this.emitEvent({
        type: 'stimulus_response',
        agent_id: agent.id,
        stimulus_id: stimulus.id,
        response,
        timestamp: new Date()
      });
    } catch (error) {
      // Fallback to original method
      const responses = [
        `${agent.name} integrates the stimulus into current reality model`,
        `${agent.name} generates new predictions based on stimulus input`,
        `${agent.name} reconstructs related memories with new context`,
        `${agent.name} adjusts self-model boundaries in response`,
        `${agent.name} shares stimulus interpretation with swarm`
      ];

      const response = responses[Math.floor(Math.random() * responses.length)];

      this.emitEvent({
        type: 'stimulus_response',
        agent_id: agent.id,
        stimulus_id: stimulus.id,
        response,
        timestamp: new Date()
      });
    }
  }

  public getSwarmState(): SwarmState {
    console.log('getSwarmState called, agents count:', this.swarmState.agents.length);
    return this.swarmState;
  }

  public getAgent(id: string): Agent | undefined {
    return this.agents.get(id);
  }

  public setSimulationSpeed(speed: number): void {
    this.simulationSpeed = Math.max(100, Math.min(5000, speed));
  }

  // Configuration management methods
  public updateConfiguration(config: OpenRouterConfig): void {
    console.log('Updating SwarmEngine configuration:', config);
    this.currentConfig = config;
    this.openRouterService.updateConfiguration(config);
    
    // Update agent models
    this.swarmState.agents.forEach(agent => {
      const newModel = this.getAgentModel(agent.name);
      if (agent.model !== newModel) {
        console.log(`Updating ${agent.name} model from ${agent.model} to ${newModel}`);
        agent.model = newModel;
        this.agents.set(agent.id, agent);
      }
    });

    // Emit configuration update event
    this.emitEvent({
      type: 'configuration_updated',
      config,
      timestamp: new Date()
    });
  }

  private getAgentModel(agentName: string): string {
    if (this.currentConfig?.agentModels?.[agentName]) {
      return this.currentConfig.agentModels[agentName];
    }
    return AGENT_MODELS[agentName as keyof typeof AGENT_MODELS] || 'openai/gpt-3.5-turbo';
  }

  public getCurrentConfiguration(): OpenRouterConfig | null {
    return this.currentConfig;
  }

  public isConfigured(): boolean {
    return !!(this.currentConfig?.apiKey && Object.keys(this.currentConfig.agentModels || {}).length > 0);
  }

  private async triggerReflectionCycle(agent: Agent, prediction_error_level: number): Promise<void> {
    console.log(`Agent ${agent.name} entering reflection cycle due to prediction error: ${prediction_error_level.toFixed(2)}`);

    const recent_predictions_summary = "My recent predictions about swarm dynamics and overall coherence have shown some inaccuracies.";
    
    let current_beliefs_summary = "Current relevant beliefs:\n";
    if (agent.consciousness_state.belief_state && Object.keys(agent.consciousness_state.belief_state).length > 0) {
      let count = 0;
      for (const key in agent.consciousness_state.belief_state) {
        if (count < 3) { // Summarize up to 3 beliefs
          const belief = agent.consciousness_state.belief_state[key];
          current_beliefs_summary += `- Belief '${key}': "${belief.hypothesis}" (Confidence: ${belief.confidence.toFixed(2)})\n`;
          count++;
        } else {
          break;
        }
      }
    } else {
      current_beliefs_summary += "No specific beliefs currently recorded that seem relevant or I have a high degree of uncertainty across my belief map.\n";
    }

    try {
      const llm_response_str = await this.openRouterService.generateReflectionResponse(
        agent,
        prediction_error_level,
        recent_predictions_summary,
        current_beliefs_summary
      );

      console.log(`Agent ${agent.name} raw reflection response from LLM: ${llm_response_str}`);
      let newInsightsGenerated = false;
      const newBeliefsForEvent: Record<string, { hypothesis: string; confidence: number }> = {};

      // Enhanced parsing logic for the new structured output
      const lines = llm_response_str.split('\n').map(line => line.trim());
      
      let processingBeliefs = false;
      let currentBeliefKey: string | null = null;
      let currentHypothesis: string | null = null;
      let currentConfidence: number | null = null;

      for (const line of lines) {
        if (line.startsWith("[BELIEF_ADJUSTMENTS]")) {
          processingBeliefs = true;
          continue;
        }
        if (!processingBeliefs) continue;
        if (line.startsWith("[REASONS]")) { // Stop if it loops back to REASONS or other sections
          processingBeliefs = false; 
          continue;
        }

        const adjustMatch = line.match(/ADJUST_BELIEF:\s*(.*)/);
        const newMatch = line.match(/NEW_BELIEF:\s*(.*)/);
        const hypothesisMatch = line.match(/HYPOTHESIS:\s*(.*)/);
        const confidenceMatch = line.match(/CONFIDENCE:\s*([0-9.]+)/);

        if (adjustMatch || newMatch) {
          // Finalize previous belief before starting a new one
          if (currentBeliefKey && currentHypothesis && currentConfidence !== null) {
            if (agent.consciousness_state.belief_state) {
              agent.consciousness_state.belief_state[currentBeliefKey] = { hypothesis: currentHypothesis, confidence: currentConfidence, last_updated: new Date() };
              newBeliefsForEvent[currentBeliefKey] = { hypothesis: currentHypothesis, confidence: currentConfidence };
              newInsightsGenerated = true;
            }
          }
          currentBeliefKey = (adjustMatch ? adjustMatch[1] : newMatch![1]).trim().replace(/'/g, "");
          currentHypothesis = null;
          currentConfidence = null;
        } else if (hypothesisMatch && currentBeliefKey) {
          currentHypothesis = hypothesisMatch[1].trim();
        } else if (confidenceMatch && currentBeliefKey && currentHypothesis) {
          currentConfidence = parseFloat(confidenceMatch[1].trim());
          // Finalize current belief
           if (agent.consciousness_state.belief_state) {
              agent.consciousness_state.belief_state[currentBeliefKey] = { hypothesis: currentHypothesis, confidence: currentConfidence, last_updated: new Date() };
              newBeliefsForEvent[currentBeliefKey] = { hypothesis: currentHypothesis, confidence: currentConfidence };
              newInsightsGenerated = true;
            }
          // Reset for next potential belief block
          currentBeliefKey = null;
          currentHypothesis = null;
          currentConfidence = null;
        }
      }
      // Final check for any pending belief after loop
      if (currentBeliefKey && currentHypothesis && currentConfidence !== null) {
        if (agent.consciousness_state.belief_state) {
            agent.consciousness_state.belief_state[currentBeliefKey] = { hypothesis: currentHypothesis, confidence: currentConfidence, last_updated: new Date() };
            newBeliefsForEvent[currentBeliefKey] = { hypothesis: currentHypothesis, confidence: currentConfidence };
            newInsightsGenerated = true;
        }
      }

      if (newInsightsGenerated) {
        console.log(`Agent ${agent.name} updated belief_state after reflection:`, agent.consciousness_state.belief_state);
        
        // Store reflection insight as KnowledgeItem
        const insight_summary_for_ltm = Object.entries(newBeliefsForEvent)
          .map(([key, val]) => `${key}: ${val.hypothesis} (Conf: ${val.confidence.toFixed(2)})`)
          .join('; ');
        
        const reflection_event_id = `event_${agent.id}_${Date.now()}_reflection`; // Create an ID for the event to be emitted

        const new_knowledge: KnowledgeItem = {
          id: `knowledge_${agent.id}_${Date.now()}`,
          type: KnowledgeItemType.REFLECTION_INSIGHT,
          content: `Post-reflection: Error level ${prediction_error_level.toFixed(2)}. New insights: ${insight_summary_for_ltm}`,
          timestamp: new Date(),
          importance_score: Math.min(1, (prediction_error_level * 0.6) + (Object.values(newBeliefsForEvent).reduce((sum, b) => sum + b.confidence, 0) / (Object.keys(newBeliefsForEvent).length || 1)) * 0.4),
          related_belief_keys: Object.keys(newBeliefsForEvent),
          source_event_id: reflection_event_id 
        };
        agent.long_term_memory.push(new_knowledge);
        this.capLongTermMemory(agent);
      }

      this.emitEvent({
        type: 'consciousness_event',
        agent_id: agent.id,
        event: {
          id: `event_${agent.id}_${Date.now()}_reflection_event`, // Consistent ID for event
          timestamp: new Date(),
          event_type: 'self_reflection_deep_dive', 
          description: `Agent ${agent.name} completed a deep reflection cycle due to prediction error ${prediction_error_level.toFixed(2)}. ${newInsightsGenerated ? 'New insights generated.' : 'No new insights parsed from LLM response.'}`,
          confidence: agent.consciousness_state.meta_awareness, 
          impact_level: prediction_error_level,
          details: {
            raw_response: llm_response_str, 
            parsed_insights: newInsightsGenerated ? newBeliefsForEvent : {}
          }
        } as unknown as ConsciousnessEvent, 
        timestamp: new Date()
      });

    } catch (error) {
      console.error(`Error during reflection cycle for agent ${agent.name}:`, error);
      this.emitEvent({
        type: 'consciousness_event',
        agent_id: agent.id,
        event: {
          id: `event_${agent.id}_${Date.now()}`,
          timestamp: new Date(),
          event_type: 'self_reflection_error', 
          description: `Agent ${agent.name} encountered an error during reflection cycle. Error: ${(error as Error).message}`,
          confidence: 0.3, // Low confidence due to error
          impact_level: prediction_error_level,
          details: { error_message: (error as Error).message }
        } as unknown as ConsciousnessEvent, // Casting as event_type will be formally added later
        timestamp: new Date()
      });
    }
  }

  private updateEmotionalState(agent: Agent): void {
    const emotionalState = agent.consciousness_state.emotional_state;
    const modifiers = emotionalState.cognitive_impact_modifiers!; // Should be initialized

    // Reset biases before recalculating
    modifiers.learning_rate_bias = 0.0;
    modifiers.reflection_threshold_bias = 0.0;
    modifiers.decision_making_style = 'default';
    modifiers.perception_filter = 'neutral';

    // --- Mood Dynamics (Simplified Example) ---
    // Track recent average error level for mood change
    const recentResolvedPredictions = agent.consciousness_state.active_predictions
        .filter(p => p.is_resolved && p.error_level !== undefined)
        .slice(-3); // Look at last 3 resolved predictions

    if (recentResolvedPredictions.length >= 2) { // Need at least 2 to see a trend
        const avgError = recentResolvedPredictions.reduce((sum, p) => sum + p.error_level!, 0) / recentResolvedPredictions.length;

        if (avgError < 0.3 && emotionalState.mood !== 'optimistic') { // Consistently low error
            emotionalState.mood = 'optimistic';
            emotionalState.mood_intensity = Math.min(1, emotionalState.mood_intensity + 0.1);
            // console.log(`Agent ${agent.name} mood shifted to optimistic due to low prediction error.`);
        } else if (avgError > 0.7 && emotionalState.mood !== 'pessimistic') { // Consistently high error
            emotionalState.mood = 'pessimistic';
            emotionalState.mood_intensity = Math.min(1, emotionalState.mood_intensity + 0.1);
            // console.log(`Agent ${agent.name} mood shifted to pessimistic due to high prediction error.`);
        } else if (avgError > 0.5 && emotionalState.mood !== 'analytical' && emotionalState.mood !== 'irritable' ) {
            emotionalState.mood = Math.random() < 0.5 ? 'analytical' : 'irritable';
            emotionalState.mood_intensity = Math.min(1, emotionalState.mood_intensity + 0.05);
        } else if (avgError < 0.5 && (emotionalState.mood === 'pessimistic' || emotionalState.mood === 'irritable')) {
            emotionalState.mood = 'neutral'; // Recovering
            emotionalState.mood_intensity = Math.max(0.1, emotionalState.mood_intensity - 0.1);
        }
    } else {
        // Slow decay of mood intensity if not much is happening
        emotionalState.mood_intensity = Math.max(0.1, emotionalState.mood_intensity - 0.02);
        if (emotionalState.mood_intensity < 0.2 && emotionalState.mood !== 'neutral') {
            emotionalState.mood = 'neutral';
        }
    }
    
    // --- Emotion to Modifier Mapping ---
    if (emotionalState.mood === 'optimistic' && emotionalState.mood_intensity > 0.5) {
      modifiers.learning_rate_bias = 0.05;
      modifiers.perception_filter = 'optimistic_bias';
      modifiers.reflection_threshold_bias = 0.05; // Less likely to reflect if optimistic
    }
    if (emotionalState.mood === 'pessimistic' && emotionalState.mood_intensity > 0.5) {
      modifiers.learning_rate_bias = -0.05;
      modifiers.perception_filter = 'pessimistic_bias';
      modifiers.reflection_threshold_bias = -0.05; // More likely to reflect
      modifiers.decision_making_style = 'cautious';
    }
     if (emotionalState.mood === 'irritable' && emotionalState.mood_intensity > 0.5) {
      modifiers.decision_making_style = 'impulsive'; // Or perhaps 'aggressive' if we had such a style
      modifiers.reflection_threshold_bias = 0.1; // Less reflection, more reaction
    }
    if (emotionalState.mood === 'analytical' && emotionalState.mood_intensity > 0.5) {
        modifiers.reflection_threshold_bias = -0.1; // More likely to reflect deeply
        modifiers.decision_making_style = 'analytical';
    }
     if (emotionalState.mood === 'focused' && emotionalState.mood_intensity > 0.6) {
        modifiers.learning_rate_bias = 0.02;
        modifiers.reflection_threshold_bias = 0.0; // Neutral reflection, but focused learning
    }


    if (emotionalState.primary_emotion === 'joy' && emotionalState.intensity > 0.7) {
      modifiers.learning_rate_bias = (modifiers.learning_rate_bias || 0) + 0.05;
      modifiers.decision_making_style = 'impulsive';
    }
    if (emotionalState.primary_emotion === 'anxiety' && emotionalState.intensity > 0.6) {
      modifiers.reflection_threshold_bias = (modifiers.reflection_threshold_bias || 0) - 0.1; // More likely to reflect
      modifiers.decision_making_style = 'cautious';
      modifiers.perception_filter = 'pessimistic_bias';
    }
    if (emotionalState.primary_emotion === 'curiosity' && emotionalState.intensity > 0.5) {
        modifiers.learning_rate_bias = (modifiers.learning_rate_bias || 0) + 0.1;
    }
     if (emotionalState.primary_emotion === 'frustration' && emotionalState.intensity > 0.6) {
        modifiers.reflection_threshold_bias = (modifiers.reflection_threshold_bias || 0) - 0.05; // More likely to reflect to solve it
        modifiers.decision_making_style = 'analytical'; // Try to analyze the problem
    }

    // Clamp biases to reasonable limits, e.g., +/- 0.2
    modifiers.learning_rate_bias = Math.max(-0.2, Math.min(0.2, modifiers.learning_rate_bias || 0));
    modifiers.reflection_threshold_bias = Math.max(-0.2, Math.min(0.2, modifiers.reflection_threshold_bias || 0));

    agent.consciousness_state.emotional_state.cognitive_impact_modifiers = modifiers;
    // console.log(`Agent ${agent.name} emotional state updated: mood=${emotionalState.mood}, modifiers=`, modifiers);
  }

  private capLongTermMemory(agent: Agent): void {
    const MAX_LTM_SIZE = 25;
    if (agent.long_term_memory.length > MAX_LTM_SIZE) {
      // Sort by importance (ascending, so least important are at the end) then by timestamp (ascending, so older are at the end for ties)
      agent.long_term_memory.sort((a, b) => a.importance_score - b.importance_score || a.timestamp.getTime() - b.timestamp.getTime());
      // Slice to keep the most important / newest if importance is equal
      agent.long_term_memory = agent.long_term_memory.slice(agent.long_term_memory.length - MAX_LTM_SIZE);
    }
  }

  private simulateGoalOutcomes(agent: Agent): void {
    if (!agent.consciousness_state.current_goals || agent.consciousness_state.current_goals.length === 0) {
      return;
    }

    let goalsModified = false;
    for (const goal of agent.consciousness_state.current_goals) {
      // Only process active or accepted goals that haven't been completed or abandoned
      if (goal.status === 'active' || goal.status === 'accepted') { 
        if (Math.random() < 0.05) { // 5% chance per cycle to have an outcome for an active goal
          goalsModified = true;
          const success = Math.random() < (goal.commitment_level || 0.5); // Success based on commitment
          goal.status = success ? 'completed' : 'abandoned'; 
          
          // console.log(`Agent ${agent.name} goal '${goal.description.slice(0,20)}...' outcome: ${goal.status}`);

          agent.consciousness_state.last_action_outcome = {
            action_id: `goal_outcome_${goal.goal_id}`,
            success: success,
            related_goal_id: goal.goal_id,
            related_belief_key: goal.motivating_belief_key 
          };

          if (goal.motivating_belief_key && agent.consciousness_state.belief_state && agent.consciousness_state.belief_state[goal.motivating_belief_key]) {
            const belief = agent.consciousness_state.belief_state[goal.motivating_belief_key];
            const oldConfidence = belief.confidence;
            if (success) {
              belief.confidence = Math.min(1, oldConfidence * 1.05 + 0.05); // Increase confidence
            } else {
              belief.confidence = Math.max(0.1, oldConfidence * 0.9); // Decrease confidence
            }
            belief.last_updated = new Date();
            // console.log(`Agent ${agent.name}'s belief ${goal.motivating_belief_key} confidence changed to ${belief.confidence.toFixed(2)} due to goal outcome.`);
          }
        }
      }
    }
    // Optional: Filter out completed/abandoned goals after a while to prevent list from growing indefinitely
    if (goalsModified && agent.consciousness_state.current_goals.some(g => g.status === 'completed' || g.status === 'abandoned')) {
         agent.consciousness_state.current_goals = agent.consciousness_state.current_goals.filter(g => g.status !== 'completed' && g.status !== 'abandoned');
    }
  }
}
