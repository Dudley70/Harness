#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Claude Code session JSONL to readable Markdown.

Usage:
    python export-session.py [session-id]
    python export-session.py              # exports most recent session
    python export-session.py latest       # exports most recent session
    python export-session.py abc123       # exports session starting with abc123

Output: .harness/transcripts/session-[id]-[date].md
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

def get_project_sessions_dir():
    """Find the Claude sessions directory for current project."""
    # Get current working directory and convert to Claude's path format
    cwd = os.getcwd()
    claude_path = cwd.replace('/', '-').lstrip('-')
    sessions_dir = Path.home() / '.claude' / 'projects' / claude_path

    if not sessions_dir.exists():
        # Try alternative format
        sessions_dir = Path.home() / '.claude' / 'projects' / f"-{claude_path}"

    return sessions_dir

def find_session_file(sessions_dir, session_id=None):
    """Find the session JSONL file."""
    jsonl_files = list(sessions_dir.glob('*.jsonl'))

    # Filter out agent files (sub-agents)
    main_sessions = [f for f in jsonl_files if not f.name.startswith('agent-')]

    if not main_sessions:
        print(f"No session files found in {sessions_dir}")
        return None

    if session_id and session_id != 'latest':
        # Find matching session
        for f in main_sessions:
            if f.stem.startswith(session_id):
                return f
        print(f"No session found matching '{session_id}'")
        return None

    # Return most recently modified
    return max(main_sessions, key=lambda f: f.stat().st_mtime)

def extract_messages(jsonl_path):
    """Extract user and assistant messages from JSONL."""
    messages = []

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                msg_type = entry.get('type')

                if msg_type == 'user':
                    content = entry.get('message', {}).get('content', '')
                    if isinstance(content, str):
                        messages.append(('user', content))
                    elif isinstance(content, list):
                        # Extract text from content blocks
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict):
                                if item.get('type') == 'text':
                                    text_parts.append(item.get('text', ''))
                                elif item.get('type') == 'tool_result':
                                    # Summarize tool results
                                    tool_content = item.get('content', '')
                                    if isinstance(tool_content, str) and len(tool_content) > 500:
                                        tool_content = tool_content[:500] + '... [truncated]'
                                    text_parts.append(f"[Tool Result]: {tool_content}")
                        if text_parts:
                            messages.append(('user', '\n'.join(text_parts)))

                elif msg_type == 'assistant':
                    content = entry.get('message', {}).get('content', [])
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                            elif item.get('type') == 'tool_use':
                                tool_name = item.get('name', 'unknown')
                                tool_input = item.get('input', {})
                                # Brief summary of tool use
                                if tool_name in ['Read', 'Write', 'Edit']:
                                    file_path = tool_input.get('file_path', '')
                                    text_parts.append(f"[{tool_name}: {file_path}]")
                                elif tool_name == 'Bash':
                                    cmd = tool_input.get('command', '')[:100]
                                    text_parts.append(f"[Bash: {cmd}...]")
                                elif tool_name == 'Task':
                                    desc = tool_input.get('description', '')
                                    text_parts.append(f"[Task: {desc}]")
                                else:
                                    text_parts.append(f"[{tool_name}]")
                    if text_parts:
                        messages.append(('assistant', '\n'.join(text_parts)))

            except json.JSONDecodeError:
                continue

    return messages

def format_markdown(messages, session_id, jsonl_path):
    """Format messages as readable markdown."""
    # Get session date from file modification time
    mtime = os.path.getmtime(jsonl_path)
    session_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')

    md_lines = [
        f"# Session Transcript",
        f"",
        f"- **Session ID:** {session_id}",
        f"- **Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- **Last Modified:** {session_date}",
        f"- **Source:** `{jsonl_path}`",
        f"",
        f"---",
        f"",
    ]

    for role, content in messages:
        if role == 'user':
            # Check if it's just a tool result
            if content.strip().startswith('[Tool Result]'):
                md_lines.append(f"*{content[:200]}...*" if len(content) > 200 else f"*{content}*")
            else:
                md_lines.append(f"## 👤 User")
                md_lines.append(f"")
                md_lines.append(content)
        else:
            md_lines.append(f"## 🤖 Assistant")
            md_lines.append(f"")
            md_lines.append(content)

        md_lines.append(f"")
        md_lines.append(f"---")
        md_lines.append(f"")

    return '\n'.join(md_lines)

def main():
    session_id = sys.argv[1] if len(sys.argv) > 1 else 'latest'

    sessions_dir = get_project_sessions_dir()
    print(f"Looking for sessions in: {sessions_dir}")

    jsonl_path = find_session_file(sessions_dir, session_id)
    if not jsonl_path:
        sys.exit(1)

    print(f"Exporting: {jsonl_path.name}")

    messages = extract_messages(jsonl_path)
    print(f"Found {len(messages)} messages")

    # Generate markdown
    md_content = format_markdown(messages, jsonl_path.stem[:8], jsonl_path)

    # Output path
    output_dir = Path('.harness/transcripts')
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime('%Y%m%d')
    output_file = output_dir / f"session-{jsonl_path.stem[:8]}-{date_str}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"✅ Exported to: {output_file}")
    print(f"   Size: {len(md_content) / 1024:.1f} KB")

if __name__ == '__main__':
    main()
