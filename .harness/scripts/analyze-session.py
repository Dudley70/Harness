#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze Claude Code session JSONL files to understand content breakdown."""

import sys
import json

def analyze_session(filepath):
    user_text = 0
    user_tool_results = 0
    assistant_text = 0
    assistant_tool_calls = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get('type') == 'user':
                    content = d.get('message', {}).get('content', '')
                    if isinstance(content, str):
                        user_text += len(content)
                    elif isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict):
                                if item.get('type') == 'tool_result':
                                    user_tool_results += len(str(item))
                                elif item.get('type') == 'text':
                                    user_text += len(item.get('text', ''))
                            else:
                                user_text += len(str(item))
                elif d.get('type') == 'assistant':
                    content = d.get('message', {}).get('content', [])
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'tool_use':
                                assistant_tool_calls += len(str(item))
                            elif item.get('type') == 'text':
                                assistant_text += len(item.get('text', ''))
            except Exception as e:
                pass

    print('=== CONTENT BREAKDOWN ===')
    print(f'User actual text:      {user_text/1024:.1f} KB')
    print(f'User tool results:     {user_tool_results/1024:.1f} KB')
    print(f'Assistant text:        {assistant_text/1024:.1f} KB')
    print(f'Assistant tool calls:  {assistant_tool_calls/1024:.1f} KB')
    print()
    print(f'HUMAN-READABLE (text): {(user_text + assistant_text)/1024:.1f} KB')
    print(f'MACHINE (tools):       {(user_tool_results + assistant_tool_calls)/1024:.1f} KB')
    print(f'TOTAL content:         {(user_text + assistant_text + user_tool_results + assistant_tool_calls)/1024:.1f} KB')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze-session.py <session.jsonl>")
        sys.exit(1)
    analyze_session(sys.argv[1])
