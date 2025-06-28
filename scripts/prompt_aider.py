#!/usr/bin/env python3
"""
Interactive script to craft precise aider commands using click.

Converted from bash version to provide better cross-platform support
and more structured command building.
"""

import subprocess
from pathlib import Path

import click


@click.command()
@click.option('-s', '--system-prompt', help='System prompt to use')
@click.option('-e', '--editable', 'editable_files', multiple=True, help='Add editable file (can be used multiple times)')
@click.option('-r', '--readonly', 'readonly_files', multiple=True, help='Add read-only file (can be used multiple times)')
@click.option('-a', '--args', 'additional_args', multiple=True, help='Additional aider arguments')
@click.option('--dry-run', is_flag=True, help='Show the aider command without running it')
def main(system_prompt, editable_files, readonly_files, additional_args, dry_run):
    """Interactive script to craft precise aider commands."""
    
    editable_files = list(editable_files)
    readonly_files = list(readonly_files)
    additional_args = list(additional_args)
    
    # If no files provided via command line, enter interactive mode
    if not editable_files and not readonly_files:
        click.echo("No files specified. Entering interactive mode...")
        click.echo()
        
        while True:
            list_files(editable_files, readonly_files)
            click.echo("Options:")
            click.echo("  e) Add editable files")
            click.echo("  r) Add read-only files")
            click.echo("  l) List current files")
            click.echo("  c) Clear all files")
            click.echo("  d) Done with file selection")
            click.echo()
            
            choice = click.prompt("Choose option").lower()
            
            if choice == 'e':
                add_files_interactive("editable", editable_files)
            elif choice == 'r':
                add_files_interactive("read-only", readonly_files)
            elif choice == 'l':
                list_files(editable_files, readonly_files)
            elif choice == 'c':
                editable_files.clear()
                readonly_files.clear()
                click.echo("All files cleared.")
            elif choice == 'd':
                break
            else:
                click.echo("Invalid option. Please try again.")
            click.echo()
    
    # Show final file selection
    list_files(editable_files, readonly_files)
    
    # Get system prompt if not provided
    if not system_prompt:
        system_prompt = click.prompt("Enter system prompt (optional, press Enter to skip)", default="", show_default=False)
        click.echo()
    
    # Get user prompt
    user_prompt = get_user_prompt()
    
    # Preview and confirm
    preview_command(editable_files, readonly_files, additional_args, system_prompt, user_prompt)
    
    if not dry_run:
        if click.confirm("Execute this command?", default=True):
            execute_aider(editable_files, readonly_files, additional_args, system_prompt, user_prompt)
        else:
            click.echo("Aborted.")


def add_files_interactive(file_type: str, file_list: list):
    """Add files interactively."""
    click.echo(f"Enter {file_type} files (one per line, empty line to finish):")
    
    while True:
        file = click.prompt("File", default="", show_default=False)
        if not file:
            break
            
        file_path = Path(file)
        if not file_path.exists():
            if not click.confirm(f"Warning: File '{file}' not found. Continue anyway?", default=False):
                continue
        
        file_list.append(file)
        click.echo(f"Added: {file}")


def list_files(editable_files: list, readonly_files: list):
    """List current file selection."""
    click.echo("Current file selection:")
    
    if editable_files:
        click.echo("  Editable files:")
        for file in editable_files:
            click.echo(f"    {file}")
    
    if readonly_files:
        click.echo("  Read-only files:")
        for file in readonly_files:
            click.echo(f"    {file}")
    
    if not editable_files and not readonly_files:
        click.echo("  No files selected")
    
    click.echo()


def get_user_prompt() -> str:
    """Get user prompt via multi-line input."""
    click.echo("Enter your prompt (paste content, then press Ctrl+D on a new line):")
    click.echo("----------------------------------------")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    user_prompt = '\n'.join(lines)
    
    click.echo("----------------------------------------")
    click.echo(f"Prompt received ({len(user_prompt)} characters)")
    click.echo()
    
    return user_prompt


def preview_command(editable_files: list, readonly_files: list, additional_args: list, 
                   system_prompt: str, user_prompt: str):
    """Preview the aider command that will be executed."""
    click.echo("Aider command that will be executed:")
    click.echo("======================================")
    
    cmd_parts = ["aider"]
    
    # Add editable files
    for file in editable_files:
        cmd_parts.append(f'--file "{file}"')
    
    # Add read-only files
    for file in readonly_files:
        cmd_parts.append(f'--read "{file}"')
    
    # Add additional args
    cmd_parts.extend(additional_args)
    
    # Add message flag if we have prompts
    if system_prompt or user_prompt:
        cmd_parts.append("--message")
    
    cmd = " ".join(cmd_parts)
    click.echo(cmd)
    click.echo("======================================")
    click.echo()
    
    if system_prompt:
        click.echo("System prompt:")
        click.echo("-------------")
        click.echo(system_prompt)
        click.echo("-------------")
        click.echo()
    
    click.echo("User prompt:")
    click.echo("------------")
    click.echo(user_prompt)
    click.echo("------------")
    click.echo()


def execute_aider(editable_files: list, readonly_files: list, additional_args: list,
                 system_prompt: str, user_prompt: str):
    """Execute the aider command."""
    aider_cmd = ["aider"]
    
    # Add editable files
    for file in editable_files:
        aider_cmd.extend(["--file", file])
    
    # Add read-only files
    for file in readonly_files:
        aider_cmd.extend(["--read", file])
    
    # Add additional arguments
    aider_cmd.extend(additional_args)
    
    # Combine system prompt and user prompt
    combined_prompt = user_prompt
    if system_prompt:
        combined_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {user_prompt}"
    
    # Add the message
    if combined_prompt:
        aider_cmd.extend(["--message", combined_prompt])
    
    click.echo("Executing aider...")
    click.echo()
    
    try:
        subprocess.run(aider_cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Aider exited with error code {e.returncode}")
        raise click.Abort()
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user")
        raise click.Abort()
    except FileNotFoundError:
        click.echo("Error: aider command not found. Make sure aider is installed and in your PATH.")
        raise click.Abort()


if __name__ == "__main__":
    main()
