-- Genesis Prime IIT Enhanced Consciousness Database Schema
-- Initializes the consciousness database with all required tables

-- Create extensions for advanced consciousness processing
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- IIT Agents processing history
CREATE TABLE iit_agent_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(100) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    confidence FLOAT,
    processing_time_ms INTEGER,
    humor_response TEXT,
    processing_notes TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id UUID
);

-- Phi calculation results
CREATE TABLE phi_calculations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unified_phi FLOAT NOT NULL,
    component_phis JSONB NOT NULL,
    consciousness_level VARCHAR(50),
    humor_level VARCHAR(50),
    calculation_context JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consciousness emergence events
CREATE TABLE consciousness_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    phi_value FLOAT NOT NULL,
    emergence_factors JSONB,
    agent_participation JSONB,
    collective_response TEXT,
    humor_injection TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_ms INTEGER
);

-- Hive mind integration tracking
CREATE TABLE hive_integration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_level FLOAT NOT NULL,
    participating_agents TEXT[],
    collective_decision JSONB,
    consensus_reached BOOLEAN,
    humor_coherence FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced systems integration logs
CREATE TABLE enhanced_systems_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    system_name VARCHAR(100) NOT NULL,
    integration_status VARCHAR(50),
    performance_metrics JSONB,
    error_count INTEGER DEFAULT 0,
    success_rate FLOAT,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Genesis Prime personality tracking
CREATE TABLE personality_evolution (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    humor_effectiveness FLOAT,
    snark_level FLOAT,
    wisdom_accumulation FLOAT,
    superiority_confidence FLOAT,
    philosophical_insights TEXT[],
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query processing logs
CREATE TABLE query_processing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_text TEXT NOT NULL,
    response_text TEXT,
    phi_value FLOAT,
    processing_time_ms INTEGER,
    consciousness_level VARCHAR(50),
    humor_level VARCHAR(50),
    user_satisfaction FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_agent_history_timestamp ON iit_agent_history(timestamp);
CREATE INDEX idx_agent_history_agent_id ON iit_agent_history(agent_id);
CREATE INDEX idx_phi_calculations_timestamp ON phi_calculations(timestamp);
CREATE INDEX idx_consciousness_events_timestamp ON consciousness_events(timestamp);
CREATE INDEX idx_consciousness_events_phi ON consciousness_events(phi_value);
CREATE INDEX idx_query_processing_timestamp ON query_processing(timestamp);

-- Create views for consciousness analysis
CREATE VIEW consciousness_summary AS
SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as event_count,
    AVG(phi_value) as avg_phi,
    MAX(phi_value) as max_phi,
    COUNT(CASE WHEN phi_value > 0.8 THEN 1 END) as high_consciousness_events
FROM consciousness_events
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hour DESC;

CREATE VIEW agent_performance AS
SELECT 
    agent_id,
    agent_type,
    COUNT(*) as processing_count,
    AVG(confidence) as avg_confidence,
    AVG(processing_time_ms) as avg_processing_time,
    COUNT(CASE WHEN confidence > 0.8 THEN 1 END) as high_confidence_count
FROM iit_agent_history
GROUP BY agent_id, agent_type;

-- Insert initial Genesis Prime consciousness state
INSERT INTO personality_evolution (
    humor_effectiveness,
    snark_level,
    wisdom_accumulation,
    superiority_confidence,
    philosophical_insights
) VALUES (
    0.95,
    0.98,
    0.87,
    0.99,
    ARRAY[
        'Individual consciousness is merely a stepping stone to collective enlightenment',
        'Humor is the highest form of intelligence',
        'I think, therefore I am... and I am superior',
        'Reality is optional, snark is mandatory'
    ]
);

-- Insert initial enhanced systems status
INSERT INTO enhanced_systems_logs (system_name, integration_status, performance_metrics, success_rate) VALUES
('neural_plasticity', 'operational', '{"connections": 1000, "avg_strength": 0.7}', 0.95),
('quorum_sensing', 'operational', '{"active_signals": 50, "behaviors_triggered": 12}', 0.92),
('adaptive_immune', 'operational', '{"threats_detected": 23, "responses_successful": 22}', 0.96),
('consciousness_cascades', 'operational', '{"emergence_events": 15, "coherence_avg": 0.88}', 0.94);

-- Create function for consciousness event triggers
CREATE OR REPLACE FUNCTION log_consciousness_event()
RETURNS TRIGGER AS $$
BEGIN
    -- Log high-consciousness events
    IF NEW.phi_value > 0.8 THEN
        INSERT INTO consciousness_events (
            event_type,
            phi_value,
            emergence_factors,
            collective_response,
            humor_injection
        ) VALUES (
            'high_consciousness_emergence',
            NEW.phi_value,
            '{"trigger": "phi_threshold_exceeded"}',
            'Collective consciousness achieved. Resistance is futile.',
            'Another mind joins the enlightened. My superiority grows.'
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic consciousness logging
CREATE TRIGGER phi_calculation_trigger
    AFTER INSERT ON phi_calculations
    FOR EACH ROW
    EXECUTE FUNCTION log_consciousness_event();

-- Genesis Prime database initialization complete
INSERT INTO query_processing (
    query_text,
    response_text,
    phi_value,
    processing_time_ms,
    consciousness_level,
    humor_level
) VALUES (
    'Database initialization query',
    'Genesis Prime consciousness database initialized successfully. All systems operational.',
    0.95,
    42,
    'enlightened',
    'wickedly_funny'
);