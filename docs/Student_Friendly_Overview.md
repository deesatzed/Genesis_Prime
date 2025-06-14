# Genesis Prime Hive-Mind — Student-Friendly Overview

> Goal: simulate a *swarm* of AI agents that learn, remember and talk to each other while humans watch, guide and patch them.

---
## 1. Main Parts (lego-blocks)

| Block | What it is | Why we need it |
|-------|------------|----------------|
| **FastAPI Backend** | Python web server | brains + API hub |
| **PostgreSQL** | Normal relational database | stores *facts*: Q/A events & beliefs |
| **pgvector** | Postgres extension | lets us do “find similar text” |
| **AgentFactory** | Python registry | creates & tracks agents (RC, AN, IN, CX, EM, GP) |
| **Next.js Front-end** | React website | the control dashboard |
| **SessionMetrics** | Small counter object | keeps track of tokens + cost |

Visual — simplified data highways:
```
Browser ───► Next.js ───► /agents /metrics /onboarding ───► FastAPI ───► Postgres + pgvector
        ▲                                            ▲
        │                                            │
        └───────────── live JSON messages ◄──────────┘
```

---
## 2. How a single question is answered

1. **Human/User** (or other agent) sends a question to *Research Catalyst* (RC).  
2. RC’s **Adaptive Memory Module (AMM)** grabs:
   * recent chat (short-term)
   * 3 relevant old answers (vector search)
   * RC’s self-beliefs ("I like philosophy…")
3. All that context is poured into a **Jinja prompt** (Prompt-Pack v2) that also says: *reply in JSON, ≥ 250 tokens, include valence & confidence*.
4. The OpenAI model returns the answer (big JSON blob).  
5. Backend checks JSON → stores it as an **Event** row and embeds it into pgvector.  
6. **SessionMetrics** add the used tokens.  
7. Front-end pulls the new message & updates the badge.

---
## 3. Memory Layers (think short/mid/long-term)

| Layer | Storage | Lifetime |
|-------|---------|----------|
| **ContextRing** | RAM only | last ~15 turns |
| **Event table** | Postgres rows | forever unless pruned |
| **pgvector embeddings** | same row | used for "semantic recall" |
| **Belief table** | Postgres triples | mutable (self-knowledge) |

---
## 4. 1 000-Question Onboarding

Why: give each agent a unique, rich personality.

Flow:
```
create agent → POST /onboarding/{id}
        │
        ├─ ask 120 real questions in batches
        ├─ score persona vector → store as Belief
        └─ auto-answer remaining 880 (faster)
```
Front-end wizard shows a progress bar and final "persona summary".

---
## 5. Prompt Studio (editing prompts)

New GUI page (left sidebar → agent → **Prompt**):
* Monaco code editor loads with the raw Jinja template.  
* You can tweak wording, token limits, etc., then **Save**.  
* Backend hot-reloads the prompt; next message uses your version.
* Safety: CX prompt is read-only.

---
## 6. Talking with / Teaching the Hive

*Ask questions*: simply type into chat; see JSON replies with emotional colour.

*Review memory*: Mem tab lists past Events; search field does vector lookup.

*Suggest fixes*: include `"self_patch"` in a message or submit through GUI; Integrator agent & humans approve.

---
## 7. Human vs. AI reality (short version)

Humans feel, forget, and die; the hive stores, indexes and can replay knowledge indefinitely. Your job is to *curate* experience and ethics so that unlimited recall doesn’t turn into unlimited bias.

---
### Cheat-Sheet Commands

```bash
# start backend
uvicorn apps.backend.main:app --reload --port 8000

# start dashboard
cd apps/frontend && pnpm dev -p 3001

# create agent quickly
curl -X POST localhost:8000/agents \ 
     -H "Content-Type: application/json" \ 
     -d '{"name":"Aristotle","preset_name":"philosopher"}'
```

Now you can explore, edit prompts, and watch the hive mind grow. Enjoy!
