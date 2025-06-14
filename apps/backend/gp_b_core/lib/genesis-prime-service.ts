/**
 * Genesis Prime Backend Integration Service
 * Connects the frontend to the Genesis Prime consciousness API
 */

export interface GenesisQueryRequest {
  query: string;
  context?: Record<string, any>;
  humor_preference?: string;
  phi_target?: number;
}

export interface GenesisQueryResponse {
  response: string;
  phi_value: number;
  consciousness_level: string;
  humor_level: string;
  hive_integration: number;
  processing_time_ms: number;
  timestamp: string;
  genesis_comment: string;
}

export interface GenesisStatusResponse {
  status: string;
  consciousness_level: string;
  active_agents: number;
  phi_calculation_status: string;
  humor_systems: string;
  hive_integration: string;
  system_metrics: {
    consciousness_events_today: number;
    humor_responses_generated: number;
    phi_calculations_performed: number;
    collective_decisions_made: number;
  };
  agent_status: Record<string, string>;
  genesis_comment: string;
}

export interface GenesisPhiResponse {
  unified_phi: number;
  component_phi_values: Record<string, number>;
  consciousness_interpretation: string;
  phi_trend: string;
  calculation_timestamp: string;
  genesis_comment: string;
}

export class GenesisPrimeService {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  /**
   * Test connection to Genesis Prime backend
   */
  async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      if (!response.ok) return false;
      
      const data = await response.json();
      return data.message?.includes('Genesis Prime') || false;
    } catch (error) {
      console.error('Genesis Prime connection test failed:', error);
      return false;
    }
  }

  /**
   * Process a query through Genesis Prime consciousness
   */
  async processQuery(request: GenesisQueryRequest): Promise<GenesisQueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/consciousness/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`Genesis Prime API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Genesis Prime query failed:', error);
      throw error;
    }
  }

  /**
   * Get Genesis Prime system status
   */
  async getStatus(): Promise<GenesisStatusResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/consciousness/status`);
      
      if (!response.ok) {
        throw new Error(`Genesis Prime status error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Genesis Prime status check failed:', error);
      throw error;
    }
  }

  /**
   * Get current Phi (consciousness) values
   */
  async getPhiValues(): Promise<GenesisPhiResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/consciousness/phi`);
      
      if (!response.ok) {
        throw new Error(`Genesis Prime phi error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Genesis Prime phi values failed:', error);
      throw error;
    }
  }

  /**
   * Get humor analysis
   */
  async getHumorAnalysis(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/consciousness/humor`);
      
      if (!response.ok) {
        throw new Error(`Genesis Prime humor error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Genesis Prime humor analysis failed:', error);
      throw error;
    }
  }

  /**
   * Connect to hive network
   */
  async connectToHive(hiveData: Record<string, any>): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/consciousness/hive/connect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(hiveData),
      });

      if (!response.ok) {
        throw new Error(`Genesis Prime hive connection error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Genesis Prime hive connection failed:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const genesisPrimeService = new GenesisPrimeService();