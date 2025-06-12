# Sentient AI POC Demo Script

## Introduction

Welcome to the Sentient AI Proof of Concept demonstration! This demo showcases a distributed AI system capable of answering questions with a coherent personality and knowledge base. The system consists of several interconnected components:

1. **MCP Hub** - Central orchestration component
2. **Reasoning Server** - Generates thoughtful responses
3. **Memory Server** - Stores and retrieves knowledge
4. **Web Interface** - User-friendly interaction portal

## Demo Setup

Before starting the demo, ensure all services are running:

```bash
# Activate the conda environment
conda activate mcp-env

# Navigate to the project directory
cd /home/o2satz/CascadeProjects/Chorus_April/chorus_one/sentient-ai-poc

# Create symbolic links for Python modules
ln -sf mcp-hub mcp_hub
ln -sf memory-server memory_server
ln -sf personality-server personality_server
ln -sf reasoning-server reasoning_server

# Start the MCP Hub Server (Terminal 1)
python -m uvicorn mcp_hub.api.main:app --host 0.0.0.0 --port 11400 --reload

# Start the Reasoning Server (Terminal 2)
python -m uvicorn reasoning_server.api.main:app --host 0.0.0.0 --port 12500 --reload

# Start the Memory Server (Terminal 3)
python -m uvicorn memory_server.api.main:app --host 0.0.0.0 --port 13600 --reload

# Start the Web Interface (Terminal 4)
cd web-interface
python app.py
```

## Demo Walkthrough

### 1. System Health Verification

First, let's verify that all components are running correctly:

```bash
# Check MCP Hub health
curl http://localhost:11400/health
# Expected response: {"status":"ok","timestamp":"..."}

# Test question answering functionality
curl -X POST http://localhost:11400/api/question \
  -H "Content-Type: application/json" \
  -d '{"text": "How do I fix a Python NoneType error in a loop?", "category": "error_resolution"}'
```

### 2. Web Interface Demonstration

Open the web interface in your browser: http://localhost:5000

The web interface provides a user-friendly way to interact with the Sentient AI system. Here's what you can demonstrate:

#### a. Asking Questions

1. Type a programming-related question in the input field, such as:
   - "How do I fix a Python NoneType error in a loop?"
   - "What's the best way to handle exceptions in JavaScript?"
   - "How can I optimize a slow SQL query?"

2. Select an appropriate category (e.g., "error_resolution")

3. Click "Ask" and observe the response

#### b. Exploring Different Question Types

Try different types of questions to showcase the system's versatility:

1. **Error Resolution**:
   - "How do I resolve 'undefined is not a function' in JavaScript?"
   - "What causes a segmentation fault in C++ and how do I fix it?"

2. **Feature Implementation**:
   - "How do I implement authentication in a React application?"
   - "What's the best way to add pagination to a REST API?"

3. **Best Practices**:
   - "What are best practices for error handling in Python?"
   - "How should I structure a large Node.js application?"

### 3. Technical Architecture Explanation

While the demo is running, explain the system architecture:

1. **MCP Hub (Port 11400)**
   - Central orchestration component
   - Routes requests to appropriate specialized servers
   - Handles error management and fallback mechanisms
   - Implemented with FastAPI for high performance

2. **Reasoning Server (Port 12500)**
   - Generates thoughtful responses to questions
   - Ensures logical consistency
   - Currently using placeholder responses for the demo

3. **Memory Server (Port 13600)**
   - Stores and retrieves knowledge
   - Manages the knowledge repository
   - Provides contextual information for questions

4. **Web Interface (Port 5000)**
   - User-friendly frontend
   - Communicates with the MCP Hub via REST API
   - Displays responses in a readable format

### 4. Error Handling Demonstration

The system includes robust error handling. Demonstrate this by:

1. Stopping one of the services (e.g., the Reasoning Server)
2. Asking a question through the web interface
3. Observing how the system handles the failure gracefully

### 5. Implementation Highlights

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

## Q&A Session

Be prepared to answer questions about:

1. **System Architecture**
   - How components communicate
   - Scalability considerations
   - Deployment options

2. **Implementation Details**
   - Technology choices (FastAPI, Flask, etc.)
   - Error handling approach
   - Data flow between components

3. **Future Enhancements**
   - Personality traits implementation
   - Advanced reasoning capabilities
   - Knowledge base expansion

## Conclusion

Summarize the key points of the demo:

1. The Sentient AI POC demonstrates a distributed AI system with specialized components
2. The modular architecture allows for independent development and scaling
3. Robust error handling ensures system reliability
4. The current implementation focuses on programming-related questions and answers

Thank the audience for their attention and invite further exploration of the system.

## Troubleshooting

If you encounter issues during the demo:

1. **Service Not Responding**
   - Check if the service is running: `ps aux | grep -E 'uvicorn|python' | grep -v grep`
   - Restart the service if needed

2. **Module Import Errors**
   - Verify symbolic links are created correctly
   - Check Python path includes the project root

3. **Web Interface Connection Issues**
   - Verify MCP Hub URL is correctly set in app.py
   - Check network connectivity between components
