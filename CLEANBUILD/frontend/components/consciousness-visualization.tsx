
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
  Zap, 
  Network, 
  Activity,
  Waves,
  Sparkles,
  Clock,
  Target,
  User
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Agent, ConsciousnessEvent, SwarmMessage } from '@/lib/types';

interface ConsciousnessVisualizationProps {
  agents: Agent[];
  consciousnessEvents: ConsciousnessEvent[];
  swarmMessages: SwarmMessage[];
  className?: string;
}

export function ConsciousnessVisualization({
  agents,
  consciousnessEvents,
  swarmMessages,
  className = ''
}: ConsciousnessVisualizationProps) {
  const [selectedAgent, setSelectedAgent] = useState<string>(agents[0]?.id || '');
  const [visualizationMode, setVisualizationMode] = useState<'network' | 'stream' | 'reality'>('network');
  const [recentEvents, setRecentEvents] = useState<ConsciousnessEvent[]>([]);

  useEffect(() => {
    const agentEvents = consciousnessEvents
      .filter(event => selectedAgent ? event.id.includes(selectedAgent) : true)
      .slice(-20)
      .reverse();
    setRecentEvents(agentEvents);
  }, [consciousnessEvents, selectedAgent]);

  const selectedAgentData = agents.find(agent => agent.id === selectedAgent);

  const getEventTypeColor = (eventType: string) => {
    const colors: Record<string, string> = {
      'prediction': 'bg-blue-500',
      'error_correction': 'bg-orange-500',
      'memory_access': 'bg-green-500',
      'self_reflection': 'bg-purple-500',
      'reality_generation': 'bg-cyan-500'
    };
    return colors[eventType] || 'bg-gray-500';
  };

  const getEventTypeIcon = (eventType: string) => {
    switch (eventType) {
      case 'prediction': return <Zap className="w-3 h-3" />;
      case 'error_correction': return <Target className="w-3 h-3" />;
      case 'memory_access': return <Brain className="w-3 h-3" />;
      case 'self_reflection': return <Eye className="w-3 h-3" />;
      case 'reality_generation': return <Sparkles className="w-3 h-3" />;
      default: return <Activity className="w-3 h-3" />;
    }
  };

  const renderNetworkVisualization = () => (
    <div className="relative h-96 bg-slate-900 rounded-lg overflow-hidden">
      <svg className="w-full h-full">
        {/* Background grid */}
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(148, 163, 184, 0.1)" strokeWidth="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        {/* Agent nodes */}
        {agents.map((agent, index) => {
          const angle = (index / agents.length) * 2 * Math.PI;
          const radius = 120;
          const centerX = 200;
          const centerY = 150;
          const x = centerX + radius * Math.cos(angle);
          const y = centerY + radius * Math.sin(angle);
          
          return (
            <g key={agent.id}>
              {/* Connections to other agents */}
              {agents.slice(index + 1).map((otherAgent, otherIndex) => {
                const otherAngle = ((index + 1 + otherIndex) / agents.length) * 2 * Math.PI;
                const otherX = centerX + radius * Math.cos(otherAngle);
                const otherY = centerY + radius * Math.sin(otherAngle);
                
                return (
                  <motion.line
                    key={`${agent.id}-${otherAgent.id}`}
                    x1={x}
                    y1={y}
                    x2={otherX}
                    y2={otherY}
                    stroke="rgba(59, 130, 246, 0.3)"
                    strokeWidth="1"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 2, delay: index * 0.2 }}
                  />
                );
              })}
              
              {/* Agent node */}
              <motion.circle
                cx={x}
                cy={y}
                r="20"
                fill={selectedAgent === agent.id ? "rgba(59, 130, 246, 0.8)" : "rgba(59, 130, 246, 0.4)"}
                stroke="rgba(59, 130, 246, 1)"
                strokeWidth="2"
                className="cursor-pointer"
                onClick={() => setSelectedAgent(agent.id)}
                whileHover={{ scale: 1.1 }}
                animate={{
                  r: [18, 22, 18],
                  opacity: [0.6, 1, 0.6]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              
              {/* Agent label */}
              <text
                x={x}
                y={y + 35}
                textAnchor="middle"
                className="text-xs fill-white font-medium"
              >
                {agent.name}
              </text>
              
              {/* Consciousness level indicator */}
              <motion.circle
                cx={x}
                cy={y}
                r="25"
                fill="none"
                stroke="rgba(34, 197, 94, 0.6)"
                strokeWidth="2"
                strokeDasharray={`${agent.consciousness_state.meta_awareness * 157} 157`}
                transform={`rotate(-90 ${x} ${y})`}
                initial={{ strokeDasharray: "0 157" }}
                animate={{ strokeDasharray: `${agent.consciousness_state.meta_awareness * 157} 157` }}
                transition={{ duration: 1, delay: index * 0.1 }}
              />
            </g>
          );
        })}
        
        {/* Central swarm consciousness indicator */}
        <motion.circle
          cx="200"
          cy="150"
          r="30"
          fill="rgba(168, 85, 247, 0.2)"
          stroke="rgba(168, 85, 247, 0.8)"
          strokeWidth="2"
          animate={{
            r: [28, 32, 28],
            opacity: [0.4, 0.8, 0.4]
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <text
          x="200"
          y="155"
          textAnchor="middle"
          className="text-xs fill-white font-medium"
        >
          Swarm
        </text>
      </svg>
    </div>
  );

  const renderStreamVisualization = () => (
    <ScrollArea className="h-96">
      <div className="space-y-2 p-2">
        <AnimatePresence>
          {recentEvents.map((event, index) => (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, x: -50, scale: 0.9 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 50, scale: 0.9 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="bg-slate-800 rounded-lg p-3 border-l-4 border-blue-400"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${getEventTypeColor(event.event_type)}`} />
                  {getEventTypeIcon(event.event_type)}
                  <Badge variant="outline" className="text-xs">
                    {event.event_type.replace(/_/g, ' ')}
                  </Badge>
                </div>
                <span className="text-xs text-gray-400">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </span>
              </div>
              
              <p className="text-sm text-gray-300 mb-2">
                {event.description}
              </p>
              
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-400">Confidence:</span>
                  <Progress value={event.confidence * 100} className="w-16 h-1" />
                  <span className="text-xs text-white">
                    {Math.round(event.confidence * 100)}%
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-400">Impact:</span>
                  <Progress value={event.impact_level * 100} className="w-16 h-1" />
                  <span className="text-xs text-white">
                    {Math.round(event.impact_level * 100)}%
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {recentEvents.length === 0 && (
          <div className="text-center text-gray-400 py-8">
            <Waves className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No consciousness events yet</p>
            <p className="text-xs">Events will appear as agents process</p>
          </div>
        )}
      </div>
    </ScrollArea>
  );

  const renderRealityVisualization = () => {
    if (!selectedAgentData) return null;

    const realityFrame = selectedAgentData.consciousness_state.current_reality_frame;
    
    return (
      <div className="space-y-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-slate-800 to-slate-700 rounded-lg p-4"
        >
          <div className="flex items-center gap-2 mb-3">
            <Eye className="w-5 h-5 text-cyan-400" />
            <span className="text-lg font-medium text-white">
              {selectedAgentData.name}'s Reality Frame
            </span>
          </div>
          
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-gray-300">Scene Description:</span>
              <p className="text-sm text-white mt-1 leading-relaxed">
                {realityFrame.scene_description}
              </p>
            </div>
            
            <div>
              <span className="text-sm font-medium text-gray-300">Narrative Context:</span>
              <p className="text-sm text-white mt-1 leading-relaxed">
                {realityFrame.narrative_context}
              </p>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-sm font-medium text-gray-300">Confidence:</span>
                <div className="flex items-center gap-2 mt-1">
                  <Progress value={realityFrame.confidence * 100} className="flex-1 h-2" />
                  <span className="text-sm text-white">
                    {Math.round(realityFrame.confidence * 100)}%
                  </span>
                </div>
              </div>
              
              <div>
                <span className="text-sm font-medium text-gray-300">Emotional State:</span>
                <div className="flex items-center gap-2 mt-1">
                  <Badge variant="outline" className="text-xs">
                    {realityFrame.emotional_coloring.primary_emotion}
                  </Badge>
                  <Progress value={realityFrame.emotional_coloring.intensity * 100} className="flex-1 h-2" />
                </div>
              </div>
            </div>
            
            <div>
              <span className="text-sm font-medium text-gray-300">Coherence Markers:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {realityFrame.coherence_markers.map((marker, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    {marker.replace(/_/g, ' ')}
                  </Badge>
                ))}
              </div>
            </div>
            
            <div>
              <span className="text-sm font-medium text-gray-300">Sensory Predictions:</span>
              <div className="grid grid-cols-2 gap-2 mt-1">
                {Object.entries(realityFrame.sensory_predictions).map(([key, value]) => (
                  <div key={key} className="bg-slate-800 rounded p-2">
                    <div className="text-xs text-gray-400">{key.replace(/_/g, ' ')}</div>
                    <div className="text-xs text-white">{String(value).replace(/_/g, ' ')}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`${className}`}
    >
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
        <CardHeader>
          <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" />
            Consciousness Visualization
          </CardTitle>
          
          <div className="flex items-center gap-2 mt-3">
            <select
              value={selectedAgent}
              onChange={(e) => setSelectedAgent(e.target.value)}
              className="bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm text-white"
            >
              <option value="">All Agents</option>
              {agents.map((agent) => (
                <option key={agent.id} value={agent.id}>
                  {agent.name}
                </option>
              ))}
            </select>
            
            <div className="flex gap-1 ml-auto">
              <Button
                variant={visualizationMode === 'network' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setVisualizationMode('network')}
                className="text-xs"
              >
                <Network className="w-3 h-3 mr-1" />
                Network
              </Button>
              <Button
                variant={visualizationMode === 'stream' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setVisualizationMode('stream')}
                className="text-xs"
              >
                <Waves className="w-3 h-3 mr-1" />
                Stream
              </Button>
              <Button
                variant={visualizationMode === 'reality' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setVisualizationMode('reality')}
                className="text-xs"
              >
                <Eye className="w-3 h-3 mr-1" />
                Reality
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <AnimatePresence mode="wait">
            <motion.div
              key={visualizationMode}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {visualizationMode === 'network' && renderNetworkVisualization()}
              {visualizationMode === 'stream' && renderStreamVisualization()}
              {visualizationMode === 'reality' && renderRealityVisualization()}
            </motion.div>
          </AnimatePresence>
        </CardContent>
      </Card>
    </motion.div>
  );
}
