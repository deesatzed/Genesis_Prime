'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Activity, 
  MessageSquare, 
  Brain, 
  Zap, 
  Clock,
  DollarSign,
  TrendingUp,
  Users,
  Eye,
  Sparkles
} from 'lucide-react';
import { SwarmState } from '@/lib/types';

interface ActivityMonitorProps {
  swarmState: SwarmState;
  isSimulationRunning: boolean;
  className?: string;
}

interface TokenMetrics {
  totalTokensUsed: number;
  averageTokensPerMessage: number;
  estimatedCost: number;
  messagesGenerated: number;
  lastActivityTime: Date | null;
  stimuliCount: number;
  behaviorsCount: number;
}

export function ActivityMonitor({ 
  swarmState, 
  isSimulationRunning, 
  className = '' 
}: ActivityMonitorProps) {
  const [metrics, setMetrics] = useState<TokenMetrics>({
    totalTokensUsed: 0,
    averageTokensPerMessage: 0,
    estimatedCost: 0,
    messagesGenerated: 0,
    lastActivityTime: null,
    stimuliCount: 0,
    behaviorsCount: 0,
  });

  const [activityLog, setActivityLog] = useState<string[]>([]);
  const [lastSimulationState, setLastSimulationState] = useState(isSimulationRunning);

  useEffect(() => {
    // Track simulation state changes
    if (isSimulationRunning !== lastSimulationState) {
      const timestamp = new Date().toLocaleTimeString();
      const activity = isSimulationRunning 
        ? `🟢 Simulation started at ${timestamp}`
        : `🔴 Simulation stopped at ${timestamp}`;
      
      setActivityLog(prev => [activity, ...prev.slice(0, 9)]); // Keep last 10 activities
      setLastSimulationState(isSimulationRunning);
    }
  }, [isSimulationRunning, lastSimulationState]);

  useEffect(() => {
    // Calculate token metrics based on swarm activity
    const messages = swarmState.communication_network.message_history || [];
    const behaviors = swarmState.emergent_behaviors || [];
    const stimuli = swarmState.stimulus_events || [];

    // Estimate tokens (simplified calculation)
    const estimatedTokensPerMessage = 50; // Average tokens per swarm message
    const estimatedTokensPerBehavior = 30; // Tokens for emergent behavior processing
    const estimatedTokensPerStimulus = 25; // Tokens for stimulus processing

    const totalTokens = 
      (messages.length * estimatedTokensPerMessage) +
      (behaviors.length * estimatedTokensPerBehavior) +
      (stimuli.length * estimatedTokensPerStimulus);

    // Rough cost estimate (varies by model, using average)
    const estimatedCostPerToken = 0.000015; // Approximate cost in USD
    const estimatedCost = totalTokens * estimatedCostPerToken;

    const averageTokens = messages.length > 0 ? Math.round(totalTokens / messages.length) : 0;
    
    const lastActivity = messages.length > 0 
      ? new Date(Math.max(...messages.map(m => new Date(m.timestamp).getTime())))
      : null;

    setMetrics({
      totalTokensUsed: totalTokens,
      averageTokensPerMessage: averageTokens,
      estimatedCost,
      messagesGenerated: messages.length,
      lastActivityTime: lastActivity,
      stimuliCount: stimuli.length,
      behaviorsCount: behaviors.length,
    });

    // Track new messages
    if (messages.length > metrics.messagesGenerated) {
      const newMessageCount = messages.length - metrics.messagesGenerated;
      const timestamp = new Date().toLocaleTimeString();
      setActivityLog(prev => [
        `💬 ${newMessageCount} new message(s) generated at ${timestamp}`,
        ...prev.slice(0, 9)
      ]);
    }

    // Track new stimuli
    if (stimuli.length > metrics.stimuliCount) {
      const newStimuliCount = stimuli.length - metrics.stimuliCount;
      const timestamp = new Date().toLocaleTimeString();
      setActivityLog(prev => [
        `🎯 ${newStimuliCount} new stimuli introduced at ${timestamp}`,
        ...prev.slice(0, 9)
      ]);
    }

    // Track new emergent behaviors
    if (behaviors.length > metrics.behaviorsCount) {
      const newBehaviorsCount = behaviors.length - metrics.behaviorsCount;
      const timestamp = new Date().toLocaleTimeString();
      setActivityLog(prev => [
        `✨ ${newBehaviorsCount} new emergent behavior(s) at ${timestamp}`,
        ...prev.slice(0, 9)
      ]);
    }
  }, [swarmState, metrics.messagesGenerated, metrics.stimuliCount, metrics.behaviorsCount]);

  const getActivityStatus = () => {
    if (!isSimulationRunning) return { text: 'Simulation Stopped', color: 'text-red-400' };
    
    const now = new Date();
    const lastActivity = metrics.lastActivityTime;
    
    if (!lastActivity) return { text: 'Waiting for Activity', color: 'text-yellow-400' };
    
    const timeSinceActivity = now.getTime() - lastActivity.getTime();
    const secondsSince = Math.floor(timeSinceActivity / 1000);
    
    if (secondsSince < 10) return { text: 'Active Now', color: 'text-green-400' };
    if (secondsSince < 60) return { text: `Active ${secondsSince}s ago`, color: 'text-blue-400' };
    
    return { text: 'Inactive', color: 'text-orange-400' };
  };

  const status = getActivityStatus();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={className}
    >
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-time Activity Status */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-green-400" />
              Real-time Activity Status
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Eye className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-medium text-white">Status</span>
                </div>
                <div className={`text-lg font-bold ${status.color}`}>
                  {status.text}
                </div>
                {isSimulationRunning && (
                  <motion.div
                    className="w-2 h-2 bg-green-400 rounded-full mt-1"
                    animate={{ scale: [1, 1.5, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                )}
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <MessageSquare className="w-4 h-4 text-purple-400" />
                  <span className="text-sm font-medium text-white">Messages</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {metrics.messagesGenerated}
                </div>
                <div className="text-xs text-slate-400">
                  Total generated
                </div>
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-medium text-white">Behaviors</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {swarmState.emergent_behaviors?.length || 0}
                </div>
                <div className="text-xs text-slate-400">
                  Emergent patterns
                </div>
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="w-4 h-4 text-orange-400" />
                  <span className="text-sm font-medium text-white">Stimuli</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {swarmState.stimulus_events?.length || 0}
                </div>
                <div className="text-xs text-slate-400">
                  Events introduced
                </div>
              </div>
            </div>

            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2">Recent Activity</div>
              <div className="space-y-1 max-h-32 overflow-y-auto">
                {activityLog.length > 0 ? (
                  activityLog.map((activity, index) => (
                    <div key={index} className="text-xs text-slate-300 bg-slate-700 rounded px-2 py-1">
                      {activity}
                    </div>
                  ))
                ) : (
                  <div className="text-xs text-slate-500 italic">
                    No activity yet - start the simulation to see real-time updates
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Token Usage & Cost Tracking */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-green-400" />
              Token Usage & Costs
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Brain className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-medium text-white">Total Tokens</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {metrics.totalTokensUsed.toLocaleString()}
                </div>
                <div className="text-xs text-slate-400">
                  Est. processing tokens
                </div>
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <span className="text-sm font-medium text-white">Avg/Message</span>
                </div>
                <div className="text-lg font-bold text-white">
                  {metrics.averageTokensPerMessage}
                </div>
                <div className="text-xs text-slate-400">
                  Tokens per message
                </div>
              </div>

              <div className="bg-slate-800 rounded-lg p-3 col-span-2">
                <div className="flex items-center gap-2 mb-2">
                  <DollarSign className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-medium text-white">Estimated Cost</span>
                </div>
                <div className="text-2xl font-bold text-green-400">
                  ${metrics.estimatedCost.toFixed(4)}
                </div>
                <div className="text-xs text-slate-400">
                  Approximate USD (varies by model)
                </div>
              </div>
            </div>

            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2">Cost Breakdown</div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Messages Processing:</span>
                  <span className="text-white">
                    ${(metrics.messagesGenerated * 50 * 0.000015).toFixed(4)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Emergent Behaviors:</span>
                  <span className="text-white">
                    ${((swarmState.emergent_behaviors?.length || 0) * 30 * 0.000015).toFixed(4)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Stimulus Processing:</span>
                  <span className="text-white">
                    ${((swarmState.stimulus_events?.length || 0) * 25 * 0.000015).toFixed(4)}
                  </span>
                </div>
                <div className="border-t border-slate-600 pt-1 mt-2 flex justify-between items-center font-medium">
                  <span className="text-slate-300">Total Estimated:</span>
                  <span className="text-green-400">${metrics.estimatedCost.toFixed(4)}</span>
                </div>
              </div>
            </div>

            <div className="text-xs text-slate-500 bg-slate-800/50 p-2 rounded">
              <strong>Note:</strong> Token counts and costs are estimates based on simulated swarm activity. 
              Actual API usage may vary depending on configured models and complexity.
            </div>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}