# AI! help me flush out this idea. I'm wanting to have sort of like this way of of building fast API HTML responses in Python using this sort of syntax where you have like you have these component classes that you can compose and it's it's got this sort of like HTML like feel to it because I'm trying to represent a tree structure and so I have this like I use the call syntax with the custom thunder method. dunder method and yeah like you can see that I can basically make like this HTML object and then I can add children objects to it by calling it again sort of it's like the first. (are for adding attributes and then the second call is for adding children and so in a way you have the same ergonomics as HTML and so you'll notice that. like if you're wanting to add either text, so if it's just the first argument to all components, there's like a there's like a text. maybe you would just call this a tag. a component is something that has. it's either a tag or a collection of tags and so I want this to be fractal composition wise and I'm just wanting to be able to return HTML that I can sort of like type check. so this base component should be a pydantic model object and so because it's a pydantic model object, I can return it as json or I can return it as HTML. that's cool. I could also even return it to some other kind of type like XML if I wanted to. but I just want json and HTML and so basically there needs to be like this. there's I've heard of this HTML dunder method that is in some cases used for like represent this thing as HTML. I don't really know how that would work. it's called render HTML there we go


import subprocess

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()


class BaseComponent(BaseModel):
    id: str | None = None
    class_: str | None = None

    children: list["BaseComponent"] = Field(default_factory=list)

    def __init__(self, text: str = ""):
        # ai? how should this be structured for pydantic?
        self.text = text

    def __call__(self, *args):
        self.children.extend(*args)
        return self

    def render_html(self):
        # ai! how do we deal with this?
        return "???"

    def render_markdown(self):
        # ai? how could we implement this somehow?
        ...


class Card(BaseComponent):
    def render(self):
        return f"""
<div class="card">
    {self.slot}
</div>
"""


class CardHeader(BaseComponent):
    def render(self):
        return f"""
<div class="card-header">
    {self.slot}
</div>
"""


class Head(BaseComponent):
    def render(self): ...


class Body(BaseComponent):
    def render(self): ...


class HTML(BaseComponent):
    def render(self):
        return f"""<!doctype html>
<html lang="{self.lang}">
    {(child.render() for child in self.children)}
</html>
        """


@app.get("/~/repos/colgandev")
async def dotfiles():
    html = HTML()(
        Head()(
            Meta(name="", content=""),
            Meta(name="", content=""),
            Meta(name="", content=""),
            Title("This is the title"),
        ),
        Body(class_="body-bg-secondary")(),
        Card()(
            CardHeader(),
            CardBody(),
            CardFooter(),
        ),
    )
    return HTMLResponse(html)


@app.post("/clipboard")
async def set_clipboard(request: Request):
    # Get the raw body as bytes and decode to string
    text = (await request.body()).decode("utf-8")

    subprocess.run(["/usr/bin/xclip"], input=text.encode())
    return Response("success")
