#!/usr/bin/env python3
"""
Run aider with configuration from markdown context files.

Context files are markdown with YAML frontmatter that specify aider configuration
and provide initial conversation context.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


def parse_context_file(file_path: Path) -> tuple[dict, str]:
    """Parse a context file and return (config, markdown_content)."""
    if not file_path.exists():
        print(f"Error: Context file {file_path} not found")
        sys.exit(1)
    
    content = file_path.read_text(encoding='utf-8')
    
    # Check for YAML frontmatter
    if content.startswith('---\n'):
        try:
            # Split on the closing --- 
            parts = content.split('\n---\n', 1)
            if len(parts) != 2:
                # Try alternative format with --- on its own line
                lines = content.split('\n')
                if len(lines) > 2 and lines[0] == '---':
                    # Find closing ---
                    end_idx = None
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            end_idx = i
                            break
                    
                    if end_idx:
                        frontmatter_lines = lines[1:end_idx]
                        content_lines = lines[end_idx + 1:]
                        frontmatter = yaml.safe_load('\n'.join(frontmatter_lines))
                        markdown_content = '\n'.join(content_lines).strip()
                    else:
                        raise ValueError("No closing --- found")
                else:
                    raise ValueError("Invalid frontmatter format")
            else:
                # Standard format: ---\ncontent\n---\nmarkdown
                frontmatter_content = parts[0][4:]  # Remove initial ---\n
                frontmatter = yaml.safe_load(frontmatter_content)
                markdown_content = parts[1].strip()
                
        except (yaml.YAMLError, ValueError) as e:
            print(f"Error parsing frontmatter in {file_path}: {e}")
            sys.exit(1)
    else:
        # No frontmatter, treat entire file as markdown
        frontmatter = {}
        markdown_content = content.strip()
    
    return frontmatter, markdown_content


def build_aider_command(config: dict, context_prompt: str, additional_prompt: str = "") -> list[str]:
    """Build aider command from config and prompts."""
    cmd = ['aider']
    
    # Add files (editable)
    for file_pattern in config.get('file', []):
        cmd.extend(['--file', str(file_pattern)])
    
    # Add read-only files
    for file_pattern in config.get('read', []):
        cmd.extend(['--read', str(file_pattern)])
    
    # Add model if specified
    if 'model' in config:
        cmd.extend(['--model', config['model']])
    
    # Add other boolean flags
    boolean_flags = {
        'cache-prompts': '--cache-prompts',
        'auto-commits': '--auto-commits', 
        'auto-lint': '--auto-lint',
        'auto-test': '--auto-test',
        'pretty': '--pretty',
        'dark-mode': '--dark-mode'
    }
    
    for config_key, flag in boolean_flags.items():
        if config.get(config_key):
            cmd.append(flag)
    
    # Add other string options
    string_options = {
        'lint-cmd': '--lint-cmd',
        'test-cmd': '--test-cmd',
        'editor': '--editor',
        'code-theme': '--code-theme'
    }
    
    for config_key, option in string_options.items():
        if config_key in config:
            cmd.extend([option, str(config[config_key])])
    
    # Combine context and additional prompt
    full_prompt = context_prompt
    if additional_prompt:
        if context_prompt:
            full_prompt += f"\n\n---\n\n{additional_prompt}"
        else:
            full_prompt = additional_prompt
    
    # Add the message
    if full_prompt:
        cmd.extend(['--message', full_prompt])
    
    return cmd


def main():
    parser = argparse.ArgumentParser(
        description='Run aider with configuration from markdown context files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s contexts/auth-feature.md
  %(prog)s contexts/ui-redesign.md "Add dark mode support"
  %(prog)s --list-contexts
  %(prog)s --dry-run contexts/auth-feature.md
        """
    )
    
    parser.add_argument(
        'context_file',
        nargs='?',
        type=Path,
        help='Path to the context file (markdown with YAML frontmatter)'
    )
    
    parser.add_argument(
        'prompt',
        nargs='?',
        help='Additional prompt to add to the context'
    )
    
    parser.add_argument(
        '--list-contexts',
        action='store_true',
        help='List available context files in contexts/ directory'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show the aider command that would be executed without running it'
    )
    
    args = parser.parse_args()
    
    # Handle list contexts
    if args.list_contexts:
        contexts_dir = Path('contexts')
        if contexts_dir.exists():
            context_files = list(contexts_dir.glob('*.md'))
            if context_files:
                print("Available context files:")
                for file in sorted(context_files):
                    print(f"  {file}")
            else:
                print("No context files found in contexts/ directory")
        else:
            print("contexts/ directory not found")
        return
    
    # Require context file for other operations
    if not args.context_file:
        parser.error("context_file is required (unless using --list-contexts)")
    
    # Parse the context file
    config, context_prompt = parse_context_file(args.context_file)
    
    # Build aider command
    aider_cmd = build_aider_command(config, context_prompt, args.prompt or "")
    
    if args.dry_run:
        print("Would execute:")
        print(" ".join(f'"{arg}"' if ' ' in arg else arg for arg in aider_cmd))
        return
    
    # Execute aider
    try:
        print(f"Running aider with context from {args.context_file}")
        if args.prompt:
            print(f"Additional prompt: {args.prompt}")
        print()
        
        subprocess.run(aider_cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Aider exited with error code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: aider command not found. Make sure aider is installed and in your PATH.")
        sys.exit(1)


if __name__ == '__main__':
    main()
