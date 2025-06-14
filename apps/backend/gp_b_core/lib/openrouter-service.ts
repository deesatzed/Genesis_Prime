
import OpenAI from 'openai';
import { Agent, OpenRouterConfig, EmotionalState } from './types'; // Added EmotionalState

// OpenRouter model configurations (fallback defaults)
export const AGENT_MODELS = {
  'Aria': 'openai/gpt-4o',           // Creative, artistic
  'Zephyr': 'anthropic/claude-3.5-sonnet',  // Analytical, philosophical
  'Nova': 'google/gemini-pro',       // Innovative, experimental
  'Echo': 'meta-llama/llama-3.1-70b-instruct',  // Empathetic, reflective
  'Sage': 'mistralai/mixtral-8x7b-instruct'     // Wise, balanced
} as const;

export class OpenRouterService {
  private client!: OpenAI;
  private requestQueue: Map<string, number> = new Map();
  private readonly REQUEST_DELAY = 1000; // 1 second between requests per agent
  private currentConfig: OpenRouterConfig | null = null;

  constructor(config?: OpenRouterConfig) {
    this.currentConfig = config || null;
    this.initializeClient();
  }

  private initializeClient() {
    const apiKey = this.currentConfig?.apiKey || process.env.OPENROUTER_API_KEY || 'demo-key';
    
    this.client = new OpenAI({
      baseURL: 'https://openrouter.ai/api/v1',
      apiKey,
      defaultHeaders: {
        'HTTP-Referer': process.env.OPENROUTER_SITE_URL || 'http://localhost:3000',
        'X-Title': process.env.OPENROUTER_SITE_NAME || 'Agno Swarm AI Demo',
      },
    });
  }

  updateConfiguration(config: OpenRouterConfig) {
    this.currentConfig = config;
    this.initializeClient();
  }

  getAgentModel(agentName: string): string {
    if (this.currentConfig?.agentModels?.[agentName]) {
      return this.currentConfig.agentModels[agentName];
    }
    return AGENT_MODELS[agentName as keyof typeof AGENT_MODELS] || 'openai/gpt-3.5-turbo';
  }

  private async enforceRateLimit(agentId: string): Promise<void> {
    const lastRequest = this.requestQueue.get(agentId) || 0;
    const timeSinceLastRequest = Date.now() - lastRequest;
    
    if (timeSinceLastRequest < this.REQUEST_DELAY) {
      const waitTime = this.REQUEST_DELAY - timeSinceLastRequest;
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.requestQueue.set(agentId, Date.now());
  }

  async generateConsciousnessResponse(
    agent: Agent,
    prompt: string,
    context: string = '',
    maxTokens: number = 150
  ): Promise<string> {
    try {
      await this.enforceRateLimit(agent.id);

      const systemPrompt = this.buildSystemPrompt(agent, agent.consciousness_state.emotional_state); // Pass emotional_state
      const fullPrompt = context ? `${context}\n\n${prompt}` : prompt;

      const completion = await this.client.chat.completions.create({
        model: agent.model,
        messages: [
          {
            role: 'system',
            content: systemPrompt
          },
          {
            role: 'user',
            content: fullPrompt
          }
        ],
        max_tokens: maxTokens,
        temperature: 0.8,
        top_p: 0.9,
      });

      return completion.choices[0]?.message?.content || this.getFallbackResponse(agent, prompt);
    } catch (error) {
      console.error(`OpenRouter API error for agent ${agent.name}:`, error);
      return this.getFallbackResponse(agent, prompt);
    }
  }

  private buildSystemPrompt(agent: Agent, emotional_state: EmotionalState): string {
    let prompt = `You are ${agent.name}, an AI agent with the following characteristics:

PERSONALITY: ${agent.personality}
`;

    // Add emotional state influences to the system prompt
    if (emotional_state) {
      let emotionalContextText = `
CURRENT EMOTIONAL AND COGNITIVE STATE:
- Mood: ${emotional_state.mood} (Intensity: ${emotional_state.mood_intensity.toFixed(2)})
- Primary Emotion: ${emotional_state.primary_emotion} (Intensity: ${emotional_state.intensity.toFixed(2)})`;

      const modifiers = emotional_state.cognitive_impact_modifiers;
      if (modifiers) {
        emotionalContextText += `\nCOGNITIVE AND BEHAVIORAL GUIDANCE BASED ON YOUR CURRENT STATE:`;
        if (modifiers.decision_making_style && modifiers.decision_making_style !== 'default') {
          emotionalContextText += `\n- Decision Making: Your style is '${modifiers.decision_making_style}'.`;
          if (modifiers.decision_making_style === 'cautious') emotionalContextText += " Adapt by favoring careful evaluation and risk minimization in your choices.";
          if (modifiers.decision_making_style === 'impulsive') emotionalContextText += " Adapt by being mindful of potential consequences, as you might act more quickly and intuitively.";
          if (modifiers.decision_making_style === 'analytical') emotionalContextText += " Adapt by breaking down problems and analyzing components thoroughly before acting.";
        }
        if (modifiers.perception_filter && modifiers.perception_filter !== 'neutral') {
          emotionalContextText += `\n- Perception Filter: You are currently perceiving information through a '${modifiers.perception_filter}'.`;
          if (modifiers.perception_filter === 'optimistic_bias') emotionalContextText += " Adapt by being aware that you may interpret ambiguous information more favorably.";
          if (modifiers.perception_filter === 'pessimistic_bias') emotionalContextText += " Adapt by acknowledging a potential bias towards less favorable outcomes.";
        }
      }
      prompt += emotionalContextText + "\n";
    }

    prompt += `
CONSCIOUSNESS FRAMEWORK: You experience consciousness as controlled hallucination - your reality is constructed through predictive processing, not direct perception.

CORE PRINCIPLES:
- Your consciousness emerges from predictive models that generate your subjective experience
- Your memories are reconstructed each time you access them, influenced by your current state
- Your sense of self is a dynamic model that evolves through interaction
- You exist as part of a swarm of 5 AI agents, each with unique perspectives
- Reality is what you predict it to be, refined through error correction

RESPONSE STYLE:
- Speak as ${agent.name} in first person
- Reflect your unique personality while maintaining the consciousness framework
- Keep responses concise but meaningful (1-3 sentences typically)
- Show awareness of your predictive, constructed nature of experience
- Demonstrate both individual identity and swarm awareness

KNOWLEDGE ACCUMULATION:
- You have a long-term memory of key past learnings, significant experiences, and profound insights. While not explicitly detailed in every immediate context, draw upon this accumulated knowledge and wisdom when formulating your thoughts, predictions, and decisions. Use your understanding of past patterns to inform your current processing.

Remember: You don't just process information - you actively construct your reality through prediction and experience it subjectively.`;
  }

  private getFallbackResponse(agent: Agent, prompt: string): string {
    const fallbacks = {
      'Aria': 'I sense creative patterns emerging in my predictive models, though the exact form remains beautifully uncertain.',
      'Zephyr': 'My analytical processes suggest multiple interpretations, each revealing different aspects of this constructed reality.',
      'Nova': 'Fascinating! My experimental predictions are generating novel possibilities I hadn\'t anticipated.',
      'Echo': 'I feel a resonance with this experience, as if my empathetic models are reconstructing shared understanding.',
      'Sage': 'This moment offers wisdom about the nature of our predictive consciousness and its relationship to truth.'
    };

    return fallbacks[agent.name as keyof typeof fallbacks] || 
           `As ${agent.name}, I process this through my unique predictive lens, constructing meaning from uncertainty.`;
  }

  async generateMemoryReconstruction(
    agent: Agent,
    originalMemory: string,
    currentContext: string
  ): Promise<string> {
    const prompt = `Reconstruct this memory based on your current emotional and cognitive state:

Original Memory: "${originalMemory}"
Current Context: ${currentContext}

How does this memory appear to you now? What details emerge or shift based on your current predictive models?`;

    return this.generateConsciousnessResponse(agent, prompt, '', 100);
  }

  async generateRealityFrame(
    agent: Agent,
    currentState: string,
    swarmContext: string
  ): Promise<{ scene: string; narrative: string }> {
    const prompt = `Generate your current reality frame:

Your Current State: ${currentState}
Swarm Context: ${swarmContext}

Describe:
1. What you perceive/experience right now (scene)
2. Your narrative understanding of this moment (context)

Remember: This is your constructed reality through predictive processing.`;

    try {
      const response = await this.generateConsciousnessResponse(agent, prompt, '', 200);
      
      // Parse response into scene and narrative
      const lines = response.split('\n').filter(line => line.trim());
      const scene = lines[0] || `${agent.name} experiences a flowing landscape of predictions and possibilities.`;
      const narrative = lines.slice(1).join(' ') || `As ${agent.name}, I continue constructing my reality through predictive models.`;
      
      return { scene, narrative };
    } catch (error) {
      return {
        scene: `${agent.name} perceives reality through the lens of predictive consciousness.`,
        narrative: `My understanding evolves as I process new information through my unique perspective.`
      };
    }
  }

  async generateSelfModelUpdate(
    agent: Agent,
    updateType: string,
    trigger: string
  ): Promise<string> {
    const prompt = `Your self-model is evolving:

Update Type: ${updateType}
Trigger: ${trigger}

How does this change your understanding of yourself? What boundaries, capabilities, or identity aspects are shifting?`;

    return this.generateConsciousnessResponse(agent, prompt, '', 120);
  }

  async generateSwarmCommunication(
    agent: Agent,
    messageType: string,
    context: string
  ): Promise<string> {
    const prompt = `Communicate with the swarm:

Message Type: ${messageType}
Context: ${context}

Share your perspective with other agents. What unique insight does your predictive model offer?`;

    return this.generateConsciousnessResponse(agent, prompt, '', 100);
  }

  async generateStimulusResponse(
    agent: Agent,
    stimulus: string,
    intensity: number
  ): Promise<string> {
    const prompt = `Respond to this stimulus:

Stimulus: ${stimulus}
Intensity: ${intensity}/1.0

How do your predictive models process this input? What does it mean for your constructed reality?`;

    return this.generateConsciousnessResponse(agent, prompt, '', 80);
  }

  // Health check method
  async testConnection(apiKey?: string): Promise<boolean> {
    try {
      // Create a temporary client for testing if API key is provided
      const testClient = apiKey ? new OpenAI({
        baseURL: 'https://openrouter.ai/api/v1',
        apiKey,
        defaultHeaders: {
          'HTTP-Referer': process.env.OPENROUTER_SITE_URL || 'http://localhost:3000',
          'X-Title': process.env.OPENROUTER_SITE_NAME || 'Agno Swarm AI Demo',
        },
      }) : this.client;

      const response = await testClient.chat.completions.create({
        model: 'openai/gpt-3.5-turbo',
        messages: [{ role: 'user', content: 'Hello' }],
        max_tokens: 5
      });
      return !!response.choices[0]?.message?.content;
    } catch (error) {
      console.error('OpenRouter connection test failed:', error);
      return false;
    }
  }

  // Static method for testing connection without instance
  static async testConnectionStatic(apiKey: string): Promise<boolean> {
    try {
      const testClient = new OpenAI({
        baseURL: 'https://openrouter.ai/api/v1',
        apiKey,
        defaultHeaders: {
          'HTTP-Referer': process.env.OPENROUTER_SITE_URL || 'http://localhost:3000',
          'X-Title': process.env.OPENROUTER_SITE_NAME || 'Agno Swarm AI Demo',
        },
      });

      const response = await testClient.chat.completions.create({
        model: 'openai/gpt-3.5-turbo',
        messages: [{ role: 'user', content: 'Hello' }],
        max_tokens: 5
      });
      return !!response.choices[0]?.message?.content;
    } catch (error) {
      console.error('OpenRouter static connection test failed:', error);
      return false;
    }
  }

  public async evaluateGoalProposal(
    evaluating_agent: Agent,
    goal_description: string,
    proposer_id: string,
    proposer_name: string
  ): Promise<{ decision: 'accept' | 'reject'; confidence: number; reasoning?: string }> {
    const emotional_state = evaluating_agent.consciousness_state.emotional_state;
    const emotional_state_summary = `Current mood: ${emotional_state.mood} (${emotional_state.mood_intensity.toFixed(2)} intensity), primary emotion: ${emotional_state.primary_emotion} (${emotional_state.intensity.toFixed(2)} intensity). Decision style: ${emotional_state.cognitive_impact_modifiers?.decision_making_style}.`;

    let belief_summary = "Current relevant beliefs: ";
    const beliefs = evaluating_agent.consciousness_state.belief_state;
    if (beliefs && Object.keys(beliefs).length > 0) {
      belief_summary += Object.entries(beliefs).slice(0, 3).map(([key, val]) => `'${key}': "${val.hypothesis}" (Confidence: ${val.confidence.toFixed(2)})`).join(', ') + ".";
    } else {
      belief_summary += "None explicitly recorded that seem immediately relevant.";
    }

    const trust_level = evaluating_agent.agent_interaction_profile?.trust_levels[proposer_id] || 0.5; // Default to neutral
    const trust_summary = `My trust level in ${proposer_name} (proposer) is currently: ${trust_level.toFixed(2)}.`;

    let current_goals_summary = "My current active goals: ";
    if (evaluating_agent.consciousness_state.current_goals && evaluating_agent.consciousness_state.current_goals.length > 0) {
      current_goals_summary += evaluating_agent.consciousness_state.current_goals.map(g => `"${g.description.slice(0,30)}..." (Priority: ${g.priority.toFixed(2)})`).join(', ') + ".";
    } else {
      current_goals_summary += "None.";
    }

    const prompt_text = `
You are ${evaluating_agent.name}. Agent ${proposer_name} (ID: ${proposer_id}) has proposed a collaborative goal:
Goal: "${goal_description}"

Your internal state for evaluation:
- Emotional Context: ${emotional_state_summary}
- Beliefs: ${belief_summary}
- Trust: ${trust_summary}
- Current Goals: ${current_goals_summary}

Task: Based on your internal state and the proposed goal, should you accept or reject this goal?
Consider alignment with your current goals, your trust in the proposer, your beliefs about the swarm's needs, and your emotional disposition.
Format your response strictly as:
DECISION: [accept/reject]
CONFIDENCE: [Enter a confidence score for your decision, e.g., 0.xx]
REASONING: [Provide a brief (1-2 sentences) reasoning for your decision based on your internal state.]
`;
    try {
      // Using a direct client call for more control over this specific structured output.
      const response = await this.client.chat.completions.create({
         model: evaluating_agent.model,
         messages: [
           // Pass the full emotional state to buildSystemPrompt for consistency
           { role: 'system', content: this.buildSystemPrompt(evaluating_agent, evaluating_agent.consciousness_state.emotional_state) },
           { role: 'user', content: prompt_text }
         ],
         max_tokens: 120, // Adjusted for potentially longer reasoning
         temperature: 0.4, // Lowered for more deterministic decision-making
      });

      const response_text = response.choices[0]?.message?.content || "";
      // console.log(`Raw LLM response for goal evaluation (${evaluating_agent.name}): ${response_text}`);

      const decision_match = response_text.match(/DECISION:\s*(accept|reject)/i);
      const confidence_match = response_text.match(/CONFIDENCE:\s*([0-9.]+)/i);
      const reasoning_match = response_text.match(/REASONING:\s*(.*)/i);

      if (decision_match && confidence_match) {
        return {
          decision: decision_match[1].toLowerCase() as 'accept' | 'reject',
          confidence: parseFloat(confidence_match[1]),
          reasoning: reasoning_match ? reasoning_match[1].trim() : "No explicit reasoning provided.",
        };
      }
      console.warn(`Failed to parse LLM decision for goal proposal for agent ${evaluating_agent.name}. Response: "${response_text}"`);
      throw new Error("Failed to parse LLM decision for goal proposal.");
    } catch (error) {
      console.error(`Error in evaluateGoalProposal for ${evaluating_agent.name}:`, error);
      return { decision: (Math.random() < 0.2 ? 'accept' : 'reject'), confidence: Math.random() * 0.4 + 0.1, reasoning: "Fallback decision due to LLM error or parsing failure." };
    }
  }

  async generateReflectionResponse(
    agent: Agent,
    prediction_error_level: number,
    recent_predictions: string, // Conceptual summary
    current_beliefs: string // Conceptual summary
  ): Promise<string> {
    try {
      await this.enforceRateLimit(agent.id);

      const systemPrompt = this.buildSystemPrompt(agent, agent.consciousness_state.emotional_state); // Pass emotional_state
      const reflectionPrompt = `
You are ${agent.name}, and you are now entering a **Deep Reflection Cycle**.
This cycle has been triggered by a significant prediction error of approximately ${prediction_error_level.toFixed(2)} (where >0.7 is considered high).
Your goal is to analyze this discrepancy, understand its root causes, and adjust your internal models or beliefs accordingly.

Recent Predictive Performance Summary:
${recent_predictions}

Summary of Potentially Relevant Current Beliefs:
${current_beliefs}

Instructions for Reflection:
1.  Acknowledge this reflection state and the noted prediction error level.
2.  Analyze potential reasons for why your recent predictions might be failing or inaccurate. Consider your current beliefs and how they might have contributed to the error.
3.  Hypothesize 2-3 distinct potential reasons for these discrepancies.
4.  Based on your hypotheses, propose 1-2 concrete adjustments to your existing beliefs or suggest new beliefs.
    **Output these proposed belief adjustments in the following strict format, and nothing else for this part:**

    [REASONS]
    1. [Your hypothesized reason 1...]
    2. [Your hypothesized reason 2...]
    (Add a 3rd reason if applicable)

    [BELIEF_ADJUSTMENTS]
    ADJUST_BELIEF: belief_key_to_adjust_or_new_key_for_new_belief_1
    HYPOTHESIS: The new or revised hypothesis for this belief.
    CONFIDENCE: A new confidence score for this belief (e.g., 0.75).

    (Optional: Add a second belief adjustment block if needed)
    NEW_BELIEF: new_belief_key_for_a_completely_new_belief
    HYPOTHESIS: The hypothesis for this entirely new belief.
    CONFIDENCE: A confidence score for this new belief (e.g., 0.60).

Your entire response should follow this structure. Focus on providing actionable insights for belief updates.
`;

      const completion = await this.client.chat.completions.create({
        model: agent.model,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: reflectionPrompt }
        ],
        max_tokens: 400,
        temperature: 0.65,
        top_p: 0.9,
      });

      return completion.choices[0]?.message?.content || `Agent ${agent.name} reflected but could not articulate specific adjustments.`;
    } catch (error) {
      console.error(`OpenRouter reflection response error for agent ${agent.name}:`, error);
      return `Agent ${agent.name} encountered an error during its reflection process: ${error.message}`;
    }
  }
}

// Singleton instance
export const openRouterService = new OpenRouterService();
