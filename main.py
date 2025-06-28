import subprocess

from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from html_components import HTML, BaseComponent, Body, Div, Head, Meta, Title

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


def format_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, "html.parser")
    return soup.prettify()


@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}


@app.get("/~/repos/colgandev")
async def dotfiles():
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
