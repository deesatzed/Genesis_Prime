Assess Compatibility of amm-production-bld-20250520 With GP_b_git Memory Structures
Integrating Memory Structures from amm-production-bld-20250520 into GP_b_git Application
Overview of amm-production-bld-20250520 Architecture

The amm-production-bld-20250520 repository appears to be an AI agent framework with robust memory augmentation capabilities. Its core functionality revolves around managing multiple AI agents (or tools) that can coordinate on tasks, all backed by a persistent memory subsystem. The architecture is modular, comprising components for agents, teams of agents, knowledge bases, and memory management. Key architectural features include:

    Agent and Team Orchestration: The system defines Agent entities (each with a role, AI model, and tools) and higher-level Team entities that coordinate multiple agents for complex tasks
    Google Drive
    Google Drive
    . Each agent/team can be configured with instructions and can share a common memory resource.

    Persistent Memory Integration: A central Memory module is integrated into agents and teams to provide long-term context. This memory is backed by a database (e.g. PostgreSQL or SQLite) to persist information across interactions
    Google Drive
    Google Drive
    . This design enables the system to store and recall facts about the user or task beyond the immediate conversation.

    Tool and Knowledge Modules: The repository includes various tools (e.g. web search, finance APIs) and knowledge base interfaces (with document chunking, SQL knowledge, etc.) to augment agent capabilities
    Google Drive
    Google Drive
    . These allow agents to retrieve external information as needed, complementing the memory system with factual knowledge.

    Runtime Configuration: Agents/teams are configured with parameters such as memory=memory (linking them to the shared Memory object) and storage (for logging agent interactions). Flags like add_memory_references and enable_agentic_memory can be toggled to control how the agent uses the memory (either passively retrieving or actively updating it)
    Google Drive
    Google Drive
    . This indicates a flexible architecture where memory usage can be tailored per agent or team.

In summary, amm-production-bld-20250520 is an agent system designed for persistent conversational memory and knowledge augmentation. Its architecture cleanly separates concerns: agents handle dialogue and reasoning, while dedicated memory components handle long-term information storage and retrieval.
Memory-Related Components in amm-production-bld-20250520

A number of modular components in this repository implement memory structures, persistent storage, and memory augmentation. These can be considered for reuse. Key memory-related components include:

    Memory Class (agno.memory.v2.memory.Memory): This is the core abstraction for long-term memory. A Memory instance is configured with an LLM model and a backing database. It stores and retrieves user-specific memories. For example, in amm-production, a Memory is created with an OpenAI GPT-4 model and a Postgres DB table for user memories
    Google Drive
    . The memory can be cleared or configured to auto-delete entries as needed
    Google Drive
    . This class likely handles embedding or summarizing inputs and retrieving relevant past memories to augment the context.

    Persistent Memory Stores: The system provides persistent storage backends for memory. Notably, PostgresMemoryDb and SqliteMemoryDb are used to save memories in a database table
    Google Drive
    Google Drive
    . The use of a SQL database means memories (user facts, conversation summaries, etc.) persist beyond a single session. The memory tables (e.g., "user_memories") store content and possibly metadata (topics, timestamps) for retrieval. This design enables cross-session continuity.

    Agent Memory Integration: Each agent can be equipped with the Memory object. In the code, agents are initialized with memory=memory to grant them access to the shared memory store
    Google Drive
    Google Drive
    . Agents also use AgentStorage (e.g. PostgresAgentStorage or SqliteStorage) to persist their interaction history or state
    Google Drive
    Google Drive
    . The AgentStorage is a complementary component that logs dialogues (by session or user) to a database table (like "agent_sessions"), ensuring a record of past conversations that can be referenced or summarized later.

    Memory Manager (MemoryManager): A higher-level utility that automatically extracts and stores salient information from dialogues. The MemoryManager uses an LLM to analyze conversation transcripts and generate concise memory entries (e.g. important facts about the user or context) for storage
    Google Drive
    . It can be configured with instructions on what to capture. In practice, the system can run the MemoryManager after each user interaction (if enable_user_memories=True) to continuously grow the knowledge base of user memories
    Google Drive
    .

    Session Summarizer (SessionSummarizer): A component responsible for condensing long interactions into summaries
    Google Drive
    . This helps manage the size of stored memory by summarizing older chat history into compact form. The summarizer uses an LLM (e.g. Claude) to produce an informal conversational summary of a session, which can be stored as a memory record
    Google Drive
    . By periodically summarizing and pruning details, the system retains important context while keeping the memory store efficient.

    Memory Agent (memory_agent.py): An example agent dedicated to demonstrating memory usage. This agent is configured with the Memory object and is allowed to update and use memories extensively. In the code, memory_agent = Agent(... memory=memory, enable_agentic_memory=True, ...) is shown, with comments indicating it can “store memories in a database” and even update them autonomously
    Google Drive
    Google Drive
    . The memory agent can ingest user statements (e.g. “My name is Ava and I like to ski”) and causes the system to record that fact as a user memory in the database
    Google Drive
    . This confirms the repository’s capability to capture user-specific facts and reuse them in future responses.

    Knowledge Base Modules: While not purely “memory” of conversations, the repository’s knowledge modules (for documents, web, etc.) serve as extended memory. Components for document chunking and retrieval (under agno.memory.v2 or knowledge packages) allow agents to remember and reference external information beyond the immediate query
    Google Drive
    Google Drive
    . For instance, a user can provide a document, and the system will chunk and store it, effectively extending the agent’s long-term knowledge. This is another form of memory augmentation (persistent knowledge).

All these components are relatively self-contained and reusable. The Memory class and its DB backends are especially modular – they could be extracted as a library to provide any application with long-term memory storage. Likewise, the MemoryManager and summarizer operate independently of the specific agents, making them candidates to plug into other systems for automated memory extraction. Together, these pieces form a comprehensive memory subsystem that can remember user details, summarize conversations, and persist information reliably.
Current Memory Architecture of GP_b_git

(Note: Direct documentation of GP_b_git’s design was not found in the provided Drive materials, so this assessment is inferred from context.)

The GP_b_git application is presumably a chatbot or agent application in the same project family. Its current memory architecture appears to be simpler or more limited compared to amm-production. From context, we infer the following about GP_b_git:

    Ephemeral Session Memory: GP_b_git likely keeps conversational context only in-memory for the duration of a session. It may rely on the model’s context window or a short history buffer of recent messages. There is no evidence of a persistent memory database in use by GP_b_git (no references to a memory DB or similar in the available materials), suggesting that once the session or application restarts, any conversation history or learned user information is lost.

    Lack of Persistent Store: Unlike amm-production, GP_b_git probably does not store chat history or user facts in an external database. If it tracks conversation state, it might do so via a Python list of past messages or a simple cache, which exists only temporarily. This means GP_b_git may not “remember” the user’s preferences or facts across separate runs. For example, if a user tells GP_b their name or some personal detail, GP_b might only remember it until the context limit is reached or the session ends.

    No Advanced Memory Augmentation: There is likely no automated summarization or knowledge extraction happening in GP_b_git’s current form. We see no indication of a module that picks out key facts or summarizes old conversations. GP_b_git’s responses are probably generated solely from the immediate prompt (recent chat turns plus maybe a static system prompt) without referencing a long-term knowledge base.

    Simpler Architecture: The GP_b_git app might be a standalone chatbot (perhaps a single-agent system) without the multi-agent orchestration found in amm-production. If so, it might not have a built-in concept of multiple tools or a memory manager. Instead, it would have a straightforward loop: take user input → feed along with recent history to the model → return output. This straightforward design would explain the absence of the sophisticated memory components identified in amm-production.

In summary, GP_b_git’s memory system is likely limited to short-term memory, lacking the persistent, augmented memory capabilities of the amm-production system. This sets the stage for significant improvement by introducing the memory components from amm-production.
Integrating amm-production Memory Components into GP_b_git

There is a clear opportunity to inject the advanced memory functionality from amm-production-bld-20250520 into GP_b_git. The integration can be mapped component-by-component, aligning each memory feature with GP_b_git’s architecture:

    Persistent Memory Database: Incorporate the MemoryDb backend into GP_b_git. This involves setting up a database (SQLite for simplicity, or PostgreSQL for more robust use) and using the SqliteMemoryDb or PostgresMemoryDb class from amm-production within GP_b. By doing so, GP_b_git can save user memories (important facts, preferences, context) to a file or DB table persistently. For example, GP_b could initialize a memory_db = SqliteMemoryDb(table_name="user_memories", db_file="gp_memory.db") and then use a Memory instance with that DB. This mirrors the pattern used in amm-production where a Memory is tied to a persistent store
    Google Drive
    . The result is that GP_b_git would no longer forget everything on restart – it could query this database on startup or before each response to retrieve relevant past information.

    Memory Class Integration: Introduce the Memory class from amm-production into GP_b’s workflow. In practice, GP_b_git’s code that handles a new user query can be extended to call memory.get_user_memories(user_id) to fetch any stored memories relevant to the query or user. Those memories can then be injected into the prompt (e.g., as additional system instructions or context text) so that the AI’s response can reference past details. Likewise, after generating a response, GP_b can call memory.add_user_memory or memory.create_user_memories to store new facts gleaned from the interaction. Essentially, GP_b_git would gain a read-write interface to long-term memory using the imported Memory API.

    Agent Architecture Alignment: If GP_b_git is currently a simple single-agent, we might adapt it to use the same Agent abstraction used in amm-production (if the code is available). For instance, GP_b could be refactored as an Agent with a specified model and the newly integrated memory object. Setting agent = Agent(model=..., memory=memory, storage=...) similar to how memory_agent is defined
    Google Drive
    would quickly plug in memory and even allow session logging. This agent would then automatically utilize the memory when generating responses (since the Agent class in amm-production likely handles injecting memory context when present). If reworking GP_b into an Agent is too intrusive, an alternative is to manually manage memory calls as described above, but aligning with the Agent/Memory design pattern would yield cleaner integration.

    MemoryManager and Automated Capture: To fully leverage memory augmentation, GP_b_git can incorporate the MemoryManager to automate the capture of new memories. After GP_b produces an answer to the user, the conversation (or the latest user message and answer) can be passed to MemoryManager which uses an LLM to distill key points. Those points would then be stored via the Memory object. For example, if the user says “I just moved to Paris and started a new job.”, the MemoryManager might extract “User has relocated to Paris” and “User began a new job” as discrete memory entries. By hooking this into GP_b’s response cycle (e.g., as a post-processing step whenever enable_user_memories is configured), we ensure GP_b’s memory grows automatically without developer manually adding each item. In code, this could mirror the enable_user_memories=True configuration used in amm-production where the system either lets the agent self-update memory or calls MemoryManager after each response
    Google Drive
    .

    Session Summarization for GP_b: Over long usage, even the persistent memory DB can grow large. Integrating the SessionSummarizer would allow GP_b_git to periodically summarize older conversations or a series of memory items into a concise note. GP_b could, for instance, trigger the summarizer at the end of a chat session or when the memory DB hits a size threshold. The summary would be saved as a special memory entry (perhaps tagged as a summary), and older granular entries could be archived or pruned. This keeps GP_b’s memory relevant and manageable over time, preventing infinite accumulation.

    Multi-turn History Storage: Borrow the AgentStorage concept to record dialogue history for GP_b. Even if GP_b is user-facing and might not need to replay its transcripts, having a log of interactions in a database table (with a session or user ID) can be valuable. It enables the MemoryManager or developers to review past conversations, and can aid in memory retrieval (the system could look up context from previous sessions if needed). Implementing this means adding a storage = SqliteStorage(table_name="gp_sessions", db_file="gp_memory.db") and logging each user/assistant message pair to it. This is analogous to how amm-production logs agent conversations for teams and agents
    Google Drive
    Google Drive
    . While not absolutely required for memory functionality, it complements the memory system and aligns GP_b with a consistent design pattern used in the other repository.

Through these integrations, GP_b_git would evolve from a stateless or short-term memory bot into one with a rich, persistent memory subsystem. Essentially, GP_b would start “remembering” user information across sessions, recalling relevant facts to personalize responses, and maintaining a knowledge base of its interactions.
Proposed Enhancements to GP_b_git’s Memory System

By leveraging the above components, several concrete enhancements can be made to GP_b_git’s capabilities:

    Long-Term User Memory: GP_b_git will be able to retain information about users (name, preferences, facts mentioned) indefinitely. For example, if a user tells GP_b about their birthday or favorite food, that fact can be stored and recalled in future conversations without needing repetition. This persistent user profile memory greatly personalizes and contextualizes the chatbot’s answers
    Google Drive
    Google Drive
    .

    Context Carryover Across Sessions: Currently, ending a session likely erases context. With a persistent memory DB, GP_b can start a new session already “knowing” what was discussed previously. A user could continue a conversation hours or days later, and GP_b_git could reference earlier topics (“As we talked about yesterday, you were preparing for a job interview…”). This creates a more continuous and coherent user experience.

    Automated Knowledge Extraction: Using MemoryManager, GP_b_git can automatically distill important pieces of each conversation and store them. This means over time GP_b builds up a knowledge base of key points without developer intervention. The bot effectively learns from each interaction. It might remember, for instance, a user’s project details from a work-related chat and later use that to give context-aware suggestions.

    Reduced Context Window Load: Rather than sending the entire conversation history to the model (which can be inefficient or hit token limits), GP_b_git can leverage stored memories. Before generating a response, it can fetch only the most relevant memory entries (using semantic search or metadata tags) and include those in the prompt. This provides the necessary context to the model while keeping prompts concise. Summarization of older chats further ensures the prompt stays within limits by replacing long transcripts with short summaries.

    Enhanced Knowledge Integration: The knowledge base components from amm-production could let GP_b ingest documents or facts into its memory. For example, GP_b_git could be enhanced to “remember” an FAQ document or a user-provided text by chunking and storing it as long-term knowledge. Later, if the conversation touches on that document’s content, GP_b can retrieve relevant chunks from memory. This effectively augments GP_b with a form of extendable memory or private knowledge specific to the user’s needs.

    Agentic Memory Updates: With enable_agentic_memory, GP_b’s underlying agent (if adapted to that framework) could autonomously decide to save information during the dialogue. The AI model could be prompted (via system instructions) to output memory-worthy facts in a special format that the system intercepts and stores. This means the AI itself participates in building the memory store (as seen with the memory_agent in amm-production), leading to a more seamless integration between dialogue and memory creation
    Google Drive
    .

    Multi-User Memory Separation: If GP_b_git ever serves multiple users, the memory system can isolate memories per user ID (a feature already present in the Memory schema). Each user would have their own set of stored memories, avoiding any data overlap. This enhancement would allow GP_b to scale to multi-user scenarios (e.g., a group chatbot or an enterprise support bot remembering each client’s context separately) with the robust backing of a database.

Collectively, these enhancements transform GP_b_git from a basic chatbot into a context-aware intelligent agent. The ability to recall past interactions and knowledge means responses can be more informed, personalized, and accurate. Users benefit from not having to repeat information, and the system can tackle more complex, long-running tasks by building on prior knowledge.
Compatibility and Refactoring Considerations

Integrating the memory components is a powerful upgrade, but it comes with technical considerations. To ensure a smooth integration of amm-production modules into GP_b_git, the following compatibility and refactoring issues need to be addressed:

    Language and Environment: Both codebases appear to be in Python (given the import syntax and usage of classes like those from agno.memory). Assuming GP_b_git is also Python-based, direct reuse of classes is feasible. We must ensure that any dependencies required by the memory components (e.g. SQLAlchemy or a specific database driver for Postgres) are installed in the GP_b_git environment. If GP_b was not using a database before, setting up a new database (even a file-based SQLite) and writing connection configurations will be necessary.

    Version Alignment: The memory components (Memory, MemoryManager, etc.) might come from a newer "v2" library (as indicated by agno.memory.v2). If GP_b_git is an older application, its code might not be immediately compatible. We should verify that the Python versions and any framework versions align. Some minor refactoring could be needed if, for instance, GP_b_git uses different data models or expects different call signatures. For example, GP_b might have its own way of handling user IDs or messages that we need to adapt when calling memory.create_user_memories(...).

    Structural Refactoring: If GP_b_git was not originally designed with an object-oriented Agent in mind, we may need to refactor its architecture to accommodate the Memory integration. This could mean: introducing a concept of User or Session ID in GP_b (to index memories), ensuring each user message and assistant response is accessible to the memory system, and possibly restructuring the main loop to call memory retrieval and storage at the right times. Adopting design patterns from amm-production (like separating an Agent class, using dependency injection for memory) could lead to cleaner integration but may require non-trivial code changes in GP_b’s core.

    Name and Namespace Conflicts: The amm-production code seems to assume certain package names (e.g., agno.memory). When integrating, we should either include that package in GP_b or transplant the relevant classes into GP_b_git’s codebase. Care must be taken to avoid naming conflicts with existing GP_b components. For example, if GP_b already has a class named Memory or a different concept of “memory”, we might need to alias the imported Memory class or clearly delineate its usage.

    Database Schema Compatibility: Using the memory store means introducing new data tables (like user_memories, agent_sessions) into GP_b’s world. If GP_b_git uses any existing database or storage, we should integrate or migrate accordingly. In case GP_b had its own simpler storage (like JSON or flat files), a decision is needed whether to run both in parallel (likely not) or convert entirely to the new database-backed approach. We should also consider any data migration – if GP_b has historical data we want to preserve, we’d need to import it into the new memory database.

    Performance Impact: Storing and querying memory introduces overhead. We must ensure that each user query in GP_b doesn’t suffer noticeable latency from DB lookups or memory generation. In practice, the overhead of a few SQL queries is minimal, but if the MemoryManager is used, that involves an additional LLM call to summarize or extract memories. We might schedule heavy operations (like summarization) during idle times or after sending the main response to the user, so as not to delay the responsiveness. Caching strategies could also be applied (e.g., caching recent memory retrieval results in-memory for quick reuse within a session).

    Security and Privacy: With persistent memory, GP_b_git will start accumulating potentially sensitive user data. It’s crucial to handle this data carefully – ensure the database is secure, access to memory entries is properly restricted per user, and possibly provide users a way to erase their stored data (which the Memory class supports via clear() or delete functions
    Google Drive
    ). This is especially important if GP_b is a user-facing product with privacy considerations.

    Testing and Alignment: Once integrated, thorough testing is needed to guarantee that GP_b_git’s existing functionality isn’t broken. The chatbot’s responses should improve with memory, but we must verify that it doesn’t introduce confusion (e.g., recalling wrong user info due to an ID mix-up). We should also test edge cases: what if the memory database is empty, or if there are many memories (does the prompt overflow?), or if the user explicitly corrects a fact (the system should update or invalidate the old memory). Such scenarios will guide minor adjustments in how we use the memory components (perhaps adding functions to update or delete specific memories when needed).

Addressing these considerations will likely require some refactoring effort, but none appear insurmountable. The memory subsystem was designed to be a drop-in enhancement, and with careful alignment of design patterns and thorough testing, GP_b_git can smoothly adopt these features.
Conclusion

Integrating the memory structures from amm-production-bld-20250520 into the GP_b_git application promises to significantly enhance its intelligence and user experience. The amm-production repository provides a proven blueprint for long-term memory in AI agents: a combination of persistent storage, automated memory extraction, and integration into the agent’s reasoning loop. By adopting components like the Memory class with a database backend, GP_b_git can transform from a stateless chatbot into a learning entity that accumulates knowledge over time.

In this analysis, we outlined how GP_b_git’s current simplistic memory (limited to ephemeral context) can be augmented with persistent user memory, session logging, and summarization. We mapped specific components (Memory DBs, MemoryManager, etc.) to new responsibilities in GP_b_git. We also highlighted the need for alignment in design and careful refactoring – ensuring that the integration does not disrupt GP_b’s operation, but rather enriches it.

With these changes, GP_b_git could, for example, greet a returning user with “Welcome back!” using details from their last visit, or provide answers that consider information the user shared weeks ago. It could also maintain a knowledge base of reference material for the user’s domain, effectively serving as an extended memory or personal assistant. The fusion of GP_b_git’s functionality with amm-production’s memory architecture would yield a more powerful hybrid system: one that combines GP_b’s original capabilities with the robust, human-like memory of the amm framework – leading to more coherent, context-aware, and helpful interactions.

Overall, this integration is a strategic improvement that aligns with modern AI assistant design, and with careful implementation, GP_b_git can achieve a new level of sophistication in handling long-term knowledge and context for its users.

Sources:

    Code excerpts from amm-production-bld-20250520 repository (Google Drive) showing memory component usage
    Google Drive
    Google Drive
    . These illustrate the integration of a persistent Memory database and model in the agent setup.

    Configuration of agents and teams in amm-production demonstrating how memory and storage are attached to AI agents
    Google Drive
    Google Drive
    .

    Example of MemoryAgent usage and memory creation in the amm-production demo, confirming the ability to store and retrieve user facts in a database
    Google Drive
    Google Drive
    .

    Directory and module listings from the repository indicating the presence of memory management, summarization, and knowledge integration components

# Memory Integration for GP\_b\_git – Product Requirements Document (PRD)

## 1  Purpose

Enable persistent, context‑aware conversation in **GP\_b\_git** by integrating the Amm–production memory subsystem (`Memory`, `MemoryManager`, `SessionSummarizer`, `AgentStorage`).

## 2  Background & Problem Statement

* **Current state:** GP\_b\_git only keeps in‑session chat history; all user context is lost on restart.
* **Opportunity:** Amm‑production‑bld‑20250520 provides modular, database‑backed long‑term memory, auto‑extraction of salient facts, session summarisation, and agent storage.

## 3  Goals & Success Metrics

| Goal                              | Metric                                              | Target             |
| --------------------------------- | --------------------------------------------------- | ------------------ |
| Recall user facts across sessions | % of factual follow‑up questions answered correctly | ≥ 90 %             |
| Control prompt size               | Avg. tokens per prompt                              | − 25 % vs baseline |
| Performance                       | P95 latency increase                                | ≤ 250 ms           |
| Privacy compliance                | GDPR/CCPA deletion workflow                         | Implemented        |

## 4  Personas

* **End User** – Converses with GP\_b; expects continuity.
* **Developer** – Maintains code; integrates memory modules.
* **DevOps/Admin** – Deploys DB, monitors performance and privacy.

## 5  Scope

**In‑scope**

1. Integrate Amm `Memory` with SQLite (dev) & Postgres (prod).
2. Automated Memory extraction & storage (`MemoryManager`).
3. Session summarisation (`SessionSummarizer`) to prevent token bloat.
4. CRUD admin endpoints for memories (export, delete).
5. CI/CD, tests, docs, observability.

**Out‑of‑scope**

* LLM fine‑tuning.
* UI/UX redesign.

## 6  Functional Requirements (FR)

| ID   | Requirement                                                           |
| ---- | --------------------------------------------------------------------- |
| FR‑1 | Store user‑specific memories in persistent DB.                        |
| FR‑2 | Retrieve top‑N relevant memories per request via semantic search.     |
| FR‑3 | Auto‑extract memories from chat using `MemoryManager`.                |
| FR‑4 | Summarise sessions ≥ 20 turns or aged > 24 h via `SessionSummarizer`. |
| FR‑5 | Expose admin API to list, delete, or export memories by user\_id.     |
| FR‑6 | Respect user opt‑out / forget‑me requests (GDPR).                     |

## 7  Non‑Functional Requirements (NFR)

* **Security:** TLS for DB, encryption at rest; role‑based access.
* **Scalability:** ≥ 1 M memory rows; 100 req/s concurrent retrieval.
* **Reliability:** ≥ 99.9 % uptime; automated DB backups.
* **Observability:** Structured logs, Prometheus metrics (`memory_entries_total`, `memory_lookup_latency_ms`).

## 8  Assumptions & Dependencies

* Unique `user_id` available at runtime.
* Python ≥ 3.13; Amm‑memory v2.\* library.
* Database: Postgres 15 (prod) / SQLite (local dev).
* OpenAI or local embedding model available for semantic search.

## 9  Milestones & Timeline

| Phase       | Deliverables                            | Duration |
| ----------- | --------------------------------------- | -------- |
| Design      | Architecture diagram, PRD sign‑off      | 1 d      |
| Setup       | DB schema, env config, dep install      | 1 d      |
| Coding      | Memory API wrapper, integration hooks   | 3 d      |
| Testing     | Unit, integration, load, security tests | 2 d      |
| Deploy      | DB migration, canary, full rollout      | 1 d      |
| Post‑Launch | Metrics review, tuning                  | 1 d      |

## 10  Risks & Mitigations

| Risk                                      | Impact             | Mitigation                                              |
| ----------------------------------------- | ------------------ | ------------------------------------------------------- |
| Token bloat if too many memories injected | High cost, latency | Cap `max_memories_per_prompt`; summarise older entries. |
| Privacy breaches via stored data          | Legal exposure     | Encrypt DB, implement deletion API, access controls.    |
| Schema mismatch with future Amm releases  | Upgrade friction   | Pin Amm versions, add integration tests.                |

## 11  Open Questions

1. Should we allow user‑editable memories?
2. Preferred scheduler for summarisation jobs (Celery vs APScheduler)?
3. Will multi‑tenant mode be required at launch or future phase?

---

*Document version 1.0 – 2025‑06‑07*

# Build Guide & Checklist – Amm Memory Integration into GP\_b\_git

---

## 0. Prerequisites

* Python 3.13
* **Amm‑memory** library v2.\* (from amm‑production‑bld‑20250520)
* Database

  * SQLite (⇢ `gp_memory.db`) for local/dev
  * PostgreSQL 15 for staging/production
* OpenAI / Ollama embedding & LLM keys

## 1. Environment Setup

* `pip install agno-memory==2.* sqlalchemy psycopg2-binary apscheduler python-dotenv`
* Append to `requirements.txt` and commit.
* Add to `.env` (or Kubernetes secret):

  ```dotenv
  MEMORY_DB_URL=sqlite:///gp_memory.db  # or postgres://user:pass@host:5432/gp_memory
  OPENAI_API_KEY=sk-...
  EMBEDDING_MODEL=text-embedding-3-large
  SUMMARY_MODEL=gpt-4o-mini
  ```

## 2. Database Initialisation

| Step             | SQLite                            | Postgres                                 |
| ---------------- | --------------------------------- | ---------------------------------------- |
| Create file / DB | `touch gp_memory.db`              | `createdb gp_memory`                     |
| Run schema       | `python scripts/create_schema.py` | `psql -d gp_memory -f sql/schema_pg.sql` |
| Verify tables    | `sqlite3 gp_memory.db ".tables"`  | `\dt` in psql                            |

Tables required:

* `user_memories`
* `agent_sessions`

> **Tip:** Use Alembic for migrations in prod.

## 3. Codebase Changes

1. **Create wrapper** `gp_b_git/memory.py`:

   ```python
   from agno.memory.v2 import Memory, SqliteMemoryDb
   memory_db = SqliteMemoryDb(table_name="user_memories", db_file="gp_memory.db")
   memory = Memory(model="gpt-4o-mini", memory_db=memory_db)
   ```
2. **Integrate in chat loop** (`main.py`):

   ```python
   memories = memory.get_user_memories(user_id, limit=5)
   prompt = build_prompt(memories, chat_history, user_msg)
   assistant_msg = llm(prompt)
   chat_history.append((user_msg, assistant_msg))
   memory.create_user_memories(user_id, chat_history[-2:])
   ```
3. **Optional** – Refactor GP\_b into `Agent` class:

   ```python
   agent = Agent(model=llm, memory=memory, storage=SqliteStorage(...))
   response = agent.chat(user_msg)
   ```

## 4. MemoryManager & Summarisation Jobs

* **Install APScheduler** or Celery.
* Create `jobs/memory_tasks.py`:

  ```python
  from agno.memory.v2 import MemoryManager, SessionSummarizer
  mem_mgr = MemoryManager(memory)
  summarizer = SessionSummarizer(model="gpt-4o-mini")

  def process_turn(user_id, turn):
      mem_mgr.extract_and_store(user_id, turn)

  def nightly_session_summaries():
      for session in list_old_sessions():
          summ = summarizer.summarize(session.transcript)
          memory.create_user_memories(session.user_id, summ)
  ```
* Schedule:

  ```cron
  # Every night at 03:00
  0 3 * * * python -m jobs.memory_tasks nightly_session_summaries
  ```

## 5. Config File

Create `config/memory.yml`:

```yaml
db_url: ${MEMORY_DB_URL}
embedding_model: text-embedding-3-large
summary_model: gpt-4o-mini
max_memories_per_prompt: 5
enable_user_memories: true
session_summary_after_turns: 20
```

## 6. Testing

* **Unit Tests**

  * `tests/test_memory_storage.py` – write & retrieve memory.
  * `tests/test_memory_manager.py` – extraction accuracy.
* **Integration Tests**

  * Simulate two sessions; assert recall of session#1 facts.
* **Load Test**

  * 500 concurrent chat sessions for 10 min using Locust; monitor latency.

## 7. CI/CD Pipeline

* Add migration step: `alembic upgrade head`.
* Run test suite on `push`.
* Build Docker image with Postgres client libs.

## 8. Security & Compliance

* Use parameterised queries; no raw SQL.
* Encrypt At‑Rest (Postgres `pgcrypto` or volume encryption; SQLite with `sqlcipher`).
* Implement `/memories/<id>` DELETE route for GDPR.
* Document data retention policy (default 365 days, configurable).

## 9. Observability

* Add Prometheus counters:

  * `memory_total_entries`
  * `memory_retrieval_duration_seconds`
* Grafana dashboard panels.
* Log examples (`json`): `{level: "INFO", event: "memory_saved", user_id: "abc"}`

## 10. Rollout

| Stage   | % Users | Duration |
| ------- | ------- | -------- |
| Canary  | 10 %    | 24 h     |
| Ramp‑up | 50 %    | 48 h     |
| Global  | 100 %   | —        |

Rollback: toggle `ENABLE_MEMORY=false` in env.

## 11. Post‑Launch Checklist

* ☐ Review Prometheus alerts
* ☐ Survey 10 pilot users on memory accuracy
* ☐ Trim old memories via `summarizer` if DB > 5 GB
* ☐ Schedule quarterly security audit

---

*Checklist version 1.0 – 2025‑06‑07*


Detailed Options to Combine Thousand Questions, GP_b_git, and AMM Memory into a Sentient-AI Simulation

(choose one or mix-and-match elements)
#	Architectural Option	Core Idea	Key Components & Flow	Strengths	Trade-offs / Risks
1	Mono-Agent + Shared Memory	Extend the existing single GP_b agent so it does everything: asks the 15–50 sample questions, builds a personality profile, and autogenerates the remaining 950+ answers—while persisting all facts in the new AMM memory tables.	1. Reuse current agent = Agent(model, memory, storage) pattern. 2. Add a Question Orchestrator class that:
a. pulls a stratified subset from Thousand_Questions DB.
b. stores user answers via Memory.create_user_memories.
c. calls a ProfileBuilder (LLM prompt) to infer Big-Five traits.
d. loops over unanswered questions, injecting traits + prior answers into prompts.
3. Save each AI answer as memory for future consistency checks.	Fastest path—minimal refactor, leverages existing Build Guide; easy to deploy in one container.	Large prompts may bloat tokens; single agent can become a bottleneck; consistency logic lives in one place—harder to debug/scale later.
2	Tri-Agent Personality Pipeline	Split responsibilities across Profiler Agent, Narrative Agent, and Validator Agent under the AMM Team class.	1. Profiler Agent: after 15–50 answers, extracts trait vector + writes to memory.
2. Narrative Agent: generates chapterized story + fills unanswered questions, reading traits from memory.
3. Validator Agent: runs in parallel; for each generated answer it checks coherence vs. stored memories (scoring via MemoryManager.consistency_score) and flags low-score answers for regen.
4. Team orchestrator aggregates results and returns final corpus.	Clear separation of concerns; easy to hot-swap better models per task; Validator gives automatic quality gate.	Requires adopting AMM Team orchestration APIs; inter-agent chatter means more DB reads/writes → latency; higher hosting cost.
3	Hybrid Retrieval-Augmented Generation (RAG)	Treat every user answer as an indexed memory chunk; future prompts retrieve the k most similar memories + trait profile to guide generation.	1. Enable memory.enable_vector_index = True (Amm supports FAISS or PGvector).
2. When Narrative Agent answers question Qx, it calls memory.search(user_id, themes_of_Qx, top_k=5) to pull semantically related prior answers.
3. Prompt includes: traits + top_k memories + current question ⇒ response.	Keeps each prompt under token limits; leverages retrieval for high coherence; easy to tune k and similarity metric.	Requires embedding model & vector DB; retrieval quality directly affects answer quality; need back-off if few matches.
4	Archetype Pre-Seed + Personal Drift	Start from one of several pre-authored “seed personas” (archetypes) to answer 1000 Q’s instantly, then overwrite or drift answers as user supplies real data.	1. Ship a seed_answers.json for e.g. Scholar, Adventurer, Caregiver, Visionary.
2. Profiler maps early user answers to nearest seed via cosine similarity on embedding space.
3. Copy seed answers into memory; mark them “tentative”.
4. As user adds answers, run Revision Agent to patch deviations, updating memory row version.	Very fast complete profile (0 cold-start latency); gives users an immediate “sentient self” to interact with.	Risk of mismatch if seed far from user; complex diff/merge logic; intellectual honesty of “assumed” memories must be transparent.
5	Graph-Backed Consistency Engine	Model every question & answer as nodes/edges in a Neo4j (or PG graph extension); use graph-rules to enforce global coherence.	1. ETL Thousand Questions into nodes (Question, Category, Theme).
2. Answers stored as (:Answer)-[:RESPONDS_TO]->(:Question) with traits props.
3. Consistency rules (Cypher or Datalog) highlight contradictions (e.g., two answers on loyalty conflict).
4. A Consistency-Fix Agent iterates over flagged subgraphs and regenerates lowest-confidence answers.	Strong global consistency guarantees; enables rich analytics & visual inspections; future knowledge-graph reasoning.	Adds second persistence layer beyond AMM memory; higher complexity & ops burden; LLM ↔ graph mapping code non-trivial.
6	Offline Pre-Compute + Real-Time Refinement	Run heavy generation offline (batch job) when user finishes sample; store all 1000 answers to memory. Real-time chat only refines specific answers on demand.	1. Trigger BatchGenerator (could be serverless) once sample complete.
2. Batch job streams answers into DB; attaches confidence metrics.
3. During conversation, if user views/edits a topic, invalidate & queue regeneration only for that cluster.
4. Summaries of clusters stored in SessionSummarizer for prompt efficiency.	Stable latency in chat; heavy GPU cost moves to cheaper batch hours; scalable for many users.	Perceived delay after sample; needs job orchestration (Celery/K8s CronJobs); must sync batch updates with live memory safely.
7	Agentic Evolution Mode (“Living Persona”)	Let the AI keep learning new memories post-1000 answers, using AMM’s autonomous memory update hooks.	1. Enable add_memory_references=True for agent output.
2. Configure MemoryManager to extract new facts from every future chat turn (<em>ex vita sentientia</em>).
3. Schedule weekly Persona-Drift Job to re-run Profiler & update trait weights based on accumulated memories.
4. Present change-log to user for transparency.	Dynamic, ever-evolving “sentient” feel; user sees growth over time.	Risk of personality drift beyond initial coherence; must expose revision controls & versioning to user; heavier long-term storage.

# **Comprehensive Implementation Blueprint – Options 1, 2, 3, 4**

> **Version 2.0 – 2025‑06‑07**   (fully supersedes v0.1)
>
> *This master document lays out exhaustive technical guidance to realise the four architectural variants for combining* **Thousand Questions (TQ)**, **GP\_b\_git**, *and* **AMM Memory**. It is designed to be self‑sufficient: a senior engineer should be able to implement any option strictly from the material herein.\*

---

## 0  Global Foundations (Shared by All Options)

| Layer                 | Decision                                                                  | Rationale                                                                      |
| --------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Programming Lang.** |  Python ≥ 3.13                                                            | aligns with GP\_b, Amm memory, async features                                  |
| **Package Manager**   | `poetry`                                                                  | lockfile reproducibility, extras groups per option                             |
| **Host OS**           |  Ubuntu 22.04 LTS containers                                              | glibc ≥ 2.35 required by PGVector; stable long‑term support                    |
| **Database**          |  PostgreSQL 15 + `pgvector` extension  (fallback SQLite + FAISS for dev)  | single poly‑store; strong ACID; vector similarity; supports Amm Storage tables |
| **LLM Provider(s)**   |  OpenAI ( `gpt-4o-mini` for prod), Local Ollama (`phi-3`) for offline dev | trade cost vs performance                                                      |
| **Embeddings**        |  `text-embedding-3-large` 1536‑dim                                        | consistent cross‑option retrieval                                              |
| **Containerisation**  |  Docker + docker‑compose; Helm charts (prod)                              | uniform Ops pipeline                                                           |
| **CI/CD**             |  GitHub Actions + ArgoCD                                                  | test & deploy per option branch                                                |

### 0.1 Directory Layout (monorepo)

```
repo/
├─ apps/
│   ├─ gp_b_core/               # existing chatbot
│   ├─ tq_api/                  # shared FastAPI micro‑service for Thousand Questions
│   ├─ option1_mono_agent/
│   ├─ option2_tri_agents/
│   ├─ option3_rag/
│   └─ option4_archetype/
├─ libs/
│   ├─ amm_memory_adapter/      # thin wrappers, DB migrations
│   ├─ persona_traits/          # profiling + Big‑Five utils
│   └─ tq_dataset/              # dataset parser + ORM models
├─ infrastructure/
│   ├─ docker/
│   ├─ helm/
│   └─ terraform/
└─ docs/                        # PRDs, ADRs, diagrams
```

### 0.2 Core Database Schema Additions

```sql
CREATE TABLE public.tq_questions (
    id            text PRIMARY KEY,
    text          text NOT NULL,
    category      text,
    themes        text[],
    complexity    smallint,
    related_ids   text[]
);

CREATE TABLE public.tq_answers (
    user_id       uuid,
    question_id   text REFERENCES tq_questions(id),
    answer_text   text,
    is_user_answer boolean,
    confidence    numeric(3,2),
    version       integer DEFAULT 1,
    created_at    timestamptz DEFAULT now(),
    PRIMARY KEY  (user_id, question_id, version)
);

CREATE TABLE public.user_profiles (
    user_id       uuid PRIMARY KEY,
    traits        jsonb,          -- Big Five & others
    seed_persona  text,           -- option 4
    seed_score    numeric(3,2),
    updated_at    timestamptz
);
```

*Liquibase* changelog provided under `infrastructure/db/changelog.yaml`.

### 0.3 Shared Pydantic Models

```python
class TraitVector(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

class TQQuestion(BaseModel):
    id: str
    text: str
    category: str
    themes: list[str]
    complexity: int
    related_ids: list[str]
```

---

## 1  Option 1 – Mono‑Agent + Shared Memory *(“Fast Track”)*

### 1.1 Sequence of Operations

```mermaid
sequenceDiagram
    participant U as User
    participant UI as UI Frontend
    participant SA as SentientAgent
    participant MEM as AMM‑Memory (PG)
    participant DB as tq_questions / tq_answers

    U->>UI: begin narrative
    UI->>SA: request sample questions
    SA->>DB: SELECT stratified subset
    SA-->>UI: list 15‑50 questions
    U->>UI: answers
    UI->>SA: submit answer batch
    SA->>MEM: create_user_memories()
    SA->>DB: INSERT tq_answers (is_user=true)
    SA->>SA: build_persona()
    SA->>MEM: store traits JSON
    Note over SA: iterate all unanswered 950+
    SA->>MEM: search top‑K memories (fast retrieval)
    SA->>SA: prompt & generate answer
    SA->>DB: INSERT tq_answers (is_user=false)
    SA-->>UI: full corpus delivered
```

### 1.2 Detailed Module Specs

| Module              | Path                                  | Key Classes / Functions                                                                    |
| ------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------ |
| **SentientAgent**   | `option1_mono_agent/agent.py`         | `run_sentience_setup()`, `ask_sample_questions()`, `build_persona()`, `answer_remaining()` |
| **QuestionSampler** | `libs/tq_dataset/sampler.py`          | `sample_questions(user_id, n)` – stratified, complexity‑weighted                           |
| **ProfileBuilder**  | `libs/persona_traits/builder.py`      | `extract_traits(answers) -> TraitVector` (OpenAI function‑calling)                         |
| **PromptTemplates** | `option1_mono_agent/prompts/*.jinja2` | `mono_agent.jinja2`, `persona_summary.jinja2`                                              |
| **Jobs**            | `option1_mono_agent/jobs/`            | `retrofill_missing.py`, `reindex_embeddings.py`                                            |

### 1.3 LLM Prompt Anatomy (`mono_agent.jinja2`)

```
SYSTEM:
You are **SentientAgent**, tasked with answering life’s thousand introspective questions as a coherent persona.

TRAITS:
{{ traits.pretty() }}

CONTEXT MEMORIES:
{% for m in memories %}• {{ m.content }} ({{m.created_at|datetime}})
{% endfor %}

CURRENT QUESTION ({{ question.id }} – {{ question.category }}): "{{ question.text }}"

GUIDELINES:
1. Maintain consistency with TRAITS and CONTEXT.
2. Depth ≥ 3 paragraphs for complexity >3.
3. Use first‑person singular.
4. Express emotional tone aligned with category {{ question.category }}.
```

### 1.4 Performance Budgets

| KPI                        | Target                         | Measurement Method                 |
| -------------------------- | ------------------------------ | ---------------------------------- |
| **Cold‑start Sample Flow** |  < 8 s total LLM time for 50 Q | bench script `perf/sample_flow.py` |
| **Gen per Remaining Q**    |  ≤ 1.1 s avg                   | concurrency test 100 parallel Q’s  |
| **DB TPS**                 |  ≥ 500 writes/s peak           | pgbench + locust                   |

### 1.5 Edge‑Case Handling

| Case                           | Strategy                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| User skips a question          | mark `answer_text=NULL, is_user_answer=true`; still feed to profiler (treated as “no data”) |
| Profiler low confidence (<0.6) | fallback to archetype (Option 4) or request more sample Q’s                                 |

### 1.6 Deployment Manifest (Docker‑Compose Excerpt)

```yaml
services:
  option1:
    build: apps/option1_mono_agent
    environment:
      DATABASE_URL: ${DATABASE_URL}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - postgres
  postgres:
    image: pgvector/postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: pass
```

### 1.7 Acceptance Test Checklist

1. ✅  Create new user → UI displays 30 sample questions chosen across ≥10 categories.
2. ✅  Complete sample → LLM traits stored row in `user_profiles` (json length 5).
3. ✅  `tq_answers` table contains 1000 rows after autobackfill.
4. ✅  Subsequent chat query references at least one user answer.

---

## 2  Option 2 – Tri‑Agent Personality Pipeline *(“Quality Split”)*

### 2.1 Component Map

```mermaid
graph TD
   subgraph AMM Team
      P(ProfilerAgent)
      N(NarrativeAgent)
      V(ValidatorAgent)
   end
   UI-->P
   MEM-. shared .->P & N & V
   DB-->N
   N-->|draft answers|V
   V-->|approve + store|MEM & DB
```

### 2.2 Agent Responsibilities

| Agent              | LLM Model             | Input                              | Output             | Memory Write           | Special Flags                 |
| ------------------ | --------------------- | ---------------------------------- | ------------------ | ---------------------- | ----------------------------- |
| **ProfilerAgent**  | `gpt-4o-mini`         | user sample answers                | `TraitVector` json | `user_profiles.traits` | `enable_agentic_memory=true`  |
| **NarrativeAgent** | `gpt-4o-mini`         | question + traits + top‑K memories | answer\_text       | `tq_answers` row       | `enable_agentic_memory=true`  |
| **ValidatorAgent** | `gpt-4o-mini` (low‑T) | answer draft + memories + traits   | score, rationale   | none (unless patch)    | `enable_agentic_memory=false` |

### 2.3 Event Flow

1. \`\` → emitted by Profiler; Team router directs pending TQ’s to Narrative.
2. Narrative streams responses in batches of 20; each batch triggers `answers_batch` event.
3. Validator processes batch; for each answer returns `consistency_score` & `confidence`.
4. If any score <0.7 → router sends `regenerate` to Narrative with constraints.
5. On pass: answers persisted; UI progress bar updated via websocket.

### 2.4 Additional Python Packages

```toml
[tool.poetry.dependencies]
redis = "^5.0"
fastapi-websocket = "^0.12"
```

### 2.5 Redis Stream Topology

| Stream              | Producer  | Consumer(s)  |
| ------------------- | --------- | ------------ |
| `profile_ready`     | Profiler  | Team Router  |
| `answers_batch`     | Narrative | Validator    |
| `validated_answers` | Validator | DB persister |

### 2.6 Validator Logic Snippet

```python
async def validate_batch(answers: list[DraftAnswer], traits: TraitVector):
    for ans in answers:
        rel = memory.search(user_id, query=ans.themes, top_k=3)
        prompt = validator_prompt(ans, traits, rel)
        judgement = await llm(prompt, temperature=0.2)
        score = float(judgement["consistency_score"])
        if score < 0.7:
            yield RegenerationRequest(ans)
        else:
            yield ApprovedAnswer(ans.text, score)
```

### 2.7 SLI/SLO Targets (per‑agent)

| Metric      | Profiler | Narrative | Validator |
| ----------- | -------- | --------- | --------- |
| p95 latency | ≤ 400 ms | ≤ 1 s     | ≤ 600 ms  |
| error rate  | < 1 %    | < 2 %     | < 1 %     |

### 2.8 Kubernetes Helm Overlay (`helm/option2/values.yaml`)

* 3 separate Deployments with HPA on CPU≥70 %.
* `redis-cluster` chart dependency.
* Grafana dashboards imported from `infra/monitoring/option2.json`.

---

## 3  Option 3 – Hybrid RAG Retrieval *(“Token Efficient”)*

### 3.1 Vector Layer Implementation

| Component                      | Tech                         | Config                                  |
| ------------------------------ | ---------------------------- | --------------------------------------- |
| `pgvector` ext                 | Postgres                     |  768‑dim, cosine, HNSW `lists=100`      |
| `embedding_service`            | FastAPI microservice wrapper | async pooling; batch upsert 256 vectors |
| `memory.enable_vector_index()` | Amm Memory hook              | `distance="cosine"`, `use_hnsw=True`    |

### 3.2 Retrieval Algorithm

```
func retrieve_memories(user_id, question):
    query_vec ← embed(question.text)
    return (
        SELECT content, created_at, metadata
        FROM user_memories
        WHERE user_id = :uid
        ORDER BY embedding <=> :query_vec
        LIMIT 5
    )
```

*(uses pgvector ****\`\`**** operator)*

### 3.3 Prompt Budget Calculation

* Base tokens per prompt ≈ 180
* Traits section ≈ 60
* 5 memories × 50 tokens ≈ 250  ➜  **Total ≈ 490**  (<2 k goal)

### 3.4 Fail‑Safe Logic

If `pgvector` downtime:

1. catch `psycopg.OperationalError`; log alert.
2. fallback to text‑search: `ORDER BY similarity(question.text, memory.content) DESC LIMIT 3`.

### 3.5 Re‑Embedding Job

Cron nightly:

```bash
poetry run python libs/amm_memory_adapter/jobs/reembed_old.py --days 7 --model text-embedding-3-large
```

Remaps any memory older than 7 days if embedding model version changed.

---

## 4  Option 4 – Archetype Pre‑Seed + Personal Drift *(“Instant Persona”)*

### 4.1 Archetype Design Guidelines

| Field              | Description                              |
| ------------------ | ---------------------------------------- |
| `persona_id`       | snake\_case identifier                   |
| `narrative_style`  | free text – voice, tone                  |
| `canonical_traits` | Big‑Five vector (float 0‑1)              |
| `answers`          | map question\_id → answer\_text          |
| `creation_notes`   | provenance, author name, dataset licence |

**Authoring Rule‑of‑Thumb**: each answer ≤ 200 tokens; maintain unique voice; ensure internal consistency; mark ambiguous areas with placeholders for drift.

### 4.2 Seed Selection Algorithm

```
► Input: first_n_answers (n=20)
► For each seed persona:
        overlap_ids ← intersection(first_n_answer_ids, seed.answer_ids)
        v_user ← embed(concat(user answers in overlap_ids))
        v_seed ← embed(concat(seed answers in overlap_ids))
        score ← cosine(v_user, v_seed)
► Choose max(score)
```

*Persist* `seed_persona`, `seed_score` in `user_profiles`.

### 4.3 Drift Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Seed
    Seed -->|user answers diverge| Drift
    Drift -->|alignment <0.4| Rebase
    Rebase --> Seed
```

* **Seed**: untouched archetype answers.
* **Drift**: answers overwritten as user expresses personal data; old versions archived in `tq_answer_history` (json diff).
* **Rebase**: switch to new seed persona or Option 3 generation if misalignment.

### 4.4 Data Governance

* Tag each seeded answer `source="seed:{persona_id}"`.
* UI must disclose AI‑fabricated content via tooltip ⚠️.
* Allow user deletion / rewrite at any time.

### 4.5 Artefact Versioning

`seed_personas/` managed separately; CI verifies:

* 100 % question coverage
* no profanity, PII
* SPDX compatible licence

---

## 5  Unified Testing & QA Plan

| Layer           | Tooling                             | Coverage Targets                                             |
| --------------- | ----------------------------------- | ------------------------------------------------------------ |
| **Unit**        | `pytest`, `pytest-asyncio`          | ≥ 85 % lines in libs & agents                                |
| **Integration** | `pytest + testcontainers‑postgres`  | flows: sample→profile→answer, RAG retrieval, archetype match |
| **Load**        | `Locust` scripts per option         | 1 k concurrent users, sustain 5 min                          |
| **E2E UI**      | `Playwright`                        | happy path + edit drift                                      |
| **Security**    | `bandit`, `trivy` container scan    | zero high severity CVEs                                      |
| **Governance**  | `openai_guardrails`, `promptjector` | no disallowed content in generated answers                   |

---

## 6  Execution Roadmap (6‑Week Sprint‑Wise)

| Week | Option 1                           | Option 2                          | Option 3                    | Option 4            | Shared Tasks                        |
| ---- | ---------------------------------- | --------------------------------- | --------------------------- | ------------------- | ----------------------------------- |
|  1   | implement sampler + agent skeleton | architect team config             | enable pgvector ext         | draft 4 archetypes  | dataset parse, Liquibase migrations |
|  2   | profile builder + persona prompt   | ProfilerAgent done                | embedding service container | seed loader script  | set‑up CI, base images              |
|  3   | auto‑answer pipeline               | NarrativeAgent + validator prompt | retrieval & fallback        | seed selection algo | logging, Sentry, Grafana            |
|  4   | UI wiring, perf tests              | event bus & HPA                   | re‑embedding cron           | drift mechanisms    | security hardening                  |
|  5   | QA & load                          | integrated E2E                    | QA                          | QA                  | doc, runbooks                       |
|  6   | Canary deploy                      | Beta user test                    | Beta user test              | Beta user test      | Post‑launch review                  |

---

## 7  Risk Register (Consolidated)

| ID   | Risk                                | Likelihood | Impact | Option(s) | Mitigation                                            |
| ---- | ----------------------------------- | ---------- | ------ | --------- | ----------------------------------------------------- |
|  R‑1 | LLM cost surge                      |  Med       |  High  | all       | real‑time token accounting; nightly batch (Opt 6 alt) |
|  R‑2 | Inconsistent persona                |  Med       |  High  | 1,4       | add validator (option 2 logic) even in option 1       |
|  R‑3 | Vector DB drift                     |  Low       |  Med   | 3         | scheduled re‑embedding, health checks                 |
|  R‑4 | User distrust of fabricated answers |  High      |  High  | 4         | full transparency UI, easy edit, audit trail          |
|  R‑5 | Ops complexity                      |  High      |  Med   | 2         | GitOps, Helm templates, tier‑1 on‑call rotation       |

---

## 8  Decision Matrix (Revisited)

| Criterion           | Weight | Opt 1    | Opt 2   | Opt 3   | Opt 4   |
| ------------------- | ------ | -------- | ------- | ------- | ------- |
| Time‑to‑POC         | 0.3    | **0.9**  | 0.4     | 0.6     | 0.7     |
| Quality / Coherence | 0.3    | 0.6      | **0.9** | 0.8     | 0.7     |
| Token Efficiency    | 0.1    | 0.5      | 0.3     | **0.9** | 0.6     |
| User Wow Factor     | 0.2    | 0.6      | 0.7     | 0.7     | **0.9** |
| Ops Complexity (-)  | 0.1    | **0.8**  | 0.3     | 0.6     | 0.5     |
| **Weighted Score**  | 1.0    | **0.74** | 0.66    | 0.75    | 0.75    |

> *Option 1 edges out for fastest demonstrable success. Options 3 and 4 tie for strategic product differentiation; Option 2 is best for research‑grade consistency.*

---

### Next Actions (choose Path)

1. Select option in **Kick‑off Meeting**.
2. Branch from `main` into `opt‑N‑dev`.
3. Follow week 1 tasks table.
4. Schedule midpoint demo end of week 3.

---

*End of Blueprint v2.0*
