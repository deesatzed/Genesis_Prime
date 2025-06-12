# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is a monorepo containing multiple AI consciousness simulation and memory management systems focused on implementing sentient AI personas through the "Thousand Questions" personality profiling approach.

### Core Projects
- **amm-production-bld-20250520** - Production Agno Memory Module (AMM) system for building AI agents with persistent memory
- **MCP_Chorus** - Multi-core AI architecture with specialized "Aspect Cores" for emergent behavior
- **chorus_one** - Sentient AI POC with distributed MCP servers simulating consciousness
- **apps/gp_b_core** - Next.js dashboard for consciousness visualization and agent interaction
- **apps/option1_mono_agent** - Single agent implementation for Thousand Questions processing

### Key Technologies
- Backend: Python 3.13+, FastAPI, Google Gemini API, LanceDB, PostgreSQL with pgvector
- Frontend: Next.js 15, TypeScript, React 18, Tailwind CSS, Radix UI components
- Memory: AMM memory subsystem with persistent storage, semantic search, session summarization
- Infrastructure: Docker, Conda environments, Prisma ORM

## Essential Commands

### Environment Setup
```bash
# AMM system environment
conda env create -f amm-production-bld-20250520/environment.yml
conda activate amm-env

# Install dependencies
pip install -r amm-production-bld-20250520/requirements.txt
```

### Development Servers
```bash
# Next.js consciousness dashboard
cd apps/gp_b_core
npm install
npm run dev              # http://localhost:3000

# AMM GUI (Streamlit)
cd amm-production-bld-20250520
python run_amm_gui.py    # http://localhost:8501

# MCP servers (chorus_one)
cd chorus_one/sentient-ai-poc
./docker-run.sh build && ./docker-run.sh start
```

### Testing
```bash
# AMM system tests
cd amm-production-bld-20250520
./run_tests.sh

# Unit tests
pytest tests/unit/ -v

# MCP component tests
python run_mcp_tests.py
```

### Build Operations
```bash
# Frontend build
cd apps/gp_b_core
npm run build
npm run start

# AMM agent from design
cd amm-production-bld-20250520
python build_amm.py designs/news_briefing_agent.json --build-type mcp_server
```

## Architecture Overview

### Memory Integration Strategy (Core Focus)
The repository implements a comprehensive plan to integrate AMM memory structures into GP_b_git applications. Four architectural options are detailed in PLAN_Notes.md:

1. **Option 1 - Mono-Agent + Shared Memory** - Single agent handles Thousand Questions processing with AMM memory backend
2. **Option 2 - Tri-Agent Pipeline** - Separate Profiler, Narrative, and Validator agents with quality gates
3. **Option 3 - Hybrid RAG** - Retrieval-augmented generation with vector similarity search
4. **Option 4 - Archetype Pre-Seed** - Pre-built personas with personal drift capabilities

### AMM Memory Components
- **Memory Class** - Core abstraction for long-term memory with LLM integration
- **MemoryManager** - Automated extraction and storage of salient conversation facts
- **SessionSummarizer** - Conversation condensation to manage context window
- **AgentStorage** - Persistent dialogue history with database backing

### Database Schema (Shared)
```sql
-- Core memory tables
user_memories (user_id, content, embedding, created_at)
agent_sessions (user_id, session_id, transcript, summary)

-- Thousand Questions specific
tq_questions (id, text, category, themes, complexity)
tq_answers (user_id, question_id, answer_text, is_user_answer, confidence)
user_profiles (user_id, traits, seed_persona, updated_at)
```

### Vector Search Configuration
- **Embeddings**: text-embedding-3-large (1536-dim)
- **Storage**: PostgreSQL with pgvector extension (production), LanceDB (development)
- **Similarity**: Cosine distance with HNSW indexing

## Key Configuration Files

- `amm-production-bld-20250520/environment.yml` - Conda environment for AMM system
- `apps/gp_b_core/package.json` - Next.js dashboard dependencies and scripts
- `chorus_one/sentient-ai-poc/docker-compose.yml` - MCP services orchestration
- `PLAN_Notes.md` - Comprehensive implementation blueprint for memory integration

## API Endpoints

### AMM System
- GUI: `http://localhost:8501`
- MCP Server: Generated dynamically based on agent design

### MCP Services (chorus_one)
- MCP Hub: `http://localhost:11400/api/`
- Memory Server: `http://localhost:13600/api/`
- Reasoning Server: `http://localhost:12500/api/`
- Personality Server: `http://localhost:14700/api/`

## Current Development Focus

The main objective is implementing the Thousand Questions personality profiling system with persistent memory. Key requirements:

1. **Memory Persistence** - Store user facts and conversation context across sessions
2. **Personality Profiling** - Extract Big Five traits from user responses to sample questions
3. **Answer Generation** - Auto-complete remaining 950+ questions based on user profile
4. **Coherence Validation** - Ensure generated answers maintain personality consistency

## Performance Targets

- **Cold-start Sample Flow**: < 8s for 50 questions
- **Answer Generation**: ≤ 1.1s average per question
- **Memory Retrieval**: ≤ 250ms p95 latency
- **Database TPS**: ≥ 500 writes/s peak

## Memory System Integration

When integrating AMM memory components:
1. Use `Memory` class with SQLite (dev) or PostgreSQL (prod) backend
2. Configure `MemoryManager` for automated fact extraction
3. Implement `SessionSummarizer` to prevent token bloat
4. Set up vector indexing for semantic similarity search
5. Follow GDPR compliance patterns for user data deletion

## Known Issues

- Docker build configuration needs resolution in chorus_one project
- Thousand Questions processing pipeline requires completion
- Authentication system for MCP server registration pending
- Vector similarity search optimization needed for large memory stores