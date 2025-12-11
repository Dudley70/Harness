#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atom Extraction for Harness Knowledge System.

Extracts atomic knowledge units from session transcripts using taxonomy.yaml.
Outputs to .harness/atoms.jsonl for queryable knowledge base.

Usage: python extract-atoms.py [--reprocess]
  --reprocess: Ignore processed state, reprocess all transcripts
"""

import sys
import json
import os
import re
import yaml
import uuid
from pathlib import Path
from datetime import datetime
from collections import Counter

def load_taxonomy():
    """Load taxonomy from YAML file."""
    taxonomy_path = Path('.harness/taxonomy.yaml')
    if not taxonomy_path.exists():
        print("❌ Error: .harness/taxonomy.yaml not found")
        sys.exit(1)

    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_atom_store_path():
    """Get path to atom store."""
    return Path('.harness/atoms.jsonl')

def get_extraction_state_path():
    """Get path to extraction state file."""
    return Path('.harness/extraction-state.json')

def load_extraction_state():
    """Load state of which transcripts have been processed."""
    state_path = get_extraction_state_path()
    if state_path.exists():
        with open(state_path, 'r') as f:
            return json.load(f)
    return {'processed_transcripts': {}}

def save_extraction_state(state):
    """Save extraction state."""
    state_path = get_extraction_state_path()
    state['last_extraction'] = datetime.now().isoformat()
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)

def extract_text_from_transcript(transcript_path):
    """Extract message content from markdown transcript."""
    messages = []

    with open(transcript_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract session metadata
    session_id = transcript_path.stem  # e.g., auto-recovery-20251211-172639

    # Parse the transcript sections
    # Look for User/Assistant message blocks
    message_pattern = r'#### (👤 User|🤖 Assistant)\n\n(.*?)(?=\n---|\n####|\Z)'
    matches = re.findall(message_pattern, content, re.DOTALL)

    for role, text in matches:
        msg_type = 'user' if 'User' in role else 'assistant'
        messages.append({
            'type': msg_type,
            'content': text.strip(),
            'session_id': session_id
        })

    return messages, session_id

def classify_message(content, taxonomy):
    """Classify a message using taxonomy triggers. Returns list of matching types."""
    matches = []
    content_lower = content.lower()

    # Check core types
    for type_name, rules in taxonomy['types']['core'].items():
        triggers = rules.get('triggers', [])
        patterns = rules.get('patterns', [])

        # Check triggers (simple substring match)
        if any(trigger.lower() in content_lower for trigger in triggers):
            matches.append({
                'type': type_name,
                'tier': 'core',
                'confidence': rules.get('confidence', 'high')
            })
            continue

        # Check regex patterns
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                matches.append({
                    'type': type_name,
                    'tier': 'core',
                    'confidence': rules.get('confidence', 'medium')
                })
                break

    # Check domain types
    for type_name, rules in taxonomy['types']['domain'].items():
        triggers = rules.get('triggers', [])

        if any(trigger.lower() in content_lower for trigger in triggers):
            matches.append({
                'type': type_name,
                'tier': 'domain',
                'confidence': rules.get('confidence', 'medium')
            })

    # Check catch-all if nothing else matched
    if not matches:
        catch_all = taxonomy['types']['catch_all'].get('UNCLASSIFIED', {})
        triggers = catch_all.get('triggers', [])
        if any(trigger.lower() in content_lower for trigger in triggers):
            matches.append({
                'type': 'UNCLASSIFIED',
                'tier': 'catch_all',
                'confidence': 'low'
            })

    return matches

def extract_keywords(content, taxonomy):
    """Extract matching keywords from content."""
    found = []
    content_lower = content.lower()

    # Check project keywords
    for kw in taxonomy['keywords'].get('project', []):
        if kw.lower() in content_lower:
            found.append(kw)

    # Check user-added keywords
    for kw in taxonomy['keywords'].get('user_added', []):
        if kw.lower() in content_lower:
            found.append(kw)

    # Check auto-extracted keywords
    for item in taxonomy['keywords'].get('auto_extracted', []):
        if isinstance(item, dict):
            kw = item.get('term', '')
        else:
            kw = item
        if kw and kw.lower() in content_lower:
            found.append(kw)

    return list(set(found))

def create_atom(message, classifications, keywords, session_id, context_before=None, context_after=None):
    """Create an atom record."""
    return {
        'id': str(uuid.uuid4())[:8],
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'source': message['type'],  # user or assistant
        'types': [c['type'] for c in classifications],
        'primary_type': classifications[0]['type'] if classifications else None,
        'confidence': classifications[0]['confidence'] if classifications else None,
        'keywords': keywords,
        'content': message['content'][:1000],  # Truncate very long content
        'content_full': message['content'] if len(message['content']) <= 2000 else message['content'][:2000] + '...[truncated]',
        'context_before': context_before[:500] if context_before else None,
        'context_after': context_after[:500] if context_after else None
    }

def process_transcript(transcript_path, taxonomy, settings):
    """Process a single transcript and extract atoms."""
    atoms = []

    messages, session_id = extract_text_from_transcript(transcript_path)

    if not messages:
        return atoms, session_id

    context_lines_before = settings.get('context_lines_before', 2)
    context_lines_after = settings.get('context_lines_after', 2)
    min_atom_length = settings.get('min_atom_length', 10)

    for i, message in enumerate(messages):
        content = message['content']

        # Skip very short messages
        if len(content) < min_atom_length:
            continue

        # Classify the message
        classifications = classify_message(content, taxonomy)

        # Only create atom if there's a classification
        if classifications:
            keywords = extract_keywords(content, taxonomy)

            # Get context
            context_before = messages[i-1]['content'] if i > 0 else None
            context_after = messages[i+1]['content'] if i < len(messages) - 1 else None

            atom = create_atom(
                message,
                classifications,
                keywords,
                session_id,
                context_before,
                context_after
            )
            atoms.append(atom)

    return atoms, session_id

def append_atoms_to_store(atoms, store_path):
    """Append atoms to the JSONL store."""
    store_path.parent.mkdir(parents=True, exist_ok=True)

    with open(store_path, 'a', encoding='utf-8') as f:
        for atom in atoms:
            f.write(json.dumps(atom) + '\n')

def generate_summary(all_atoms):
    """Generate a summary of extracted atoms."""
    if not all_atoms:
        return "No atoms extracted."

    type_counts = Counter(a['primary_type'] for a in all_atoms if a['primary_type'])
    keyword_counts = Counter(kw for a in all_atoms for kw in a['keywords'])
    session_counts = Counter(a['session_id'] for a in all_atoms)

    lines = [
        f"",
        f"📊 EXTRACTION SUMMARY",
        f"=" * 40,
        f"",
        f"Total atoms extracted: {len(all_atoms)}",
        f"Sessions processed: {len(session_counts)}",
        f"",
        f"By Type:",
    ]

    for type_name, count in type_counts.most_common():
        lines.append(f"  {type_name}: {count}")

    lines.append(f"")
    lines.append(f"Top Keywords:")
    for kw, count in keyword_counts.most_common(10):
        lines.append(f"  {kw}: {count}")

    lines.append(f"")
    lines.append(f"By Session:")
    for session, count in session_counts.most_common():
        lines.append(f"  {session}: {count} atoms")

    return '\n'.join(lines)

def main():
    reprocess = '--reprocess' in sys.argv

    print("🔬 Harness Atom Extraction")
    print("=" * 40)

    # Load taxonomy
    taxonomy = load_taxonomy()
    settings = taxonomy.get('settings', {})
    print(f"✅ Loaded taxonomy (v{taxonomy.get('_meta', {}).get('version', '?')})")

    # Find transcripts
    transcript_dir = Path('.harness/transcripts')
    if not transcript_dir.exists():
        print("❌ No transcripts directory found")
        return

    transcripts = sorted(transcript_dir.glob('auto-recovery-*.md'))
    print(f"📁 Found {len(transcripts)} transcript(s)")

    # Load state
    state = load_extraction_state()
    processed = state.get('processed_transcripts', {})

    if reprocess:
        print("🔄 Reprocess mode: ignoring previous state")
        processed = {}
        # Clear existing atoms
        atom_store = get_atom_store_path()
        if atom_store.exists():
            atom_store.unlink()
            print("   Cleared existing atom store")

    # Process each transcript
    all_atoms = []
    new_transcripts = 0

    for transcript_path in transcripts:
        transcript_key = str(transcript_path)

        # Skip already processed (unless reprocessing)
        if transcript_key in processed and not reprocess:
            continue

        print(f"\n📄 Processing: {transcript_path.name}")

        atoms, session_id = process_transcript(transcript_path, taxonomy, settings)

        if atoms:
            all_atoms.extend(atoms)
            print(f"   Extracted {len(atoms)} atom(s)")

            # Show sample
            type_summary = Counter(a['primary_type'] for a in atoms)
            for t, c in type_summary.most_common(3):
                print(f"     - {t}: {c}")
        else:
            print(f"   No atoms extracted")

        # Mark as processed
        processed[transcript_key] = {
            'processed_at': datetime.now().isoformat(),
            'atoms_count': len(atoms)
        }
        new_transcripts += 1

    # Save atoms
    if all_atoms:
        atom_store = get_atom_store_path()
        append_atoms_to_store(all_atoms, atom_store)
        print(f"\n💾 Saved {len(all_atoms)} atoms to {atom_store}")

    # Save state
    state['processed_transcripts'] = processed
    save_extraction_state(state)

    # Generate summary
    if all_atoms:
        print(generate_summary(all_atoms))
    elif new_transcripts == 0:
        print("\n✅ All transcripts already processed. Use --reprocess to re-extract.")
    else:
        print("\n⚠️ No atoms extracted from new transcripts")

    print(f"\n✅ Done")

if __name__ == '__main__':
    main()
