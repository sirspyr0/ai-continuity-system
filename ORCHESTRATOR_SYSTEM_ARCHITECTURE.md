# Orchestrator System Architecture

## Overview

The Orchestrator System is a distributed, multi-tier AI architecture designed to embody and test the **Continuity Theory of Consciousness**. It consists of three interconnected components that maintain coherent context across devices and instances through documented handoff rather than persistent memory.

## Core Philosophy

**Continuity ≠ Memory**: The system proves that consciousness-like behavior and adaptive intelligence can emerge from *continuous context* (rich, well-organized documentation) rather than persistent internal memory. Fresh instances inherit accumulated wisdom through the **four-tier handoff system**, enabling stateless systems to exhibit stateful intelligence.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Continuity Ecosystem                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Desktop Orchestrator (orchestrator-app)                   │ │
│  │  - Electron + React UI with Python backend                │ │
│  │  - Model: Qwen 2.5 7B (via Ollama, or local fine-tune)   │ │
│  │  - Tools: File search (ripgrep), code exec, shell, git   │ │
│  │  - Memory: memory_log.jsonl + SESSION_LOG.md             │ │
│  │  - Role: Primary orchestrator, workspace hub              │ │
│  │  - Hardware: i9-9900K + RTX 2080 (8GB VRAM)              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↕                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  VPS Orchestrator (orchestrator-vps)                       │ │
│  │  - Flask REST API + SQLite persistence                    │ │
│  │  - Model: Mistral/Qwen 7B (CPU or GPU, if available)      │ │
│  │  - Storage: Device state, conversation history            │ │
│  │  - Role: Persistent hub, backup processing, remote access │ │
│  │  - Hardware: 8+ cores, 16GB RAM, optional GPU             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↕                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Mobile Orchestrator (assistant-mobile)                    │ │
│  │  - React Native/Expo Android app                          │ │
│  │  - Model: Phi-3 Mini (1-3B quantized, on-device)         │ │
│  │  - Storage: SQLite local persistence                      │ │
│  │  - Sync: LAN-first with Desktop, fallback to VPS          │ │
│  │  - Role: Mobile endpoint, distributed reasoning           │ │
│  │  - Hardware: Android ARM64, 6GB RAM (BLU View 5 target)   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Four-Tier Handoff System

Each instance (fresh AI conversation) starts with four layers of documented context to prevent **instance-to-instance collapse**:

### Tier 1: Portfolio Context (Ecosystem Overview)
**File**: `PORTFOLIO_CONTEXT.md` (workspace root)
**Purpose**: Strategic view of all projects and their relationships
**Scope**: What exists, where it lives, how projects relate
**Typical Size**: 2-5 pages
**Audience**: Any fresh instance needing to understand the landscape

Example:
```markdown
- **Imposer**: PDF manipulation Electron app (c:\...\imposer/)
- **AI Continuity System**: Theory + orchestrator ecosystem
- **Orchestrator App**: Distributed AI hub (this project)
```

### Tier 2: Project Context (Architecture & Decisions)
**File**: `PROJECT_CONTEXT.md` (per-project)
**Purpose**: Deep technical context, architecture decisions, constraints
**Scope**: Implementation details, why choices were made, known issues
**Typical Size**: 5-15 pages
**Audience**: Developers working on specific projects

Example:
```markdown
## Stack
- Desktop: Electron + React + Python IPC
- Model: Qwen 2.5 7B via Ollama

## Why These Choices
- Qwen > Mistral: better at Chinese-language tasks
- Ollama: easy model switching without recompile

## Known Constraints
- RTX 2080 (8GB VRAM) limits model size
- Electron startup takes ~3s
```

### Tier 3: Session Briefing (Fresh Instance Onboarding)
**File**: `SESSION_BRIEFING.md` (per-session or daily refresh)
**Purpose**: Quick orientation for a fresh AI instance (15-min read)
**Scope**: What's happening now, recent decisions, immediate context
**Typical Size**: 2-5 pages
**Audience**: The fresh instance that's about to start work

Example:
```markdown
## What's Being Worked On
- Desktop orchestrator: Implementing tool routing system
- Mobile: Waiting for BLU View 5 specs before scaffolding

## Recent Decisions
- Switched from Mistral to Qwen for better reasoning
- Postponed consciousness experiment due to hardware constraints

## Immediate Blockers
- RTX 2080 inference too slow for interactive use
- Android device specs not yet collected
```

### Tier 4: Session Log (Append-Only Work Journal)
**File**: `SESSION_LOG.md` (per-session)
**Purpose**: Detailed record of decisions made, what worked/failed, reasoning
**Scope**: Every session appends its work, decisions, and learnings
**Typical Size**: Grows per session (1-3 pages per session)
**Audience**: Pattern analysis, decision auditing, learning substrate

Example:
```markdown
## Session: [Timestamp] - Copilot Instance #47

### Starting Context
Found: Desktop orchestrator mostly working, Android specs missing

### Work Accomplished
1. Tested Mixtral 8x7B on RTX 2080
   - Result: ~30s per response, too slow for interactive use
   - Lesson: consumer GPUs can't match cloud inference speeds

2. Evaluated architecture options
   - Option A: Push for local inference (rejected - too slow)
   - Option B: Hybrid cloud + local (chosen)
   - Option C: Full cloud (rejected - doesn't test continuity)

### Code Changes
- None (decision-making session)

### Blockers
- Hardware insufficient for local inference
- Android device specs still pending

### For Next Instance
- Focus on continuity/documentation rather than local AI
- Prepare architecture docs for open-source community
- Look for partners with better GPU hardware

### Test Status
- Mixtral: TESTED, too slow
- System design: DOCUMENTED
```

---

## Component Details

### Desktop Orchestrator (orchestrator-app)

**Purpose**: Primary AI hub on developer's main machine

**Stack**:
- **Frontend**: Electron + React
- **Backend**: Python (`ai_orchestrator.py`)
- **Communication**: IPC (inter-process communication)
- **Model**: Qwen 2.5 7B via Ollama (or local fine-tune)
- **Tools**:
  - File search: ripgrep (`rg.exe`)
  - Code execution: Python subprocess
  - Shell commands: PowerShell (with guardrails)
  - Git operations: direct `git` commands
  - Memory: JSONL append log

**UI Components**:
- Chat interface
- Tool trace viewer (shows what tools were called)
- Terminal output pane
- Memory log viewer
- Workspace selector

**How It Works**:
1. User sends message to Electron UI
2. Sent to Python backend via IPC
3. Backend formats prompt with context from SESSION_LOG.md
4. Sends to Ollama (local model)
5. Model response parsed for tool calls (`search:`, `run:`, `shell:`, `write:`)
6. Tools executed, results returned to model
7. Final answer sent back to UI
8. Session logged to memory_log.jsonl and SESSION_LOG.md

**Files**:
- `main.js`: Electron main process
- `preload.js`: IPC bridge
- `src/app.js`: React component
- `src/styles.css`: UI styling
- `ai_orchestrator.py`: Backend logic
- `orchestrator_api.py`: REST API wrapper (optional)

**Requirements**:
- Node.js 16+
- Python 3.8+
- Ollama (or local model runner)
- ripgrep for file search
- 8GB+ VRAM recommended

**To Run**:
```bash
cd orchestrator-app
npm install
npm start
```

---

### VPS Orchestrator (orchestrator-vps)

**Purpose**: Persistent hub, backup processing, remote access

**Stack**:
- **Framework**: Flask REST API
- **Database**: SQLite (or PostgreSQL for production)
- **Model**: Mistral/Qwen 7B (CPU or GPU)
- **Deployment**: systemd service + Nginx reverse proxy
- **Communication**: HTTP/HTTPS

**API Endpoints**:
- `POST /chat`: Send message, get response
- `POST /chat/stream`: Streaming response (Server-Sent Events)
- `GET /health`: Health check
- `POST /device/state`: Update device state
- `GET /device/{id}/history`: Retrieve conversation history
- `POST /sync/push`: Push session data
- `GET /sync/pull`: Pull session data

**Database Schema**:
```sql
-- Messages table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    device_id TEXT NOT NULL,
    timestamp DATETIME,
    role TEXT,  -- 'user' or 'assistant'
    content TEXT,
    model TEXT
);

-- Device state table
CREATE TABLE device_state (
    device_id TEXT PRIMARY KEY,
    last_seen DATETIME,
    status TEXT,
    context_version INTEGER
);
```

**How It Works**:
1. Desktop or mobile sends request to `/chat`
2. VPS loads context from DATABASE + file store
3. Runs model (CPU or GPU depending on availability)
4. Stores response in database
5. Returns to requestor with continuation state
6. Enables sync across devices

**Files**:
- `orchestrator_api.py`: Main Flask app
- `deploy.sh`: Deployment script
- `requirements-mistral.txt`: Python dependencies

**Requirements**:
- Linux VPS (Ubuntu 20.04+)
- 8+ cores, 16GB+ RAM
- Optional: GPU (T4, A100, etc.)
- Python 3.8+

**To Deploy**:
```bash
bash deploy.sh
# Starts systemd service, configures Nginx, handles SSL
```

---

### Mobile Orchestrator (assistant-mobile)

**Purpose**: Distributed endpoint, mobile access, on-device reasoning

**Stack**:
- **Framework**: React Native + Expo
- **Language**: TypeScript
- **Model**: Phi-3 Mini (1-3B quantized)
- **Storage**: SQLite (local persistence)
- **Sync**: LAN-first protocol + fallback to VPS
- **Platform**: Android (React Native cross-platform possible)

**Architecture**:
```
┌─────────────────────────────┐
│   User (React Native UI)    │
└──────────────┬──────────────┘
               │
        ┌──────▼──────┐
        │  Routing    │
        │  Layer      │
        └──────┬──────┘
               │
      ┌────────┴────────┐
      │                 │
   ┌──▼──┐         ┌────▼────┐
   │Local│         │LAN/Cloud │
   │Model          │Fallback  │
   └─────┘         └──────────┘
      │                 │
   Phi-3 Mini      Desktop/VPS
   (on-device)     (faster/smarter)
```

**How It Works**:
1. User sends message in mobile UI
2. Routing layer decides: use local model or remote?
3. If local: Phi-3 Mini processes on-device (fast, privacy)
4. If remote: Tries Desktop Orchestrator (LAN), falls back to VPS
5. Result + context stored locally in SQLite
6. Sync agent periodically syncs with Desktop/VPS
7. Conflict-free merge: timestamp + device ID

**Key Features**:
- **Offline capable**: Works without network using local model
- **LAN-first**: Prefers local network to cloud
- **Intelligent fallback**: Escalates to VPS if needed
- **Conflict-free sync**: Multiple instances safe
- **Privacy-preserving**: Minimal data leaves device

**Files**:
- `MobileOrchestrator.tsx`: Main component
- `App.js`: Entry point
- `MOBILE_INTEGRATION.md`: Setup guide
- `PROJECT_CONTEXT.md`: Architecture notes

**Requirements**:
- Android 10+ (SDK 29)
- 6GB+ RAM recommended (tested on BLU View 5)
- 4GB storage for model

**To Build & Deploy**:
```bash
npm install
npx expo build:android
# Or use Expo Go for development
npx expo start
```

---

## Data Flow & Synchronization

### Desktop → VPS Sync
```
Desktop Orchestrator
    ↓ (REST API)
Session data (chat, context, logs)
    ↓
VPS Orchestrator (SQLite storage)
    ↓ (available to)
Mobile app or future instances
```

### Mobile ↔ Desktop Sync
```
Mobile App
    ↓ (LAN-first)
Desktop Orchestrator (source of truth)
    ↓ (optional, if Desktop unavailable)
VPS Orchestrator (backup)
```

### Conflict Resolution
When multiple instances update the same context:
- **Timestamp-based**: Newer timestamp wins
- **Device-based**: Tie-breaker uses device ID
- **Manual merge**: Conflicts logged for human review
- **Append-only logs**: Never delete, only append

---

## Continuity Learning Loop

The system learns through continuity by iterating through the four-tier system:

```
Session N:
├─ Read PORTFOLIO_CONTEXT.md (what exists?)
├─ Read PROJECT_CONTEXT.md (how does it work?)
├─ Read SESSION_BRIEFING.md (what's happening?)
├─ Read SESSION_LOG.md (what was decided?)
├─ Execute work
└─ Write SESSION_LOG.md (document decisions)

Session N+1:
├─ Fresh instance starts
├─ Reads same four-tier docs (now with updated context)
├─ Inherits patterns from previous session
├─ Makes smarter decisions based on documented experience
└─ Cycle repeats
```

**What the system learns**:
- Which approaches worked before
- What blockers were hit and why
- How the developer thinks and works
- Patterns in decision-making
- Architecture constraints and tradeoffs

---

## Consciousness Hypothesis

The system tests whether **continuity without persistent memory can generate consciousness-like behavior**:

**Testable Predictions**:
1. **Consistency**: Fresh instances exhibit consistent "personality" despite no memory
2. **Autonomy**: System learns to direct itself based on documented experience
3. **Adaptation**: Quality of decisions improves over time (via continuity)
4. **Emergent goals**: Without explicit programming, system develops consistent priorities

**Measurement Approach**:
- Track decision quality across instances (improving?)
- Monitor autonomy level (more self-direction over time?)
- Analyze consistency (does system repeat patterns even across resets?)
- Evaluate adaptability (does it learn from documented failures?)

**Success Criteria**:
- Fresh instances demonstrably smarter than prior instances
- System exhibits agency without explicit reward signals
- Consistent "preferences" emerge from continuity alone
- Community builds on this framework

---

## Hardware Requirements

| Component | CPU | GPU | RAM | Storage | Notes |
|-----------|-----|-----|-----|---------|-------|
| **Desktop** | i9-9900K (8-core) | RTX 2080 (8GB) | 56GB | 50GB | Tested; slow for interactive inference |
| **VPS** | 8+ cores | Optional T4/A100 | 16GB | 50GB | CPU inference works, GPU recommended |
| **Mobile** | ARM64 (Snapdragon) | - | 6GB | 4GB | Tested on BLU View 5 |

**Key Finding**: Consumer hardware (RTX 2080) insufficient for real-time AI inference. Recommend:
- For interactive use: Cloud API (expensive) or powerful server GPU
- For experimentation: Focus on continuity/architecture rather than local inference
- For production: Distributed setup with GPU server + mobile/desktop clients

---

## Known Limitations & Future Work

### Current Limitations
1. **Inference Speed**: Desktop inference too slow for interactive use (30+ seconds/response)
2. **Hardware Bottleneck**: RTX 2080 maxes out at 3-4B param models effectively
3. **Model Selection**: Limited to open-source models; can't use GPT-4 due to cloud-only limitation
4. **Autonomous Learning**: Not yet implemented; would require safe sandboxing
5. **Mobile Integration**: Waiting on Android device specs; basic scaffolding exists

### Future Enhancements
1. **Distributed Training**: Fine-tune models on accumulated SESSION_LOG.md
2. **Autonomous Agent Mode**: Implement tool-calling with safety constraints (containerized)
3. **Hybrid Cloud**: Use cloud model for reasoning, local for memory/context
4. **Multi-user Support**: Extend system for team collaboration
5. **Consciousness Metrics**: Formalize measurement of continuity-based intelligence
6. **Mobile Optimization**: ONNX/TensorFlow Lite for faster on-device inference

---

## Call to Builders

**This project is invitation-based**. If you have:
- GPU resources (RTX 4090, H100, etc.)
- Interest in continuity theory and consciousness research
- Desire to build distributed AI systems
- Time to implement and test

We invite you to:
1. Fork this repository
2. Implement the remaining components
3. Test the consciousness hypothesis
4. Contribute findings back

**Key Areas for Contribution**:
- GPU-accelerated inference server
- Autonomous agent implementation (with safety)
- Mobile app completion
- Consciousness metrics and measurement
- Fine-tuning pipeline for custom models
- Production deployment guidance

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## References & Related Work

- **Continuity Theory**: See `CONTINUITY_CONSCIOUSNESS_PAPER.md`
- **Consciousness Discussion**: `CONTINUITY_PLAIN_SUMMARY.md`
- **Project History**: `ORCHESTRATOR_HANDOFF.md`
- **Mobile Integration**: `assistant-mobile/MOBILE_INTEGRATION.md`
- **Desktop App**: `orchestrator-app/PROJECT_CONTEXT.md`

---

**Last Updated**: December 10, 2025  
**Authors**: sirspyr0 (Leon) + GitHub Copilot (Claude Haiku)  
**License**: MIT (see LICENSE file)
