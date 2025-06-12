
import { NextRequest, NextResponse } from 'next/server';
import { openRouterService, OpenRouterService } from '@/lib/openrouter-service';

export async function GET() {
  try {
    // Skip actual API test during build time
    if (process.env.NODE_ENV === 'production' || process.env.NEXT_PHASE === 'phase-production-build') {
      return NextResponse.json({
        success: true,
        connected: false,
        message: 'OpenRouter API connection skipped during build - using fallback responses'
      });
    }

    const isConnected = await openRouterService.testConnection();
    
    return NextResponse.json({
      success: true,
      connected: isConnected,
      message: isConnected 
        ? 'OpenRouter API connection successful' 
        : 'OpenRouter API connection failed - using fallback responses'
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      connected: false,
      message: 'Error testing OpenRouter connection',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { apiKey } = body;

    if (!apiKey) {
      return NextResponse.json({
        connected: false,
        message: 'API key is required'
      }, { status: 400 });
    }

    // Test the connection with the provided API key
    const isConnected = await OpenRouterService.testConnectionStatic(apiKey);
    
    return NextResponse.json({
      connected: isConnected,
      message: isConnected ? 'OpenRouter connection successful' : 'OpenRouter connection failed - check your API key'
    });
  } catch (error) {
    console.error('OpenRouter test error:', error);
    return NextResponse.json({
      connected: false,
      message: 'Failed to test OpenRouter connection'
    }, { status: 500 });
  }
}
