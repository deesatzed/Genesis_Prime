# Sentient AI POC Implementation Checklist - Part 1: Setup and Foundation

## Project Setup Phase

### 1. Development Environment Setup
- [x] Create project directory structure
```bash
mkdir -p sentient-ai-poc/{mcp-hub,memory-server,personality-server,reasoning-server,client-interface,shared,docs,tests}
mkdir -p sentient-ai-poc/shared/{models,schemas,utils}
mkdir -p sentient-ai-poc/docs/{architecture,api,deployment}
mkdir -p sentient-ai-poc/tests/{unit,integration,e2e}
```

- [x] **Implement directory error handling (added 2025-03-23)**
```python
# Create a centralized directory manager in shared/utils/directory_manager.py
# Features:
#  - Automatic directory creation and validation
#  - Comprehensive error handling and recovery
#  - Backup mechanisms for critical files
#  - Fallback approaches when primary access methods fail
```

- [ ] Initialize Git repository
```bash
cd sentient-ai-poc
git init
echo "# Sentient AI POC" > README.md
echo ".env" > .gitignore
echo "**/__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore
echo ".pytest_cache/" >> .gitignore
git add .
git commit -m "Initial project structure"
```

- [ ] Set up Python virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

- [ ] Create requirements files
```python
# requirements-dev.txt
pytest==7.3.1
pytest-asyncio==0.21.0
black==23.3.0
isort==5.12.0
mypy==1.3.0
pylint==2.17.4

# requirements.txt
fastapi==0.95.1
uvicorn==0.22.0
pydantic==1.10.8
langchain==0.0.200
openai==0.27.7
python-dotenv==1.0.0
aiohttp==3.8.4
motor==3.1.2
pytest==7.3.1
httpx==0.24.1
```

- [ ] Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Configuration and Environment Setup
- [ ] Create base configuration class
```python
# sentient-ai-poc/shared/utils/config.py
import os
from typing import Dict, Optional, Any
from pydantic import BaseSettings, Field

class BaseConfig(BaseSettings):
    """Base configuration for all services."""
    
    # Environment
    ENV: str = Field("development", env="ENV")
    DEBUG: bool = Field(False, env="DEBUG")
    
    # Service discovery
    MCP_HUB_URL: str = Field("http://localhost:8000", env="MCP_HUB_URL")
    MEMORY_SERVER_URL: str = Field("http://localhost:8001", env="MEMORY_SERVER_URL")
    PERSONALITY_SERVER_URL: str = Field("http://localhost:8002", env="PERSONALITY_SERVER_URL")
    REASONING_SERVER_URL: str = Field("http://localhost:8003", env="REASONING_SERVER_URL")
    
    # AI Configuration
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

- [ ] Create .env file with environment variables
```
# .env
ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Service URLs
MCP_HUB_URL=http://localhost:8000
MEMORY_SERVER_URL=http://localhost:8001
PERSONALITY_SERVER_URL=http://localhost:8002
REASONING_SERVER_URL=http://localhost:8003

# OpenAI API key
OPENAI_API_KEY=your-api-key-here
```

### 3. Shared Model Definitions
- [ ] Create base models for communication
```python
# sentient-ai-poc/shared/models/base.py
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class Response(BaseModel):
    """Standard response model."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None

class Question(BaseModel):
    """Question model."""
    id: str
    text: str
    category: str
    themes: List[str] = []
    complexity: int = Field(1, ge=1, le=5)
    related_questions: List[str] = []
    knowledge_dependencies: List[str] = []
    personality_dimensions: List[str] = []

class QuestionResponse(BaseModel):
    """Response to a question."""
    question_id: str
    response: str
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
```

- [ ] Create personality and knowledge models
```python
# sentient-ai-poc/shared/models/personality.py
from typing import Dict, List, Optional, Any, Union, Tuple
from pydantic import BaseModel, Field, validator
from datetime import datetime

class PersonalityTrait(BaseModel):
    """Model for a personality trait."""
    value: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)

class CoreValue(BaseModel):
    """Model for a core value."""
    value: str
    importance: float = Field(..., ge=0.0, le=1.0)
    description: str

class Experience(BaseModel):
    """Model for a formative experience."""
    id: str
    description: str
    emotional_impact: str
    significance: float = Field(..., ge=0.0, le=1.0)

class OriginStory(BaseModel):
    """Model for the AI's origin story."""
    creation_narrative: str
    self_awareness_development: str
    formative_experiences: List[Experience] = []

class Personality(BaseModel):
    """Main personality model."""
    core_traits: Dict[str, PersonalityTrait]
    origin_story: OriginStory
    core_values: List[CoreValue] = []
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"
```

```python
# sentient-ai-poc/shared/models/knowledge.py
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime

class KnowledgeItem(BaseModel):
    """Model for a knowledge item."""
    id: str
    content: str
    category: str
    tags: List[str] = []
    confidence: float = Field(..., ge=0.0, le=1.0)
    emotional_tone: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class KnowledgeCategory(BaseModel):
    """Model for a knowledge category."""
    name: str
    description: str
    items: Dict[str, KnowledgeItem] = {}
```

### 4. Logging Setup
- [ ] Create logging configuration
```python
# sentient-ai-poc/shared/utils/logging.py
import logging
import sys
from typing import Optional
import os

def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """Set up a logger with the specified name and level."""
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")
        
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
        
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
```

### 5. Docker Configuration
- [ ] Create Docker Compose configuration for local development
```yaml
# docker-compose.yml
version: '3.8'

services:
  mcp-hub:
    build:
      context: .
      dockerfile: ./mcp-hub/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./mcp-hub:/app/mcp-hub
      - ./shared:/app/shared
    env_file:
      - .env
    environment:
      - PORT=8000

  memory-server:
    build:
      context: .
      dockerfile: ./memory-server/Dockerfile
    ports:
      - "8001:8001"
    volumes:
      - ./memory-server:/app/memory-server
      - ./shared:/app/shared
    env_file:
      - .env
    environment:
      - PORT=8001

  personality-server:
    build:
      context: .
      dockerfile: ./personality-server/Dockerfile
    ports:
      - "8002:8002"
    volumes:
      - ./personality-server:/app/personality-server
      - ./shared:/app/shared
    env_file:
      - .env
    environment:
      - PORT=8002

  reasoning-server:
    build:
      context: .
      dockerfile: ./reasoning-server/Dockerfile
    ports:
      - "8003:8003"
    volumes:
      - ./reasoning-server:/app/reasoning-server
      - ./shared:/app/shared
    env_file:
      - .env
    environment:
      - PORT=8003

  client-interface:
    build:
      context: .
      dockerfile: ./client-interface/Dockerfile
    ports:
      - "8080:8080"
    volumes:
      - ./client-interface:/app/client-interface
    env_file:
      - .env
    environment:
      - PORT=8080
    depends_on:
      - mcp-hub
```

- [ ] Create base Dockerfile template
```dockerfile
# Base Dockerfile template
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./shared /app/shared
COPY ./${SERVICE_DIR} /app/${SERVICE_DIR}

ENV PYTHONPATH=/app

CMD ["python", "-m", "${SERVICE_MODULE}.main"]
```

## 6. CI/CD Pipeline Setup
- [ ] Create GitHub Actions workflow file
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run linting
        run: |
          black --check .
          isort --check-only --profile black .
          pylint --disable=C0111,C0301,R0903 sentient-ai-poc/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest
```

## Thousand Questions Processing Phase

### 1. Data Parsing and Structure
- [ ] Create parser for Thousand Questions dataset
```python
# sentient-ai-poc/memory-server/thousand_questions/parser.py
import re
from typing import List, Dict, Any, Optional
import os
from shared.models.base import Question

def process_thousand_questions(file_path: str) -> List[Question]:
    """
    Process raw thousand questions file into structured format with metadata.
    
    Args:
        file_path: Path to the thousand questions text file
        
    Returns:
        List of Question objects with metadata
    """
    questions = []
    current_category = None
    question_id = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a category header
        if not line.startswith(' '):
            current_category = line.lower().replace(' & ', '_').replace(' ', '_')
            continue
            
        # This is a question
        question_text = line.strip()
        if question_text.startswith('    '):
            question_text = question_text[4:]  # Remove leading spaces
            
        # Generate a unique ID
        question_id += 1
        question_id_str = f"q_{question_id:04d}"
        
        # Extract themes from question text
        themes = extract_themes(question_text, current_category)
        
        # Estimate question complexity
        complexity = estimate_complexity(question_text)
        
        # Create question object with basic metadata
        question = Question(
            id=question_id_str,
            text=question_text,
            category=current_category,
            themes=themes,
            complexity=complexity,
            related_questions=[],  # To be filled in post-processing
            knowledge_dependencies=identify_knowledge_dependencies(question_text, current_category),
            personality_dimensions=identify_personality_dimensions(question_text)
        )
        
        questions.append(question)
    
    # Post-process to establish relationships between questions
    questions = establish_question_relationships(questions)
    
    return questions

def extract_themes(question_text: str, category: str) -> List[str]:
    """Extract themes from question text."""
    # Simple keyword-based theme extraction
    themes = []
    theme_keywords = {
        "childhood": ["child", "young", "grow", "early"],
        "values": ["value", "belief", "principle", "ethic"],
        "purpose": ["purpose", "meaning", "goal", "mission"],
        "relationships": ["relationship", "friend", "family", "partner"],
        # Add more theme keywords...
    }
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in question_text.lower() for keyword in keywords):
            themes.append(theme)
    
    # Add category as a theme
    themes.append(category)
    
    return themes

def estimate_complexity(question_text: str) -> int:
    """Estimate question complexity on a scale of 1-5."""
    # Simple heuristics for complexity
    complexity = 1
    
    # Length-based complexity
    if len(question_text) > 100:
        complexity += 1
        
    # Multi-part questions
    if "?" in question_text[question_text.find("?") + 1:]:
        complexity += 1
        
    # Complex concepts
    complex_concepts = ["paradox", "wisdom", "philosophy", "existential", "meaning", 
                         "legacy", "consciousness", "mortality", "ethical"]
    for concept in complex_concepts:
        if concept in question_text.lower():
            complexity += 1
            break
            
    # Cap at 5
    return min(complexity, 5)

def identify_knowledge_dependencies(question_text: str, category: str) -> List[str]:
    """Identify knowledge dependencies for the question."""
    # Simple mapping of dependencies based on category and keywords
    dependencies = []
    
    category_dependencies = {
        "early_life": ["childhood_experiences", "formative_memories"],
        "values_perspective_purpose": ["core_values", "worldview"],
        "relationships": ["relationship_experiences", "social_values"],
        # Add more category dependencies...
    }
    
    # Add category-based dependencies
    if category in category_dependencies:
        dependencies.extend(category_dependencies[category])
    
    # Add keyword-based dependencies
    keyword_dependencies = {
        "family": "family_relationships",
        "friend": "friendship_experiences",
        "work": "career_experiences",
        "love": "romantic_relationships",
        # Add more keyword dependencies...
    }
    
    for keyword, dependency in keyword_dependencies.items():
        if keyword in question_text.lower() and dependency not in dependencies:
            dependencies.append(dependency)
    
    return dependencies

def identify_personality_dimensions(question_text: str) -> List[str]:
    """Identify personality dimensions relevant to the question."""
    # Map questions to Big Five personality dimensions
    dimensions = []
    
    dimension_keywords = {
        "openness": ["new experience", "creative", "curious", "imaginative", "art", "intellectual"],
        "conscientiousness": ["organized", "responsible", "disciplined", "goal", "plan", "prepared"],
        "extraversion": ["social", "outgoing", "energetic", "assertive", "talkative"],
        "agreeableness": ["compassion", "empathy", "cooperation", "warm", "kind"],
        "neuroticism": ["worry", "anxiety", "fear", "stress", "emotional stability"]
    }
    
    for dimension, keywords in dimension_keywords.items():
        if any(keyword in question_text.lower() for keyword in keywords):
            dimensions.append(dimension)
    
    # Ensure at least one dimension
    if not dimensions:
        dimensions.append("openness")  # Default to openness
        
    return dimensions

def establish_question_relationships(questions: List[Question]) -> List[Question]:
    """Establish relationships between questions based on themes and content."""
    # Create lookup for efficient access
    questions_by_id = {q.id: q for q in questions}
    
    for question in questions:
        related_ids = []
        
        # Find questions in the same category
        same_category_questions = [
            q for q in questions 
            if q.category == question.category and q.id != question.id
        ]
        
        # Find questions with shared themes
        for q in same_category_questions:
            shared_themes = set(question.themes).intersection(set(q.themes))
            if len(shared_themes) >= 2:  # At least 2 shared themes
                related_ids.append(q.id)
        
        # Limit related questions to prevent over-connection
        related_ids = related_ids[:5]
        question.related_questions = related_ids
    
    return questions
```

- [ ] Create script to run initial parsing
```python
# sentient-ai-poc/memory-server/scripts/process_questions.py
import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from memory_server.thousand_questions.parser import process_thousand_questions
from shared.utils.logging import setup_logger

logger = setup_logger("process_questions")

def main():
    """Process the thousand questions dataset and save as JSON."""
    input_file = os.path.join(project_root, "data", "thousand_questions.txt")
    output_file = os.path.join(project_root, "data", "processed_questions.json")
    
    logger.info(f"Processing questions from {input_file}")
    questions = process_thousand_questions(input_file)
    logger.info(f"Processed {len(questions)} questions")
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Convert questions to dict for JSON serialization
    questions_data = [q.dict() for q in questions]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_data, f, indent=2)
    
    logger.info(f"Saved processed questions to {output_file}")

if __name__ == "__main__":
    main()
```

### 2. Question Repository Implementation
- [ ] Create repository for question storage and retrieval
```python
# sentient-ai-poc/memory-server/thousand_questions/repository.py
import json
from typing import List, Dict, Optional, Any, Union
import os
from pathlib import Path

from shared.models.base import Question
from shared.utils.logging import setup_logger

logger = setup_logger("question_repository")

class QuestionRepository:
    """Repository for managing question data."""
    
    def __init__(self, data_file: str):
        """
        Initialize the question repository.
        
        Args:
            data_file: Path to the processed questions JSON file
        """
        self.data_file = data_file
        self.questions: Dict[str, Question] = {}
        self.questions_by_category: Dict[str, List[Question]] = {}
        self.questions_by_theme: Dict[str, List[Question]] = {}
        self._load_questions()
    
    def _load_questions(self) -> None:
        """Load questions from the data file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
            
            # Convert to Question objects
            for q_data in questions_data:
                question = Question(**q_data)
                self.questions[question.id] = question
                
                # Index by category
                if question.category not in self.questions_by_category:
                    self.questions_by_category[question.category] = []
                self.questions_by_category[question.category].append(question)
                
                # Index by theme
                for theme in question.themes:
                    if theme not in self.questions_by_theme:
                        self.questions_by_theme[theme] = []
                    self.questions_by_theme[theme].append(question)
            
            logger.info(f"Loaded {len(self.questions)} questions")
        except FileNotFoundError:
            logger.warning(f"Question data file not found: {self.data_file}")
        except json.JSONDecodeError:
            logger.error(f"Error parsing question data file: {self.data_file}")
    
    def get_question(self, question_id: str) -> Optional[Question]:
        """Get a question by ID."""
        return self.questions.get(question_id)
    
    def get_questions_by_category(self, category: str) -> List[Question]:
        """Get all questions in a category."""
        return self.questions_by_category.get(category, [])
    
    def get_questions_by_theme(self, theme: str) -> List[Question]:
        """Get all questions with a specific theme."""
        return self.questions_by_theme.get(theme, [])
    
    def get_related_questions(self, question_id: str) -> List[Question]:
        """Get questions related to a specific question."""
        question = self.get_question(question_id)
        if not question:
            return []
        
        related_questions = []
        for related_id in question.related_questions:
            related_question = self.get_question(related_id)
            if related_question:
                related_questions.append(related_question)
        
        return related_questions
    
    def get_all_questions(self) -> List[Question]:
        """Get all questions."""
        return list(self.questions.values())
    
    def get_all_categories(self) -> List[str]:
        """Get all categories."""
        return list(self.questions_by_category.keys())
    
    def get_all_themes(self) -> List[str]:
        """Get all themes."""
        return list(self.questions_by_theme.keys())
```
