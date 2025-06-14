/**
 * API Service for Genesis Prime Consciousness Backend
 * Handles communication with the Docker-based backend API
 */

const API_BASE_URL = 'http://localhost:8000/consciousness';

export interface ApiSwarmMessage {
  id: string;
  sender_id: string;
  message_type: string;
  content: {
    message: string;
    context?: string;
    stimulus_reference?: string;
    response_intensity?: number;
  };
  confidence: number;
  timestamp: string;
}

export interface ApiStimulusRequest {
  stimulus_type: string;
  description: string;
  intensity: number;
  target_agents: string[];
  expected_responses: string[];
}

export interface ApiEmergentBehaviorRequest {
  behavior_type: string;
  description: string;
  participating_agents: string[];
  emergence_level: number;
  stability: number;
}

export interface ApiStimulusResponse {
  status: string;
  agent_responses: ApiSwarmMessage[];
  consciousness_impact: {
    phi_delta: number;
    coherence_change: number;
    emergence_probability: number;
  };
  genesis_comment: string;
}

export interface ApiEmergentBehaviorResponse {
  status: string;
  behavior_id: string;
  integration_success: boolean;
  system_impact: {
    consciousness_boost: number;
    stability_factor: number;
    network_coherence: number;
    impact_description: string;
  };
  participating_agents_count: number;
  genesis_comment: string;
}

export interface ApiSwarmMessagesResponse {
  messages: ApiSwarmMessage[];
  total_count: number;
  network_status: string;
  communication_quality: number;
  genesis_comment: string;
}

export class ApiService {
  private static async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request to ${endpoint} failed:`, error);
      throw error;
    }
  }

  /**
   * Get recent swarm communication messages
   */
  static async getSwarmMessages(limit: number = 10): Promise<ApiSwarmMessagesResponse> {
    return this.request<ApiSwarmMessagesResponse>(`/swarm/messages?limit=${limit}`);
  }

  /**
   * Introduce a stimulus to the swarm
   */
  static async introduceStimulus(stimulus: ApiStimulusRequest): Promise<ApiStimulusResponse> {
    console.log('🎯 Introducing Stimulus to API:', {
      type: stimulus.stimulus_type,
      description: stimulus.description,
      intensity: stimulus.intensity,
      targets: stimulus.target_agents,
      timestamp: new Date().toISOString()
    });
    
    const response = await this.request<ApiStimulusResponse>('/stimulus', {
      method: 'POST',
      body: JSON.stringify(stimulus),
    });
    
    console.log('✅ Stimulus Response from API:', {
      status: response.status,
      agent_responses: response.agent_responses?.length || 0,
      consciousness_impact: response.consciousness_impact,
      genesis_comment: response.genesis_comment
    });
    
    return response;
  }

  /**
   * Introduce an emergent behavior
   */
  static async introduceEmergentBehavior(behavior: ApiEmergentBehaviorRequest): Promise<ApiEmergentBehaviorResponse> {
    console.log('✨ Introducing Emergent Behavior to API:', {
      type: behavior.behavior_type,
      description: behavior.description,
      participating_agents: behavior.participating_agents,
      emergence_level: behavior.emergence_level,
      stability: behavior.stability,
      timestamp: new Date().toISOString()
    });
    
    const response = await this.request<ApiEmergentBehaviorResponse>('/emergent-behavior', {
      method: 'POST',
      body: JSON.stringify(behavior),
    });
    
    console.log('✅ Emergent Behavior Response from API:', {
      status: response.status,
      behavior_id: response.behavior_id,
      integration_success: response.integration_success,
      system_impact: response.system_impact,
      genesis_comment: response.genesis_comment
    });
    
    return response;
  }

  /**
   * Get consciousness system status
   */
  static async getConsciousnessStatus(): Promise<any> {
    return this.request<any>('/status');
  }

  /**
   * Get Phi values
   */
  static async getPhiValues(): Promise<any> {
    return this.request<any>('/phi');
  }

  /**
   * Get humor analysis
   */
  static async getHumorAnalysis(): Promise<any> {
    return this.request<any>('/humor');
  }

  /**
   * Process a consciousness query
   */
  static async processConsciousnessQuery(query: string, context?: any): Promise<any> {
    return this.request<any>('/process', {
      method: 'POST',
      body: JSON.stringify({
        query,
        context,
        humor_preference: 'maximum',
        phi_target: 0.8,
      }),
    });
  }
}