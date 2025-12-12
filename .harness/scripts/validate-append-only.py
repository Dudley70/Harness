#!/usr/bin/env python3
"""
Validate append-only files haven't had content removed.

This script checks staged changes against append-only rules:
- next_session_actions in project-state.yaml: no task removals
- decision-log.md: no decision removals
- lessons-learned.md: no lesson removals
- ideas.yaml: no idea removals
- questions.yaml: no question removals

Usage:
    python3 validate-append-only.py           # Check staged changes
    python3 validate-append-only.py --audit   # Audit full git history
"""

import subprocess
import sys
import re
from pathlib import Path

# Files and their append-only patterns
APPEND_ONLY_RULES = {
    '.harness/project-state.yaml': {
        'name': 'Task items',
        'pattern': r'"P[0-2]:',  # Lines containing P0/P1/P2: task markers
        'section': 'next_session_actions',
    },
    '.harness/decision-log.md': {
        'name': 'Decisions',
        'pattern': r'^## Decision #\d+',
        'section': None,
    },
    '.harness/lessons-learned.md': {
        'name': 'Lessons',
        'pattern': r'^## Lesson #\d+',
        'section': None,
    },
    '.harness/ideas.yaml': {
        'name': 'Ideas',
        'pattern': r'^  [a-z_]+:$',  # Top-level idea keys
        'section': 'ideas',
    },
    '.harness/questions.yaml': {
        'name': 'Questions',
        'pattern': r'^  Q\d+:',
        'section': 'questions',
    },
}


def get_staged_diff(file_path: str) -> str:
    """Get the staged diff for a file."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def get_deletions_from_diff(diff: str, pattern: str) -> list[str]:
    """Extract deleted lines matching pattern from diff."""
    deletions = []
    for line in diff.split('\n'):
        # Lines starting with - (but not ---) are deletions
        if line.startswith('-') and not line.startswith('---'):
            # Remove the leading -
            content = line[1:]
            if re.search(pattern, content):
                deletions.append(content.strip())
    return deletions


def check_staged_changes() -> tuple[bool, list[str]]:
    """Check staged changes for violations."""
    violations = []

    for file_path, rules in APPEND_ONLY_RULES.items():
        diff = get_staged_diff(file_path)
        if not diff:
            continue

        deletions = get_deletions_from_diff(diff, rules['pattern'])

        # Filter out DONE/OBSOLETE markers (these are allowed)
        real_deletions = [
            d for d in deletions
            if 'DONE:' not in d and 'OBSOLETE:' not in d
        ]

        if real_deletions:
            violations.append(f"\n{rules['name']} removed from {file_path}:")
            for d in real_deletions:
                violations.append(f"  - {d}")

    return len(violations) == 0, violations


def audit_git_history() -> dict[str, list[str]]:
    """Audit full git history for all deletions."""
    all_deletions = {}

    for file_path, rules in APPEND_ONLY_RULES.items():
        try:
            result = subprocess.run(
                ['git', 'log', '-p', '--all', '--', file_path],
                capture_output=True,
                text=True,
                check=True
            )

            deletions = get_deletions_from_diff(result.stdout, rules['pattern'])

            # Filter out DONE/OBSOLETE
            real_deletions = [
                d for d in deletions
                if 'DONE:' not in d and 'OBSOLETE:' not in d
            ]

            if real_deletions:
                all_deletions[file_path] = list(set(real_deletions))  # Dedupe

        except subprocess.CalledProcessError:
            continue

    return all_deletions


def main():
    if '--audit' in sys.argv:
        print("Auditing full git history for append-only violations...\n")
        deletions = audit_git_history()

        if not deletions:
            print("No violations found in git history.")
            return 0

        total = 0
        for file_path, items in deletions.items():
            rules = APPEND_ONLY_RULES[file_path]
            print(f"\n{rules['name']} deleted from {file_path}: ({len(items)} items)")
            for item in sorted(items):
                print(f"  - {item}")
            total += len(items)

        print(f"\n TOTAL: {total} items deleted across history")
        return 1

    else:
        # Check staged changes (for pre-commit hook)
        passed, violations = check_staged_changes()

        if passed:
            print("Append-only validation passed.")
            return 0

        print("APPEND-ONLY VIOLATION DETECTED!")
        print("=" * 50)
        for v in violations:
            print(v)
        print("\n" + "=" * 50)
        print("Items cannot be removed from append-only files.")
        print("Mark as DONE: or OBSOLETE: instead of deleting.")
        print("\nTo bypass (NOT recommended): git commit --no-verify")
        return 1


if __name__ == '__main__':
    sys.exit(main())
