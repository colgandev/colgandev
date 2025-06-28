import subprocess

from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from html_components import HTML, BaseComponent, Body, Div, Head, Meta, Title, Link, H1, H2, P, A, Button, Ul, Li

app = FastAPI()


# Custom Components using render() method
class Card(BaseComponent):
    def render(self):
        return Div(class_="card")(*self.children)


class CardHeader(BaseComponent):
    def render(self):
        return Div(class_="card-header")(*self.children)


class CardBody(BaseComponent):
    def render(self):
        return Div(class_="card-body")(*self.children)


class CardFooter(BaseComponent):
    def render(self):
        return Div(class_="card-footer")(*self.children)


class Layout(BaseComponent):
    page_title: str = "Colgan Development"
    description: str = "David Colgan's development tools and configuration"
    
    def render(self):
        return HTML()(
            Head()(
                Meta(charset="utf-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1"),
                Meta(name="description", content=self.description),
                Meta(name="author", content="David Colgan"),
                Title()(self.page_title),
                Link(
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                    rel="stylesheet",
                ),
                Link(
                    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css",
                    rel="stylesheet",
                ),
            ),
            Body(class_="bg-light")(
                *self.children
            ),
        )


class Container(BaseComponent):
    def render(self):
        return Div(class_="container py-4")(*self.children)


class Row(BaseComponent):
    def render(self):
        return Div(class_="row")(*self.children)


class Col(BaseComponent):
    size: str = "12"
    
    def render(self):
        return Div(class_=f"col-{self.size}")(*self.children)


class Alert(BaseComponent):
    variant: str = "primary"
    
    def render(self):
        return Div(class_=f"alert alert-{self.variant}")(*self.children)


class Badge(BaseComponent):
    variant: str = "primary"
    
    def render(self):
        return Div(class_=f"badge bg-{self.variant}")(*self.children)


def format_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, "html.parser")
    return soup.prettify()


@app.get("/")
async def root():
    html = Layout(
        page_title="Colgan Development - Home",
        description="David Colgan's development environment, tools, and configuration"
    )(
        Container()(
            Row()(
                Col(size="12")(
                    H1(class_="display-4 mb-4")("🚀 Colgan Development"),
                    Alert(variant="info")(
                        "Welcome to my development environment! This is built with FastAPI and custom HTML components."
                    ),
                )
            ),
            Row()(
                Col(size="md-6")(
                    Card()(
                        CardHeader()(
                            H2(class_="h5 mb-0")("🛠️ Development Tools")
                        ),
                        CardBody()(
                            P()("Here are some of the tools and technologies I use:"),
                            Ul(class_="list-unstyled")(
                                Li(class_="mb-2")(
                                    Badge(variant="primary")("Python 3.13"),
                                    " Modern Python with type hints"
                                ),
                                Li(class_="mb-2")(
                                    Badge(variant="success")("FastAPI"),
                                    " High-performance web framework"
                                ),
                                Li(class_="mb-2")(
                                    Badge(variant="info")("Pydantic"),
                                    " Data validation with type safety"
                                ),
                                Li(class_="mb-2")(
                                    Badge(variant="warning")("Bootstrap 5.3"),
                                    " Modern CSS framework"
                                ),
                            )
                        )
                    )
                ),
                Col(size="md-6")(
                    Card()(
                        CardHeader()(
                            H2(class_="h5 mb-0")("📁 Quick Links")
                        ),
                        CardBody()(
                            P()("Explore different parts of my setup:"),
                            Div(class_="d-grid gap-2")(
                                A(
                                    href="/~/repos/colgandev",
                                    class_="btn btn-outline-primary"
                                )("📂 Dotfiles & Config"),
                                Button(
                                    type="button",
                                    class_="btn btn-outline-secondary",
                                    disabled=True
                                )("🔧 Tools (Coming Soon)"),
                                Button(
                                    type="button", 
                                    class_="btn btn-outline-secondary",
                                    disabled=True
                                )("📊 Dashboard (Coming Soon)"),
                            )
                        )
                    )
                )
            ),
            Row()(
                Col(size="12")(
                    Card(class_="mt-4")(
                        CardHeader()(
                            H2(class_="h5 mb-0")("💡 About This System")
                        ),
                        CardBody()(
                            P()(
                                "This website is built using a custom HTML component system that provides "
                                "type-safe templating directly in Python. No separate template files needed!"
                            ),
                            P()(
                                "The components are built with Pydantic for validation and use a fluent API "
                                "that formats beautifully with Black. It's like JSX but for Python!"
                            ),
                            Alert(variant="success")(
                                "🎯 Type-safe • 🔧 Composable • 🎨 Beautiful syntax • ⚡ Fast development"
                            )
                        )
                    )
                )
            )
        )
    )
    return HTMLResponse(format_html(html.render_html()))


@app.get("/~/repos/colgandev")
async def dotfiles():
    """
    These are my dotfiles. Feel free to use them!
    """
    html = HTML()(
        Head()(
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(name="description", content="David Colgan's dotfiles and development setup"),
            Meta(name="author", content="David Colgan"),
            Title()("David Colgan Development Setup"),
        ),
        Body(class_="body-bg-secondary")(
            Card()(
                CardHeader()("Development Configuration"),
                CardBody()("These are my dotfiles and local development setup."),
                CardFooter()("Feel free to use them!"),
            ),
        ),
    )
    return HTMLResponse(format_html(html.render_html()))


@app.post("/clipboard")
async def set_clipboard(request: Request):
    # Get the raw body as bytes and decode to string
    text = (await request.body()).decode("utf-8")

    subprocess.run(["/usr/bin/xclip"], input=text.encode())
    return Response("success")
