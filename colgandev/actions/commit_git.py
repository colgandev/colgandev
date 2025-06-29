import subprocess
import tempfile

import click
from anthropic import Anthropic


def get_staged_diff():
    """Get the diff of staged changes."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
    return result.stdout


def generate_commit_message(diff_content):
    """Generate commit message using Claude."""
    client = Anthropic()

    prompt = f"""Please write a concise, informative git commit message for the following staged changes. 
Follow conventional commit format if applicable (feat:, fix:, docs:, etc.).
Keep it under 72 characters for the first line.

Staged changes:
{diff_content}

Just return the commit message, nothing else."""

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",  # Haiku is sufficient for commit messages
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text.strip()


def open_editor_with_message(message):
    """Open git's configured editor with pre-filled commit message."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(message)
        f.flush()

        # Use git's configured editor
        subprocess.run(["git", "config", "--get", "core.editor"], check=True)
        subprocess.run(["git", "commit", "--template", f.name], check=True)


@click.command()
def main():
    """Generate AI commit message and open editor for staged changes."""
    # Check if there are staged changes
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if result.returncode == 0:
        click.echo("No staged changes found. Stage some changes first with 'git add'.")
        return

    # Get staged diff
    diff = get_staged_diff()

    # Generate commit message
    click.echo("Generating commit message...")
    commit_message = generate_commit_message(diff)

    # Open editor with pre-filled message
    open_editor_with_message(commit_message)


if __name__ == "__main__":
    main()
