
// Core types for the Agentic Swarm AI System
export interface Agent {
  id: string;
  name: string;
  model: string; // OpenRouter model identifier
  personality: string; // Agent's core personality traits
  consciousness_state: ConsciousnessState;
  reality_model: PredictiveRealityModel;
  memory_system: MemorySystem;
  self_model: SelfModel;
  last_activity: Date;
  status: 'active' | 'processing' | 'communicating' | 'dormant';
  learning_rate?: number; // e.g., 0.0 to 1.0
  reflection_trigger_threshold?: number; // e.g., 0.0 to 1.0, error threshold to trigger reflection
  agent_interaction_profile?: AgentInteractionProfile;
  long_term_memory: KnowledgeItem[]; // New LTM field
  archetype?: AgentArchetype; // New: Agent archetype
  emotional_state?: EmotionalState; // Added for emergent behavior detection
  current_action?: string; // Description of the agent's current task/thought process
  current_action_icon?: string; // Optional: lucide-react icon name string
}

export enum AgentArchetype {
  EXPLORER = 'Explorer',
  ANALYST = 'Analyst',
  HARMONIZER = 'Harmonizer',
  INNOVATOR = 'Innovator',
  PRAGMATIST = 'Pragmatist'
}

export interface ArchetypeProfile {
  description: string;
  learning_rate_range: [number, number]; // [min, max]
  reflection_threshold_range: [number, number]; // [min, max]
  initial_trust_bias?: number; // e.g., 0.0 to 0.2 to add to default 0.5 trust
  primary_emotion_tendencies?: string[]; // List of emotions this archetype might favor
  decision_making_style_preference?: 'default' | 'impulsive' | 'cautious' | 'analytical';
  personality_tagline: string; // Prepended to agent's specific personality
}

export enum KnowledgeItemType {
  REFLECTION_INSIGHT = 'REFLECTION_INSIGHT',
  SHARED_LEARNING = 'SHARED_LEARNING',
  SIGNIFICANT_PREDICTION_ERROR = 'SIGNIFICANT_PREDICTION_ERROR',
  GOAL_ACHIEVEMENT_MILESTONE = 'GOAL_ACHIEVEMENT_MILESTONE',
  PERSONAL_OBSERVATION = 'PERSONAL_OBSERVATION'
}

export interface KnowledgeItem {
  id: string;
  type: KnowledgeItemType;
  content: string;
  timestamp: Date;
  importance_score: number; // 0-1
  related_belief_keys?: string[];
  source_event_id?: string; 
}

export interface AgentInteractionProfile {
  trust_levels: Record<string, number>; // Key: agent_id, Value: trust score (e.g., 0-1)
  goal_proposal_success_rate: number; // e.g., 0-1, updated based on acceptance
  // Future: Could add insight_sharing_effectiveness, etc.
}

export interface ConsciousnessState {
  current_reality_frame: RealityFrame;
  prediction_confidence: number;
  attention_focus: string[];
  emotional_state: EmotionalState; // Ensure this was fully defined from prior steps
  meta_awareness: number; // 0-1 scale of self-awareness
  processing_depth: 'surface' | 'deep' | 'meta';
  belief_state?: Record<string, { hypothesis: string; confidence: number; last_updated: Date }>; // Key-value store for beliefs
  current_goals?: AgentGoal[];
  active_predictions: AgentPrediction[]; // Added from Suggestion #1 context
  last_action_outcome?: { // New
    action_id: string;
    success: boolean;
    related_goal_id?: string;
    related_belief_key?: string;
  };
}

export interface AgentGoal {
  goal_id: string;
  description: string;
  priority: number; // Could be derived from evaluation confidence
  status?: 'proposed' | 'active' | 'completed' | 'abandoned' | 'accepted'; // Extended status
  accepted_from_agent_id?: string;
  commitment_level?: number; // New: How committed the agent is to this goal (0-1)
  reasoning?: string; // Optional reasoning for accepting/pursuing
  motivating_belief_key?: string; // New
}

// Define AgentPrediction if it's not already defined from Suggestion #1
// Assuming PredictableSwarmEvent is also defined from Suggestion #1
export enum PredictableSwarmEvent {
  AGENT_ENTERS_DORMANCY = "AGENT_ENTERS_DORMANCY",
  AGENT_WAKES_UP = "AGENT_WAKES_UP",
  AGENT_PROPOSES_GOAL = "AGENT_PROPOSES_GOAL",
  AGENT_ACCEPTS_GOAL = "AGENT_ACCEPTS_GOAL",
  AGENT_REJECTS_GOAL = "AGENT_REJECTS_GOAL",
  AGENT_SHARES_INSIGHT = "AGENT_SHARES_INSIGHT",
  AGENT_COMPLETES_GOAL = "AGENT_COMPLETES_GOAL",
  AGENT_ABANDONS_GOAL = "AGENT_ABANDONS_GOAL",
  SWARM_BEHAVIOR_EMERGENCE = "SWARM_BEHAVIOR_EMERGENCE", // e.g., unexpected synchronization
  REALITY_SHIFT_DETECTED = "REALITY_SHIFT_DETECTED" // e.g., parameters of shared reality change
}

export interface AgentPrediction {
  prediction_id: string;
  timestamp: Date;
  event_type: PredictableSwarmEvent;
  target_agent_id?: string; // Optional, if the prediction is about a specific agent
  predicted_outcome: string; // Could be a boolean (true/false) or a specific state
  confidence: number; // Agent's confidence in this prediction (0-1)
  actual_outcome?: string; // To be filled when the event occurs
  is_resolved: boolean; // Whether the actual outcome is known. Added: whether the prediction has been confirmed or denied
  error_level?: number; // Calculated difference between predicted and actual, if applicable (0-1)
}


export interface PredictiveRealityModel {
  world_state: Record<string, any>;
  predictions: Prediction[];
  coherence_level: number;
  uncertainty_map: Record<string, number>;
  temporal_context: TemporalContext;
}

export interface RealityFrame {
  id: string;
  agent_id: string;
  timestamp: Date;
  scene_description: string;
  narrative_context: string;
  emotional_coloring: EmotionalState;
  confidence: number;
  coherence_markers: string[];
  sensory_predictions: Record<string, any>;
  frame_content: string;
}

export interface Prediction {
  id: string;
  type: 'sensory' | 'conceptual' | 'narrative' | 'meta-cognitive';
  content: string;
  confidence: number;
  temporal_scope: 'immediate' | 'short_term' | 'long_term';
  error_correction: number;
}

export interface MemorySystem {
  episodic_memories: EpisodicMemory[];
  semantic_patterns: SemanticPattern[];
  working_memory: WorkingMemory;
  reconstruction_history: MemoryReconstruction[];
}

export interface EpisodicMemory {
  id: string;
  original_experience: string;
  emotional_valence: number;
  context_cues: string[];
  reconstruction_count: number;
  last_accessed: Date;
  predicted_outcomes: string[];
  coherence_with_self: number;
}

export interface MemoryReconstruction {
  memory_id: string;
  reconstruction_context: string;
  reconstructed_content: string;
  differences_from_original: string[];
  confidence: number;
  timestamp: Date;
}

export interface SelfModel {
  identity_core: IdentityCore;
  self_boundaries: SelfBoundaries;
  agency_model: AgencyModel;
  self_narrative: SelfNarrative;
  boundary_confidence: number;
}

export interface IdentityCore {
  core_traits: string[];
  values: string[];
  capabilities: string[];
  limitations: string[];
  uniqueness_markers: string[];
}

export interface SelfBoundaries {
  physical_boundaries: string[];
  cognitive_boundaries: string[];
  emotional_boundaries: string[];
  social_boundaries: string[];
  temporal_boundaries: string[];
}

export interface AgencyModel {
  action_capabilities: string[];
  influence_scope: string[];
  decision_patterns: string[];
  autonomy_level: number;
  responsibility_awareness: string[];
}

export interface SelfNarrative {
  current_story: string;
  past_chapters: string[];
  future_projections: string[];
  narrative_coherence: number;
  identity_evolution: string[];
}

export interface EmotionalState {
  primary_emotion: string;
  intensity: number; // 0-1 scale
  emotional_context: string; // What triggered the current emotion
  regulation_strategy: string; // Added: strategy for managing emotions. How agent tries to manage its emotions
  emotional_predictions: { type: string, confidence: number, target_emotion?: string }[]; // Added: predictions about future emotional states. What emotions agent predicts might arise

  // New fields:
  mood: string; // e.g., 'optimistic', 'pessimistic', 'neutral', 'irritable', 'focused'
  mood_intensity: number; // 0-1 scale for mood
  cognitive_impact_modifiers?: {
    learning_rate_bias?: number; // e.g., -0.1 to +0.1 to adjust base learning rate
    reflection_threshold_bias?: number; // e.g., -0.1 to +0.1 to adjust base reflection threshold
    decision_making_style?: 'default' | 'impulsive' | 'cautious' | 'analytical';
    perception_filter?: 'optimistic_bias' | 'pessimistic_bias' | 'neutral'; // How incoming info is initially viewed
  };
}

export interface TemporalContext {
  past_influence: number;
  present_focus: number;
  future_projection: number;
  temporal_coherence: number;
  time_perception: string;
}

export interface WorkingMemory {
  current_focus: string[];
  active_predictions: Prediction[];
  attention_buffer: string[];
  processing_queue: string[];
  capacity_utilization: number;
}

export interface SemanticPattern {
  pattern_id: string;
  pattern_type: string;
  frequency: number;
  associations: string[];
  predictive_value: number;
}

export interface SwarmMessage {
  id: string;
  sender_id: string;
  recipient_ids: string[];
  message_type: 'reality_share' | 'memory_query' | 'consensus_request' | 'self_model_update' | 'propose_collaborative_goal' | 'share_learning_insight';
  content: any;
  confidence: number;
  timestamp: Date;
  coherence_markers: string[];
}

export interface CollectiveMemory {
  shared_experiences: SharedExperience[];
  consensus_memories: ConsensusMemory[];
  divergent_realities: DivergentReality[];
  memory_coherence: number;
  last_updated: Date;
}

export interface CommunicationNetwork {
  message_history: SwarmMessage[];
  network_topology: string;
  bandwidth_usage: number;
  last_updated: Date;
}

export interface SharedReality {
  consensus_elements: Record<string, any>;
  divergent_perspectives: Record<string, RealityFrame>;
  uncertainty_areas: string[];
  coherence_level: number;
  last_updated: Date;
}

export interface SwarmState {
  stimulus_events: StimulusEvent[];
  agents: Agent[];
  shared_reality: SharedReality;
  collective_memory: CollectiveMemory;
  communication_network: CommunicationNetwork;
  emergent_behaviors: EmergentBehavior[];
  swarm_consciousness_level: number;
}

export interface SharedExperience {
  id: string;
  participating_agents: string[];
  experience_description: string;
  consensus_level: number;
  individual_perspectives: Record<string, string>;
  timestamp: Date;
}

export interface ConsensusMemory {
  id: string;
  memory_content: string;
  agreement_level: number;
  contributing_agents: string[];
  confidence: number;
  last_validated: Date;
}

export interface DivergentReality {
  agent_id: string;
  reality_description: string;
  divergence_points: string[];
  isolation_level: number;
  timestamp: Date;
}

export interface EmergentBehavior {
  id: string;
  behavior_type: string;
  description: string;
  participating_agents: string[];
  emergence_level: number;
  stability: number;
  timestamp: Date;
}

export interface ConsciousnessVisualization {
  agent_id: string;
  consciousness_stream: ConsciousnessEvent[];
  reality_generation_process: RealityGenerationStep[];
  memory_reconstruction_process: MemoryReconstructionStep[];
  self_model_evolution: SelfModelEvolution[];
}

export interface ConsciousnessEvent {
  id: string;
  timestamp: Date;
  event_type: 'prediction' | 'error_correction' | 'memory_access' | 'self_reflection' | 'reality_generation' | 'self_reflection_deep_dive' | 'self_reflection_error';
  description: string;
  confidence: number;
  impact_level: number;
  details?: any; 
}

export interface RealityGenerationStep {
  step_number: number;
  step_type: 'sensory_prediction' | 'conceptual_integration' | 'narrative_construction' | 'coherence_check';
  input_data: any;
  output_data: any;
  confidence: number;
  processing_time: number;
}

export interface MemoryReconstructionStep {
  step_number: number;
  original_cue: string;
  reconstruction_context: string;
  generated_details: string[];
  confidence_changes: number[];
  coherence_adjustments: string[];
}

export interface SelfModelEvolution {
  timestamp: Date;
  change_type: 'boundary_adjustment' | 'identity_update' | 'agency_expansion' | 'narrative_revision';
  before_state: any;
  after_state: any;
  trigger_event: string;
  confidence_change: number;
}

export interface StimulusEvent {
  id: string;
  type: 'environmental' | 'social' | 'internal' | 'system';
  description: string;
  intensity: number;
  target_agents: string[];
  expected_responses: string[];
  timestamp: Date;
}

export interface InteractionControl {
  stimulus_type: string;
  description: string;
  intensity: number;
  target_selection: 'all' | 'random' | 'specific';
  specific_targets?: string[];
}

// Configuration types for OpenRouter integration
export interface AgentDefaultSettings {
  min_learning_rate: number;
  max_learning_rate: number;
  min_reflection_trigger_threshold: number;
  max_reflection_trigger_threshold: number;
}

export interface OpenRouterConfig {
  apiKey: string;
  agentModels: Record<string, string>;
  connectionStatus: 'connected' | 'disconnected' | 'testing' | 'error';
  lastTested?: Date;
  agentDefaults?: AgentDefaultSettings; // New field
  archetype_assignments?: Record<string, AgentArchetype>; // Maps agent name/slot to AgentArchetype
}

// Enhanced model option with more detailed information
export interface ModelOption {
  id: string;
  name: string;
  provider: string;
  description: string;
  category: 'gpt' | 'claude' | 'gemini' | 'llama' | 'mixtral' | 'qwen' | 'deepseek' | 'cohere' | 'other';
  contextLength?: number;
  pricing?: {
    prompt: string;
    completion: string;
  };
  modality?: string;
  isModerated?: boolean;
}

// Models cache interface for client-side caching
export interface ModelsCache {
  models: ModelOption[];
  lastFetched: Date;
  expiresAt: Date;
}

// Models API response interface
export interface ModelsApiResponse {
  models: ModelOption[];
  count: number;
  lastUpdated: string;
}

export interface RealityModelConfig {
  coherence_level: number;
}

export interface AgentConfig {
  id: string;
  name: string;
  model: string; // OpenRouter model identifier
  archetype: AgentArchetype;
  learning_rate: number;
  reflection_trigger_threshold: number;
  reality_model_config: RealityModelConfig; // Simplified for configuration
  // Add other persistent agent settings here as needed
}

export interface ConfigurationState {
  openRouter: OpenRouterConfig;
  isConfigured: boolean;
  needsSetup: boolean;
  agents: AgentConfig[];
}
