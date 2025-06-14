-- Schema for quorum sensing signal molecules
BEGIN;

CREATE TABLE IF NOT EXISTS signal_molecules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    signal_type TEXT NOT NULL,
    strength FLOAT NOT NULL,
    source_agent TEXT,
    metadata JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_signal_type ON signal_molecules(signal_type);
CREATE INDEX IF NOT EXISTS idx_signal_time ON signal_molecules(timestamp DESC);

COMMIT;
