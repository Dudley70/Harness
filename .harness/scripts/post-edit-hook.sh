#!/bin/bash
# Post-Edit Hook for Document Integrity Validation (D17)
# Triggers real-time validation after Edit/Write to .harness/ or 00-governance/

# Read stdin JSON
INPUT=$(cat)

# Extract file path from tool_input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
    exit 0  # No file path, skip
fi

# Check if file is in monitored directories
if [[ "$FILE_PATH" == *".harness/"* ]] || [[ "$FILE_PATH" == *"00-governance/"* ]]; then
    # Get project directory
    PROJECT_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
    if [ -z "$PROJECT_DIR" ]; then
        PROJECT_DIR="$CLAUDE_PROJECT_DIR"
    fi

    # Make file path relative to project
    REL_PATH="${FILE_PATH#$PROJECT_DIR/}"

    # Run validation
    if [ -f "$PROJECT_DIR/.harness/scripts/validate-integrity.py" ]; then
        python3 "$PROJECT_DIR/.harness/scripts/validate-integrity.py" --realtime "$REL_PATH" 2>&1
        EXIT_CODE=$?

        if [ $EXIT_CODE -eq 2 ]; then
            # Critical error - return blocking message
            echo '{"decision": "block", "reason": "Document integrity violation detected. Check the warning above."}'
            exit 0
        elif [ $EXIT_CODE -eq 1 ]; then
            # Warning - allow but inform
            echo '{"decision": "allow", "hookSpecificOutput": {"warning": "Document integrity warning - see output above"}}'
            exit 0
        fi
    fi
fi

# No issues
exit 0
