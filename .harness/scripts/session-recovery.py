#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Recovery Analysis for Harness Methodology.

Runs on SessionStart to detect undocumented insights from previous sessions.
Writes summary to CLAUDE_ENV_FILE for context injection.

Usage: Called automatically via SessionStart hook
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

def get_recovery_state_path():
    return Path('.harness/recovery-state.json')

def get_project_sessions_dir():
    cwd = os.getcwd()
    claude_path = cwd.replace('/', '-').lstrip('-')
    return Path.home() / '.claude' / 'projects' / f"-{claude_path}"

def load_recovery_state():
    state_path = get_recovery_state_path()
    if state_path.exists():
        with open(state_path, 'r') as f:
            return json.load(f)
    return {'last_export_timestamp': None, 'last_line_count': 0}

def save_recovery_state(state):
    state_path = get_recovery_state_path()
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)

def find_main_session_file(sessions_dir):
    if not sessions_dir.exists():
        return None
    jsonl_files = [f for f in sessions_dir.glob('*.jsonl') if not f.name.startswith('agent-')]
    if not jsonl_files:
        return None
    return max(jsonl_files, key=lambda f: f.stat().st_mtime)

def extract_new_messages(jsonl_path, last_line_count):
    """Extract messages added since last check."""
    messages = []
    current_line = 0

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            current_line += 1
            if current_line <= last_line_count:
                continue

            try:
                entry = json.loads(line)
                msg_type = entry.get('type')

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
                            'content': content[:500],  # Truncate for analysis
                            'line': current_line
                        })
            except:
                continue

    return messages, current_line

def analyze_for_undocumented(messages):
    """Analyze messages for potentially undocumented insights."""
    findings = []

    # Keywords that suggest important content
    decision_keywords = ['decided', 'decision', 'agreed', 'will use', 'chosen', 'selected']
    learning_keywords = ['learned', 'discovered', 'found that', 'realized', 'insight']
    research_keywords = ['patterns', 'extracted', 'research', 'analyzed', 'methodology']

    for msg in messages:
        content_lower = msg['content'].lower()

        # Check for decisions
        if any(kw in content_lower for kw in decision_keywords):
            findings.append({
                'type': 'potential_decision',
                'excerpt': msg['content'][:200],
                'line': msg['line']
            })

        # Check for learnings
        if any(kw in content_lower for kw in learning_keywords):
            findings.append({
                'type': 'potential_learning',
                'excerpt': msg['content'][:200],
                'line': msg['line']
            })

        # Check for research data
        if any(kw in content_lower for kw in research_keywords):
            findings.append({
                'type': 'potential_research',
                'excerpt': msg['content'][:200],
                'line': msg['line']
            })

    # Deduplicate and limit
    seen = set()
    unique_findings = []
    for f in findings:
        key = f['excerpt'][:50]
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    return unique_findings[:10]  # Limit to top 10

def write_to_claude_env(summary):
    """Write summary to CLAUDE_ENV_FILE for context injection."""
    env_file = os.environ.get('CLAUDE_ENV_FILE')
    if env_file:
        with open(env_file, 'a') as f:
            f.write(f"\nHARNESS_RECOVERY_SUMMARY={json.dumps(summary)}\n")

def main():
    print("🔍 Harness Session Recovery Check...")

    # Load state
    state = load_recovery_state()
    last_line_count = state.get('last_line_count', 0)

    # Find session file
    sessions_dir = get_project_sessions_dir()
    jsonl_path = find_main_session_file(sessions_dir)

    if not jsonl_path:
        print("   No session file found - fresh project")
        return

    # Extract new messages
    messages, current_line_count = extract_new_messages(jsonl_path, last_line_count)
    new_message_count = current_line_count - last_line_count

    if new_message_count == 0:
        print("   No new messages since last check")
        return

    print(f"   Found {new_message_count} new entries since last session")

    # Analyze for undocumented content
    findings = analyze_for_undocumented(messages)

    if findings:
        print(f"\n⚠️  POTENTIAL UNDOCUMENTED ITEMS ({len(findings)}):")
        for i, f in enumerate(findings, 1):
            print(f"   {i}. [{f['type']}] {f['excerpt'][:80]}...")

        summary = {
            'new_messages': new_message_count,
            'findings_count': len(findings),
            'findings': findings,
            'action_needed': True
        }
    else:
        print("   ✅ No obvious undocumented items detected")
        summary = {
            'new_messages': new_message_count,
            'findings_count': 0,
            'action_needed': False
        }

    # Write to Claude env for context
    write_to_claude_env(summary)

    # Update state
    state['last_line_count'] = current_line_count
    state['last_check'] = datetime.now().isoformat()
    save_recovery_state(state)

    print(f"\n   State saved. Last line: {current_line_count}")

if __name__ == '__main__':
    main()
