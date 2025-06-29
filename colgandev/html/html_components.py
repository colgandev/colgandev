"""
HTML component classes for building web UIs with type safety and validation.

This module provides Pydantic-based classes for all standard HTML elements,
with proper attribute validation and HTML rendering capabilities. Components
can be composed together to build complex UIs while maintaining type safety.
"""

import html

from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


def validate_url(url: str) -> str:
    """Validate URL to prevent XSS via javascript: and other dangerous schemes"""
    if url.lower().startswith(("javascript:", "data:", "vbscript:")):
        return "#"  # Safe fallback
    return html.escape(url)


def format_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, "html.parser")
    return soup.prettify()


def render(component: "HTMLComponent") -> HTMLResponse:
    """
    Render a FastAPI HTMLResponse from the provided component structure.
    """

    return HTMLResponse(
        format_html(
            component.render_html(),
        ),
    )


class HTMLComponent(BaseModel):
    id: str | None = None
    class_: str | None = Field(None, alias="class")
    style: str | None = None
    title: str | None = None
    data_testid: str | None = Field(None, alias="data-testid")
    hidden: bool | None = None
    children: list["HTMLComponent"] = Field(default_factory=list)
    tag: str = "div"

    def __call__(self, *args, **kwargs):
        new_component = self.model_copy()

        # Convert all string arguments to TextComponent objects
        for arg in args:
            if isinstance(arg, str):
                new_component.children.append(TextComponent(text=arg))
            else:
                new_component.children.append(arg)

        return new_component

    def render(self) -> "HTMLComponent":
        return self

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.style:
            attrs.append(f'style="{html.escape(rendered.style)}"')
        if rendered.title:
            attrs.append(f'title="{html.escape(rendered.title)}"')
        if rendered.data_testid:
            attrs.append(f'data-testid="{html.escape(rendered.data_testid)}"')
        if rendered.hidden:
            attrs.append("hidden")

        attrs_str = " " + " ".join(attrs) if attrs else ""

        if not rendered.children:
            return f"<{rendered.tag}{attrs_str} />"

        children_html = "".join(child.render_html() for child in rendered.children)
        return f"<{rendered.tag}{attrs_str}>{children_html}</{rendered.tag}>"

    def render_markdown(self):
        if self.tag == "h1":
            return f"# {self.children[0] if self.children else ''}\n"
        elif self.tag == "h2":
            return f"## {self.children[0] if self.children else ''}\n"
        elif self.tag == "p":
            return f"{self.children[0] if self.children else ''}\n\n"
        else:
            return str(self.children[0]) if self.children else ""


class TextComponent(HTMLComponent):
    text: str
    tag: str = "span"

    def render_html(self):
        return html.escape(self.text)


# Basic HTML Elements
class Div(HTMLComponent):
    tag: str = "div"


class Span(HTMLComponent):
    tag: str = "span"


class P(HTMLComponent):
    tag: str = "p"


class H1(HTMLComponent):
    tag: str = "h1"


class H2(HTMLComponent):
    tag: str = "h2"


class H3(HTMLComponent):
    tag: str = "h3"


class H4(HTMLComponent):
    tag: str = "h4"


class H5(HTMLComponent):
    tag: str = "h5"


class H6(HTMLComponent):
    tag: str = "h6"


# Interactive Elements
class A(HTMLComponent):
    href: str | None = None
    target: str | None = None
    rel: str | None = None
    tag: str = "a"

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.href:
            attrs.append(f'href="{validate_url(rendered.href)}"')
        if rendered.target:
            attrs.append(f'target="{html.escape(rendered.target)}"')
        if rendered.rel:
            attrs.append(f'rel="{html.escape(rendered.rel)}"')

        attrs_str = " " + " ".join(attrs) if attrs else ""
        children_html = "".join(child.render_html() for child in rendered.children)
        return f"<{rendered.tag}{attrs_str}>{children_html}</{rendered.tag}>"


class Button(HTMLComponent):
    type: str | None = None
    disabled: bool | None = None
    tag: str = "button"

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.type:
            attrs.append(f'type="{html.escape(rendered.type)}"')
        if rendered.disabled:
            attrs.append("disabled")

        attrs_str = " " + " ".join(attrs) if attrs else ""
        children_html = "".join(child.render_html() for child in rendered.children)
        return f"<{rendered.tag}{attrs_str}>{children_html}</{rendered.tag}>"


# Form Elements
class Input(HTMLComponent):
    type: str | None = None
    name: str | None = None
    value: str | None = None
    placeholder: str | None = None
    required: bool | None = None
    disabled: bool | None = None
    tag: str = "input"

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.type:
            attrs.append(f'type="{html.escape(rendered.type)}"')
        if rendered.name:
            attrs.append(f'name="{html.escape(rendered.name)}"')
        if rendered.value:
            attrs.append(f'value="{html.escape(rendered.value)}"')
        if rendered.placeholder:
            attrs.append(f'placeholder="{html.escape(rendered.placeholder)}"')
        if rendered.required:
            attrs.append("required")
        if rendered.disabled:
            attrs.append("disabled")

        attrs_str = " " + " ".join(attrs) if attrs else ""
        return f"<{rendered.tag}{attrs_str} />"


class Form(HTMLComponent):
    action: str | None = None
    method: str | None = None
    tag: str = "form"

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.action:
            attrs.append(f'action="{html.escape(rendered.action)}"')
        if rendered.method:
            attrs.append(f'method="{html.escape(rendered.method)}"')

        attrs_str = " " + " ".join(attrs) if attrs else ""
        children_html = "".join(child.render_html() for child in rendered.children)
        return f"<{rendered.tag}{attrs_str}>{children_html}</{rendered.tag}>"


class Label(HTMLComponent):
    for_: str | None = Field(None, alias="for")
    tag: str = "label"

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.for_:
            attrs.append(f'for="{html.escape(rendered.for_)}"')

        attrs_str = " " + " ".join(attrs) if attrs else ""
        children_html = "".join(child.render_html() for child in rendered.children)
        return f"<{rendered.tag}{attrs_str}>{children_html}</{rendered.tag}>"


# List Elements
class Ul(HTMLComponent):
    tag: str = "ul"


class Ol(HTMLComponent):
    tag: str = "ol"


class Li(HTMLComponent):
    tag: str = "li"


# Table Elements
class Table(HTMLComponent):
    tag: str = "table"


class Thead(HTMLComponent):
    tag: str = "thead"


class Tbody(HTMLComponent):
    tag: str = "tbody"


class Tr(HTMLComponent):
    tag: str = "tr"


class Th(HTMLComponent):
    tag: str = "th"


class Td(HTMLComponent):
    tag: str = "td"


# Media Elements
class Img(HTMLComponent):
    src: str | None = None
    alt: str | None = None
    width: str | None = None
    height: str | None = None
    tag: str = "img"

    def render_html(self):
        rendered = self.render()
        attrs = []

        if rendered.id:
            attrs.append(f'id="{html.escape(rendered.id)}"')
        if rendered.class_:
            attrs.append(f'class="{html.escape(rendered.class_)}"')
        if rendered.src:
            attrs.append(f'src="{validate_url(rendered.src)}"')
        if rendered.alt:
            attrs.append(f'alt="{html.escape(rendered.alt)}"')
        if rendered.width:
            attrs.append(f'width="{html.escape(rendered.width)}"')
        if rendered.height:
            attrs.append(f'height="{html.escape(rendered.height)}"')

        attrs_str = " " + " ".join(attrs) if attrs else ""
        return f"<{rendered.tag}{attrs_str} />"


# Document Structure
class Head(HTMLComponent):
    tag: str = "head"


class Body(HTMLComponent):
    tag: str = "body"


class Meta(HTMLComponent):
    name: str | None = None
    content: str | None = None
    charset: str | None = None
    http_equiv: str | None = Field(None, alias="http-equiv")
    tag: str = "meta"

    def render_html(self):
        attrs = []
        if self.name:
            attrs.append(f'name="{html.escape(self.name)}"')
        if self.content:
            attrs.append(f'content="{html.escape(self.content)}"')
        if self.charset:
            attrs.append(f'charset="{html.escape(self.charset)}"')
        if self.http_equiv:
            attrs.append(f'http-equiv="{html.escape(self.http_equiv)}"')
        attrs_str = " " + " ".join(attrs) if attrs else ""
        return f"<meta{attrs_str} />"


class Title(HTMLComponent):
    tag: str = "title"

    def render_html(self):
        children_html = "".join(child.render_html() for child in self.children)
        return f"<title>{children_html}</title>"


class Link(HTMLComponent):
    href: str | None = None
    rel: str | None = None
    type: str | None = None
    tag: str = "link"

    def render_html(self):
        attrs = []
        if self.href:
            attrs.append(f'href="{validate_url(self.href)}"')
        if self.rel:
            attrs.append(f'rel="{html.escape(self.rel)}"')
        if self.type:
            attrs.append(f'type="{html.escape(self.type)}"')
        attrs_str = " " + " ".join(attrs) if attrs else ""
        return f"<link{attrs_str} />"


class RawHTML(HTMLComponent):
    html: str

    def render_html(self):
        return self.html


class HTML(HTMLComponent):
    lang: str = "en"
    tag: str = "html"

    def render_html(self):
        children_html = "".join(child.render_html() for child in self.children)
        return f'<!doctype html>\n<html lang="{html.escape(self.lang)}">\n{children_html}\n</html>'
