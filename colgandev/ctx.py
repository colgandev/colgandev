"""
Context functions for template rendering and content composition.

Provides utility functions for including files, getting current time,
and embedding code blocks in content.
"""

from datetime import datetime
from pathlib import Path

from colgandev.settings import BASE_DIR


def file(path: str) -> str:
    """Load file content from BASE_DIR + relative_path"""
    file_path = BASE_DIR / path
    return file_path.read_text()


def now() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()


def code(path: str, lang: str = "python") -> str:
    """Include code file with syntax highlighting markup"""
    content = file(path)
    return f"```{lang}\n{content}\n```"
