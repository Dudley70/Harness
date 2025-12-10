#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Recovery Analysis for Harness Methodology.

Scans ALL Harness-related project folders for new content since last check.
Runs on SessionStart to:
1. Detect undocumented insights from previous sessions
2. Auto-export new content to markdown transcript

Usage: Called automatically via SessionStart hook, or manually
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

def get_recovery_state_path():
    return Path('.harness/recovery-state.json')

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
                timestamp = entry.get('timestamp', '')

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
                            'line': current_line,
                            'timestamp': timestamp,
                            'source': str(jsonl_path)
                        })
            except:
                continue

    return messages, current_line

def export_new_content_to_transcript(all_new_messages, harness_folders):
    """Export new content to an incremental transcript file."""
    if not all_new_messages:
        return None

    from datetime import datetime

    # Create transcript directory
    transcript_dir = Path('.harness/transcripts')
    transcript_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_file = transcript_dir / f"auto-recovery-{timestamp}.md"

    # Group messages by source
    by_source = {}
    for msg in all_new_messages:
        source = msg['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(msg)

    # Generate markdown
    lines = [
        f"# Auto-Recovered Transcript",
        f"",
        f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Sources:** {len(by_source)} session file(s)",
        f"- **Total Messages:** {len(all_new_messages)}",
        f"",
        f"---",
        f"",
    ]

    for source, messages in by_source.items():
        source_name = Path(source).parent.name
        lines.append(f"## Source: {source_name}")
        lines.append(f"")

        for msg in messages:
            role_emoji = "👤" if msg['type'] == 'user' else "🤖"
            role_name = "User" if msg['type'] == 'user' else "Assistant"
            lines.append(f"### {role_emoji} {role_name}")
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
    """Analyze messages for potentially undocumented insights."""
    findings = []

    decision_keywords = ['decided', 'decision', 'agreed', 'will use', 'chosen', 'selected', 'approved']
    learning_keywords = ['learned', 'discovered', 'found that', 'realized', 'insight', 'key finding']
    research_keywords = ['patterns', 'extracted', 'research', 'analyzed', 'methodology', 'extracted']
    action_keywords = ['todo', 'next step', 'action item', 'should create', 'need to']

    for msg in messages:
        content_lower = msg['content'].lower()

        for kw_list, finding_type in [
            (decision_keywords, 'potential_decision'),
            (learning_keywords, 'potential_learning'),
            (research_keywords, 'potential_research'),
            (action_keywords, 'potential_action'),
        ]:
            if any(kw in content_lower for kw in kw_list):
                findings.append({
                    'type': finding_type,
                    'excerpt': msg['content'][:200],
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

    return unique_findings[:15]  # Limit to top 15

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
    total_new_entries = 0

    for folder in harness_folders:
        session_files = find_session_files(folder)
        for jsonl_path in session_files:
            filepath_key = str(jsonl_path)
            last_line = processed_files.get(filepath_key, 0)

            messages, current_line = extract_new_messages(jsonl_path, last_line)
            new_count = current_line - last_line

            if new_count > 0:
                print(f"   📁 {folder.name}")
                print(f"      └── {jsonl_path.name}: {new_count} new entries")
                all_new_messages.extend(messages)
                total_new_entries += new_count

            # Update processed state
            processed_files[filepath_key] = current_line

    if total_new_entries == 0:
        print("   ✅ No new content since last check")
        save_recovery_state({'processed_files': processed_files})
        return

    print(f"\n   Total: {total_new_entries} new entries across all sessions")

    # Auto-export new content to transcript
    export_file = export_new_content_to_transcript(all_new_messages, harness_folders)
    if export_file:
        print(f"\n   📝 Auto-exported to: {export_file}")

    # Analyze for undocumented content
    findings = analyze_for_undocumented(all_new_messages)

    if findings:
        print(f"\n⚠️  POTENTIAL UNDOCUMENTED ITEMS ({len(findings)}):")
        print("   Review these and document if important:\n")
        for i, f in enumerate(findings, 1):
            source_short = Path(f['source']).parent.name[:30]
            print(f"   {i}. [{f['type'].replace('potential_', '').upper()}] ({source_short})")
            print(f"      {f['excerpt'][:80]}...")
            print()
    else:
        print("   ✅ No obvious undocumented items detected")

    # Save updated state
    save_recovery_state({'processed_files': processed_files})
    print(f"   State saved.")

if __name__ == '__main__':
    main()
