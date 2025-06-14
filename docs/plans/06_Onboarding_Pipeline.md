# Thousand-Question Onboarding Pipeline

## Purpose
Automatically build a rich persona for each new agent using an expanded **1 000-question** framework.

## Flowchart
```
  Start
    │
    ▼
 sampleQuestions(120) ──► askLLM ──► storeAnswer(Event) ──► ΔAnswerCount >= 120?
    │                                         │
    │                                         └──► continue batching
    ▼
 scorePersonaVector ──► createBelief("persona_summary")
    │
    ▼
 autoAnswerRemaining(880) via _generate_answer()
    │
    ▼
 DONE (persona ready)
```

## API
| Method | Path | Body | SSE/WS Events |
|--------|------|------|---------------|
| `POST` | `/onboarding/{agent_id}` | `{ "preset": "scientist" }` | `progress`, `done` |

## Front-End Wizard
* Stepper UI (Start → 10% → 100%).
* Live persona summary shown on completion.

## Metrics
* Tokens consumed counted in `SessionMetrics`.
* On completion, Belief node `persona_summary` available for all future prompts.
