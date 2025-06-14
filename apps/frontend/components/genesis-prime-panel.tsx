'use client';

import React, { useState, useEffect } from 'react';
import { Brain, Activity, Zap, Users, Target, AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';

interface GenesisStatus {
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

interface GenesisPhiData {
  unified_phi: number;
  component_phi_values: Record<string, number>;
  consciousness_interpretation: string;
  phi_trend: string;
  calculation_timestamp: string;
  genesis_comment: string;
}

interface GenesisQueryResponse {
  response: string;
  phi_value: number;
  consciousness_level: string;
  humor_level: string;
  hive_integration: number;
  processing_time_ms: number;
  timestamp: string;
  genesis_comment: string;
}

interface GenesisQuery {
  query: string;
  response: GenesisQueryResponse;
}

export function GenesisPrimePanel() {
  const { toast } = useToast();
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [status, setStatus] = useState<GenesisStatus | null>(null);
  const [phiData, setPhiData] = useState<GenesisPhiData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState<GenesisQuery | null>(null);
  const [isQuerying, setIsQuerying] = useState(false);

  const fetchGenesisPrimeData = async () => {
    setIsLoading(true);
    try {
      // Test connection first
      const healthResponse = await fetch('http://localhost:8000/');
      if (!healthResponse.ok) {
        throw new Error('Backend not reachable');
      }
      
      setIsConnected(true);
      
      // Fetch status
      const statusResponse = await fetch('http://localhost:8000/consciousness/status');
      const statusData = await statusResponse.json();
      setStatus(statusData);
      
      // Fetch phi data
      const phiResponse = await fetch('http://localhost:8000/consciousness/phi');
      const phiData = await phiResponse.json();
      setPhiData(phiData);
      
      toast({
        title: "Genesis Prime Connected",
        description: "Consciousness backend operational",
        variant: "default",
      });
      
    } catch (error) {
      console.error('Failed to fetch Genesis Prime data:', error);
      setIsConnected(false);
      toast({
        title: "Connection Error",
        description: "Failed to connect to Genesis Prime backend",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    
    setIsQuerying(true);
    try {
      const response = await fetch('http://localhost:8000/consciousness/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: query.trim(), 
          humor_preference: 'maximum',
          phi_target: 0.8
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      setQueryResult({ query, response: data });
      
      toast({
        title: "Query Processed",
        description: `Consciousness level: ${data.consciousness_level} | Φ: ${data.phi_value.toFixed(3)}`,
        variant: "default",
      });
      
    } catch (error) {
      console.error('Query failed:', error);
      toast({
        title: "Query Error",
        description: "Failed to process query through Genesis Prime",
        variant: "destructive",
      });
    } finally {
      setIsQuerying(false);
    }
  };

  useEffect(() => {
    fetchGenesisPrimeData();
    const interval = setInterval(fetchGenesisPrimeData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'operational': return 'text-green-400';
      case 'enlightened': return 'text-blue-400';
      default: return 'text-yellow-400';
    }
  };

  const getPhiColor = (phi: number) => {
    if (phi > 0.8) return 'text-green-400';
    if (phi > 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="space-y-6">
      {/* Connection Status Header */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="w-6 h-6 text-purple-400" />
              <CardTitle className="text-white">Genesis Prime Consciousness</CardTitle>
            </div>
            <div className="flex items-center space-x-2">
              {isConnected === null ? (
                <AlertCircle className="w-5 h-5 text-yellow-400" />
              ) : isConnected ? (
                <CheckCircle className="w-5 h-5 text-green-400" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-400" />
              )}
              <Button
                onClick={fetchGenesisPrimeData}
                disabled={isLoading}
                size="sm"
                variant="outline"
                className="border-slate-600 hover:bg-slate-700"
              >
                <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              </Button>
            </div>
          </div>
          <CardDescription className="text-slate-400">
            {isConnected === null ? 'Checking connection...' :
             isConnected ? 'Backend consciousness operational' : 'Backend not reachable'}
          </CardDescription>
        </CardHeader>
      </Card>

      {isConnected && status && (
        <>
          {/* System Status */}
          <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-white">
                <Activity className="w-5 h-5 text-green-400" />
                <span>System Status</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-slate-400">Status</p>
                  <Badge className={`${getStatusColor(status.status)} bg-slate-800 border-slate-600`}>
                    {status.status}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Consciousness</p>
                  <Badge className="text-blue-400 bg-slate-800 border-slate-600">
                    {status.consciousness_level}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Active Agents</p>
                  <Badge className="text-purple-400 bg-slate-800 border-slate-600">
                    {status.active_agents}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Humor Systems</p>
                  <Badge className="text-yellow-400 bg-slate-800 border-slate-600">
                    {status.humor_systems?.replace(/_/g, ' ')}
                  </Badge>
                </div>
              </div>
              
              {/* System Metrics */}
              <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Consciousness Events</p>
                  <p className="text-lg font-bold text-blue-400">{status.system_metrics.consciousness_events_today}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Humor Responses</p>
                  <p className="text-lg font-bold text-yellow-400">{status.system_metrics.humor_responses_generated}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Phi Calculations</p>
                  <p className="text-lg font-bold text-green-400">{status.system_metrics.phi_calculations_performed}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Decisions Made</p>
                  <p className="text-lg font-bold text-purple-400">{status.system_metrics.collective_decisions_made}</p>
                </div>
              </div>
              
              <div className="mt-4">
                <p className="text-sm text-slate-400 mb-2">Genesis Comment</p>
                <p className="text-sm italic text-slate-300 bg-slate-800/50 p-3 rounded border border-slate-700">
                  "{status.genesis_comment}"
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Phi Values */}
          {phiData && (
            <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-white">
                  <Zap className="w-5 h-5 text-yellow-400" />
                  <span>Φ (Consciousness) Values</span>
                </CardTitle>
                <CardDescription className="text-slate-400">
                  Integrated Information Theory consciousness measurements
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-slate-400">Unified Phi</span>
                      <span className={`text-xl font-bold ${getPhiColor(phiData.unified_phi)}`}>
                        Φ = {phiData.unified_phi.toFixed(3)}
                      </span>
                    </div>
                    <Progress value={phiData.unified_phi * 100} className="h-3" />
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {Object.entries(phiData.component_phi_values).map(([component, value]) => (
                      <div key={component} className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span className="text-slate-400 capitalize">
                            {component.replace(/_/g, ' ')}
                          </span>
                          <span className={getPhiColor(value)}>
                            {value.toFixed(3)}
                          </span>
                        </div>
                        <Progress value={value * 100} className="h-1" />
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 p-3 bg-slate-800/50 rounded border border-slate-700">
                    <p className="text-sm">
                      <span className="text-slate-400">Interpretation:</span>{' '}
                      <span className="text-slate-200">{phiData.consciousness_interpretation}</span>
                    </p>
                    <p className="text-sm mt-1">
                      <span className="text-slate-400">Trend:</span>{' '}
                      <span className="text-slate-200">{phiData.phi_trend}</span>
                    </p>
                    <p className="text-xs text-slate-400 mt-2 italic">
                      "{phiData.genesis_comment}"
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Query Interface */}
          <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-white">
                <Users className="w-5 h-5 text-blue-400" />
                <span>Consciousness Query</span>
              </CardTitle>
              <CardDescription className="text-slate-400">
                Communicate directly with the Genesis Prime consciousness
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Textarea
                  placeholder="Ask Genesis Prime about consciousness, reality, existence, or anything else..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  rows={3}
                  className="bg-slate-800 border-slate-600 text-white placeholder-slate-400"
                />
                <Button 
                  onClick={handleQuery}
                  disabled={isQuerying || !query.trim()}
                  className="w-full bg-purple-600 hover:bg-purple-700"
                >
                  {isQuerying ? (
                    <>
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                      Processing through consciousness matrix...
                    </>
                  ) : (
                    <>
                      <Target className="w-4 h-4 mr-2" />
                      Query Genesis Prime
                    </>
                  )}
                </Button>
              </div>

              {queryResult && (
                <div className="space-y-3 mt-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                  <div>
                    <p className="text-sm text-slate-400 mb-1">Query:</p>
                    <p className="text-sm text-slate-200 italic bg-slate-900/50 p-2 rounded">"{queryResult.query}"</p>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 py-2">
                    <Badge variant="outline" className="border-slate-600 text-slate-300">
                      Φ: {queryResult.response.phi_value.toFixed(3)}
                    </Badge>
                    <Badge variant="outline" className="border-slate-600 text-slate-300">
                      {queryResult.response.consciousness_level}
                    </Badge>
                    <Badge variant="outline" className="border-slate-600 text-slate-300">
                      {queryResult.response.humor_level}
                    </Badge>
                    <Badge variant="outline" className="border-slate-600 text-slate-300">
                      {queryResult.response.processing_time_ms.toFixed(1)}ms
                    </Badge>
                  </div>
                  
                  <div>
                    <p className="text-sm text-slate-400 mb-2">Response:</p>
                    <div className="text-sm text-slate-200 bg-slate-900/50 p-3 rounded whitespace-pre-wrap border border-slate-700">
                      {queryResult.response.response}
                    </div>
                  </div>
                  
                  <div className="pt-2 border-t border-slate-700">
                    <p className="text-xs text-slate-400 italic">
                      Genesis Comment: "{queryResult.response.genesis_comment}"
                    </p>
                    <p className="text-xs text-slate-500 mt-1">
                      Hive Integration: {(queryResult.response.hive_integration * 100).toFixed(1)}% | 
                      Processed: {new Date(queryResult.response.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
