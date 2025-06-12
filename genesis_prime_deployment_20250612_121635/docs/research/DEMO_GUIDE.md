# Sentient AI POC Demo Guide

## System Overview

The Sentient AI Proof of Concept demonstrates a distributed AI system capable of answering questions with a coherent personality and knowledge base. The system consists of several interconnected components:

1. **MCP Hub** - Central orchestration component that routes requests to specialized servers
2. **Reasoning Server** - Generates thoughtful responses to questions
3. **Memory Server** - Stores and retrieves knowledge
4. **Web Interface** - User-friendly interaction portal for interacting with the system

## Demo Setup

### Prerequisites

1. Activate the conda environment:
   ```bash
   conda activate mcp-env
   ```

2. Navigate to the project directory:
   ```bash
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   ```

### Starting the Services

1. Create symbolic links for Python modules (if not already done):
   ```bash
   ln -sf mcp-hub mcp_hub
   ln -sf memory-server memory_server
   ln -sf personality-server personality_server
   ln -sf reasoning-server reasoning_server
   ```

2. Stop any existing servers:
   ```bash
   pkill -f "python.*uvicorn"
   ```

3. Start the MCP Hub Server (Terminal 1):
   ```bash
   python -m uvicorn mcp_hub.api.main:app --host 0.0.0.0 --port 11400 --reload
   ```

4. Start the Reasoning Server (Terminal 2):
   ```bash
   python -m uvicorn reasoning_server.api.main:app --host 0.0.0.0 --port 12500 --reload
   ```

5. Start the Memory Server (Terminal 3):
   ```bash
   python -m uvicorn memory_server.api.main:app --host 0.0.0.0 --port 13600 --reload
   ```

6. Start the Web Interface (Terminal 4):
   ```bash
   cd web-interface
   python app.py
   ```
   The web interface will be available at http://localhost:5000

## Demo Options

You can interact with the system through either the web interface or the command-line demo script.

### Thousand Questions Processing

The Thousand Questions processor allows the AI to build a comprehensive knowledge base and personality profile by processing a diverse set of introspective questions:

1. **Running the Processor**:
   ```bash
   # Navigate to the project directory
   cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc
   
   # Run with default settings
   python thousand_questions_processor.py
   
   # Run with custom batch size
   python thousand_questions_processor.py --batch-size=20
   
   # Run with custom input and output paths
   python thousand_questions_processor.py --questions-path=custom_questions.json --output-path=custom_responses.json
   ```

2. **Monitoring Progress**:
   ```bash
   # View the processing log
   tail -f thousand_questions_processing.log
   
   # Check the output file for progress
   cat processed_responses.json | grep -A5 metadata
   ```

3. **Testing Knowledge Integration** (once fully implemented):
   After processing a significant number of questions, the AI's responses should reflect the knowledge gained from the Thousand Questions. Try asking questions that relate to the AI's values, beliefs, or preferences to see how the responses have been enhanced by the knowledge base.

### Basic Usage

1. Check system health:
   ```bash
   python cli_demo.py --health
   ```

2. Ask a single question:
   ```bash
   python cli_demo.py -q "How do I fix a Python NoneType error in a loop?" -c "error_resolution"
   ```

3. Run in interactive mode:
   ```bash
   python cli_demo.py -i
   ```

### Interactive Mode Commands

In interactive mode, you can:
- Type a question directly to send it to the MCP Hub
- Type `health` to check the MCP Hub health
- Type `category: NAME` to set a question category (e.g., `category: error_resolution`)
- Type `exit` or `quit` to end the session

## Demo Scenarios

### 1. Error Resolution

Try asking programming error-related questions:

```
How do I fix a Python NoneType error in a loop?
What causes a segmentation fault in C++ and how do I fix it?
How to resolve "undefined is not a function" in JavaScript?
```

### 2. Feature Implementation

Ask about implementing specific features:

```
How do I implement authentication in a React application?
What's the best way to add pagination to a REST API?
How can I create a responsive layout with CSS Grid?
```

### 3. Best Practices

Inquire about programming best practices:

```
What are best practices for error handling in Python?
How should I structure a large Node.js application?
What's the recommended way to handle state in React?
```

## System Architecture Explanation

While demonstrating the system, you can explain the architecture:

### MCP Hub (Port 11400)
- Central orchestration component
- Routes requests to appropriate specialized servers
- Handles error management and fallback mechanisms
- Implemented with FastAPI for high performance

### Reasoning Server (Port 12500)
- Generates thoughtful responses to questions
- Ensures logical consistency
- Uses enhanced responses for common questions about philosophy, programming, and general knowledge

### Memory Server (Port 13600)
- Stores and retrieves knowledge
- Manages the knowledge repository
- Provides contextual information for questions
- Stores responses to the Thousand Questions
- Will eventually support knowledge graph capabilities

### Thousand Questions Processor
- Asynchronous batch processor for handling all questions
- Processes questions through the MCP Hub
- Stores responses in the Memory Server
- Tracks progress and handles errors gracefully
- Provides detailed logging and progress reporting

## Implementation Highlights

Highlight some key implementation features:

1. **Server Registration System**
   - Servers register with the MCP Hub
   - Health monitoring ensures system reliability
   - Load balancing capabilities for scalability

2. **Standardized Error Handling**
   - Consistent error responses across all components
   - Detailed error information for debugging
   - Graceful degradation when services are unavailable

3. **Modular Architecture**
   - Components can be developed and scaled independently
   - Clear separation of concerns
   - Extensible design for adding new capabilities

## Troubleshooting

If you encounter issues during the demo:

1. **Service Not Responding**
   - Check if the service is running: `ps aux | grep -E 'uvicorn|python' | grep -v grep`
   - Restart the service if needed

2. **Module Import Errors**
   - Verify symbolic links are created correctly
   - Check Python path includes the project root

3. **CLI Demo Script Issues**
   - Ensure the MCP Hub URL is correct (default: http://localhost:11400)
   - Verify the script has execute permissions: `chmod +x cli_demo.py`

## Next Steps

After the demo, here are potential next steps for the project:

1. **Complete Thousand Questions Processing System**
   - Enhance Memory Server with knowledge graph capabilities
   - Implement personality profile generation from responses
   - Create knowledge integration for Reasoning Server
   - Develop monitoring and management tools

2. **Further Enhance Response Generation**
   - Expand the library of enhanced responses
   - Implement more sophisticated reasoning capabilities
   - Add support for more question categories

3. **Expand Knowledge Base**
   - Integrate processed Thousand Questions into the knowledge base
   - Implement semantic search for knowledge retrieval
   - Develop knowledge visualization tools

4. **Implement Personality Features**
   - Generate personality traits from Thousand Questions responses
   - Ensure consistent personality across interactions
   - Create adaptive personality evolution based on interactions
