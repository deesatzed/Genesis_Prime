-- Database schema for Thousand Questions Sentient AI system
-- Based on PLAN_Notes.md specifications

BEGIN;

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create extension for vector similarity (if using pgvector)
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Core questions table
CREATE TABLE IF NOT EXISTS tq_questions (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    category TEXT,
    themes TEXT[],
    complexity SMALLINT,
    related_ids TEXT[]
);

-- User answers to questions
CREATE TABLE IF NOT EXISTS tq_answers (
    user_id UUID NOT NULL,
    question_id TEXT NOT NULL REFERENCES tq_questions(id),
    answer_text TEXT,
    is_user_answer BOOLEAN DEFAULT FALSE,
    confidence NUMERIC(3,2),
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, question_id, version)
);

-- User personality profiles
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id UUID PRIMARY KEY,
    traits JSONB,          -- Big Five & other traits
    seed_persona TEXT,     -- For option 4
    seed_score NUMERIC(3,2),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User memories (compatible with AMM system)
CREATE TABLE IF NOT EXISTS user_memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    content TEXT NOT NULL,
    embedding FLOAT8[],    -- Vector embedding (1536 dimensions for text-embedding-3-large)
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agent sessions (for conversation history)
CREATE TABLE IF NOT EXISTS agent_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    session_id TEXT,
    transcript JSONB,      -- Array of message objects
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tq_answers_user_id ON tq_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_tq_answers_question_id ON tq_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_tq_answers_is_user_answer ON tq_answers(is_user_answer);
CREATE INDEX IF NOT EXISTS idx_tq_questions_category ON tq_questions(category);
CREATE INDEX IF NOT EXISTS idx_tq_questions_themes ON tq_questions USING GIN(themes);
CREATE INDEX IF NOT EXISTS idx_user_memories_user_id ON user_memories(user_id);
CREATE INDEX IF NOT EXISTS idx_user_memories_created_at ON user_memories(created_at);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_user_id ON agent_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_session_id ON agent_sessions(session_id);

-- Vector similarity index (uncomment if using pgvector)
-- CREATE INDEX IF NOT EXISTS idx_user_memories_embedding ON user_memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

COMMIT;