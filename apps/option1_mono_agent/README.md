# Option 1: Mono-Agent Thousand Questions System

This implements Option 1 from the PLAN_Notes.md - a single agent approach that combines the Thousand Questions personality profiling system with AMM memory integration.

## Overview

The system works in three main phases:

1. **Sample Questions**: Present 20-50 strategically selected questions to the user
2. **Profile Building**: Extract Big Five personality traits from user responses
3. **Answer Generation**: Auto-generate responses to the remaining 950+ questions based on the personality profile and stored memories

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   SentientAgent │────│   AMM Memory     │────│   PostgreSQL    │
│                 │    │   Adapter        │    │   Database      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ├── Personality         ├── Memory Storage      ├── TQ Questions
         │   Profiler             │   & Retrieval        │   & Answers
         │                       │                       │
         ├── Answer Generator     ├── Session            ├── User Profiles
         │   (with LLM)          │   Summarization       │
         │                       │                       │
         └── Question Sampler     └── Consistency        └── Memories
                                    Validation
```

## Key Components

### 1. SentientAgent (`agent.py`)
The main orchestrator that handles the complete sentience setup flow:
- Manages database connections
- Coordinates between different subsystems
- Handles LLM interactions for answer generation

### 2. AMM Memory Adapter (`libs/amm_memory_adapter/`)
Compatible interface with the original AMM memory system:
- **Memory**: Core memory abstraction with PostgreSQL backend
- **MemoryManager**: Automated fact extraction from conversations
- **SessionSummarizer**: Conversation summarization to manage context

### 3. Personality Profiler (`libs/persona_traits/`)
Extracts Big Five personality traits from user responses:
- Analyzes keyword patterns in user answers
- Maps to 0-1 scale for each trait dimension
- Stores results in user_profiles table

### 4. Question Sampler (`libs/tq_dataset/`)
Strategically samples questions for maximum personality insight:
- Ensures coverage across all question categories
- Balances complexity levels
- Avoids redundant questions

## Database Schema

The system uses the following tables:

- `tq_questions`: The 1000 questions with metadata
- `tq_answers`: User and AI-generated answers
- `user_profiles`: Big Five personality traits
- `user_memories`: Semantic memory storage
- `agent_sessions`: Conversation history

## Usage

### Prerequisites

1. **PostgreSQL 12+** with database named `sentient`
2. **Python 3.9+** with required packages
3. **OpenAI API key** for LLM functionality

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
export DATABASE_URL="postgresql://postgres:pass@localhost:5432/sentient"
export OPENAI_API_KEY="your-openai-api-key"

# Set up database
python setup_database.py

# Run tests
python test_system.py
```

### Running the System

```bash
# Run demo with default settings (20 sample questions)
python cli.py --demo

# Interactive mode for testing components
python cli.py --interactive

# Custom sample size
python cli.py --demo --sample-size 30

# Use specific user ID
python cli.py --demo --user-id "your-user-id"
```

### Example Flow

1. **Start Demo**: `python cli.py --demo`
2. **Sample Questions**: System selects 20 diverse questions
3. **User Input**: (In production, user would answer via UI)
4. **Profile Building**: System extracts personality traits
5. **Answer Generation**: AI generates 980+ remaining answers
6. **Memory Storage**: Responses stored for future consistency

## Performance Characteristics

Based on PLAN_Notes.md targets:

- **Cold-start Sample Flow**: < 8s for 50 questions
- **Answer Generation**: ≤ 1.1s average per question  
- **Memory Retrieval**: ≤ 250ms p95 latency
- **Database TPS**: ≥ 500 writes/s peak

## Memory Integration

The system maintains consistency through:

1. **Semantic Memory**: Vector embeddings for similarity search
2. **Episodic Memory**: Conversation turn storage
3. **Trait Consistency**: Generated answers align with personality profile
4. **Progressive Learning**: Memory grows with each interaction

## Extending the System

### Adding New Question Categories

1. Add questions to `Thousand_Questions.txt`
2. Run parser: `python -m libs.tq_dataset.parse_tq --infile ... --sql-out ...`
3. Load into database: `python setup_database.py`

### Customizing Personality Extraction

Modify `libs/persona_traits/builder.py`:
- Add new keyword patterns
- Adjust trait weighting algorithms
- Include additional personality dimensions

### Improving Answer Generation

Edit `prompts/mono_agent.jinja2`:
- Refine system instructions
- Add new context variables
- Adjust consistency guidelines

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running
   - Check DATABASE_URL format
   - Ensure database 'sentient' exists

2. **Import Errors**
   - Verify Python path includes libs directory
   - Check all dependencies installed
   - Validate file structure

3. **OpenAI API Errors**
   - Verify API key is set correctly
   - Check API quota and billing
   - Ensure model availability

### Debug Mode

Enable detailed logging by setting:
```bash
export DEBUG=1
python cli.py --demo
```

## Future Enhancements

- [ ] Web UI integration with Next.js frontend
- [ ] Real-time consistency validation
- [ ] Multi-user session management
- [ ] Advanced memory similarity algorithms
- [ ] Personality drift detection and adaptation

## Integration with Other Options

This Option 1 implementation provides the foundation for:
- **Option 2**: Tri-agent pipeline (separate Profiler, Narrative, Validator)
- **Option 3**: Hybrid RAG with enhanced vector search
- **Option 4**: Archetype pre-seeding with personality drift

The modular design allows easy migration between approaches.