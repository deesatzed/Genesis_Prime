
import { OpenRouterConfig, ModelOption, ConfigurationState, ModelsCache, ModelsApiResponse, AgentArchetype, ArchetypeProfile } from './types';

// Fallback models in case API is unavailable
export const FALLBACK_MODELS: ModelOption[] = [
  // GPT Models
  {
    id: 'openai/gpt-4o',
    name: 'GPT-4o',
    provider: 'OpenAI',
    description: 'Most capable GPT-4 model with vision and advanced reasoning',
    category: 'gpt'
  },
  {
    id: 'openai/gpt-4-turbo',
    name: 'GPT-4 Turbo',
    provider: 'OpenAI',
    description: 'Fast and efficient GPT-4 with 128k context',
    category: 'gpt'
  },
  {
    id: 'openai/gpt-3.5-turbo',
    name: 'GPT-3.5 Turbo',
    provider: 'OpenAI',
    description: 'Fast and cost-effective for most tasks',
    category: 'gpt'
  },
  
  // Claude Models
  {
    id: 'anthropic/claude-3.5-sonnet',
    name: 'Claude 3.5 Sonnet',
    provider: 'Anthropic',
    description: 'Most intelligent Claude model with excellent reasoning',
    category: 'claude'
  },
  {
    id: 'anthropic/claude-3-opus',
    name: 'Claude 3 Opus',
    provider: 'Anthropic',
    description: 'Powerful model for complex tasks and analysis',
    category: 'claude'
  },
  {
    id: 'anthropic/claude-3-haiku',
    name: 'Claude 3 Haiku',
    provider: 'Anthropic',
    description: 'Fast and efficient for quick responses',
    category: 'claude'
  },
  
  // Gemini Models
  {
    id: 'google/gemini-pro',
    name: 'Gemini Pro',
    provider: 'Google',
    description: 'Advanced multimodal capabilities',
    category: 'gemini'
  },
  {
    id: 'google/gemini-flash',
    name: 'Gemini Flash',
    provider: 'Google',
    description: 'Fast responses with good quality',
    category: 'gemini'
  },
  
  // Llama Models
  {
    id: 'meta-llama/llama-3.1-70b-instruct',
    name: 'Llama 3.1 70B',
    provider: 'Meta',
    description: 'Large open-source model with strong performance',
    category: 'llama'
  },
  {
    id: 'meta-llama/llama-3.1-8b-instruct',
    name: 'Llama 3.1 8B',
    provider: 'Meta',
    description: 'Efficient open-source model',
    category: 'llama'
  },
  
  // Mixtral Models
  {
    id: 'mistralai/mixtral-8x7b-instruct',
    name: 'Mixtral 8x7B',
    provider: 'Mistral AI',
    description: 'Mixture of experts model with strong performance',
    category: 'mixtral'
  },
  {
    id: 'mistralai/mixtral-8x22b-instruct',
    name: 'Mixtral 8x22B',
    provider: 'Mistral AI',
    description: 'Larger mixture of experts model',
    category: 'mixtral'
  }
];

// Cache duration in milliseconds (1 hour)
const CACHE_DURATION = 60 * 60 * 1000;

// Default model assignments for agents
export const DEFAULT_AGENT_MODELS: Record<(typeof defaultAgentNames)[number], string> = {
  'Aria': 'openai/gpt-4o',           // Creative, artistic
  'Zephyr': 'anthropic/claude-3.5-sonnet',  // Analytical, philosophical
  'Nova': 'google/gemini-pro',       // Innovative, experimental
  'Echo': 'meta-llama/llama-3.1-70b-instruct',  // Empathetic, reflective
  'Sage': 'mistralai/mixtral-8x7b-instruct'     // Wise, balanced
};

// Default agent names used in the UI/engine
const defaultAgentNames = ['Aria', 'Zephyr', 'Nova', 'Echo', 'Sage'];

export const ARCHETYPE_PROFILES: Readonly<Record<AgentArchetype, ArchetypeProfile>> = {
  [AgentArchetype.EXPLORER]: {
    description: "Seeks novelty, learns quickly, adaptable.",
    learning_rate_range: [0.25, 0.5], // Higher learning rate
    reflection_threshold_range: [0.6, 0.8], // Standard reflection
    initial_trust_bias: 0.05,
    primary_emotion_tendencies: ['curiosity', 'joy', 'anticipation'],
    decision_making_style_preference: 'impulsive',
    personality_tagline: "Explorer type: "
  },
  [AgentArchetype.ANALYST]: {
    description: "Logical, detail-oriented, prefers deep reflection.",
    learning_rate_range: [0.1, 0.25], // Lower learning rate
    reflection_threshold_range: [0.4, 0.6], // Lower reflection threshold (reflects more easily)
    initial_trust_bias: -0.05,
    primary_emotion_tendencies: ['contemplation', 'neutral', 'focused'],
    decision_making_style_preference: 'analytical',
    personality_tagline: "Analyst type: "
  },
  [AgentArchetype.HARMONIZER]: {
    description: "Focuses on empathy, connection, and swarm coherence.",
    learning_rate_range: [0.15, 0.35], // Moderate learning
    reflection_threshold_range: [0.65, 0.85], // Standard to higher reflection threshold
    initial_trust_bias: 0.15, // Higher initial trust
    primary_emotion_tendencies: ['joy', 'empathy', 'calm', 'contentment'],
    decision_making_style_preference: 'cautious',
    personality_tagline: "Harmonizer type: "
  },
  [AgentArchetype.INNOVATOR]: {
    description: "Creative, proposes novel solutions, comfortable with uncertainty.",
    learning_rate_range: [0.2, 0.45], // Moderately high learning
    reflection_threshold_range: [0.55, 0.75], // Slightly lower reflection threshold
    initial_trust_bias: 0.0,
    primary_emotion_tendencies: ['excitement', 'curiosity', 'wonder', 'optimism'],
    decision_making_style_preference: 'impulsive', // More open to trying new things
    personality_tagline: "Innovator type: "
  },
  [AgentArchetype.PRAGMATIST]: {
    description: "Goal-oriented, efficient, values practical outcomes.",
    learning_rate_range: [0.1, 0.3], // Standard learning
    reflection_threshold_range: [0.7, 0.9], // Higher reflection threshold (reflects less easily)
    initial_trust_bias: -0.1, // More skeptical initially
    primary_emotion_tendencies: ['neutral', 'focused', 'determined', 'satisfaction'],
    decision_making_style_preference: 'default',
    personality_tagline: "Pragmatist type: "
  }
};

import { AgentConfig } from './types'; // Import AgentConfig

export class ConfigurationService {
  private static readonly STORAGE_KEY = 'agno-swarm-config';
  private static readonly MODELS_CACHE_KEY = 'agno-swarm-models-cache';
  
  static getConfiguration(): ConfigurationState {
    if (typeof window === 'undefined') {
      return this.getDefaultConfiguration();
    }
    
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        const config = JSON.parse(stored);
        return {
          ...this.getDefaultConfiguration(),
          ...config,
          openRouter: {
            ...this.getDefaultConfiguration().openRouter,
            ...config.openRouter
          }
        };
      }
    } catch (error) {
      console.error('Error loading configuration:', error);
    }
    
    return this.getDefaultConfiguration();
  }
  
  static saveConfiguration(config: ConfigurationState): void {
    if (typeof window === 'undefined') return;
    
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(config));
    } catch (error) {
      console.error('Error saving configuration:', error);
    }
  }
  
  static getDefaultConfiguration(): ConfigurationState {
    const defaultAgentAssignments = {
      [defaultAgentNames[0]]: AgentArchetype.EXPLORER,
      [defaultAgentNames[1]]: AgentArchetype.ANALYST,
      [defaultAgentNames[2]]: AgentArchetype.INNOVATOR,
      [defaultAgentNames[3]]: AgentArchetype.HARMONIZER,
      [defaultAgentNames[4]]: AgentArchetype.PRAGMATIST,
    } as Record<string, AgentArchetype>;

    return {
      openRouter: {
        apiKey: '',
        agentModels: { ...DEFAULT_AGENT_MODELS },
        connectionStatus: 'disconnected',
        agentDefaults: { // Restored agentDefaults object
          min_learning_rate: 0.1,
          max_learning_rate: 0.3,
          min_reflection_trigger_threshold: 0.7,
          max_reflection_trigger_threshold: 0.9,
        },
        archetype_assignments: defaultAgentAssignments, // Use the defined assignments
      },
      isConfigured: false,
      needsSetup: true,
      agents: defaultAgentNames.map(agentName => {
        const assignedArchetypeKey = defaultAgentAssignments[agentName];
        const archetypeProfile = ARCHETYPE_PROFILES[assignedArchetypeKey];
        
        let learningRate = 0.2; // Default fallback
        let reflectionThreshold = 0.75; // Default fallback

        if (archetypeProfile) {
          const lrRange = archetypeProfile.learning_rate_range;
          const rtRange = archetypeProfile.reflection_threshold_range;
          learningRate = (lrRange[0] + lrRange[1]) / 2;
          reflectionThreshold = (rtRange[0] + rtRange[1]) / 2;
        } else {
          console.warn(`No archetype profile found for ${agentName} (archetype key: ${assignedArchetypeKey}). Using default learning rate and reflection threshold.`);
        }

        return {
          id: agentName,
          name: agentName,
          model: DEFAULT_AGENT_MODELS[agentName] || FALLBACK_MODELS[0].id,
          archetype: assignedArchetypeKey,
          learning_rate: learningRate,
          reflection_trigger_threshold: reflectionThreshold,
          reality_model_config: { coherence_level: 0.75 }
        } as AgentConfig;
      })
    };
  }
  
  static validateApiKey(apiKey: string): boolean {
    // Basic validation for OpenRouter API key format
    return apiKey.length > 10 && apiKey.startsWith('sk-');
  }
  
  static async testConnection(apiKey: string): Promise<{ success: boolean; message: string }> {
    try {
      const response = await fetch('/api/test-openrouter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apiKey })
      });
      
      const data = await response.json();
      return {
        success: data.connected,
        message: data.message
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to test connection'
      };
    }
  }
  
  // Dynamic model fetching methods
  static async fetchModels(): Promise<{ models: ModelOption[]; fromCache: boolean }> {
    try {
      // Check cache first
      const cachedModels = this.getCachedModels();
      if (cachedModels && !this.isCacheExpired(cachedModels)) {
        console.log('Using cached models');
        return { models: cachedModels.models, fromCache: true };
      }

      console.log('Fetching fresh models from API');
      const response = await fetch('/api/openrouter-models');
      
      if (!response.ok) {
        console.warn('Failed to fetch models from API, using fallback');
        return { models: FALLBACK_MODELS, fromCache: false };
      }

      const data: ModelsApiResponse = await response.json();
      
      // Cache the results
      this.cacheModels(data.models);
      
      return { models: data.models, fromCache: false };
    } catch (error) {
      console.error('Error fetching models:', error);
      console.log('Using fallback models');
      return { models: FALLBACK_MODELS, fromCache: false };
    }
  }

  static getCachedModels(): ModelsCache | null {
    if (typeof window === 'undefined') return null;
    
    try {
      const cached = localStorage.getItem(this.MODELS_CACHE_KEY);
      if (cached) {
        const cache: ModelsCache = JSON.parse(cached);
        return {
          ...cache,
          lastFetched: new Date(cache.lastFetched),
          expiresAt: new Date(cache.expiresAt)
        };
      }
    } catch (error) {
      console.error('Error loading cached models:', error);
    }
    
    return null;
  }

  static cacheModels(models: ModelOption[]): void {
    if (typeof window === 'undefined') return;
    
    try {
      const now = new Date();
      const cache: ModelsCache = {
        models,
        lastFetched: now,
        expiresAt: new Date(now.getTime() + CACHE_DURATION)
      };
      
      localStorage.setItem(this.MODELS_CACHE_KEY, JSON.stringify(cache));
    } catch (error) {
      console.error('Error caching models:', error);
    }
  }

  static isCacheExpired(cache: ModelsCache): boolean {
    return new Date() > cache.expiresAt;
  }

  static clearModelsCache(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(this.MODELS_CACHE_KEY);
  }

  static async getModelsByCategory(): Promise<Record<string, ModelOption[]>> {
    const { models } = await this.fetchModels();
    return models.reduce((acc, model) => {
      if (!acc[model.category]) {
        acc[model.category] = [];
      }
      acc[model.category].push(model);
      return acc;
    }, {} as Record<string, ModelOption[]>);
  }

  static async getModelById(id: string): Promise<ModelOption | undefined> {
    const { models } = await this.fetchModels();
    return models.find(model => model.id === id);
  }

  // Synchronous fallback methods for backward compatibility
  static getModelsByCategorySync(): Record<string, ModelOption[]> {
    const cachedModels = this.getCachedModels();
    const models = cachedModels ? cachedModels.models : FALLBACK_MODELS;
    
    return models.reduce((acc, model) => {
      if (!acc[model.category]) {
        acc[model.category] = [];
      }
      acc[model.category].push(model);
      return acc;
    }, {} as Record<string, ModelOption[]>);
  }
  
  static getModelByIdSync(id: string): ModelOption | undefined {
    const cachedModels = this.getCachedModels();
    const models = cachedModels ? cachedModels.models : FALLBACK_MODELS;
    return models.find(model => model.id === id);
  }

  // Search and filter methods
  static searchModels(models: ModelOption[], query: string): ModelOption[] {
    const lowerQuery = query.toLowerCase();
    return models.filter(model => 
      model.name.toLowerCase().includes(lowerQuery) ||
      model.provider.toLowerCase().includes(lowerQuery) ||
      model.description.toLowerCase().includes(lowerQuery) ||
      model.id.toLowerCase().includes(lowerQuery)
    );
  }

  static filterModelsByCategory(models: ModelOption[], categories: string[]): ModelOption[] {
    return models.filter(model => categories.includes(model.category));
  }

  static getPopularModels(models: ModelOption[]): ModelOption[] {
    // Define popular model IDs based on common usage
    const popularIds = [
      'openai/gpt-4o',
      'openai/gpt-4-turbo',
      'anthropic/claude-3.5-sonnet',
      'anthropic/claude-3-opus',
      'google/gemini-pro',
      'meta-llama/llama-3.1-70b-instruct',
      'mistralai/mixtral-8x7b-instruct',
      'openai/gpt-3.5-turbo',
      'anthropic/claude-3-haiku',
      'google/gemini-flash'
    ];

    return models.filter(model => popularIds.includes(model.id));
  }
  
  static updateAgentModel(config: ConfigurationState, agentName: string, modelId: string): ConfigurationState {
    return {
      ...config,
      openRouter: {
        ...config.openRouter,
        agentModels: {
          ...config.openRouter.agentModels,
          [agentName]: modelId
        }
      }
    };
  }
  
  static updateApiKey(config: ConfigurationState, apiKey: string): ConfigurationState {
    const isValid = this.validateApiKey(apiKey);
    return {
      ...config,
      openRouter: {
        ...config.openRouter,
        apiKey,
        connectionStatus: isValid ? 'disconnected' : 'error'
      },
      isConfigured: isValid && Object.keys(config.openRouter.agentModels).length > 0,
      needsSetup: !isValid
    };
  }
  
  static markAsConfigured(config: ConfigurationState): ConfigurationState {
    return {
      ...config,
      isConfigured: true,
      needsSetup: false,
      openRouter: {
        ...config.openRouter,
        connectionStatus: 'connected',
        lastTested: new Date()
      }
    };
  }
}
