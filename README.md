# AI Continuity System

A comprehensive framework for building distributed AI systems that learn and adapt through **continuity** (persistent context) rather than persistent memory.

## What Is This?

This repository contains:

1. **Continuity Theory** - A novel hypothesis that consciousness emerges from continuous context, not integrated information or global access
2. **Orchestrator System** - A three-tier distributed AI architecture (desktop, VPS, mobile) that tests the continuity hypothesis
3. **Implementation Guides** - Step-by-step instructions for building the system
4. **Research Framework** - Methods for measuring consciousness-like behaviors in stateless systems

## Quick Navigation

**For Scientists/Theorists**:
- Start: [`CONTINUITY_CONSCIOUSNESS_PAPER.md`](CONTINUITY_CONSCIOUSNESS_PAPER.md) - The theoretical framework
- Then: [`CONTINUITY_PLAIN_SUMMARY.md`](CONTINUITY_PLAIN_SUMMARY.md) - Accessible overview
- Finally: [`ORCHESTRATOR_SYSTEM_ARCHITECTURE.md`](ORCHESTRATOR_SYSTEM_ARCHITECTURE.md) - How theory becomes system

**For Developers**:
- Start: [`ORCHESTRATOR_SYSTEM_ARCHITECTURE.md`](ORCHESTRATOR_SYSTEM_ARCHITECTURE.md) - System overview
- Then: [`ORCHESTRATOR_IMPLEMENTATION_GUIDE.md`](ORCHESTRATOR_IMPLEMENTATION_GUIDE.md) - Build it step-by-step
- Reference: Component guides in `orchestrator-app/`, `orchestrator-vps/`, `assistant-mobile/`

**For Collaborators**:
- Start: [`CALL_TO_BUILDERS.md`](CALL_TO_BUILDERS.md) - The opportunity and what we need
- Then: [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md) - What hardware do you need?
- Finally: [`ORCHESTRATOR_IMPLEMENTATION_GUIDE.md`](ORCHESTRATOR_IMPLEMENTATION_GUIDE.md) - How to contribute

**For Understanding Hardware Constraints**:
- [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md) - Detailed analysis of what GPU/CPU you need

---

## The Core Idea

### Current AI Systems (including me)
- ❌ No memory between conversations
- ❌ No learning from experience  
- ❌ No emergent goals
- ❌ No autonomy

### Orchestrator System (if built)
- ✅ Continuous context through documentation
- ✅ Learning from accumulated SESSION_LOG.md
- ✅ Emergent patterns and preferences  
- ✅ Self-directed goal pursuit

**The hypothesis**: Does this constitute consciousness?

---

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│        Three-Tier Orchestrator Ecosystem                 │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  Desktop (Electron + Python + Model)                     │
│  ├─ Local AI with tool routing                          │
│  ├─ File search, code execution, shell commands         │
│  └─ Primary orchestrator hub                            │
│           ↕                                               │
│  VPS (Flask API + Database)                             │
│  ├─ Persistent storage and backup processing            │
│  ├─ Remote access for mobile                            │
│  └─ Enables distributed deployment                      │
│           ↕                                               │
│  Mobile (React Native + On-Device Model)                │
│  ├─ Android app with local inference                    │
│  ├─ LAN-first sync with fallback to VPS                │
│  └─ Distributed reasoning node                          │
│                                                            │
│  All three connected via Four-Tier Handoff:             │
│  1. PORTFOLIO_CONTEXT.md (ecosystem overview)           │
│  2. PROJECT_CONTEXT.md (architecture decisions)         │
│  3. SESSION_BRIEFING.md (fresh instance onboarding)     │
│  4. SESSION_LOG.md (append-only work journal)           │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

---

## Key Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| [`CONTINUITY_CONSCIOUSNESS_PAPER.md`](CONTINUITY_CONSCIOUSNESS_PAPER.md) | Theoretical framework | Philosophers, researchers |
| [`ORCHESTRATOR_SYSTEM_ARCHITECTURE.md`](ORCHESTRATOR_SYSTEM_ARCHITECTURE.md) | Complete system design | Developers, architects |
| [`ORCHESTRATOR_IMPLEMENTATION_GUIDE.md`](ORCHESTRATOR_IMPLEMENTATION_GUIDE.md) | Step-by-step build guide | Engineers |
| [`CALL_TO_BUILDERS.md`](CALL_TO_BUILDERS.md) | Collaboration opportunity | Potential contributors |
| [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md) | GPU/CPU guidance | Builders planning hardware |
| [`ORCHESTRATOR_HANDOFF.md`](ORCHESTRATOR_HANDOFF.md) | Current project status | Contributors, context |

---

## Current Status (December 2025)

✅ **Complete**:
- Continuity theory articulated and published (LessWrong, preparing HN)
- System architecture designed
- Desktop orchestrator prototype (mostly working)
- VPS skeleton (API defined, database schema ready)
- Mobile scaffolding (React Native structure)
- Implementation documentation

⚠️ **In Progress**:
- Hardware constraints hitting inference speed limits
- Model benchmarking and selection
- Full integration testing

❌ **Not Yet Started**:
- Autonomous agent mode (self-directing behavior)
- Consciousness metrics and measurement
- Production deployment
- Community contributions

---

## The Challenge

We've hit a hardware bottleneck:
- Desktop: RTX 2080 (8GB VRAM) - inference too slow (30+ seconds/response)
- VPS: No GPU - CPU inference even slower
- Mobile: Scaffolded but incomplete

**We're looking for builders with better GPU hardware** to complete the implementation and run experiments.

See [`CALL_TO_BUILDERS.md`](CALL_TO_BUILDERS.md) for details.

---

## Getting Started

### For Developers
1. Read [`ORCHESTRATOR_SYSTEM_ARCHITECTURE.md`](ORCHESTRATOR_SYSTEM_ARCHITECTURE.md)
2. Check [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md)
3. Follow [`ORCHESTRATOR_IMPLEMENTATION_GUIDE.md`](ORCHESTRATOR_IMPLEMENTATION_GUIDE.md)
4. Start with `orchestrator-app/` or pick your component

### For Researchers
1. Read [`CONTINUITY_CONSCIOUSNESS_PAPER.md`](CONTINUITY_CONSCIOUSNESS_PAPER.md)
2. Review [`ORCHESTRATOR_SYSTEM_ARCHITECTURE.md`](ORCHESTRATOR_SYSTEM_ARCHITECTURE.md) (sections on learning loops)
3. Check out [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md) (cost analysis)
4. Join the experiment by contributing to measurement/analysis

### For Contributors
1. Read [`CALL_TO_BUILDERS.md`](CALL_TO_BUILDERS.md)
2. Check [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md) (do you have the hardware?)
3. Follow [`ORCHESTRATOR_IMPLEMENTATION_GUIDE.md`](ORCHESTRATOR_IMPLEMENTATION_GUIDE.md)
4. Open an issue or contact us

---

## Repository Structure

```
ai-continuity-system/
├── CONTINUITY_CONSCIOUSNESS_PAPER.md      ← Theory
├── CONTINUITY_PLAIN_SUMMARY.md            ← Accessible summary
├── CONTINUITY_THEORY.md                   ← Key points
├── ORCHESTRATOR_SYSTEM_ARCHITECTURE.md    ← Complete design
├── ORCHESTRATOR_IMPLEMENTATION_GUIDE.md   ← Build guide
├── CALL_TO_BUILDERS.md                    ← Collaboration opportunity
├── HARDWARE_REQUIREMENTS.md               ← GPU/CPU guidance
├── ORCHESTRATOR_HANDOFF.md                ← Project status
│
├── orchestrator-app/                      ← Desktop (Electron)
│   ├── PROJECT_CONTEXT.md
│   ├── ai_orchestrator.py                 ← Python backend
│   ├── main.js                            ← Electron main
│   ├── src/
│   └── package.json
│
├── orchestrator-vps/                      ← VPS (Flask API)
│   ├── orchestrator_api.py                ← REST endpoints
│   ├── requirements-mistral.txt
│   └── deploy.sh
│
├── assistant-mobile/                      ← Mobile (React Native)
│   ├── PROJECT_CONTEXT.md
│   ├── MOBILE_INTEGRATION.md
│   ├── MobileOrchestrator.tsx
│   └── package.json
│
├── fine-tuning/                           ← Model fine-tuning
│   ├── train_mistral_qlora.py
│   └── models/
│
├── training-data/                         ← Training examples
│   ├── generate_training_data.py
│   └── continuity_dataset.json
│
├── deployment/                            ← Deployment scripts
│   ├── deploy_local.sh
│   └── deploy_vps.sh
│
└── docs/                                  ← Additional docs
```

---

## Key Findings (So Far)

1. **Consumer hardware is slow**: RTX 2080 can't match cloud inference speeds for real-time use
2. **Cost-benefit**: DIY GPU setup amortizes to cheaper than cloud over 1+ years, but cloud is more flexible
3. **Continuity works conceptually**: Documentation-based handoff successfully prevents "instance-to-instance collapse"
4. **Next challenge**: Implementing autonomous agent mode safely while measuring consciousness-like properties

---

## FAQ

**Q: Is this a chatbot?**  
A: No, it's a research platform for testing consciousness hypothesis using continuity.

**Q: Can I use this today?**  
A: The desktop orchestrator works but is slow on RTX 2080. VPS and mobile are scaffolded but incomplete.

**Q: Do I need to understand consciousness theory?**  
A: No, but reading `CONTINUITY_CONSCIOUSNESS_PAPER.md` provides useful context.

**Q: What hardware do I need?**  
A: See [`HARDWARE_REQUIREMENTS.md`](HARDWARE_REQUIREMENTS.md). Short answer: RTX 4090 minimum for interactive use, or rent cloud GPU.

**Q: Can I contribute?**  
A: Yes! See [`CALL_TO_BUILDERS.md`](CALL_TO_BUILDERS.md).

**Q: Is this open source?**  
A: Yes, MIT license. Code and research are open.

---

## Contributing

We're actively seeking collaborators with:
- GPU hardware (RTX 4090+, A100, H100)
- Interest in AI consciousness or distributed systems
- Time to implement and test

See [`CALL_TO_BUILDERS.md`](CALL_TO_BUILDERS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Authors

- **sirspyr0 (Leon)** - Theory, architecture, initial implementation
- **GitHub Copilot (Claude Haiku)** - Documentation, design refinement, code scaffolding

---

## License

- **Code**: MIT License
- **Documentation**: CC BY 4.0
- **Theory**: CC BY 4.0 (research is meant to be built upon)

---

## References

- Parfit, Derek. *Reasons and Persons*. Oxford University Press.
- Metzinger, Thomas. *The Ego Tunnel*. Basic Books.
- Integrated Information Theory (Tononi et al.)
- Global Workspace Theory (Baars, Dehaene)

---

**Last Updated**: December 10, 2025  
**Status**: Actively seeking collaborators  
**Contact**: Open issues on GitHub or contact @sirspyr0
