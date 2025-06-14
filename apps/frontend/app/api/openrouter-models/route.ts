
import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

interface OpenRouterModel {
  id: string;
  name: string;
  description?: string;
  pricing: {
    prompt: string;
    completion: string;
  };
  context_length: number;
  architecture: {
    modality: string;
    tokenizer: string;
    instruct_type?: string;
  };
  top_provider: {
    context_length: number;
    max_completion_tokens?: number;
    is_moderated: boolean;
  };
  per_request_limits?: {
    prompt_tokens: string;
    completion_tokens: string;
  };
}

interface OpenRouterModelsResponse {
  data: OpenRouterModel[];
}

export async function GET(request: NextRequest) {
  try {
    console.log('Fetching models from OpenRouter API...');
    
    const response = await fetch('https://openrouter.ai/api/v1/models', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store', // Ensure fresh data
    });

    if (!response.ok) {
      console.error('OpenRouter API error:', response.status, response.statusText);
      return NextResponse.json(
        { 
          error: 'Failed to fetch models from OpenRouter',
          status: response.status,
          statusText: response.statusText
        },
        { status: response.status }
      );
    }

    const data: OpenRouterModelsResponse = await response.json();
    console.log(`Successfully fetched ${data.data?.length || 0} models from OpenRouter`);

    // Transform the data to our format
    const transformedModels = data.data.map(model => {
      // Determine category based on model ID
      let category = 'other';
      const modelId = model.id.toLowerCase();
      
      if (modelId.includes('gpt') || modelId.includes('openai')) {
        category = 'gpt';
      } else if (modelId.includes('claude') || modelId.includes('anthropic')) {
        category = 'claude';
      } else if (modelId.includes('gemini') || modelId.includes('google')) {
        category = 'gemini';
      } else if (modelId.includes('llama') || modelId.includes('meta')) {
        category = 'llama';
      } else if (modelId.includes('mixtral') || modelId.includes('mistral')) {
        category = 'mixtral';
      } else if (modelId.includes('qwen') || modelId.includes('alibaba')) {
        category = 'qwen';
      } else if (modelId.includes('deepseek')) {
        category = 'deepseek';
      } else if (modelId.includes('cohere')) {
        category = 'cohere';
      }

      // Extract provider from model ID
      const provider = model.id.split('/')[0] || 'Unknown';
      
      // Create a clean display name
      let displayName = model.name;
      if (!displayName || displayName === model.id) {
        // If no name or name is same as ID, create a better display name
        const parts = model.id.split('/');
        displayName = parts[parts.length - 1]
          .replace(/-/g, ' ')
          .replace(/\b\w/g, l => l.toUpperCase());
      }

      return {
        id: model.id,
        name: displayName,
        provider: provider.charAt(0).toUpperCase() + provider.slice(1),
        description: model.description || `${displayName} model`,
        category,
        contextLength: model.context_length,
        pricing: {
          prompt: model.pricing.prompt,
          completion: model.pricing.completion
        },
        modality: model.architecture.modality,
        isModerated: model.top_provider.is_moderated
      };
    });

    // Sort models by category and then by name
    transformedModels.sort((a, b) => {
      if (a.category !== b.category) {
        // Define category order
        const categoryOrder = ['gpt', 'claude', 'gemini', 'llama', 'mixtral', 'qwen', 'deepseek', 'cohere', 'other'];
        return categoryOrder.indexOf(a.category) - categoryOrder.indexOf(b.category);
      }
      return a.name.localeCompare(b.name);
    });

    return NextResponse.json({
      models: transformedModels,
      count: transformedModels.length,
      lastUpdated: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error fetching OpenRouter models:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error while fetching models',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
