#!/bin/bash

# prompt_aider.sh - Interactive script to craft precise aider commands

set -euo pipefail

# Initialize arrays for files
EDITABLE_FILES=()
READONLY_FILES=()
SYSTEM_PROMPT=""
AIDER_ARGS=()

# Function to display usage
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -s <prompt>    System prompt to use"
    echo "  -e <file>      Add editable file (can be used multiple times)"
    echo "  -r <file>      Add read-only file (can be used multiple times)"
    echo "  -a <args>      Additional aider arguments"
    echo "  -h             Show this help"
    echo ""
    echo "Interactive mode will prompt for files if none provided via options."
    exit 1
}

# Function to add files interactively
add_files_interactive() {
    local file_type="$1"
    local array_name="$2"

    echo "Enter $file_type files (one per line, empty line to finish):"
    while IFS= read -r file; do
        [[ -z "$file" ]] && break

        if [[ ! -f "$file" ]]; then
            echo "Warning: File '$file' not found. Continue anyway? (y/N)"
            read -r confirm
            [[ "$confirm" != [yY] ]] && continue
        fi

        if [[ "$array_name" == "EDITABLE_FILES" ]]; then
            EDITABLE_FILES+=("$file")
        else
            READONLY_FILES+=("$file")
        fi

        echo "Added: $file"
    done
}

# Function to list current files
list_files() {
    echo "Current file selection:"
    if [[ ${#EDITABLE_FILES[@]} -gt 0 ]]; then
        echo "  Editable files:"
        printf "    %s\n" "${EDITABLE_FILES[@]}"
    fi
    if [[ ${#READONLY_FILES[@]} -gt 0 ]]; then
        echo "  Read-only files:"
        printf "    %s\n" "${READONLY_FILES[@]}"
    fi
    if [[ ${#EDITABLE_FILES[@]} -eq 0 && ${#READONLY_FILES[@]} -eq 0 ]]; then
        echo "  No files selected"
    fi
    echo
}

# Function to get user prompt
get_user_prompt() {
    echo "Enter your prompt (paste content, then press Ctrl+D on a new line):"
    echo "----------------------------------------"

    # Read all input until EOF
    USER_PROMPT=$(cat)

    echo "----------------------------------------"
    echo "Prompt received (${#USER_PROMPT} characters)"
    echo
}

# Function to preview and confirm command
preview_command() {
    echo "Aider command that will be executed:"
    echo "======================================"

    local cmd="aider"

    # Add system prompt if provided
    [[ -n "$SYSTEM_PROMPT" ]] && cmd+=" --message"

    # Add editable files
    for file in "${EDITABLE_FILES[@]}"; do
        cmd+=" --file \"$file\""
    done

    # Add read-only files
    for file in "${READONLY_FILES[@]}"; do
        cmd+=" --read \"$file\""
    done

    # Add additional args
    for arg in "${AIDER_ARGS[@]}"; do
        cmd+=" $arg"
    done

    echo "$cmd"
    echo "======================================"
    echo
    echo "User prompt:"
    echo "------------"
    echo "$USER_PROMPT"
    echo "------------"
    echo
}

# Function to execute aider
execute_aider() {
    local aider_cmd=(aider)

    # Add editable files
    for file in "${EDITABLE_FILES[@]}"; do
        aider_cmd+=(--file "$file")
    done

    # Add read-only files
    for file in "${READONLY_FILES[@]}"; do
        aider_cmd+=(--read "$file")
    done

    # Add additional arguments
    for arg in "${AIDER_ARGS[@]}"; do
        aider_cmd+=($arg)
    done

    # Combine system prompt and user prompt
    local combined_prompt="$USER_PROMPT"
    if [[ -n "$SYSTEM_PROMPT" ]]; then
        combined_prompt="SYSTEM: $SYSTEM_PROMPT

USER: $USER_PROMPT"
    fi

    # Add the message
    aider_cmd+=(--message "$combined_prompt")

    echo "Executing aider..."
    echo
    "${aider_cmd[@]}"
}

# Parse command line arguments
while getopts "s:e:r:a:h" opt; do
    case $opt in
    s)
        SYSTEM_PROMPT="$OPTARG"
        ;;
    e)
        EDITABLE_FILES+=("$OPTARG")
        ;;
    r)
        READONLY_FILES+=("$OPTARG")
        ;;
    a)
        AIDER_ARGS+=("$OPTARG")
        ;;
    h)
        usage
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        usage
        ;;
    esac
done

# Main interactive flow
echo "=== Aider Helper Script ==="
echo

# If no files provided via command line, enter interactive mode
if [[ ${#EDITABLE_FILES[@]} -eq 0 && ${#READONLY_FILES[@]} -eq 0 ]]; then
    echo "No files specified. Entering interactive mode..."
    echo

    while true; do
        list_files
        echo "Options:"
        echo "  e) Add editable files"
        echo "  r) Add read-only files"
        echo "  l) List current files"
        echo "  c) Clear all files"
        echo "  d) Done with file selection"
        echo

        read -p "Choose option: " choice

        case $choice in
        e | E)
            add_files_interactive "editable" "EDITABLE_FILES"
            ;;
        r | R)
            add_files_interactive "read-only" "READONLY_FILES"
            ;;
        l | L)
            list_files
            ;;
        c | C)
            EDITABLE_FILES=()
            READONLY_FILES=()
            echo "All files cleared."
            ;;
        d | D)
            break
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
        esac
        echo
    done
fi

# Show final file selection
list_files

# Get system prompt if not provided
if [[ -z "$SYSTEM_PROMPT" ]]; then
    read -p "Enter system prompt (optional, press Enter to skip): " SYSTEM_PROMPT
    echo
fi

# Get user prompt
get_user_prompt

# Preview and confirm
preview_command

read -p "Execute this command? (Y/n): " confirm
if [[ "$confirm" == [nN] ]]; then
    echo "Aborted."
    exit 0
fi

# Execute aider
execute_aider
