"""Session-scoped token & cost metrics for Genesis Prime backend."""
from __future__ import annotations
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class SessionMetrics(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0

    def add(self, prompt: int, completion: int, cost: float):
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.cost_usd += cost

    def reset(self):
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.cost_usd = 0.0

# ------------- FastAPI dependency -----------------
from fastapi import Request, Depends

def get_metrics(request: Request) -> SessionMetrics:
    # Initialize lazily for unit tests
    if not hasattr(request.app.state, "metrics"):
        request.app.state.metrics = SessionMetrics()
    return request.app.state.metrics
