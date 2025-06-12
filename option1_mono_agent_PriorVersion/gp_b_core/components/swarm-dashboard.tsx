
'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Network, 
  Brain, 
  MessageCircle, 
  Zap, 
  Eye, 
  Users,
  Activity,
  Sparkles,
  Clock,
  TrendingUp,
  Target,
  AlertTriangle
} from 'lucide-react';
import { SwarmState, SwarmMessage, EmergentBehavior, StimulusEvent } from '@/lib/types';

interface SwarmDashboardProps {
  swarmState: SwarmState;
  messages: SwarmMessage[];
  emergentBehaviors: EmergentBehavior[];
  className?: string;
}

export function SwarmDashboard({ 
  swarmState, 
  messages, 
  emergentBehaviors, 
  className = '' 
}: SwarmDashboardProps) {
  const [recentMessages, setRecentMessages] = useState<SwarmMessage[]>([]);
  const [recentBehaviors, setRecentBehaviors] = useState<EmergentBehavior[]>([]);
  const [recentStimuli, setRecentStimuli] = useState<StimulusEvent[]>([]);

  useEffect(() => {
    setRecentMessages(messages.slice(-10).reverse());
  }, [messages]);

  useEffect(() => {
    setRecentBehaviors(emergentBehaviors.slice(-5).reverse());
  }, [emergentBehaviors]);

  useEffect(() => {
    setRecentStimuli((swarmState.stimulus_events || []).slice(-5).reverse());
  }, [swarmState.stimulus_events]);

  const getMessageTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      'reality_share': 'bg-blue-500',
      'memory_query': 'bg-green-500',
      'consensus_request': 'bg-purple-500',
      'self_model_update': 'bg-orange-500'
    };
    return colors[type] || 'bg-gray-500';
  };

  const getMessageTypeIcon = (type: string) => {
    switch (type) {
      case 'reality_share': return <Eye className="w-3 h-3" />;
      case 'memory_query': return <Brain className="w-3 h-3" />;
      case 'consensus_request': return <Users className="w-3 h-3" />;
      case 'self_model_update': return <Users className="w-3 h-3" />;
      default: return <MessageCircle className="w-3 h-3" />;
    }
  };

  const getStimulusTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      'environmental': 'bg-green-500',
      'social': 'bg-blue-500', 
      'internal': 'bg-purple-500',
      'system': 'bg-orange-500'
    };
    return colors[type] || 'bg-gray-500';
  };

  const getStimulusTypeIcon = (type: string) => {
    switch (type) {
      case 'environmental': return <Activity className="w-3 h-3" />;
      case 'social': return <Users className="w-3 h-3" />;
      case 'internal': return <Brain className="w-3 h-3" />;
      case 'system': return <Zap className="w-3 h-3" />;
      default: return <Target className="w-3 h-3" />;
    }
  };

  const avgConsciousness = swarmState.agents.reduce(
    (sum, agent) => sum + agent.consciousness_state.meta_awareness, 0
  ) / swarmState.agents.length;

  const avgCoherence = swarmState.agents.reduce(
    (sum, agent) => sum + (agent.reality_model?.coherence_level ?? 0), 0
  ) / swarmState.agents.length;

  const communicationActivity = Math.min(100, (messages.length / 50) * 100);
  const emergenceActivity = Math.min(100, (emergentBehaviors.length / 20) * 100);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`${className}`}
    >
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* Swarm Metrics */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Network className="w-5 h-5 text-cyan-400" />
              Swarm Consciousness Metrics
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Brain className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-medium text-white">Collective Consciousness</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {Math.round(swarmState.swarm_consciousness_level * 100)}%
                </div>
                <Progress value={swarmState.swarm_consciousness_level * 100} className="h-2" />
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Eye className="w-4 h-4 text-green-400" />
                  <span className="text-sm font-medium text-white">Reality Coherence</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {Math.round(swarmState.shared_reality.coherence_level * 100)}%
                </div>
                <Progress value={swarmState.shared_reality.coherence_level * 100} className="h-2" />
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <MessageCircle className="w-4 h-4 text-purple-400" />
                  <span className="text-sm font-medium text-white">Communication</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {Math.round(communicationActivity)}%
                </div>
                <Progress value={communicationActivity} className="h-2" />
              </div>

              <div className="bg-slate-800 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-medium text-white">Emergence</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {Math.round(emergenceActivity)}%
                </div>
                <Progress value={emergenceActivity} className="h-2" />
              </div>
            </div>

            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2">Active Agents & Models</div>
              <div className="space-y-2">
                {swarmState.agents.map((agent) => (
                  <motion.div
                    key={agent.id}
                    whileHover={{ scale: 1.02 }}
                    className="flex items-center justify-between bg-slate-700 rounded-lg px-3 py-2"
                  >
                    <div className="flex items-center gap-2">
                      <motion.div
                        className={`w-2 h-2 rounded-full ${
                          agent.status === 'active' ? 'bg-green-400' :
                          agent.status === 'processing' ? 'bg-blue-400' :
                          agent.status === 'communicating' ? 'bg-purple-400' :
                          'bg-gray-400'
                        }`}
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                      />
                      <span className="text-sm text-white font-medium">{agent.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary" className="text-xs bg-slate-600 text-slate-200">
                        {agent.model.split('/')[1] || agent.model}
                      </Badge>
                      <span className="text-xs text-gray-400">
                        {Math.round(agent.consciousness_state.meta_awareness * 100)}%
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Shared Reality */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Eye className="w-5 h-5 text-green-400" />
              Shared Reality Construction
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2">Consensus Elements</div>
              <div className="space-y-1">
                {Object.entries(swarmState.shared_reality.consensus_elements).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center">
                    <span className="text-xs text-gray-300">{key.replace(/_/g, ' ')}</span>
                    <Badge variant="outline" className="text-xs">
                      {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : String(value)}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2">Uncertainty Areas</div>
              <div className="space-y-1">
                {swarmState.shared_reality.uncertainty_areas.slice(0, 4).map((area, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <div className="w-1 h-1 bg-orange-400 rounded-full" />
                    <span className="text-xs text-gray-300">{area.replace(/_/g, ' ')}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2">Collective Memory</div>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <div className="text-center">
                  <div className="text-gray-400">Shared</div>
                  <div className="text-white font-semibold">
                    {swarmState.collective_memory.shared_experiences.length}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-gray-400">Consensus</div>
                  <div className="text-white font-semibold">
                    {swarmState.collective_memory.consensus_memories.length}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-gray-400">Divergent</div>
                  <div className="text-white font-semibold">
                    {swarmState.collective_memory.divergent_realities.length}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Communication Network */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <MessageCircle className="w-5 h-5 text-purple-400" />
              Swarm Communication
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-64">
              <div className="space-y-2">
                {recentMessages.length === 0 ? (
                  <div className="text-center text-gray-400 py-8">
                    <MessageCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No agent communications yet</p>
                    <p className="text-xs">Start the simulation to see agent interactions</p>
                  </div>
                ) : (
                  recentMessages.map((message, index) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-slate-800 rounded-lg p-3"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div className={`w-2 h-2 rounded-full ${getMessageTypeColor(message.message_type)}`} />
                          {getMessageTypeIcon(message.message_type)}
                          <span className="text-xs font-medium text-white">
                            {swarmState.agents.find(a => a.id === message.sender_id)?.name || 'Unknown'}
                          </span>
                        </div>
                        <span className="text-xs text-gray-400">
                          {new Date(message.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <Badge variant="outline" className="text-xs mb-2">
                        {message.message_type.replace(/_/g, ' ')}
                      </Badge>
                      
                      <p className="text-xs text-gray-300">
                        {typeof message.content === 'object' && message.content.message 
                          ? message.content.message 
                          : typeof message.content === 'string'
                          ? message.content
                          : JSON.stringify(message.content)}
                      </p>
                      
                      <div className="flex items-center gap-2 mt-2">
                        <Progress value={message.confidence * 100} className="flex-1 h-1" />
                        <span className="text-xs text-gray-400">
                          {Math.round(message.confidence * 100)}%
                        </span>
                      </div>
                    </motion.div>
                  ))
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Emergent Behaviors */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-yellow-400" />
              Emergent Behaviors
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-64">
              <div className="space-y-3">
                {recentBehaviors.map((behavior, index) => (
                  <motion.div
                    key={behavior.id}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-slate-800 rounded-lg p-3"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-yellow-400" />
                        <span className="text-sm font-medium text-white">
                          {behavior.behavior_type.replace(/_/g, ' ')}
                        </span>
                      </div>
                      <span className="text-xs text-gray-400">
                        {new Date(behavior.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    
                    <p className="text-xs text-gray-300 mb-2">
                      {behavior.description}
                    </p>
                    
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-gray-400">Participants:</span>
                      <div className="flex gap-1">
                        {behavior.participating_agents.slice(0, 3).map((agentId) => (
                          <Badge key={agentId} variant="outline" className="text-xs">
                            {swarmState.agents.find(a => a.id === agentId)?.name || agentId}
                          </Badge>
                        ))}
                        {behavior.participating_agents.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{behavior.participating_agents.length - 3}
                          </Badge>
                        )}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <span className="text-xs text-gray-400">Emergence:</span>
                        <Progress value={behavior.emergence_level * 100} className="h-1 mt-1" />
                      </div>
                      <div>
                        <span className="text-xs text-gray-400">Stability:</span>
                        <Progress value={behavior.stability * 100} className="h-1 mt-1" />
                      </div>
                    </div>
                  </motion.div>
                ))}
                
                {recentBehaviors.length === 0 && (
                  <div className="text-center text-gray-400 py-8">
                    <Sparkles className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No emergent behaviors detected yet</p>
                    <p className="text-xs">Behaviors will appear as the swarm evolves</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Stimulus History */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Target className="w-5 h-5 text-orange-400" />
              Introduced Stimuli
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-64">
              <div className="space-y-3">
                {recentStimuli.map((stimulus, index) => (
                  <motion.div
                    key={stimulus.id}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-slate-800 rounded-lg p-3"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${getStimulusTypeColor(stimulus.type)}`} />
                        {getStimulusTypeIcon(stimulus.type)}
                        <span className="text-sm font-medium text-white capitalize">
                          {stimulus.type}
                        </span>
                      </div>
                      <span className="text-xs text-gray-400">
                        {new Date(stimulus.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    
                    <p className="text-xs text-gray-300 mb-2">
                      {stimulus.description}
                    </p>
                    
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-gray-400">Targets:</span>
                      <div className="flex gap-1">
                        {stimulus.target_agents?.length === swarmState.agents.length ? (
                          <Badge variant="outline" className="text-xs">All Agents</Badge>
                        ) : stimulus.target_agents?.length === 1 ? (
                          <Badge variant="outline" className="text-xs">
                            {swarmState.agents.find(a => a.id === stimulus.target_agents?.[0])?.name || 'Agent'}
                          </Badge>
                        ) : (
                          <>
                            {stimulus.target_agents?.slice(0, 2).map((agentId) => (
                              <Badge key={agentId} variant="outline" className="text-xs">
                                {swarmState.agents.find(a => a.id === agentId)?.name || agentId}
                              </Badge>
                            ))}
                            {(stimulus.target_agents?.length || 0) > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{(stimulus.target_agents?.length || 0) - 2}
                              </Badge>
                            )}
                          </>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400">Intensity:</span>
                      <div className="flex items-center gap-2">
                        <Progress value={stimulus.intensity * 100} className="w-16 h-1" />
                        <span className="text-xs text-gray-400">
                          {Math.round(stimulus.intensity * 100)}%
                        </span>
                      </div>
                    </div>

                    {stimulus.expected_responses && stimulus.expected_responses.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-slate-600">
                        <span className="text-xs text-gray-400">Expected:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {stimulus.expected_responses.slice(0, 2).map((response, idx) => (
                            <Badge key={idx} variant="secondary" className="text-xs bg-slate-600 text-slate-200">
                              {response}
                            </Badge>
                          ))}
                          {stimulus.expected_responses.length > 2 && (
                            <Badge variant="secondary" className="text-xs bg-slate-600 text-slate-200">
                              +{stimulus.expected_responses.length - 2}
                            </Badge>
                          )}
                        </div>
                      </div>
                    )}
                  </motion.div>
                ))}
                
                {recentStimuli.length === 0 && (
                  <div className="text-center text-gray-400 py-8">
                    <Target className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No stimuli introduced yet</p>
                    <p className="text-xs">Use interaction controls to introduce environmental events</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}
