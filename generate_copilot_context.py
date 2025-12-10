"""
Generate Copilot Context Prompt
Automatically creates a comprehensive context prompt for GitHub Copilot
to restore session memory across instances.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add current dir to path for continuity_rag import
sys.path.insert(0, str(Path(__file__).parent))

try:
    from continuity_rag import ContinuityRAG
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Warning: continuity_rag not available")


def read_file_safe(file_path: Path) -> str:
    """Safely read a file with fallback encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"
    except Exception as e:
        return f"[Error: {e}]"


def generate_context_prompt(workspace_root: Path, project_filter: str = None) -> str:
    """Generate comprehensive context prompt for Copilot."""
    
    lines = []
    lines.append("=" * 80)
    lines.append("CONTINUITY CONTEXT INITIALIZATION")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)
    lines.append("")
    lines.append("**Instructions for AI Assistant:**")
    lines.append("Read and internalize the following context to restore continuity.")
    lines.append("This represents the state of our collaborative work.")
    lines.append("")
    
    # 1. Portfolio Context
    portfolio_file = workspace_root / "PORTFOLIO_CONTEXT.md"
    if portfolio_file.exists():
        lines.append("## PORTFOLIO CONTEXT")
        lines.append("-" * 80)
        content = read_file_safe(portfolio_file)
        lines.append(content[:3000])  # First 3000 chars
        if len(content) > 3000:
            lines.append("\n[...truncated for brevity...]")
        lines.append("")
    
    # 2. Project-Specific Context
    lines.append("## PROJECT CONTEXTS")
    lines.append("-" * 80)
    
    # Find all PROJECT_CONTEXT.md files
    project_contexts = list(workspace_root.glob("**/PROJECT_CONTEXT.md"))
    
    if project_filter:
        project_contexts = [p for p in project_contexts if project_filter.lower() in str(p).lower()]
    
    for project_file in project_contexts[:5]:  # Limit to 5 projects
        project_name = project_file.parent.name
        lines.append(f"\n### Project: {project_name}")
        lines.append(f"Path: {project_file.relative_to(workspace_root)}")
        lines.append("")
        
        content = read_file_safe(project_file)
        lines.append(content[:2000])  # First 2000 chars per project
        if len(content) > 2000:
            lines.append("\n[...see full file for details...]")
        lines.append("")
    
    # 3. Recent Session Briefings
    lines.append("## RECENT SESSION BRIEFINGS")
    lines.append("-" * 80)
    
    session_briefings = sorted(
        workspace_root.glob("**/SESSION_BRIEFING*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    for briefing in session_briefings[:3]:  # Most recent 3
        project_name = briefing.parent.name
        lines.append(f"\n### {project_name} - {briefing.name}")
        lines.append("")
        
        content = read_file_safe(briefing)
        lines.append(content[:1500])
        if len(content) > 1500:
            lines.append("\n[...truncated...]")
        lines.append("")
    
    # 4. RAG-Retrieved Context (if available)
    if RAG_AVAILABLE:
        lines.append("## RAG-RETRIEVED RELEVANT CONTEXT")
        lines.append("-" * 80)
        lines.append("")
        
        try:
            rag = ContinuityRAG(str(workspace_root))
            rag.index_documents()
            
            # Get session context
            rag_context = rag.get_session_context(project_filter)
            lines.append(rag_context[:2000])
            lines.append("")
        except Exception as e:
            lines.append(f"[RAG unavailable: {e}]")
            lines.append("")
    
    # 5. Summary Instructions
    lines.append("=" * 80)
    lines.append("CONTEXT LOADED - READY FOR SESSION")
    lines.append("=" * 80)
    lines.append("")
    lines.append("**What You Should Know:**")
    lines.append("- You have access to the full project portfolio and context")
    lines.append("- You understand the continuity system architecture")
    lines.append("- You know the current state of active projects")
    lines.append("- You can reference this context throughout our conversation")
    lines.append("")
    lines.append("**Please acknowledge:**")
    lines.append("1. Which projects you're aware of")
    lines.append("2. What the most recent work involved")
    lines.append("3. That you're ready to continue from where we left off")
    lines.append("")
    
    return "\n".join(lines)


def main():
    """Generate context and output to file/clipboard."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Copilot context prompt")
    parser.add_argument("--workspace", default=".", help="Workspace root path")
    parser.add_argument("--project", help="Filter for specific project")
    parser.add_argument("--output", default="COPILOT_CONTEXT.txt", help="Output file")
    parser.add_argument("--clipboard", action="store_true", help="Copy to clipboard")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace).resolve()
    
    print(f"Generating Copilot context for: {workspace_root}")
    if args.project:
        print(f"Filtering for project: {args.project}")
    
    # Generate context
    context = generate_context_prompt(workspace_root, args.project)
    
    # Write to file
    output_file = workspace_root / args.output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(context)
    
    print(f"\n✓ Context written to: {output_file}")
    print(f"  ({len(context)} characters)")
    
    # Copy to clipboard if requested
    if args.clipboard:
        try:
            import pyperclip
            pyperclip.copy(context)
            print("✓ Copied to clipboard!")
        except ImportError:
            print("⚠ Install 'pyperclip' for clipboard support: pip install pyperclip")
        except Exception as e:
            print(f"⚠ Clipboard copy failed: {e}")
    
    print("\nNext steps:")
    print("1. Open GitHub Copilot Chat in VS Code")
    print("2. Paste the content of COPILOT_CONTEXT.txt")
    print("3. Copilot will acknowledge and remember your projects!")


if __name__ == "__main__":
    main()
