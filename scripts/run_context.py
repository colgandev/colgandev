#!/usr/bin/env python3
"""
Run aider with configuration from markdown context files.

Context files are markdown with YAML frontmatter that specify aider configuration
and provide initial conversation context.
"""

import subprocess
import sys
from pathlib import Path

import click
import frontmatter


def build_aider_command(config: dict, context_prompt: str, additional_prompt: str = "") -> list[str]:
    """Build aider command from config and prompts."""
    cmd = ['aider']
    
    # Add files and read-only files
    for file_pattern in config.get('file', []):
        cmd.extend(['--file', str(file_pattern)])
    for file_pattern in config.get('read', []):
        cmd.extend(['--read', str(file_pattern)])
    
    # Add model if specified
    if 'model' in config:
        cmd.extend(['--model', config['model']])
    
    # Add boolean flags
    boolean_flags = ['cache-prompts', 'auto-commits', 'auto-lint', 'auto-test', 'pretty', 'dark-mode']
    for flag in boolean_flags:
        if config.get(flag):
            cmd.append(f'--{flag}')
    
    # Add string options
    string_options = ['lint-cmd', 'test-cmd', 'editor', 'code-theme']
    for option in string_options:
        if option in config:
            cmd.extend([f'--{option}', str(config[option])])
    
    # Combine prompts
    full_prompt = context_prompt
    if additional_prompt:
        full_prompt = f"{context_prompt}\n\n---\n\n{additional_prompt}" if context_prompt else additional_prompt
    
    if full_prompt:
        cmd.extend(['--message', full_prompt])
    
    return cmd


@click.group(invoke_without_command=True)
@click.argument('context_file', type=click.Path(exists=True, path_type=Path), required=False)
@click.argument('prompt', required=False)
@click.option('--dry-run', is_flag=True, help='Show the aider command without running it')
@click.pass_context
def cli(ctx, context_file, prompt, dry_run):
    """Run aider with configuration from markdown context files."""
    if ctx.invoked_subcommand is not None:
        return
    
    if not context_file:
        click.echo("Error: context_file is required")
        ctx.exit(1)
    
    # Parse the context file using frontmatter library
    try:
        post = frontmatter.load(context_file)
        config = post.metadata
        context_prompt = post.content.strip()
    except Exception as e:
        click.echo(f"Error parsing context file {context_file}: {e}")
        ctx.exit(1)
    
    # Build and execute aider command
    aider_cmd = build_aider_command(config, context_prompt, prompt or "")
    
    if dry_run:
        click.echo("Would execute:")
        click.echo(" ".join(f'"{arg}"' if ' ' in arg else arg for arg in aider_cmd))
        return
    
    try:
        click.echo(f"Running aider with context from {context_file}")
        if prompt:
            click.echo(f"Additional prompt: {prompt}")
        click.echo()
        
        subprocess.run(aider_cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        click.echo(f"Aider exited with error code {e.returncode}")
        ctx.exit(e.returncode)
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user")
        ctx.exit(1)
    except FileNotFoundError:
        click.echo("Error: aider command not found. Make sure aider is installed and in your PATH.")
        ctx.exit(1)


@cli.command()
def list_contexts():
    """List available context files in contexts/ directory."""
    contexts_dir = Path('contexts')
    if contexts_dir.exists():
        context_files = list(contexts_dir.glob('*.md'))
        if context_files:
            click.echo("Available context files:")
            for file in sorted(context_files):
                click.echo(f"  {file}")
        else:
            click.echo("No context files found in contexts/ directory")
    else:
        click.echo("contexts/ directory not found")


if __name__ == '__main__':
    cli()
