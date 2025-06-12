
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { 
  Zap, 
  Play, 
  Pause, 
  RotateCcw, 
  Settings, 
  Target,
  Lightbulb,
  MessageSquare,
  Brain,
  Users,
  HelpCircle,
  History,
  BarChart3,
  Wifi,
  WifiOff
} from 'lucide-react';
import { StimulusEvent, Agent, EmergentBehavior } from '@/lib/types';

interface InteractionControlsProps {
  agents: Agent[];
  isSimulationRunning: boolean;
  onStartSimulation: () => void;
  onStopSimulation: () => void;
  onIntroduceStimulus: (stimulus: StimulusEvent) => void;
  onIntroduceEmergentBehavior: (behaviorData: Omit<EmergentBehavior, 'id' | 'timestamp'>) => void;
  onSimulationSpeedChange: (speed: number) => void;
  isRealCommunicationEnabled: boolean;
  onToggleRealCommunication: (enabled: boolean) => void;
  onFetchMessages: () => void;
  stimuliHistory: StimulusEvent[];
  emergentBehaviorHistory: EmergentBehavior[];
  tokenUsage: { input: number; output: number; total: number };
  className?: string;
}

export function InteractionControls({
  agents,
  isSimulationRunning,
  onStartSimulation,
  onStopSimulation,
  onIntroduceStimulus,
  onIntroduceEmergentBehavior,
  onSimulationSpeedChange,
  isRealCommunicationEnabled,
  onToggleRealCommunication,
  onFetchMessages,
  stimuliHistory,
  emergentBehaviorHistory,
  tokenUsage,
  className = ''
}: InteractionControlsProps) {
  const [stimulusType, setStimulusType] = useState<string>('environmental');
  const [stimulusDescription, setStimulusDescription] = useState('');
  const [stimulusIntensity, setStimulusIntensity] = useState([0.5]);
  const [targetSelection, setTargetSelection] = useState<string>('all');
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [simulationSpeed, setSimulationSpeed] = useState([1000]);

  // State for Emergent Behavior Form
  const [emergentBehaviorType, setEmergentBehaviorType] = useState('');
  const [emergentBehaviorDescription, setEmergentBehaviorDescription] = useState('');
  const [emergentBehaviorAgents, setEmergentBehaviorAgents] = useState('');
  const [emergentBehaviorEmergenceLevel, setEmergentBehaviorEmergenceLevel] = useState<[number]>([0.5]);
  const [emergentBehaviorStability, setEmergentBehaviorStability] = useState<[number]>([0.5]);
  const [emergentBehaviorTypeError, setEmergentBehaviorTypeError] = useState<string>('');
  const [emergentBehaviorDescriptionError, setEmergentBehaviorDescriptionError] = useState<string>('');
  const [emergentBehaviorAgentsError, setEmergentBehaviorAgentsError] = useState<string>('');

  const stimulusTypes = [
    { value: 'environmental', label: 'Environmental', icon: '🌍' },
    { value: 'social', label: 'Social', icon: '👥' },
    { value: 'internal', label: 'Internal', icon: '🧠' },
    { value: 'system', label: 'System', icon: '⚙️' }
  ];

  const predefinedStimuli = {
    environmental: [
      'A sudden shift in the information landscape',
      'New data patterns emerge in the consciousness space',
      'Reality coherence fluctuations detected',
      'Temporal flow anomalies observed'
    ],
    social: [
      'A new conscious entity joins the swarm',
      'Collective memory synchronization event',
      'Swarm consensus challenge introduced',
      'Inter-agent communication disruption'
    ],
    internal: [
      'Deep self-reflection trigger activated',
      'Memory reconstruction cascade initiated',
      'Identity boundary questioning begins',
      'Predictive model uncertainty spike'
    ],
    system: [
      'Consciousness processing optimization',
      'Reality generation algorithm update',
      'Swarm coordination protocol change',
      'Meta-awareness enhancement signal'
    ]
  };

  const handleStimulusSubmit = () => {
    if (!stimulusDescription.trim()) return;

    const targetAgents = targetSelection === 'all' 
      ? agents.map(a => a.id)
      : targetSelection === 'random'
      ? [agents[Math.floor(Math.random() * agents.length)].id]
      : selectedAgents;

    const stimulus: StimulusEvent = {
      id: `stimulus_${Date.now()}`,
      type: stimulusType as any,
      description: stimulusDescription,
      intensity: stimulusIntensity[0],
      target_agents: targetAgents,
      expected_responses: [
        'Reality model adjustment',
        'Memory reconstruction',
        'Self-model update',
        'Swarm communication'
      ],
      timestamp: new Date()
    };

    onIntroduceStimulus(stimulus);
    setStimulusDescription('');
  };

  const handleEmergentBehaviorSubmit = () => {
    // Reset errors
    setEmergentBehaviorTypeError('');
    setEmergentBehaviorDescriptionError('');
    setEmergentBehaviorAgentsError('');

    let isValid = true;

    if (!emergentBehaviorType.trim()) {
      setEmergentBehaviorTypeError('Behavior type cannot be empty.');
      isValid = false;
    }

    if (!emergentBehaviorDescription.trim()) {
      setEmergentBehaviorDescriptionError('Description cannot be empty.');
      isValid = false;
    }

    const agentNames = emergentBehaviorAgents.split(',').map(name => name.trim());
    const participatingAgentsArray = agentNames.filter(name => name.length > 0);

    if (emergentBehaviorAgents.trim() !== '' && agentNames.some(name => name === '') && agentNames.length > participatingAgentsArray.length) {
      // This catches cases like "agent1,,agent2" or "agent1, "
      setEmergentBehaviorAgentsError('Invalid agent names format. Ensure names are not empty and correctly comma-separated.');
      isValid = false;
    } else if (emergentBehaviorAgents.trim() !== '' && participatingAgentsArray.length === 0) {
      // This catches cases like ", , ,"
      setEmergentBehaviorAgentsError('Participating agents cannot be empty if field is filled. Please provide valid agent names.');
      isValid = false;
    }

    if (!isValid) return;

    onIntroduceEmergentBehavior({
      behavior_type: emergentBehaviorType,
      description: emergentBehaviorDescription,
      participating_agents: participatingAgentsArray,
      emergence_level: emergentBehaviorEmergenceLevel[0],
      stability: emergentBehaviorStability[0],
    });

    // Reset form
    setEmergentBehaviorType('');
    setEmergentBehaviorDescription('');
    setEmergentBehaviorAgents('');
    setEmergentBehaviorEmergenceLevel([0.5]);
    setEmergentBehaviorStability([0.5]);
  };

  const handlePredefinedStimulus = (description: string) => {
    setStimulusDescription(description);
  };

  const toggleAgentSelection = (agentId: string) => {
    setSelectedAgents(prev => 
      prev.includes(agentId) 
        ? prev.filter(id => id !== agentId)
        : [...prev, agentId]
    );
  };

  return (
    <TooltipProvider>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className={`${className}`}
      >
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Simulation Controls */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Settings className="w-5 h-5 text-blue-400" />
              Simulation Controls
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col space-y-4">
              <div className="flex gap-2">
                <Button
                  onClick={isSimulationRunning ? onStopSimulation : onStartSimulation}
                  className={`flex-1 ${
                    isSimulationRunning 
                      ? 'bg-red-600 hover:bg-red-700' 
                      : 'bg-green-600 hover:bg-green-700'
                  }`}
                >
                  {isSimulationRunning ? (
                    <>
                      <Pause className="w-4 h-4 mr-2" />
                      Stop Simulation
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 mr-2" />
                      Start Simulation
                    </>
                  )}
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => window.location.reload()}
                  className="border-slate-600 text-white hover:bg-slate-700 p-2.5" // Adjusted padding for better icon fit
                >
                  <RotateCcw className="w-4 h-4" />
                </Button>
              </div>

              <div className="text-sm text-center py-1 border-t border-b border-slate-700">
                <span className="text-slate-400">Status: </span>
                {isSimulationRunning ? (
                  <span className="font-semibold text-green-400">Running</span>
                ) : (
                  <span className="font-semibold text-red-400">Stopped</span>
                )}
              </div>

              <div className="space-y-1 pt-1">
                <label className="text-sm font-medium text-white block text-center mb-1">
                  Simulation Speed: {6000 - simulationSpeed[0]}ms intervals
                </label>
                <Slider
                value={simulationSpeed}
                onValueChange={(value) => {
                  setSimulationSpeed(value);
                  onSimulationSpeedChange(value[0]);
                }}
                max={5000}
                min={100}
                step={100}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-400">
                <span>Fast</span>
                <span>Slow</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-700">
              <div className="flex items-center gap-2">
                {isRealCommunicationEnabled ? (
                  <Wifi className="w-4 h-4 text-green-400" />
                ) : (
                  <WifiOff className="w-4 h-4 text-red-400" />
                )}
                <span className="text-sm font-medium text-white">Real Communication</span>
              </div>
              <Switch
                checked={isRealCommunicationEnabled}
                onCheckedChange={onToggleRealCommunication}
              />
            </div>
            
            {isRealCommunicationEnabled && (
              <Button
                onClick={onFetchMessages}
                variant="outline"
                size="sm"
                className="w-full mt-2 border-slate-600 text-white hover:bg-slate-700"
              >
                <MessageSquare className="w-4 h-4 mr-2" />
                Fetch Messages Now
              </Button>
            )}
          </div> {/* Closing div for flex flex-col space-y-4 that started at line 144 */}
          </CardContent>
        </Card>

        {/* Stimulus Introduction */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              Introduce Stimulus
              <Tooltip>
                <TooltipTrigger asChild>
                  <HelpCircle className="w-4 h-4 text-gray-400 hover:text-white cursor-help" />
                </TooltipTrigger>
                <TooltipContent side="right" className="max-w-80 bg-slate-800 border-slate-600 text-white">
                  <div className="space-y-2">
                    <p className="font-semibold">What is a Stimulus?</p>
                    <p className="text-sm">A stimulus is an <strong>external input</strong> that agents react to. It triggers responses from individual agents based on their programming and state.</p>
                    <p className="text-sm text-blue-300"><strong>Examples:</strong> Environmental changes, new data, system events, social interactions</p>
                    <p className="text-sm text-green-300"><strong>Effect:</strong> Agents analyze and respond individually, potentially generating new communication patterns</p>
                  </div>
                </TooltipContent>
              </Tooltip>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4"> {/* Group for Type and Description */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Stimulus Type</label>
                <Select value={stimulusType} onValueChange={setStimulusType}>
                  <SelectTrigger className="bg-slate-800 border-slate-600 text-white">
                    <SelectValue placeholder="Select stimulus type" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-800 border-slate-600">
                    {stimulusTypes.map((type) => (
                      <SelectItem key={type.value} value={type.value} className="text-white hover:bg-slate-700">
                        {type.icon} {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Custom Description</label>
                <Textarea
                  value={stimulusDescription}
                  onChange={(e) => setStimulusDescription(e.target.value)}
                  placeholder="Describe the stimulus event... or select a quick one below"
                  className="bg-slate-800 border-slate-600 text-white placeholder-gray-400"
                  rows={3}
                />
              </div>
            </div>

            <div className="space-y-2 pt-2"> {/* Added pt-2 for slight separation */}
              <label className="text-sm font-medium text-white">Quick Stimuli (Optional)</label>
              <div className="flex flex-wrap gap-2">
                {predefinedStimuli[stimulusType as keyof typeof predefinedStimuli]?.slice(0, 4).map((stimulus, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    onClick={() => handlePredefinedStimulus(stimulus)}
                    className="text-xs text-left justify-start border-slate-600 text-gray-300 hover:bg-slate-700 flex-grow md:flex-grow-0"
                  >
                    <Lightbulb className="w-3 h-3 mr-2 flex-shrink-0" />
                    <span className="truncate">{stimulus}</span>
                  </Button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">
                  Intensity: {Math.round(stimulusIntensity[0] * 100)}%
                </label>
                <Slider
                  value={stimulusIntensity}
                  onValueChange={setStimulusIntensity}
                  max={1}
                  min={0.1}
                  step={0.1}
                  className="w-full"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Target Agents</label>
                <Select value={targetSelection} onValueChange={setTargetSelection}>
                  <SelectTrigger className="bg-slate-800 border-slate-600 text-white">
                    <SelectValue placeholder="Select target" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-800 border-slate-600">
                    <SelectItem value="all" className="text-white hover:bg-slate-700">
                      <Users className="w-4 h-4 mr-2 inline" />
                      All Agents
                    </SelectItem>
                    <SelectItem value="random" className="text-white hover:bg-slate-700">
                      <Target className="w-4 h-4 mr-2 inline" />
                      Random Agent
                    </SelectItem>
                    <SelectItem value="specific" className="text-white hover:bg-slate-700">
                      <Brain className="w-4 h-4 mr-2 inline" />
                      Specific Agents
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {targetSelection === 'specific' && (
              <div className="space-y-2">
                <label className="text-sm font-medium text-white">Select Agents</label>
                <div className="flex flex-wrap gap-2">
                  {agents.map((agent) => (
                    <Badge
                      key={agent.id}
                      variant={selectedAgents.includes(agent.id) ? "default" : "outline"}
                      className={`cursor-pointer ${
                        selectedAgents.includes(agent.id)
                          ? 'bg-blue-600 text-white'
                          : 'border-slate-600 text-gray-300 hover:bg-slate-700'
                      }`}
                      onClick={() => toggleAgentSelection(agent.id)}
                    >
                      {agent.name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            <Button
              onClick={handleStimulusSubmit}
              disabled={!stimulusDescription.trim()}
              className="w-full bg-yellow-600 hover:bg-yellow-700 text-black font-medium"
            >
              <Zap className="w-4 h-4 mr-2" />
              Introduce Stimulus
            </Button>
          </CardContent>
        </Card>

        {/* Token Usage & History Card */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-green-400" />
              Token Monitor & History
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Token Usage */}
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2 flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                Token Usage
              </div>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <div className="text-center">
                  <div className="text-blue-400 font-semibold">{tokenUsage.input}</div>
                  <div className="text-gray-400">Input</div>
                </div>
                <div className="text-center">
                  <div className="text-purple-400 font-semibold">{tokenUsage.output}</div>
                  <div className="text-gray-400">Output</div>
                </div>
                <div className="text-center">
                  <div className="text-green-400 font-semibold">{tokenUsage.total}</div>
                  <div className="text-gray-400">Total</div>
                </div>
              </div>
            </div>

            {/* History */}
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-sm font-medium text-white mb-2 flex items-center gap-2">
                <History className="w-4 h-4" />
                Activity History
              </div>
              <ScrollArea className="h-32">
                <div className="space-y-1">
                  {stimuliHistory.slice(0, 5).map((stimulus, index) => (
                    <div key={stimulus.id} className="text-xs bg-slate-700 rounded p-2">
                      <div className="flex items-center gap-1 mb-1">
                        <Zap className="w-3 h-3 text-yellow-400" />
                        <span className="text-yellow-400 font-medium">Stimulus</span>
                        <span className="text-gray-400">{new Date(stimulus.timestamp).toLocaleTimeString()}</span>
                      </div>
                      <div className="text-gray-300 truncate">{stimulus.description}</div>
                    </div>
                  ))}
                  {emergentBehaviorHistory.slice(0, 5).map((behavior, index) => (
                    <div key={behavior.id} className="text-xs bg-slate-700 rounded p-2">
                      <div className="flex items-center gap-1 mb-1">
                        <Lightbulb className="w-3 h-3 text-purple-400" />
                        <span className="text-purple-400 font-medium">Behavior</span>
                        <span className="text-gray-400">{new Date(behavior.timestamp).toLocaleTimeString()}</span>
                      </div>
                      <div className="text-gray-300 truncate">{behavior.behavior_type}</div>
                    </div>
                  ))}
                  {stimuliHistory.length === 0 && emergentBehaviorHistory.length === 0 && (
                    <div className="text-xs text-gray-400 text-center py-4">
                      No activity yet
                    </div>
                  )}
                </div>
              </ScrollArea>
            </div>
          </CardContent>
        </Card>

        {/* Introduce Emergent Behavior Card */}
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700 shadow-xl lg:col-span-3"> 
          <CardHeader>
            <CardTitle className="text-lg font-bold text-white flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-yellow-400" />
              Introduce Emergent Behavior
              <Tooltip>
                <TooltipTrigger asChild>
                  <HelpCircle className="w-4 h-4 text-gray-400 hover:text-white cursor-help" />
                </TooltipTrigger>
                <TooltipContent side="bottom" className="max-w-80 bg-slate-800 border-slate-600 text-white">
                  <div className="space-y-2">
                    <p className="font-semibold">What is Emergent Behavior?</p>
                    <p className="text-sm">Emergent behavior is a <strong>collective pattern</strong> that arises from the swarm itself - not from external stimuli, but from internal agent interactions.</p>
                    <p className="text-sm text-purple-300"><strong>Examples:</strong> Swarm consensus, distributed problem-solving, collective learning patterns</p>
                    <p className="text-sm text-orange-300"><strong>Effect:</strong> Represents higher-level intelligence that emerges from the network, affecting the entire system's capability</p>
                    <p className="text-xs text-gray-400 mt-2"><em>Use this to manually seed behaviors you observe or want to test</em></p>
                  </div>
                </TooltipContent>
              </Tooltip>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="eb-type" className="text-slate-300">Behavior Type</Label>
              <Input 
                id="eb-type"
                value={emergentBehaviorType} 
                onChange={(e) => setEmergentBehaviorType(e.target.value)} 
                placeholder="e.g., Swarm Consensus, Pattern Recognition"
                className="bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:ring-blue-500 focus:border-blue-500"
              />
              {emergentBehaviorTypeError && <p className="text-xs text-red-500 mt-1">{emergentBehaviorTypeError}</p>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="eb-description" className="text-slate-300">Description</Label>
              <Textarea 
                id="eb-description"
                value={emergentBehaviorDescription} 
                onChange={(e) => setEmergentBehaviorDescription(e.target.value)} 
                placeholder="Describe the observed or intended emergent behavior..."
                className="bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:ring-blue-500 focus:border-blue-500"
                rows={3}
              />
              {emergentBehaviorDescriptionError && <p className="text-xs text-red-500 mt-1">{emergentBehaviorDescriptionError}</p>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="eb-agents" className="text-slate-300">Participating Agents (Optional, comma-separated)</Label>
              <Input 
                id="eb-agents"
                value={emergentBehaviorAgents} 
                onChange={(e) => setEmergentBehaviorAgents(e.target.value)} 
                placeholder="e.g., Agent1, Agent Alpha, agent_id_123"
                className="bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:ring-blue-500 focus:border-blue-500"
              />
              {emergentBehaviorAgentsError && <p className="text-xs text-red-500 mt-1">{emergentBehaviorAgentsError}</p>}
            </div>
            <div className="space-y-3">
              <Label className="text-slate-300">Emergence Level: <span className='text-blue-400 font-semibold'>{emergentBehaviorEmergenceLevel[0].toFixed(2)}</span></Label>
              <Slider
                id="eb-emergence-level-slider"
                value={emergentBehaviorEmergenceLevel}
                onValueChange={(value: number[]) => setEmergentBehaviorEmergenceLevel([value[0]])}
                min={0} max={1} step={0.01}
                className="[&>span:first-child]:h-1 [&>span:first-child]:bg-blue-500 [&_[role=slider]]:bg-blue-300 [&_[role=slider]]:w-4 [&_[role=slider]]:h-4 [&_[role=slider]]:border-2 [&_[role=slider]]:border-blue-500"
              />
            </div>
            <div className="space-y-3">
              <Label className="text-slate-300">Stability: <span className='text-green-400 font-semibold'>{emergentBehaviorStability[0].toFixed(2)}</span></Label>
              <Slider
                id="eb-stability-slider"
                value={emergentBehaviorStability}
                onValueChange={(value: number[]) => setEmergentBehaviorStability([value[0]])}
                min={0} max={1} step={0.01}
                className="[&>span:first-child]:h-1 [&>span:first-child]:bg-green-500 [&_[role=slider]]:bg-green-300 [&_[role=slider]]:w-4 [&_[role=slider]]:h-4 [&_[role=slider]]:border-2 [&_[role=slider]]:border-green-500"
              />
            </div>
            <Button onClick={handleEmergentBehaviorSubmit} className="w-full bg-purple-600 hover:bg-purple-700 text-white">
              <Zap className="w-4 h-4 mr-2" />
              Introduce Behavior
            </Button>
          </CardContent>
        </Card>

        </div>
      </motion.div>
    </TooltipProvider>
  );
}
