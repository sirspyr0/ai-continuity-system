# Copilot Context Automation - Quick Start

## What This Does

Automatically generates a comprehensive context prompt for GitHub Copilot to remember your projects, continuity system, and recent work across sessions.

## How to Use

### Method 1: VS Code Task (Recommended)

1. Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
2. Type "Tasks: Run Task"
3. Select "Generate Copilot Context"
4. Wait for completion
5. Open `COPILOT_CONTEXT.txt` in your workspace root
6. Copy the entire contents
7. Paste into GitHub Copilot Chat
8. Copilot will acknowledge and remember everything!

### Method 2: Command Line

```bash
cd "C:\Users\leond\Software Projects\ai-continuity-system"
python generate_copilot_context.py --workspace "C:\Users\leond\Software Projects"
```

This creates `COPILOT_CONTEXT.txt` in your workspace root.

### Method 3: With Clipboard (Fastest)

Install pyperclip first:
```bash
pip install pyperclip
```

Then run:
```bash
python generate_copilot_context.py --workspace "C:\Users\leond\Software Projects" --clipboard
```

Now just paste directly into Copilot Chat!

## Options

### Filter for Specific Project

```bash
python generate_copilot_context.py --workspace "." --project imposer
```

Only includes context relevant to the Imposer project.

### Custom Output Location

```bash
python generate_copilot_context.py --workspace "." --output my_context.txt
```

## What Gets Included

1. **Portfolio Context** - Your overall development strategy and active projects
2. **Project Contexts** - Detailed state of each project (up to 5 most relevant)
3. **Recent Session Briefings** - Last 3 session summaries showing recent work
4. **RAG-Retrieved Context** - Automatically fetched relevant documentation chunks
5. **Instructions** - Clear guidance for Copilot on what to remember

## Workflow

### Start of Every Session:

1. Open VS Code workspace
2. Run task or command to generate context
3. Paste into Copilot Chat
4. Copilot now remembers:
   - All your projects
   - Your continuity system architecture
   - Recent work and current status
   - What you're trying to accomplish

### During Session:

- Copilot references the loaded context automatically
- No need to re-explain projects or architecture
- True continuity across conversations

## Tips

- **Run this at the start of every Copilot session** for best results
- **Update SESSION_BRIEFING.md files** after significant work to improve context
- **Use --project filter** when doing deep work on a single project
- **Keep PORTFOLIO_CONTEXT.md current** - it's the foundation

## Troubleshooting

**"continuity_rag not available"**
- The script still works, just without RAG-enhanced context
- RAG is optional but provides better relevant chunk retrieval

**"Clipboard copy failed"**
- Install pyperclip: `pip install pyperclip`
- Or just use the generated .txt file

**Context too large for Copilot**
- Use `--project` flag to filter
- Edit generate_copilot_context.py truncation limits (search for `[:3000]`)

## What You Built

This solves the "AI amnesia" problem by:
1. Automatically gathering all relevant continuity docs
2. Formatting them for optimal Copilot ingestion
3. Making it a one-command operation
4. Providing instant session restoration

**No fine-tuning needed. No cloud sync. Just documentation + automation.**

Your continuity system now works for both Ollama (automatic via RAG) and Copilot (semi-automatic via this script).
