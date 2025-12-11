#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Recovery Analysis for Harness Methodology.

Scans ALL Harness-related project folders for new content since last check.
Runs on SessionStart to:
1. Detect undocumented insights from previous sessions
2. Auto-export new content to markdown transcript with progressive disclosure:
   - Session profile (tool usage stats)
   - Files touched
   - Action checklist (decisions, errors, todos)
   - Full transcript
3. Check for decision-log.md entries not yet synced to vision.md

Usage: Called automatically via SessionStart hook, or manually
"""

import sys
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter

def get_recovery_state_path():
    return Path('.harness/recovery-state.json')


def run_git_command(cmd, cwd=None):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=cwd
        )
        return result.stdout.strip(), result.returncode == 0
    except:
        return "", False


def check_git_health():
    """Check git status across worktrees and branches."""
    print("\n🔀 GIT HEALTH CHECK")

    # Get worktrees
    worktrees_output, ok = run_git_command("git worktree list")
    if not ok:
        print("   ⚠️  Not a git repository or git not available")
        return

    worktrees = []
    for line in worktrees_output.split('\n'):
        if line.strip():
            parts = line.split()
            if len(parts) >= 2:
                path = parts[0]
                branch = parts[-1].strip('[]') if '[' in line else 'detached'
                worktrees.append({'path': path, 'branch': branch})

    # Get current branch
    current_branch, _ = run_git_command("git rev-parse --abbrev-ref HEAD")

    # Get remote branches
    remote_branches, _ = run_git_command("git branch -r")
    remote_list = [b.strip().replace('origin/', '') for b in remote_branches.split('\n') if b.strip()]

    # Check each branch status
    branches_info = []
    local_branches, _ = run_git_command("git branch --format='%(refname:short)'")

    for branch in local_branches.split('\n'):
        branch = branch.strip().strip("'")
        if not branch:
            continue

        # Check if ahead/behind main
        ahead, _ = run_git_command(f"git rev-list main..{branch} --count")
        behind, _ = run_git_command(f"git rev-list {branch}..main --count")

        ahead = int(ahead) if ahead.isdigit() else 0
        behind = int(behind) if behind.isdigit() else 0

        on_remote = branch in remote_list or branch == 'main'
        is_current = branch == current_branch

        branches_info.append({
            'name': branch,
            'ahead': ahead,
            'behind': behind,
            'on_remote': on_remote,
            'is_current': is_current
        })

    # Check for uncommitted changes
    status_output, _ = run_git_command("git status --porcelain")
    has_uncommitted = bool(status_output.strip())

    # Build status display
    print("   ╔═══════════════════════════════════════════════════════════╗")

    # Determine overall status
    unmerged = [b for b in branches_info if b['ahead'] > 0 and b['name'] != 'main']
    stale = [b for b in branches_info if b['behind'] > 0 and b['name'] != 'main']
    unpushed = [b for b in branches_info if not b['on_remote'] and b['name'] != 'main']

    if not unmerged and not has_uncommitted and not unpushed:
        print("   ║              GIT STATUS - ALL CLEAN! ✅                   ║")
    else:
        print("   ║              GIT STATUS - ACTION NEEDED ⚠️                ║")

    print("   ╠═══════════════════════════════════════════════════════════╣")
    print("   ║ Branch               │ vs Main  │ GitHub │ Status        ║")
    print("   ╠═══════════════════════════════════════════════════════════╣")

    for b in branches_info:
        name = b['name'][:18].ljust(18)
        if b['name'] == 'main':
            vs_main = "BASE".ljust(8)
        elif b['ahead'] > 0 and b['behind'] > 0:
            vs_main = f"+{b['ahead']}/-{b['behind']}".ljust(8)
        elif b['ahead'] > 0:
            vs_main = f"+{b['ahead']}".ljust(8)
        elif b['behind'] > 0:
            vs_main = f"-{b['behind']}".ljust(8)
        else:
            vs_main = "=".ljust(8)

        github = "✅" if b['on_remote'] else "❌"

        if b['is_current']:
            status = "← HERE"
        elif b['name'] == 'main':
            status = "base"
        elif b['ahead'] > 0:
            status = "MERGE ME"
        elif b['behind'] > 0:
            status = "stale"
        else:
            status = "ok"

        print(f"   ║ {name} │ {vs_main} │   {github}    │ {status.ljust(13)} ║")

    print("   ╠═══════════════════════════════════════════════════════════╣")

    # Worktrees section
    print("   ║ WORKTREES                                                 ║")
    for wt in worktrees[:3]:  # Limit to 3
        path_short = wt['path'][-45:] if len(wt['path']) > 45 else wt['path']
        print(f"   ║  {path_short.ljust(45)} → {wt['branch'][:10]} ║")
    if len(worktrees) > 3:
        print(f"   ║  ... and {len(worktrees) - 3} more                                        ║")

    print("   ╠═══════════════════════════════════════════════════════════╣")

    # Summary
    if has_uncommitted:
        print("   ║ ⚠️  Uncommitted changes in working directory              ║")
    if unmerged:
        names = ', '.join(b['name'] for b in unmerged[:3])
        print(f"   ║ 📤 Unmerged branches: {names[:35].ljust(35)} ║")
    if unpushed:
        names = ', '.join(b['name'] for b in unpushed[:3])
        print(f"   ║ 🔒 Not on GitHub: {names[:39].ljust(39)} ║")
    if not unmerged and not has_uncommitted and not unpushed:
        print("   ║ ✅ All work merged and pushed                             ║")

    print("   ╚═══════════════════════════════════════════════════════════╝")


def check_decision_sync():
    """Check if decision-log.md has entries not yet reflected in vision.md."""
    decision_log = Path('.harness/decision-log.md')
    vision_file = Path('00-governance/vision.md')

    if not decision_log.exists() or not vision_file.exists():
        return None, None

    # Count decisions in decision-log.md
    decision_count = 0
    with open(decision_log, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('## Decision #'):
                decision_count += 1

    # Find last session mentioned in vision.md principles
    last_session_in_vision = 0
    with open(vision_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for "From Session N:" patterns
        session_matches = re.findall(r'From Session (\d+):', content)
        if session_matches:
            last_session_in_vision = max(int(s) for s in session_matches)

    return decision_count, last_session_in_vision

def find_all_harness_folders():
    """Find ALL project folders related to Harness."""
    claude_projects = Path.home() / '.claude' / 'projects'
    if not claude_projects.exists():
        return []

    harness_folders = []
    for folder in claude_projects.iterdir():
        if folder.is_dir() and 'harness' in folder.name.lower():
            harness_folders.append(folder)

    return harness_folders

def find_session_files(folder):
    """Find main session files (not agent files) in a folder."""
    return [f for f in folder.glob('*.jsonl') if not f.name.startswith('agent-')]

def load_recovery_state():
    state_path = get_recovery_state_path()
    if state_path.exists():
        with open(state_path, 'r') as f:
            return json.load(f)
    return {
        'last_check_timestamp': None,
        'processed_files': {}  # {filepath: last_line_count}
    }

def save_recovery_state(state):
    state_path = get_recovery_state_path()
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state['last_check_timestamp'] = datetime.now().isoformat()
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)

def extract_new_entries(jsonl_path, last_line_count):
    """Extract all entries (messages + tool calls) added since last check."""
    messages = []
    tool_calls = []
    files_touched = set()
    current_line = 0

    # Patterns for extracting file paths
    file_patterns = [
        r'["\']?(/[^"\'<>\s]+\.(py|ts|js|tsx|jsx|yaml|yml|json|md|txt|css|html))["\']?',
        r'file[_-]?path["\s:]+["\']?([^"\'<>\s]+)["\']?',
    ]

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            current_line += 1
            if current_line <= last_line_count:
                continue

            try:
                entry = json.loads(line)
                msg_type = entry.get('type')
                timestamp = entry.get('timestamp', '')

                # Extract user/assistant messages
                if msg_type in ['user', 'assistant']:
                    content = entry.get('message', {}).get('content', '')
                    if isinstance(content, list):
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                        content = ' '.join(text_parts)
                    if content:
                        messages.append({
                            'type': msg_type,
                            'content': content[:500],
                            'full_content': content,
                            'line': current_line,
                            'timestamp': timestamp,
                            'source': str(jsonl_path)
                        })

                # Extract tool calls from assistant messages (nested in content)
                if msg_type == 'assistant':
                    message_obj = entry.get('message', {})
                    content_list = message_obj.get('content', [])
                    if isinstance(content_list, list):
                        for content_item in content_list:
                            if isinstance(content_item, dict) and content_item.get('type') == 'tool_use':
                                tool_name = content_item.get('name', 'unknown')
                                tool_input = content_item.get('input', {})
                                tool_calls.append({
                                    'name': tool_name,
                                    'timestamp': timestamp
                                })

                                # Extract file paths from tool inputs
                                if isinstance(tool_input, dict):
                                    for key, value in tool_input.items():
                                        if isinstance(value, str):
                                            for pattern in file_patterns:
                                                matches = re.findall(pattern, value, re.IGNORECASE)
                                                for match in matches:
                                                    if isinstance(match, tuple):
                                                        files_touched.add(match[0])
                                                    else:
                                                        files_touched.add(match)

            except:
                continue

    return messages, tool_calls, list(files_touched), current_line


def build_session_profile(tool_calls, files_touched, messages):
    """Build a session profile from tool usage statistics."""
    if not tool_calls and not messages:
        return None

    tool_counts = Counter(tc['name'] for tc in tool_calls)
    total_tools = len(tool_calls)

    # Categorize tools
    edit_tools = tool_counts.get('Edit', 0) + tool_counts.get('Write', 0) + tool_counts.get('NotebookEdit', 0)
    read_tools = tool_counts.get('Read', 0)
    search_tools = tool_counts.get('Grep', 0) + tool_counts.get('Glob', 0)
    bash_tools = tool_counts.get('Bash', 0)

    # Determine session character
    if total_tools == 0:
        character = "Discussion-focused (no tool usage)"
        character_emoji = "💬"
    elif edit_tools > total_tools * 0.4:
        character = "Implementation-heavy"
        character_emoji = "🔧"
    elif read_tools > total_tools * 0.4:
        character = "Exploration/Research"
        character_emoji = "🔍"
    elif search_tools > total_tools * 0.3:
        character = "Codebase exploration"
        character_emoji = "🗺️"
    elif bash_tools > total_tools * 0.3:
        character = "System/DevOps tasks"
        character_emoji = "⚙️"
    else:
        character = "Mixed activities"
        character_emoji = "📋"

    return {
        'total_tools': total_tools,
        'total_messages': len(messages),
        'character': character,
        'character_emoji': character_emoji,
        'tool_counts': dict(tool_counts),
        'files_touched': len(files_touched),
        'edit_percentage': round(edit_tools / max(total_tools, 1) * 100),
        'top_tools': tool_counts.most_common(5)
    }

def export_new_content_to_transcript(all_new_messages, all_tool_calls, all_files_touched, findings):
    """Export new content to transcript with progressive disclosure format."""
    if not all_new_messages and not all_tool_calls:
        return None

    # Create transcript directory
    transcript_dir = Path('.harness/transcripts')
    transcript_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_file = transcript_dir / f"auto-recovery-{ts}.md"

    # Build session profile
    profile = build_session_profile(all_tool_calls, all_files_touched, all_new_messages)

    # Group messages by source
    by_source = {}
    for msg in all_new_messages:
        source = msg['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(msg)

    # === Generate markdown with progressive disclosure ===
    lines = [
        f"# Auto-Recovered Transcript",
        f"",
        f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Sources:** {len(by_source)} session file(s)",
        f"- **Total Messages:** {len(all_new_messages)}",
        f"",
    ]

    # === Level 0: Session Profile ===
    if profile:
        lines.extend([
            f"## Session Profile",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Character | {profile['character_emoji']} {profile['character']} |",
            f"| Tool Calls | {profile['total_tools']} |",
            f"| Messages | {profile['total_messages']} |",
            f"| Files Touched | {profile['files_touched']} |",
            f"| Edit Ratio | {profile['edit_percentage']}% |",
            f"",
        ])
        if profile['top_tools']:
            lines.append("**Top Tools:** " + ", ".join(f"{t[0]} ({t[1]})" for t in profile['top_tools']))
            lines.append("")

    # === Level 1: Files Touched ===
    if all_files_touched:
        lines.extend([
            f"## Files Touched ({len(all_files_touched)})",
            f"",
        ])
        # Group by directory
        by_dir = {}
        for f in sorted(all_files_touched):
            dir_name = str(Path(f).parent)
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(Path(f).name)

        for dir_name, files in sorted(by_dir.items()):
            lines.append(f"- `{dir_name}/`")
            for fname in files:
                lines.append(f"  - {fname}")
        lines.append("")

    # === Level 2: Action Checklist ===
    if findings:
        high_priority = [f for f in findings if f['priority'] == 1]
        medium_priority = [f for f in findings if f['priority'] == 2]

        lines.extend([
            f"## Recovery Checklist",
            f"",
        ])

        if high_priority:
            lines.append("### High Priority")
            lines.append("")
            for f in high_priority:
                lines.append(f"- [ ] **[{f['type']}]** {f['excerpt'][:100]}...")
            lines.append("")

        if medium_priority:
            lines.append("### Review if Relevant")
            lines.append("")
            for f in medium_priority:
                lines.append(f"- [ ] [{f['type']}] {f['excerpt'][:80]}...")
            lines.append("")

    lines.append("---")
    lines.append("")

    # === Level 3: Full Transcript ===
    lines.extend([
        f"## Full Transcript",
        f"",
    ])

    for source, messages in by_source.items():
        source_name = Path(source).parent.name
        lines.append(f"### Source: {source_name}")
        lines.append(f"")

        for msg in messages:
            role_emoji = "👤" if msg['type'] == 'user' else "🤖"
            role_name = "User" if msg['type'] == 'user' else "Assistant"
            lines.append(f"#### {role_emoji} {role_name}")
            lines.append(f"")
            lines.append(msg['content'])
            lines.append(f"")
            lines.append(f"---")
            lines.append(f"")

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_file


def analyze_for_undocumented(messages):
    """Analyze messages for potentially undocumented insights with expanded triggers."""
    findings = []

    # Original conversational keywords
    decision_keywords = ['decided', 'decision', 'agreed', 'will use', 'chosen', 'selected', 'approved', 'going with', 'settled on']
    learning_keywords = ['learned', 'discovered', 'found that', 'realized', 'insight', 'key finding', 'turns out', 'interesting']
    research_keywords = ['patterns', 'extracted', 'research', 'analyzed', 'methodology', 'architecture']
    action_keywords = ['todo', 'next step', 'action item', 'should create', 'need to', 'must', 'will implement']

    # Technical keywords (new)
    code_keywords = ['implement', 'refactor', 'created', 'modified', 'deleted', 'updated', 'added function', 'added method']
    error_keywords = ['error', 'failed', 'exception', 'bug', 'fix', 'broken', 'issue', 'problem', 'crash']
    config_keywords = ['configured', 'setup', 'installed', 'enabled', 'disabled', 'setting']

    # Priority levels for sorting
    high_priority = [
        (decision_keywords, 'DECISION', 1),
        (error_keywords, 'ERROR', 1),
        (action_keywords, 'ACTION', 1),
    ]
    medium_priority = [
        (learning_keywords, 'LEARNING', 2),
        (research_keywords, 'RESEARCH', 2),
        (code_keywords, 'CODE', 2),
        (config_keywords, 'CONFIG', 2),
    ]

    all_checks = high_priority + medium_priority

    for msg in messages:
        content_lower = msg['content'].lower()

        for kw_list, finding_type, priority in all_checks:
            if any(kw in content_lower for kw in kw_list):
                findings.append({
                    'type': finding_type,
                    'priority': priority,
                    'excerpt': msg['content'][:500],  # Increased for full context
                    'line': msg['line'],
                    'source': msg['source'],
                    'timestamp': msg['timestamp']
                })
                break  # Only one finding per message

    # Deduplicate
    seen = set()
    unique_findings = []
    for f in findings:
        key = f['excerpt'][:50]
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Sort by priority (high first), then limit
    unique_findings.sort(key=lambda x: x['priority'])
    return unique_findings[:20]  # Increased limit to 20

def main():
    print("🔍 Harness Session Recovery Check...")
    print(f"   Scanning for ALL Harness-related project folders...")

    # Load state
    state = load_recovery_state()
    processed_files = state.get('processed_files', {})
    last_check = state.get('last_check_timestamp', 'Never')

    print(f"   Last check: {last_check}")

    # Find all Harness folders
    harness_folders = find_all_harness_folders()
    print(f"   Found {len(harness_folders)} Harness-related folder(s)")

    all_new_messages = []
    all_tool_calls = []
    all_files_touched = []
    total_new_entries = 0

    for folder in harness_folders:
        session_files = find_session_files(folder)
        for jsonl_path in session_files:
            filepath_key = str(jsonl_path)
            last_line = processed_files.get(filepath_key, 0)

            # Use new extraction function that captures tool calls and files
            messages, tool_calls, files_touched, current_line = extract_new_entries(jsonl_path, last_line)
            new_count = current_line - last_line

            if new_count > 0:
                print(f"   📁 {folder.name}")
                print(f"      └── {jsonl_path.name}: {new_count} new entries")
                all_new_messages.extend(messages)
                all_tool_calls.extend(tool_calls)
                all_files_touched.extend(files_touched)
                total_new_entries += new_count

            # Update processed state
            processed_files[filepath_key] = current_line

    if total_new_entries == 0:
        print("   ✅ No new content since last check")
        save_recovery_state({'processed_files': processed_files})
        return

    print(f"\n   Total: {total_new_entries} new entries across all sessions")

    # Analyze for undocumented content FIRST (needed for export)
    findings = analyze_for_undocumented(all_new_messages)

    # Build session profile for console output
    profile = build_session_profile(all_tool_calls, all_files_touched, all_new_messages)
    if profile:
        print(f"   Session: {profile['character_emoji']} {profile['character']}")
        print(f"   Tools: {profile['total_tools']} | Files: {profile['files_touched']} | Messages: {profile['total_messages']}")

    # Auto-export new content to transcript with full progressive disclosure
    all_files_unique = list(set(all_files_touched))
    export_file = export_new_content_to_transcript(all_new_messages, all_tool_calls, all_files_unique, findings)
    if export_file:
        print(f"\n   📝 Auto-exported to: {export_file}")

    # Print findings summary to console - FULL CONTENT for high priority
    if findings:
        high_priority = [f for f in findings if f['priority'] == 1]
        medium_priority = [f for f in findings if f['priority'] == 2]

        print(f"\n⚠️  RECOVERY CHECKLIST ({len(findings)} items, {len(high_priority)} high priority):")

        # HIGH PRIORITY: Print FULL content so Claude receives it
        if high_priority:
            print("\n🔴 HIGH PRIORITY ITEMS (full content for context):\n")
            for i, f in enumerate(high_priority[:10], 1):  # Top 10 high priority with full content
                print(f"   {i}. [{f['type']}]")
                print(f"      {f['excerpt']}")  # FULL excerpt, not truncated
                print()

        # Medium priority: Just summaries
        if medium_priority:
            print(f"🟡 MEDIUM PRIORITY ({len(medium_priority)} items - summaries only):\n")
            for i, f in enumerate(medium_priority[:5], 1):
                print(f"   {i}. [{f['type']}] {f['excerpt'][:80]}...")
            if len(medium_priority) > 5:
                print(f"   ... and {len(medium_priority) - 5} more in transcript")
            print()
    else:
        print("   ✅ No obvious undocumented items detected")

    # Check decision-sync status
    decision_count, last_session_synced = check_decision_sync()
    if decision_count is not None:
        # Get current session from decision-log (approximate by counting unique session markers)
        decision_log = Path('.harness/decision-log.md')
        current_session = 0
        if decision_log.exists():
            with open(decision_log, 'r', encoding='utf-8') as f:
                content = f.read()
                session_markers = re.findall(r'\(Session (\d+)\)', content)
                if session_markers:
                    current_session = max(int(s) for s in session_markers)

        if current_session > last_session_synced:
            sessions_behind = current_session - last_session_synced
            print(f"\n📋 SYNC NEEDED: vision.md principles last updated for Session {last_session_synced}")
            print(f"   {sessions_behind} session(s) of decisions not yet reflected in core principles")
            print(f"   Run: Review decision-log.md and extract new principles to vision.md")

    # Save updated state
    save_recovery_state({'processed_files': processed_files})
    print(f"\n   State saved.")

    # Run git health check
    check_git_health()

if __name__ == '__main__':
    main()
