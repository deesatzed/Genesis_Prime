
'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { useToast } from '@/hooks/use-toast';
import {
  Settings,
  Key,
  Brain,
  CheckCircle,
  XCircle,
  Loader2,
  Info,
  Wifi,
  WifiOff,
  Save,
  TestTube,
  Search,
  RefreshCw,
  Filter,
  Star,
  X,
  SlidersHorizontal, // For new section icon
  InfoIcon,
  Download, // For Download Config button
  Upload // For Upload Config button
} from 'lucide-react';
import { ConfigurationState, ModelOption, AgentDefaultSettings, AgentArchetype } from '@/lib/types'; // Added AgentArchetype
import { ConfigurationService } from '@/lib/config-service';
import { Slider } from '@/components/ui/slider'; // Import Slider

interface SettingsPanelProps {
  configuration: ConfigurationState;
  onConfigurationChange: (config: ConfigurationState) => void;
  onConfigurationSave: (config: ConfigurationState) => void;
}

export function SettingsPanel({ 
  configuration, 
  onConfigurationChange, 
  onConfigurationSave 
}: SettingsPanelProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [localConfig, setLocalConfig] = useState<ConfigurationState>(configuration);
  const [isTestingConnection, setIsTestingConnection] = useState(false);
  const [connectionTestResult, setConnectionTestResult] = useState<{
    success: boolean;
    message: string;
  } | null>(null);
  
  // Model loading state
  const [availableModels, setAvailableModels] = useState<ModelOption[]>([]);
  const [isLoadingModels, setIsLoadingModels] = useState(false);
  const [modelsFromCache, setModelsFromCache] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [showOnlyPopular, setShowOnlyPopular] = useState(false);
  
  const { toast } = useToast();
  const [selectingModelForAgent, setSelectingModelForAgent] = useState<string | null>(null);
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleDownloadConfiguration = () => {
    try {
      const jsonString = JSON.stringify(localConfig, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const href = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = href;
      link.download = 'agno-swarm-config.json';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(href);
      toast({
        title: 'Configuration Downloaded',
        description: 'agno-swarm-config.json has been downloaded.',
      });
    } catch (error) {
      console.error('Failed to download configuration:', error);
      toast({
        title: 'Download Failed',
        description: 'Could not prepare the configuration for download.',
        variant: 'destructive',
      });
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result;
        if (typeof text !== 'string') {
          throw new Error('File content is not a string.');
        }
        const uploadedConfig = JSON.parse(text) as ConfigurationState;

        // Basic validation
        if (!uploadedConfig.openRouter || !uploadedConfig.agents) {
          throw new Error('Invalid configuration file structure.');
        }
        
        // Further validation can be added here (e.g., using a Zod schema)

        setLocalConfig(uploadedConfig);
        // Reset connection test result as API key might have changed
        setConnectionTestResult(null);
        toast({
          title: 'Configuration Uploaded',
          description: 'Settings have been loaded. Review and save if needed.',
        });
      } catch (error) {
        console.error('Failed to upload configuration:', error);
        toast({
          title: 'Upload Failed',
          description: error instanceof Error ? error.message : 'Could not parse or apply the configuration file.',
          variant: 'destructive',
        });
      }
    };
    reader.onerror = () => {
      toast({
        title: 'File Read Error',
        description: 'Could not read the selected file.',
        variant: 'destructive',
      });
    };
    reader.readAsText(file);
    
    // Reset file input value to allow uploading the same file again if needed
    if (event.target) {
      event.target.value = '';
    }
  };

  useEffect(() => {
    setLocalConfig(configuration);
  }, [configuration]);

  // Load models when dialog opens
  useEffect(() => {
    if (isOpen) {
      loadModels();
    }
  }, [isOpen]);

  const loadModels = async () => {
    setIsLoadingModels(true);
    try {
      const { models, fromCache } = await ConfigurationService.fetchModels();
      setAvailableModels(models);
      setModelsFromCache(fromCache);
      
      if (fromCache) {
        toast({
          title: "Models Loaded",
          description: "Using cached model list",
        });
      } else {
        toast({
          title: "Models Updated",
          description: `Loaded ${models.length} models from OpenRouter`,
        });
      }
    } catch (error) {
      toast({
        title: "Failed to Load Models",
        description: "Using fallback model list",
        variant: "destructive",
      });
    } finally {
      setIsLoadingModels(false);
    }
  };

  const refreshModels = async () => {
    toast({
      title: "Refreshing Models List",
      description: "Attempting to fetch the latest models from OpenRouter...",
    });
    ConfigurationService.clearModelsCache();
    await loadModels();
  };

  const handleApiKeyChange = (apiKey: string) => {
    const updatedConfig = ConfigurationService.updateApiKey(localConfig, apiKey);
    setLocalConfig(updatedConfig);
    setConnectionTestResult(null);
  };

  const handleModelChange = (agentName: string, modelId: string) => {
    console.log('[SettingsPanel] handleModelChange called for agent:', agentName, 'with new modelId:', modelId);
    console.log('[SettingsPanel] localConfig.openRouter.agentModels BEFORE update:', JSON.parse(JSON.stringify(localConfig.openRouter.agentModels)));
    const updatedConfig = ConfigurationService.updateAgentModel(localConfig, agentName, modelId);
    console.log('[SettingsPanel] updatedConfig.openRouter.agentModels AFTER update (before setLocalConfig):', JSON.parse(JSON.stringify(updatedConfig.openRouter.agentModels)));
    setLocalConfig(prevConfig => {
      console.log('[SettingsPanel] setLocalConfig updater - prevConfig.openRouter.agentModels:', JSON.parse(JSON.stringify(prevConfig.openRouter.agentModels)));
      console.log('[SettingsPanel] setLocalConfig updater - applying updatedConfig.openRouter.agentModels:', JSON.parse(JSON.stringify(updatedConfig.openRouter.agentModels)));
      return updatedConfig;
    });
    // To see the truly updated localConfig after React's state update, a useEffect is better.
    // We'll add one if these logs show the update is happening correctly up to setLocalConfig.
  };

  const handleTestConnection = async () => {
    if (!ConfigurationService.validateApiKey(localConfig.openRouter.apiKey)) {
      toast({
        title: "Invalid API Key",
        description: "Please enter a valid OpenRouter API key (starts with 'sk-')",
        variant: "destructive",
      });
      return;
    }

    setIsTestingConnection(true);
    setConnectionTestResult(null);

    try {
      const result = await ConfigurationService.testConnection(localConfig.openRouter.apiKey);
      setConnectionTestResult(result);
      
      if (result.success) {
        toast({
          title: "Connection Successful",
          description: "OpenRouter API connection is working correctly",
        });
      } else {
        toast({
          title: "Connection Failed",
          description: result.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      setConnectionTestResult({
        success: false,
        message: 'Failed to test connection'
      });
      toast({
        title: "Test Failed",
        description: "Unable to test the connection",
        variant: "destructive",
      });
    } finally {
      setIsTestingConnection(false);
    }
  };

  const handleSaveConfiguration = () => {
    if (!ConfigurationService.validateApiKey(localConfig.openRouter.apiKey)) {
      toast({
        title: "Invalid Configuration",
        description: "Please enter a valid API key before saving",
        variant: "destructive",
      });
      return;
    }

    const configToSave = connectionTestResult?.success 
        ? ConfigurationService.markAsConfigured(localConfig) 
        : localConfig;

      onConfigurationSave(configToSave);
    setIsOpen(false);
    
    toast({
      title: "Configuration Saved",
      description: "Your OpenRouter settings have been saved successfully",
    });
  };

  const handleApplyChanges = () => {
    onConfigurationChange(localConfig);
    toast({
      title: "Changes Applied",
      description: "Configuration updated without saving to storage",
    });
  };

  const getFilteredModels = (): ModelOption[] => {
    let filtered = [...availableModels];

    // Apply search filter
    if (searchQuery.trim()) {
      filtered = ConfigurationService.searchModels(filtered, searchQuery);
    }

    // Apply category filter
    if (selectedCategories.length > 0) {
      filtered = ConfigurationService.filterModelsByCategory(filtered, selectedCategories);
    }

    // Apply popular filter
    if (showOnlyPopular) {
      filtered = ConfigurationService.getPopularModels(filtered);
    }

    return filtered;
  };

  const getModelsByCategory = (): Record<string, ModelOption[]> => {
    const filtered = getFilteredModels();
    return filtered.reduce((acc, model) => {
      if (!acc[model.category]) {
        acc[model.category] = [];
      }
      acc[model.category].push(model);
      return acc;
    }, {} as Record<string, ModelOption[]>);
  };

  const getModelInfo = (modelId: string): ModelOption | undefined => {
    return availableModels.find(model => model.id === modelId);
  };

  const getAllCategories = (): string[] => {
    const categories = new Set(availableModels.map(model => model.category));
    return Array.from(categories).sort();
  };

  const toggleCategory = (category: string) => {
    setSelectedCategories(prev => 
      prev.includes(category) 
        ? prev.filter(c => c !== category)
        : [...prev, category]
    );
  };

  const agentNames = ['Aria', 'Zephyr', 'Nova', 'Echo', 'Sage'];
  const agentDescriptions = {
    'Aria': 'Creative and artistic consciousness',
    'Zephyr': 'Analytical and philosophical mind',
    'Nova': 'Innovative and experimental thinker',
    'Echo': 'Empathetic and reflective nature',
    'Sage': 'Wise and balanced perspective'
  };

  return (
    <TooltipProvider>
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <Settings className="w-4 h-4" />
            Settings
            {!configuration.isConfigured && (
              <Badge variant="destructive" className="ml-1 px-1 py-0 text-xs">
                Setup Required
              </Badge>
            )}
          </Button>
        </DialogTrigger>
        
        <DialogContent className="max-w-4xl h-[90vh] flex flex-col">
          <DialogHeader className="flex-shrink-0">
            <div className="flex items-center justify-between">
              <DialogTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Agno Swarm Configuration
              </DialogTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsOpen(false)}
                className="h-6 w-6 p-0 hover:bg-gray-100"
              >
                <X className="h-4 w-4" />
                <span className="sr-only">Close</span>
              </Button>
            </div>
            <DialogDescription>
              Configure your OpenRouter API key and select LLM models for each agent
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-6 flex-grow overflow-y-auto p-6">
            {/* API Key Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Key className="w-5 h-5" />
                  OpenRouter API Key
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="api-key">API Key</Label>
                  <div className="flex gap-2">
                    <Input
                      id="api-key"
                      type="password"
                      placeholder="sk-or-v1-..."
                      value={localConfig.openRouter.apiKey}
                      onChange={(e) => handleApiKeyChange(e.target.value)}
                      className="flex-1"
                    />
                    <Button
                      onClick={handleTestConnection}
                      disabled={isTestingConnection || !localConfig.openRouter.apiKey}
                      variant="outline"
                      className="gap-2"
                    >
                      {isTestingConnection ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <TestTube className="w-4 h-4" />
                      )}
                      Test
                    </Button>
                  </div>
                  
                  <AnimatePresence>
                    {connectionTestResult && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className={`flex items-center gap-2 text-sm p-2 rounded ${
                          connectionTestResult.success 
                            ? 'bg-green-50 text-green-700 border border-green-200' 
                            : 'bg-red-50 text-red-700 border border-red-200'
                        }`}
                      >
                        {connectionTestResult.success ? (
                          <CheckCircle className="w-4 h-4" />
                        ) : (
                          <XCircle className="w-4 h-4" />
                        )}
                        {connectionTestResult.message}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                <div className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <Info className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
                  <div className="text-sm text-blue-700">
                    <p className="font-medium mb-1">Get your OpenRouter API key:</p>
                    <p>Visit <a href="https://openrouter.ai/keys" target="_blank" rel="noopener noreferrer" className="underline">openrouter.ai/keys</a> to create an account and generate your API key.</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Agent Model Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-lg">
                  <div className="flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    Agent Model Assignment
                  </div>
                  <div className="flex items-center gap-2">
                    {modelsFromCache && (
                      <Badge variant="outline" className="text-xs">
                        Cached
                      </Badge>
                    )}
                    <Button
                      onClick={refreshModels}
                      disabled={isLoadingModels}
                      variant="outline"
                      size="sm"
                      className="gap-1"
                    >
                      {isLoadingModels ? (
                        <Loader2 className="w-3 h-3 animate-spin" />
                      ) : (
                        <RefreshCw className="w-3 h-3" />
                      )}
                      Refresh
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">

                    {/* Agent Default Parameters Section */}
                    <Card className="border-gray-200 shadow-sm">
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-md">
                          <SlidersHorizontal className="w-4 h-4" />
                          Agent Default Parameters
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-6 pt-2">
                        {(['min_learning_rate', 'max_learning_rate', 'min_reflection_trigger_threshold', 'max_reflection_trigger_threshold'] as const).map((key) => {
                          const agentDefaults = localConfig.openRouter.agentDefaults || ConfigurationService.getDefaultConfiguration().openRouter.agentDefaults!;
                          const currentVal = agentDefaults[key];

                          let label = '';
                          let tooltipText = '';
                          if (key === 'min_learning_rate') { label = 'Min Learning Rate'; tooltipText = 'Minimum initial learning rate for agents (0.01-1.0). Affects how much an agent updates its beliefs from shared insights.'; }
                          if (key === 'max_learning_rate') { label = 'Max Learning Rate'; tooltipText = 'Maximum initial learning rate for agents (0.01-1.0).'; }
                          if (key === 'min_reflection_trigger_threshold') { label = 'Min Reflection Threshold'; tooltipText = 'Minimum error level (0.01-1.0) to trigger an agent\'s reflection cycle.'; }
                          if (key === 'max_reflection_trigger_threshold') { label = 'Max Reflection Threshold'; tooltipText = 'Maximum error level (0.01-1.0) to trigger an agent\'s reflection cycle.'; }

                          return (
                            <div key={key} className="space-y-2">
                              <div className="flex items-center justify-between">
                                <Label htmlFor={key} className="text-sm font-medium">
                                  {label}
                                </Label>
                                <Tooltip>
                                  <TooltipTrigger asChild>
                                    <InfoIcon className="w-3.5 h-3.5 text-gray-400 cursor-help" />
                                  </TooltipTrigger>
                                  <TooltipContent side="top" className="max-w-xs">
                                    <p>{tooltipText}</p>
                                  </TooltipContent>
                                </Tooltip>
                              </div>
                              <div className="flex items-center gap-3">
                                <Slider
                                  id={key}
                                  min={0.01}
                                  max={1.0}
                                  step={0.01}
                                  value={[currentVal]}
                                  onValueChange={([newValue]) => {
                                    const newAgentDefaults = {
                                      ...(localConfig.openRouter.agentDefaults || ConfigurationService.getDefaultConfiguration().openRouter.agentDefaults!),
                                      [key]: newValue,
                                    };
                                    // Ensure min <= max for rates and thresholds
                                    if (key === 'min_learning_rate' && newValue > newAgentDefaults.max_learning_rate) {
                                      newAgentDefaults.max_learning_rate = newValue;
                                    }
                                    if (key === 'max_learning_rate' && newValue < newAgentDefaults.min_learning_rate) {
                                      newAgentDefaults.min_learning_rate = newValue;
                                    }
                                    if (key === 'min_reflection_trigger_threshold' && newValue > newAgentDefaults.max_reflection_trigger_threshold) {
                                      newAgentDefaults.max_reflection_trigger_threshold = newValue;
                                    }
                                    if (key === 'max_reflection_trigger_threshold' && newValue < newAgentDefaults.min_reflection_trigger_threshold) {
                                      newAgentDefaults.min_reflection_trigger_threshold = newValue;
                                    }

                                    setLocalConfig(prevConfig => ({
                                      ...prevConfig,
                                      openRouter: {
                                        ...prevConfig.openRouter,
                                        agentDefaults: newAgentDefaults,
                                      },
                                    }));
                                  }}
                                  className="flex-1"
                                />
                                <Input
                                  type="number"
                                  value={currentVal.toFixed(2)}
                                  onChange={(e) => {
                                    let numValue = parseFloat(e.target.value);
                                    if (isNaN(numValue)) numValue = 0.01;
                                    if (numValue < 0.01) numValue = 0.01;
                                    if (numValue > 1.0) numValue = 1.0;
                                     const newAgentDefaults = {
                                      ...(localConfig.openRouter.agentDefaults || ConfigurationService.getDefaultConfiguration().openRouter.agentDefaults!),
                                      [key]: numValue,
                                    };
                                     // Ensure min <= max
                                    if (key === 'min_learning_rate' && numValue > newAgentDefaults.max_learning_rate) newAgentDefaults.max_learning_rate = numValue;
                                    if (key === 'max_learning_rate' && numValue < newAgentDefaults.min_learning_rate) newAgentDefaults.min_learning_rate = numValue;
                                    if (key === 'min_reflection_trigger_threshold' && numValue > newAgentDefaults.max_reflection_trigger_threshold) newAgentDefaults.max_reflection_trigger_threshold = numValue;
                                    if (key === 'max_reflection_trigger_threshold' && numValue < newAgentDefaults.min_reflection_trigger_threshold) newAgentDefaults.min_reflection_trigger_threshold = numValue;

                                    setLocalConfig(prevConfig => ({
                                      ...prevConfig,
                                      openRouter: {
                                        ...prevConfig.openRouter,
                                        agentDefaults: newAgentDefaults,
                                      },
                                    }));
                                  }}
                                  className="w-20 text-sm"
                                  min={0.01} max={1.0} step={0.01}
                                />
                              </div>
                            </div>
                          );
                        })}
                      </CardContent>
                    </Card>

                {/* Conditional Rendering: Agent List OR Model Browser */}
                {selectingModelForAgent === null ? (
                  // AGENT LIST VIEW
                  <div className="space-y-4 mt-4">
                    <h3 className="text-md font-medium text-gray-800">Current Agent Assignments:</h3>
                    {agentNames.map((agentName) => {
                      const currentModel = localConfig.openRouter.agentModels[agentName];
                      const modelInfo = getModelInfo(currentModel);
                      return (
                        <div key={agentName} className="p-4 border border-gray-200 rounded-lg bg-gray-50/50 flex items-center justify-between">
                          <div>
                            <Label className="text-base font-medium">{agentName}</Label>
                            <p className="text-sm text-gray-600">
                              {agentDescriptions[agentName as keyof typeof agentDescriptions]}
                            </p>
                            {modelInfo ? (
                              <p className="text-xs text-blue-600 mt-1">
                                Current: {modelInfo.name} ({modelInfo.provider})
                              </p>
                            ) : (
                              <p className="text-xs text-red-600 mt-1">No model selected</p>
                            )}
                          </div>
                          <div className="flex flex-col space-y-2 items-end">
                            <Button onClick={() => setSelectingModelForAgent(agentName)} variant="outline" size="sm" className="w-full">
                              Change Model
                            </Button>
                            <div className="w-full">
                              <Label htmlFor={`archetype-${agentName}`} className="sr-only">Archetype for {agentName}</Label>
                              <Select
                                value={localConfig.openRouter.archetype_assignments?.[agentName] || AgentArchetype.PRAGMATIST}
                                onValueChange={(value) => {
                                  const newAssignments = {
                                    ...(localConfig.openRouter.archetype_assignments || {}),
                                    [agentName]: value as AgentArchetype
                                  };
                                  const updatedConfig = {
                                    ...localConfig,
                                    openRouter: {
                                      ...localConfig.openRouter,
                                      archetype_assignments: newAssignments
                                    }
                                  };
                                  setLocalConfig(updatedConfig);
                                }}
                              >
                                <SelectTrigger id={`archetype-${agentName}`} className="w-full text-xs h-8">
                                  <SelectValue placeholder="Select archetype" />
                                </SelectTrigger>
                                <SelectContent>
                                  {Object.values(AgentArchetype).map(arch => (
                                    <SelectItem key={arch} value={arch} className="text-xs">{arch}</SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  // MODEL BROWSER VIEW
                  <div className="space-y-4 mt-4">
                    <div className="flex justify-between items-center">
                        <h3 className="text-md font-medium text-gray-800">
                            Select Model for: <span className="font-bold text-indigo-600">{selectingModelForAgent}</span>
                        </h3>
                        <Button onClick={() => setSelectingModelForAgent(null)} variant="ghost" size="sm" className="gap-1">
                            <X className="w-4 h-4" /> Cancel
                        </Button>
                    </div>

                    {/* Model Search and Filters (copied from original) */}
                    <div className="space-y-3">
                      <div className="flex gap-2">
                        <div className="relative flex-1">
                          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                          <Input
                            placeholder="Search models..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="pl-10"
                          />
                        </div>
                        <Button
                          onClick={() => setShowOnlyPopular(!showOnlyPopular)}
                          variant={showOnlyPopular ? "default" : "outline"}
                          size="sm"
                          className="gap-1"
                        >
                          <Star className="w-4 h-4" />
                          Popular
                        </Button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {getAllCategories().map((category) => (
                          <Button
                            key={category}
                            onClick={() => toggleCategory(category)}
                            variant={selectedCategories.includes(category) ? "default" : "outline"}
                            size="sm"
                            className="text-xs"
                          >
                            {category.toUpperCase()}
                          </Button>
                        ))}
                        {selectedCategories.length > 0 && (
                          <Button
                            onClick={() => setSelectedCategories([])}
                            variant="ghost"
                            size="sm"
                            className="text-xs"
                          >
                            Clear
                          </Button>
                        )}
                      </div>
                      <div className="text-sm text-gray-600">
                        Showing {getFilteredModels().length} of {availableModels.length} models
                      </div>
                    </div>
                    {/* End of copied Model Search and Filters */}
                    
                    <Separator />

                    {/* Enhanced Model Listing */}
                    <div className="space-y-2 pr-2 py-2">
                      {isLoadingModels ? (
                        <div className="flex justify-center items-center py-10">
                          <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
                          <p className="ml-2 text-gray-600">Loading models...</p>
                        </div>
                      ) : getFilteredModels().length > 0 ? (
                        getFilteredModels().map((model) => (
                          <motion.div
                            key={model.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.2 }}
                            onClick={() => {
                              if (selectingModelForAgent) { // Ensure selectingModelForAgent is not null
                                handleModelChange(selectingModelForAgent, model.id);
                                setSelectingModelForAgent(null);
                              }
                            }}
                            className="p-3 border border-gray-200 rounded-lg hover:bg-indigo-50 hover:border-indigo-300 cursor-pointer transition-colors shadow-sm"
                          >
                            <div className="flex justify-between items-start">
                              <h4 className="font-semibold text-sm text-indigo-700 flex-1 break-words pr-2">{model.name}</h4>
                              <Badge variant="outline" className="text-xs whitespace-nowrap">{model.provider}</Badge>
                            </div>
                            <p className="text-xs text-gray-500 mt-1 mb-2 break-words">
                              {model.description ? (model.description.length > 100 ? model.description.substring(0, 97) + '...' : model.description) : 'No description available.'}
                            </p>
                            <div className="flex flex-wrap items-center gap-2 text-xs">
                              {model.contextLength && (
                                <Badge variant="secondary" className="font-normal">Context: {model.contextLength.toLocaleString()} tokens</Badge>
                              )}
                              <Badge variant="secondary" className="font-normal">Category: {model.category}</Badge>
                            </div>
                          </motion.div>
                        ))
                      ) : (
                        <p className="text-sm text-gray-500 text-center py-10">No models match your criteria.</p>
                      )}
                    </div>
                  </div>
                )} 

              </CardContent>
            </Card>

            {/* Current Status */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  {configuration.openRouter.connectionStatus === 'connected' ? (
                    <Wifi className="w-5 h-5 text-green-500" />
                  ) : (
                    <WifiOff className="w-5 h-5 text-red-500" />
                  )}
                  Current Status
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Configuration Status:</span>
                    <Badge 
                      variant={configuration.isConfigured ? "default" : "destructive"}
                      className="ml-2"
                    >
                      {configuration.isConfigured ? "Configured" : "Needs Setup"}
                    </Badge>
                  </div>
                  <div>
                    <span className="font-medium">Connection Status:</span>
                    <Badge 
                      variant={configuration.openRouter.connectionStatus === 'connected' ? "default" : "secondary"}
                      className="ml-2"
                    >
                      {configuration.openRouter.connectionStatus}
                    </Badge>
                  </div>
                  <div>
                    <span className="font-medium">Available Models:</span>
                    <Badge variant="outline" className="ml-2">
                      {availableModels.length} models
                    </Badge>
                  </div>
                  <div>
                    <span className="font-medium">Models Source:</span>
                    <Badge variant={modelsFromCache ? "secondary" : "default"} className="ml-2">
                      {modelsFromCache ? "Cached" : "Fresh"}
                    </Badge>
                  </div>
                  {configuration.openRouter.lastTested && (
                    <div className="col-span-2">
                      <span className="font-medium">Last Tested:</span>
                      <span className="ml-2 text-gray-600">
                        {configuration.openRouter.lastTested.toLocaleString()}
                      </span>
                    </div>
                  )}
                </div>

                {/* Model Summary */}
                {availableModels.length > 0 && (
                  <div className="space-y-2">
                    <span className="font-medium text-sm">Model Categories:</span>
                    <div className="flex flex-wrap gap-1">
                      {getAllCategories().map((category) => {
                        const count = availableModels.filter(m => m.category === category).length;
                        return (
                          <Badge key={category} variant="outline" className="text-xs">
                            {category.toUpperCase()} ({count})
                          </Badge>
                        );
                      })}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between items-center pt-4 pb-4 px-6 border-t flex-shrink-0"> {/* Added pb-4 px-6 and items-center for better spacing with more buttons */}
            <div className="flex gap-2"> {/* Group left-side buttons */}
              <Button
                onClick={handleApplyChanges}
                variant="outline"
                className="gap-2"
              >
                Apply Changes
              </Button>
              <Button
                onClick={handleDownloadConfiguration}
                variant="outline"
                className="gap-2"
              >
                <Download className="w-4 h-4" />
                Download Config
              </Button>
              <input 
                type="file"
                accept=".json"
                ref={fileInputRef}
                onChange={handleFileUpload}
                className="hidden"
                id="upload-config-input"
              />
              <Button
                onClick={() => fileInputRef.current?.click()}
                variant="outline"
                className="gap-2"
              >
                <Upload className="w-4 h-4" />
                Upload Config
              </Button>
            </div>
            
            <div className="flex gap-2">
              <Button
                onClick={() => setIsOpen(false)}
                variant="outline"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSaveConfiguration}
                className="gap-2"
                disabled={!ConfigurationService.validateApiKey(localConfig.openRouter.apiKey)}
              >
                <Save className="w-4 h-4" />
                Save Configuration
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </TooltipProvider>
  );
}
