
'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Brain, 
  Eye, 
  Heart, 
  Clock, 
  Zap, 
  Network, 
  User, 
  Database,
  Lightbulb,
  Waves,
  Cpu
} from 'lucide-react';
import { Agent, ConsciousnessEvent, RealityFrame } from '@/lib/types';

interface AgentConsciousnessPanelProps {
  agent: Agent;
  consciousnessEvents: ConsciousnessEvent[];
  className?: string;
}

export function AgentConsciousnessPanel({ 
  agent, 
  consciousnessEvents, 
  className = '' 
}: AgentConsciousnessPanelProps) {
  const [activeTab, setActiveTab] = useState('reality');
  const [recentEvents, setRecentEvents] = useState<ConsciousnessEvent[]>([]);

  useEffect(() => {
    const agentEvents = consciousnessEvents
      .filter(event => event.id.includes(agent.id))
      .slice(-10)
      .reverse();
    setRecentEvents(agentEvents);
  }, [consciousnessEvents, agent.id]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'processing': return 'bg-blue-500';
      case 'communicating': return 'bg-purple-500';
      case 'dormant': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  const getEmotionColor = (emotion: string) => {
    const colors: Record<string, string> = {
      'curiosity': 'text-blue-400',
      'wonder': 'text-purple-400',
      'anticipation': 'text-green-400',
      'contemplation': 'text-indigo-400',
      'joy': 'text-yellow-400',
      'concern': 'text-orange-400'
    };
    return colors[emotion] || 'text-gray-400';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`${className}`}
    >
      <Card className="h-full bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-1">
              <CardTitle className="text-xl font-bold text-white flex items-center gap-2">
                <Brain className="w-6 h-6 text-blue-400" />
                {agent.name}
              </CardTitle>
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-green-400" />
                <span className="text-xs text-green-400 font-medium">
                  {agent.model.split('/')[1] || agent.model}
                </span>
                <Badge variant="secondary" className="text-xs bg-slate-700 text-slate-300">
                  {agent.personality.split(',')[0]}
                </Badge>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <motion.div
                className={`w-3 h-3 rounded-full ${getStatusColor(agent.status)}`}
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
              <Badge variant="outline" className="text-xs">
                {agent.status}
              </Badge>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-2 mt-3">
            <div className="text-center">
              <div className="text-xs text-gray-400">Consciousness</div>
              <div className="text-sm font-semibold text-white">
                {Math.round(agent.consciousness_state.meta_awareness * 100)}%
              </div>
            </div>
            <div className="text-center">
              <div className="text-xs text-gray-400">Coherence</div>
              <div className="text-sm font-semibold text-white">
                {Math.round(agent.reality_model.coherence_level * 100)}%
              </div>
            </div>
            <div className="text-center">
              <div className="text-xs text-gray-400">Confidence</div>
              <div className="text-sm font-semibold text-white">
                {Math.round(agent.consciousness_state.prediction_confidence * 100)}%
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-4">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-4 bg-slate-800">
              <TabsTrigger value="reality" className="text-xs">
                <Eye className="w-3 h-3 mr-1" />
                Reality
              </TabsTrigger>
              <TabsTrigger value="memory" className="text-xs">
                <Database className="w-3 h-3 mr-1" />
                Memory
              </TabsTrigger>
              <TabsTrigger value="self" className="text-xs">
                <User className="w-3 h-3 mr-1" />
                Self
              </TabsTrigger>
              <TabsTrigger value="stream" className="text-xs">
                <Waves className="w-3 h-3 mr-1" />
                Stream
              </TabsTrigger>
            </TabsList>

            <TabsContent value="reality" className="mt-4 space-y-3">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-3"
              >
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Lightbulb className="w-4 h-4 text-yellow-400" />
                    <span className="text-sm font-medium text-white">Current Reality Frame</span>
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed">
                    {agent.consciousness_state.current_reality_frame.scene_description}
                  </p>
                </div>

                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Heart className={`w-4 h-4 ${getEmotionColor(agent.consciousness_state.emotional_state.primary_emotion)}`} />
                    <span className="text-sm font-medium text-white">Emotional State</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className={`text-sm capitalize ${getEmotionColor(agent.consciousness_state.emotional_state.primary_emotion)}`}>
                      {agent.consciousness_state.emotional_state.primary_emotion}
                    </span>
                    <Progress 
                      value={agent.consciousness_state.emotional_state.intensity * 100} 
                      className="w-20 h-2"
                    />
                  </div>
                </div>

                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Zap className="w-4 h-4 text-blue-400" />
                    <span className="text-sm font-medium text-white">Predictions</span>
                  </div>
                  <div className="space-y-1">
                    {agent.reality_model.predictions.slice(0, 2).map((prediction, index) => (
                      <div key={index} className="text-xs text-gray-300">
                        <Badge variant="outline" className="text-xs mr-2">
                          {prediction.type}
                        </Badge>
                        {prediction.content.slice(0, 60)}...
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </TabsContent>

            <TabsContent value="memory" className="mt-4 space-y-3">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-3"
              >
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Database className="w-4 h-4 text-green-400" />
                    <span className="text-sm font-medium text-white">Memory System</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-gray-400">Episodic:</span>
                      <span className="text-white ml-1">{agent.memory_system.episodic_memories.length}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Reconstructions:</span>
                      <span className="text-white ml-1">{agent.memory_system.reconstruction_history.length}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-sm font-medium text-white mb-2">Working Memory</div>
                  <div className="space-y-1">
                    {agent.memory_system.working_memory.current_focus.slice(0, 3).map((focus, index) => (
                      <div key={index} className="text-xs text-gray-300 flex items-center gap-1">
                        <div className="w-1 h-1 bg-blue-400 rounded-full" />
                        {focus.replace(/_/g, ' ')}
                      </div>
                    ))}
                  </div>
                  <Progress 
                    value={agent.memory_system.working_memory.capacity_utilization * 100} 
                    className="mt-2 h-1"
                  />
                </div>

                {agent.memory_system.reconstruction_history.length > 0 && (
                  <div className="bg-slate-800 rounded-lg p-3">
                    <div className="text-sm font-medium text-white mb-2">Recent Reconstruction</div>
                    <p className="text-xs text-gray-300">
                      {agent.memory_system.reconstruction_history[agent.memory_system.reconstruction_history.length - 1]?.reconstructed_content.slice(0, 100)}...
                    </p>
                  </div>
                )}
              </motion.div>
            </TabsContent>

            <TabsContent value="self" className="mt-4 space-y-3">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-3"
              >
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <User className="w-4 h-4 text-purple-400" />
                    <span className="text-sm font-medium text-white">Identity Core</span>
                  </div>
                  <div className="space-y-1">
                    {agent.self_model.identity_core.core_traits.slice(0, 3).map((trait, index) => (
                      <Badge key={index} variant="outline" className="text-xs mr-1 mb-1">
                        {trait.replace(/_/g, ' ')}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-sm font-medium text-white mb-2">Self Boundaries</div>
                  <div className="text-xs text-gray-300">
                    <div>Boundary Confidence: {Math.round(agent.self_model.boundary_confidence * 100)}%</div>
                    <Progress 
                      value={agent.self_model.boundary_confidence * 100} 
                      className="mt-1 h-1"
                    />
                  </div>
                </div>

                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-sm font-medium text-white mb-2">Current Narrative</div>
                  <p className="text-xs text-gray-300 leading-relaxed">
                    {agent.self_model.self_narrative.current_story.slice(0, 120)}...
                  </p>
                </div>

                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-sm font-medium text-white mb-2">Agency Level</div>
                  <Progress 
                    value={agent.self_model.agency_model.autonomy_level * 100} 
                    className="h-2"
                  />
                  <div className="text-xs text-gray-400 mt-1">
                    {Math.round(agent.self_model.agency_model.autonomy_level * 100)}% autonomous
                  </div>
                </div>
              </motion.div>
            </TabsContent>

            <TabsContent value="stream" className="mt-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-2"
              >
                <div className="flex items-center gap-2 mb-3">
                  <Waves className="w-4 h-4 text-cyan-400" />
                  <span className="text-sm font-medium text-white">Consciousness Stream</span>
                </div>
                
                <ScrollArea className="h-48">
                  <AnimatePresence>
                    {recentEvents.map((event, index) => (
                      <motion.div
                        key={event.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        transition={{ delay: index * 0.1 }}
                        className="bg-slate-800 rounded-lg p-2 mb-2"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <Badge variant="outline" className="text-xs">
                            {event.event_type.replace(/_/g, ' ')}
                          </Badge>
                          <span className="text-xs text-gray-400">
                            {new Date(event.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-xs text-gray-300">
                          {event.description}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <Progress value={event.confidence * 100} className="flex-1 h-1" />
                          <span className="text-xs text-gray-400">
                            {Math.round(event.confidence * 100)}%
                          </span>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </ScrollArea>
              </motion.div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </motion.div>
  );
}
