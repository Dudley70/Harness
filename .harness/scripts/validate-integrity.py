#!/usr/bin/env python3
"""
Harness Document Integrity Validator

Validates document integrity based on rules in document-controls.yaml.
This is core infrastructure for Harness - files ARE the memory.

Usage:
    python3 validate-integrity.py              # Check staged changes (pre-commit)
    python3 validate-integrity.py --audit      # Audit full git history
    python3 validate-integrity.py --check      # Check protected files exist
    python3 validate-integrity.py --full       # Run all checks
    python3 validate-integrity.py --realtime FILE  # Real-time check for PostToolUse hook

See Decision #16, #17 in decision-log.md for rationale.
"""

import subprocess
import sys
import re
import fnmatch
from pathlib import Path
from typing import Optional

# Try to import yaml, fall back to basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def find_project_root() -> Path:
    """Find the project root by looking for .harness directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / '.harness').is_dir():
            return current
        current = current.parent
    return Path.cwd()


def load_config(project_root: Path) -> dict:
    """Load document-controls.yaml config."""
    config_path = project_root / '.harness' / 'document-controls.yaml'

    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        print("Document integrity cannot be validated without document-controls.yaml")
        sys.exit(1)

    with open(config_path, 'r') as f:
        content = f.read()

    if HAS_YAML:
        return yaml.safe_load(content)
    else:
        # Basic fallback - just check if file exists
        print("WARNING: PyYAML not installed. Using basic validation only.")
        return {'append_only': {}, 'immutable': {}, 'protected': [], 'free': []}


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


def get_full_diff(file_path: str) -> str:
    """Get the full git history diff for a file."""
    try:
        result = subprocess.run(
            ['git', 'log', '-p', '--all', '--', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def get_deletions_from_diff(diff: str, pattern: str, status_prefixes: list[str]) -> list[str]:
    """Extract deleted lines matching pattern from diff, excluding status changes."""
    deletions = []
    for line in diff.split('\n'):
        # Lines starting with - (but not ---) are deletions
        if line.startswith('-') and not line.startswith('---'):
            content = line[1:].strip()
            if re.search(pattern, content):
                # Check if this is a status change (allowed)
                is_status_change = any(prefix in content for prefix in status_prefixes)
                if not is_status_change:
                    deletions.append(content)
    return deletions


def check_append_only(config: dict, project_root: Path, audit: bool = False) -> tuple[bool, list[str]]:
    """Check append-only rules."""
    violations = []
    status_prefixes = config.get('status_prefixes', [])
    append_only = config.get('append_only', {})

    for file_path, rules in append_only.items():
        if isinstance(rules, dict):
            # File has sections or direct pattern
            if 'sections' in rules:
                for section_name, section_rules in rules['sections'].items():
                    pattern = section_rules.get('pattern', '.*')
                    diff = get_full_diff(file_path) if audit else get_staged_diff(file_path)
                    if diff:
                        deletions = get_deletions_from_diff(diff, pattern, status_prefixes)
                        if deletions:
                            violations.append(f"\n[APPEND-ONLY VIOLATION] {file_path} ({section_name}):")
                            for d in deletions[:10]:  # Limit output
                                violations.append(f"  - {d[:80]}...")
                            if len(deletions) > 10:
                                violations.append(f"  ... and {len(deletions) - 10} more")
            elif 'pattern' in rules:
                pattern = rules['pattern']
                diff = get_full_diff(file_path) if audit else get_staged_diff(file_path)
                if diff:
                    deletions = get_deletions_from_diff(diff, pattern, status_prefixes)
                    if deletions:
                        violations.append(f"\n[APPEND-ONLY VIOLATION] {file_path}:")
                        for d in deletions[:10]:
                            violations.append(f"  - {d[:80]}...")
                        if len(deletions) > 10:
                            violations.append(f"  ... and {len(deletions) - 10} more")
        else:
            # Simple true/false - protect entire file
            diff = get_full_diff(file_path) if audit else get_staged_diff(file_path)
            if diff:
                # Any deletion is a violation
                deletions = [l[1:].strip() for l in diff.split('\n')
                            if l.startswith('-') and not l.startswith('---') and l[1:].strip()]
                # Filter out status changes
                real_deletions = [d for d in deletions
                                 if not any(prefix in d for prefix in status_prefixes)]
                if real_deletions:
                    violations.append(f"\n[APPEND-ONLY VIOLATION] {file_path}:")
                    for d in real_deletions[:5]:
                        violations.append(f"  - {d[:80]}...")

    return len(violations) == 0, violations


def check_immutable(config: dict, project_root: Path) -> tuple[bool, list[str]]:
    """Check immutable rules - files cannot be modified at all."""
    violations = []
    immutable = config.get('immutable', {})

    for file_pattern, rules in immutable.items():
        # Handle glob patterns
        if '*' in file_pattern:
            # For now, just check if any matching files are being modified
            diff = get_staged_diff(file_pattern)
        else:
            diff = get_staged_diff(file_pattern)

        if diff:
            violations.append(f"\n[IMMUTABLE VIOLATION] {file_pattern}:")
            violations.append(f"  This file cannot be modified. It is marked as immutable.")
            violations.append(f"  To append new entries, use a different approach (e.g., new atoms).")

    return len(violations) == 0, violations


def check_protected_exist(config: dict, project_root: Path) -> tuple[bool, list[str]]:
    """Check that protected files exist."""
    warnings = []
    protected = config.get('protected', [])

    for file_path in protected:
        full_path = project_root / file_path
        if not full_path.exists():
            warnings.append(f"[MISSING] Protected file does not exist: {file_path}")

    return len(warnings) == 0, warnings


def check_unregistered(config: dict, project_root: Path) -> tuple[bool, list[str]]:
    """Check for unregistered files in monitored directories."""
    warnings = []
    validation = config.get('validation', {})

    if not validation.get('warn_unregistered', True):
        return True, []

    # Collect all registered files
    registered = set()

    for file_path in config.get('append_only', {}).keys():
        registered.add(file_path)
    for file_path in config.get('immutable', {}).keys():
        registered.add(file_path)
    for file_path in config.get('protected', []):
        registered.add(file_path)
    for pattern in config.get('free', []):
        registered.add(pattern)

    # Get ignore patterns
    ignore_patterns = validation.get('ignore_patterns', [])

    # Scan directories
    scan_dirs = validation.get('scan_directories', ['.harness/'])

    for scan_dir in scan_dirs:
        scan_path = project_root / scan_dir
        if not scan_path.exists():
            continue

        for file_path in scan_path.rglob('*'):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(project_root))

                # Check if ignored
                should_ignore = False
                for pattern in ignore_patterns:
                    if fnmatch.fnmatch(file_path.name, pattern):
                        should_ignore = True
                        break
                if should_ignore:
                    continue

                # Check if registered (direct or via glob)
                is_registered = False
                for reg_pattern in registered:
                    if '*' in reg_pattern:
                        if fnmatch.fnmatch(rel_path, reg_pattern):
                            is_registered = True
                            break
                    elif rel_path == reg_pattern:
                        is_registered = True
                        break

                if not is_registered:
                    warnings.append(f"[UNREGISTERED] {rel_path}")

    return len(warnings) == 0, warnings


def check_content_location(config: dict, project_root: Path, file_path: str, content: str = None) -> tuple[bool, list[str]]:
    """
    Check if content is in the correct location (D17).
    Warns if content type markers appear in wrong files.
    """
    warnings = []
    locations = config.get('locations', {})

    # Read file content if not provided
    if content is None:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
            except:
                return True, []
        else:
            return True, []

    # Check for misplaced content
    content_markers = {
        'decisions': (r'## Decision #\d+', '.harness/decision-log.md'),
        'lessons': (r'## Lesson #\d+', '.harness/lessons-learned.md'),
        'tasks': (r'"P[0-2]:', '.harness/project-state.yaml'),
    }

    for content_type, (pattern, expected_file) in content_markers.items():
        if re.search(pattern, content):
            if file_path != expected_file and not file_path.endswith(expected_file):
                loc_config = locations.get(content_type, {})
                expected = loc_config.get('file', expected_file)
                warnings.append(
                    f"[WRONG LOCATION] {content_type} content found in {file_path}\n"
                    f"  → Should be in: {expected}\n"
                    f"  → See: document-controls.yaml locations.{content_type}"
                )

    return len(warnings) == 0, warnings


def check_registration(config: dict, project_root: Path, file_path: str) -> tuple[bool, list[str]]:
    """
    Check if file is registered in PROJECT-MAP.md (D17).
    """
    warnings = []
    registration = config.get('registration', {})

    if not registration:
        return True, []

    index_file = registration.get('index_file', '.harness/PROJECT-MAP.md')
    required_for = registration.get('required_for', [])
    excludes = registration.get('excludes', [])

    # Check if file matches required patterns
    needs_registration = False
    for pattern in required_for:
        if fnmatch.fnmatch(file_path, pattern):
            needs_registration = True
            break

    # Check if excluded
    for pattern in excludes:
        if fnmatch.fnmatch(file_path, pattern):
            needs_registration = False
            break

    if not needs_registration:
        return True, []

    # Check if registered in index file
    index_path = project_root / index_file
    if not index_path.exists():
        warnings.append(f"[NO INDEX] Index file {index_file} does not exist")
        return False, warnings

    try:
        with open(index_path, 'r') as f:
            index_content = f.read()

        # Check if file is mentioned (by name or path)
        file_name = Path(file_path).name
        if file_path not in index_content and file_name not in index_content:
            warnings.append(
                f"[NOT REGISTERED] {file_path} is not in {index_file}\n"
                f"  → Add it to PROJECT-MAP.md for discoverability\n"
                f"  → Or add to registration.excludes if intentional"
            )
    except:
        pass

    return len(warnings) == 0, warnings


def validate_realtime(config: dict, project_root: Path, file_path: str) -> int:
    """
    Real-time validation for PostToolUse hook (D17).
    Returns exit code (0 = pass, 1 = warnings, 2 = errors).
    """
    all_warnings = []
    has_errors = False

    # Check content location
    passed, messages = check_content_location(config, project_root, file_path)
    if not passed:
        all_warnings.extend(messages)

    # Check registration
    passed, messages = check_registration(config, project_root, file_path)
    if not passed:
        all_warnings.extend(messages)

    # Check append-only (if file is in config)
    append_only = config.get('append_only', {})
    if file_path in append_only or any(file_path.endswith(k) for k in append_only.keys()):
        # Get unstaged diff for this file
        try:
            result = subprocess.run(
                ['git', 'diff', '--', file_path],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            if result.stdout:
                status_prefixes = config.get('status_prefixes', [])
                deletions = get_deletions_from_diff(result.stdout, '.*', status_prefixes)
                if deletions:
                    has_errors = True
                    all_warnings.append(f"[APPEND-ONLY] Deletions detected in {file_path}")
                    for d in deletions[:3]:
                        all_warnings.append(f"  - {d[:60]}...")
        except:
            pass

    if all_warnings:
        print("\n⚠️  DOCUMENT INTEGRITY WARNING")
        print("=" * 50)
        for msg in all_warnings:
            print(msg)
        print("=" * 50)
        return 2 if has_errors else 1

    return 0


def main():
    project_root = find_project_root()
    config = load_config(project_root)

    audit_mode = '--audit' in sys.argv
    check_mode = '--check' in sys.argv
    full_mode = '--full' in sys.argv
    realtime_mode = '--realtime' in sys.argv

    # Handle realtime mode (D17 - PostToolUse hook)
    if realtime_mode:
        try:
            file_idx = sys.argv.index('--realtime') + 1
            file_path = sys.argv[file_idx] if file_idx < len(sys.argv) else None
            if file_path:
                return validate_realtime(config, project_root, file_path)
            else:
                print("ERROR: --realtime requires a file path")
                return 1
        except (IndexError, ValueError):
            print("ERROR: --realtime requires a file path")
            return 1

    all_passed = True
    all_messages = []

    # Pre-commit mode (default) or audit mode
    if not check_mode or full_mode:
        passed, messages = check_append_only(config, project_root, audit=audit_mode)
        if not passed:
            all_passed = False
            all_messages.extend(messages)

        passed, messages = check_immutable(config, project_root)
        if not passed:
            all_passed = False
            all_messages.extend(messages)

        # Always check for unregistered files in pre-commit mode
        if not audit_mode:
            passed, messages = check_unregistered(config, project_root)
            if not passed:
                print("\n⚠️  UNREGISTERED FILES DETECTED:")
                for msg in messages:
                    print(f"  {msg}")
                print("\n  Add to .harness/document-controls.yaml or the file may be unprotected.")
                print("  See: .claude/skills/harness/document-management/SKILL.md")

    # Check protected files exist
    if check_mode or full_mode:
        passed, messages = check_protected_exist(config, project_root)
        if not passed:
            all_passed = False
            all_messages.extend(messages)

        passed, messages = check_unregistered(config, project_root)
        if not passed:
            # Unregistered is a warning, not a blocker
            print("\n⚠️  WARNINGS:")
            for msg in messages:
                print(f"  {msg}")
            print("\nConsider adding these files to document-controls.yaml")

    if not all_passed:
        print("\n" + "=" * 60)
        print("DOCUMENT INTEGRITY VIOLATION DETECTED")
        print("=" * 60)
        for msg in all_messages:
            print(msg)
        print("\n" + "=" * 60)
        print("Files ARE the memory. Memory corruption = system failure.")
        print("\nTo fix append-only violations:")
        print("  - Mark items as DONE: or OBSOLETE: instead of deleting")
        print("  - Add new items, don't remove old ones")
        print("\nTo bypass (NOT RECOMMENDED): git commit --no-verify")
        print("=" * 60)
        return 1

    if audit_mode:
        print("Audit complete. No violations found in git history.")
    elif check_mode:
        print("Protected file check complete. All files exist.")
    elif full_mode:
        print("Full integrity check complete. All checks passed.")
    else:
        print("Document integrity validation passed.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
