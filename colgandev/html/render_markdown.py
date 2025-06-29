import re

import markdown
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


class URLEmbedExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # Process URL embeds before markdown converts URLs to links
        md.preprocessors.register(URLEmbedPreprocessor(md), "url_embed", 25)
        md.treeprocessors.register(ExternalLinksTreeProcessor(md), "external_links", 0)


class URLEmbedPreprocessor(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        processed_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                processed_lines.append(line)
                continue

            # Check if line contains only a URL
            url_pattern = r"^(https?://[^\s]+|/[^\s]*)$"
            if not re.match(url_pattern, stripped):
                processed_lines.append(line)
                continue

            # YouTube URLs - convert to iframe embed
            youtube_pattern = (
                r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]+)"
            )
            youtube_match = re.match(youtube_pattern, stripped)
            if youtube_match:
                video_id = escape(youtube_match.group(1))
                embed_html = (
                    f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" '
                    f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                )
                processed_lines.append(embed_html)
                continue

            # Asset URLs - convert to HTMX
            if stripped.startswith("/_/"):
                escaped_url = escape(stripped)
                processed_lines.append(f'<div hx-get="{escaped_url}" hx-trigger="revealed"></div>')
                continue

            # Let other URLs be processed normally by markdown (they'll get target="_blank" from ExternalLinksTreeProcessor)
            processed_lines.append(line)

        return processed_lines


class ExternalLinksTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root):
        for link in root.iter("a"):
            href = link.get("href", "")
            if href and (href.startswith("http://") or href.startswith("https://")):
                link.set("target", "_blank")
                link.set("rel", "noopener noreferrer")


md = markdown.Markdown(
    extensions=["fenced_code", URLEmbedExtension()],
    extension_configs={
        "fenced_code": {
            "lang_prefix": "language-",
        }
    },
)


@register.filter
def render_markdown(value):
    """
    Process markdown content with URL embedding integrated into markdown processing
    """
    if not value:
        return ""

    return mark_safe(md.convert(value))
