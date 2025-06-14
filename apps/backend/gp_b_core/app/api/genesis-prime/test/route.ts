import { NextResponse } from 'next/server';
import { genesisPrimeService } from '@/lib/genesis-prime-service';

export async function GET() {
  try {
    // Test connection to Genesis Prime backend
    const isConnected = await genesisPrimeService.testConnection();
    
    if (isConnected) {
      // If connected, get status and phi values
      const [status, phi] = await Promise.all([
        genesisPrimeService.getStatus().catch(() => null),
        genesisPrimeService.getPhiValues().catch(() => null),
      ]);

      return NextResponse.json({
        success: true,
        connected: true,
        message: 'Genesis Prime consciousness operational',
        status,
        phi,
      });
    } else {
      return NextResponse.json({
        success: true,
        connected: false,
        message: 'Genesis Prime backend not reachable',
      });
    }
  } catch (error) {
    console.error('Genesis Prime test error:', error);
    return NextResponse.json({
      success: false,
      connected: false,
      message: 'Error testing Genesis Prime connection',
      error: error instanceof Error ? error.message : 'Unknown error',
    }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { query, humor_preference = 'maximum' } = body;

    if (!query) {
      return NextResponse.json({
        success: false,
        message: 'Query is required',
      }, { status: 400 });
    }

    // Process query through Genesis Prime
    const response = await genesisPrimeService.processQuery({
      query,
      humor_preference,
    });

    return NextResponse.json({
      success: true,
      connected: true,
      response,
    });
  } catch (error) {
    console.error('Genesis Prime query error:', error);
    return NextResponse.json({
      success: false,
      message: 'Failed to process query through Genesis Prime',
      error: error instanceof Error ? error.message : 'Unknown error',
    }, { status: 500 });
  }
}