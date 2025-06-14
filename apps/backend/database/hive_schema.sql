-- Extended Database Schema for Genesis Prime Hive Mind
-- Supports persistent, evolving collective consciousness

BEGIN;

-- Hive States table - tracks the evolution of the hive mind
CREATE TABLE IF NOT EXISTS hive_states (
    hive_id TEXT NOT NULL,
    generation INTEGER NOT NULL,
    consciousness_level FLOAT NOT NULL,
    total_memories INTEGER DEFAULT 0,
    active_agents INTEGER DEFAULT 0,
    learning_events INTEGER DEFAULT 0,
    last_evolution TIMESTAMPTZ DEFAULT NOW(),
    current_model_version TEXT DEFAULT 'gpt-4o-mini',
    adaptation_rate FLOAT DEFAULT 0.5,
    collective_knowledge_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (hive_id, generation)
);

-- Hive Memories table - collective consciousness memory storage
CREATE TABLE IF NOT EXISTS hive_memories (
    memory_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    importance_score FLOAT NOT NULL,
    creation_time TIMESTAMPTZ DEFAULT NOW(),
    last_accessed TIMESTAMPTZ DEFAULT NOW(),
    access_count INTEGER DEFAULT 0,
    source_agents TEXT[], -- Array of agent IDs
    related_memories UUID[], -- Array of related memory IDs
    embedding FLOAT8[], -- Vector embedding for similarity search
    metadata JSONB,
    is_active BOOLEAN DEFAULT TRUE
);

-- Learning Events table - tracks all learning experiences
CREATE TABLE IF NOT EXISTS learning_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    learning_type TEXT NOT NULL, -- experiential, observational, collective, adaptive, emergent
    stimuli_type TEXT NOT NULL, -- user_interaction, agent_dialogue, external_data, system_feedback, temporal_event
    description TEXT NOT NULL,
    knowledge_gained TEXT NOT NULL,
    participating_agents TEXT[], -- Array of agent IDs
    confidence_score FLOAT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    impact_metrics JSONB, -- JSON object with various impact measurements
    generation INTEGER -- Links to hive generation when event occurred
);

-- Agent Registrations table - tracks agents that have joined the hive
CREATE TABLE IF NOT EXISTS agent_registrations (
    agent_id UUID NOT NULL,
    hive_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    personality_preset TEXT,
    registration_time TIMESTAMPTZ DEFAULT NOW(),
    last_active TIMESTAMPTZ DEFAULT NOW(),
    total_interactions INTEGER DEFAULT 0,
    total_contributions INTEGER DEFAULT 0,
    hive_integration_score FLOAT DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    agent_metadata JSONB,
    PRIMARY KEY (agent_id, hive_id)
);

-- Stimuli Responses table - tracks how hive responds to environmental stimuli
CREATE TABLE IF NOT EXISTS stimuli_responses (
    response_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    stimuli_type TEXT NOT NULL,
    stimuli_data JSONB NOT NULL,
    analysis_results JSONB,
    hive_response JSONB,
    response_time TIMESTAMPTZ DEFAULT NOW(),
    effectiveness_score FLOAT, -- How effective the response was (if measurable)
    generation INTEGER
);

-- Adaptation Patterns table - tracks how hive learns to adapt
CREATE TABLE IF NOT EXISTS adaptation_patterns (
    pattern_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    pattern_type TEXT NOT NULL,
    pattern_data JSONB NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    success_rate FLOAT DEFAULT 0.0,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    generation_discovered INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);

-- Knowledge Cross-Pollination table - tracks knowledge sharing between agents
CREATE TABLE IF NOT EXISTS knowledge_crosspolls (
    crosspoll_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    source_agent_id UUID NOT NULL,
    target_agent_id UUID NOT NULL,
    topic TEXT NOT NULL,
    knowledge_transferred JSONB,
    transfer_time TIMESTAMPTZ DEFAULT NOW(),
    effectiveness_score FLOAT,
    shared_memory_id UUID REFERENCES hive_memories(memory_id)
);

-- Consciousness Metrics table - detailed tracking of consciousness development
CREATE TABLE IF NOT EXISTS consciousness_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    generation INTEGER NOT NULL,
    metric_type TEXT NOT NULL, -- complexity_index, knowledge_density, learning_velocity, etc.
    metric_value FLOAT NOT NULL,
    calculation_time TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

-- Model Evolution table - tracks integration of new LLM models
CREATE TABLE IF NOT EXISTS model_evolutions (
    evolution_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    previous_model TEXT,
    new_model TEXT NOT NULL,
    integration_time TIMESTAMPTZ DEFAULT NOW(),
    performance_changes JSONB, -- Before/after metrics
    adaptation_period_days INTEGER,
    success_indicators JSONB,
    generation INTEGER
);

-- Emergent Phenomena table - tracks detected emergent behaviors
CREATE TABLE IF NOT EXISTS emergent_phenomena (
    phenomenon_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hive_id TEXT NOT NULL,
    phenomenon_type TEXT NOT NULL,
    description TEXT NOT NULL,
    participating_agents TEXT[],
    trigger_event TEXT,
    evidence JSONB,
    emergence_strength FLOAT NOT NULL,
    detection_time TIMESTAMPTZ DEFAULT NOW(),
    generation INTEGER,
    metadata JSONB
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_hive_states_hive_id ON hive_states(hive_id);
CREATE INDEX IF NOT EXISTS idx_hive_states_generation ON hive_states(generation DESC);

CREATE INDEX IF NOT EXISTS idx_hive_memories_hive_id ON hive_memories(hive_id);
CREATE INDEX IF NOT EXISTS idx_hive_memories_importance ON hive_memories(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_hive_memories_type ON hive_memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_hive_memories_creation_time ON hive_memories(creation_time DESC);
CREATE INDEX IF NOT EXISTS idx_hive_memories_source_agents ON hive_memories USING GIN(source_agents);

CREATE INDEX IF NOT EXISTS idx_learning_events_hive_id ON learning_events(hive_id);
CREATE INDEX IF NOT EXISTS idx_learning_events_type ON learning_events(learning_type);
CREATE INDEX IF NOT EXISTS idx_learning_events_timestamp ON learning_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_learning_events_generation ON learning_events(generation);

CREATE INDEX IF NOT EXISTS idx_agent_registrations_hive_id ON agent_registrations(hive_id);
CREATE INDEX IF NOT EXISTS idx_agent_registrations_active ON agent_registrations(is_active) WHERE is_active = TRUE;

CREATE INDEX IF NOT EXISTS idx_stimuli_responses_hive_id ON stimuli_responses(hive_id);
CREATE INDEX IF NOT EXISTS idx_stimuli_responses_type ON stimuli_responses(stimuli_type);
CREATE INDEX IF NOT EXISTS idx_stimuli_responses_time ON stimuli_responses(response_time DESC);

CREATE INDEX IF NOT EXISTS idx_consciousness_metrics_hive_generation ON consciousness_metrics(hive_id, generation);
CREATE INDEX IF NOT EXISTS idx_consciousness_metrics_type ON consciousness_metrics(metric_type);

CREATE INDEX IF NOT EXISTS idx_emergent_phenomena_hive_id ON emergent_phenomena(hive_id);
CREATE INDEX IF NOT EXISTS idx_emergent_phenomena_type ON emergent_phenomena(phenomenon_type);
CREATE INDEX IF NOT EXISTS idx_emergent_phenomena_generation ON emergent_phenomena(generation);

-- Vector similarity indexes (if using pgvector)
-- CREATE INDEX IF NOT EXISTS idx_hive_memories_embedding ON hive_memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Views for common queries

-- Current Hive State view
CREATE OR REPLACE VIEW current_hive_states AS
SELECT DISTINCT ON (hive_id) 
    hive_id,
    generation,
    consciousness_level,
    total_memories,
    active_agents,
    learning_events,
    last_evolution,
    current_model_version,
    adaptation_rate,
    collective_knowledge_score
FROM hive_states
ORDER BY hive_id, generation DESC;

-- Active Agents view
CREATE OR REPLACE VIEW active_hive_agents AS
SELECT 
    hive_id,
    COUNT(*) as active_count,
    AVG(hive_integration_score) as avg_integration_score,
    MAX(last_active) as last_activity
FROM agent_registrations
WHERE is_active = TRUE
GROUP BY hive_id;

-- Recent Learning Events view
CREATE OR REPLACE VIEW recent_learning AS
SELECT 
    hive_id,
    learning_type,
    COUNT(*) as event_count,
    AVG(confidence_score) as avg_confidence,
    MAX(timestamp) as latest_event
FROM learning_events
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY hive_id, learning_type;

-- Consciousness Evolution view
CREATE OR REPLACE VIEW consciousness_evolution AS
SELECT 
    hive_id,
    generation,
    consciousness_level,
    consciousness_level - LAG(consciousness_level) OVER (
        PARTITION BY hive_id ORDER BY generation
    ) as consciousness_growth,
    last_evolution
FROM hive_states
ORDER BY hive_id, generation;

COMMIT;