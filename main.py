# AI! help me flush out this idea. I'm wanting to have sort of like this way of of building fast API HTML responses in Python using this sort of syntax where you have like you have these component classes that you can compose and it's it's got this sort of like HTML like feel to it because I'm trying to represent a tree structure and so I have this like I use the call syntax with the custom thunder method. dunder method and yeah like you can see that I can basically make like this HTML object and then I can add children objects to it by calling it again sort of it's like the first. (are for adding attributes and then the second call is for adding children and so in a way you have the same ergonomics as HTML and so you'll notice that. like if you're wanting to add either text, so if it's just the first argument to all components, there's like a there's like a text. maybe you would just call this a tag. a component is something that has. it's either a tag or a collection of tags and so I want this to be fractal composition wise and I'm just wanting to be able to return HTML that I can sort of like type check. so this base component should be a pydantic model object and so because it's a pydantic model object, I can return it as json or I can return it as HTML. that's cool. I could also even return it to some other kind of type like XML if I wanted to. but I just want json and HTML and so basically there needs to be like this. there's I've heard of this HTML dunder method that is in some cases used for like represent this thing as HTML. I don't really know how that would work. it's called render HTML there we go


import subprocess

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()


class BaseComponent(BaseModel):
    text: str = ""
    id: str | None = None
    class_: str | None = Field(None, alias="class")
    children: list["BaseComponent"] = Field(default_factory=list)
    tag: str = "div"

    # Allow arbitrary attributes for HTML attributes
    model_config = {"extra": "allow"}

    def __call__(self, *children, **attrs):
        # First call sets attributes, second call adds children
        if children:
            new_component = self.model_copy()
            new_component.children.extend(children)
            return new_component
        else:
            # Set attributes
            for key, value in attrs.items():
                setattr(self, key, value)
            return self

    def render_html(self):
        attrs = []
        if self.id:
            attrs.append(f'id="{self.id}"')
        if self.class_:
            attrs.append(f'class="{self.class_}"')

        # Add any extra attributes
        for key, value in self.__dict__.items():
            if key not in {"text", "id", "class_", "children", "tag"} and value is not None:
                attrs.append(f'{key.replace("_", "-")}="{value}"')

        attrs_str = " " + " ".join(attrs) if attrs else ""

        if not self.children and not self.text:
            return f"<{self.tag}{attrs_str} />"

        children_html = "".join(
            child.render_html() if hasattr(child, "render_html") else str(child) for child in self.children
        )
        content = self.text + children_html

        return f"<{self.tag}{attrs_str}>{content}</{self.tag}>"

    def render_markdown(self):
        # Basic markdown rendering - can be expanded
        if self.tag == "h1":
            return f"# {self.text}\n"
        elif self.tag == "h2":
            return f"## {self.text}\n"
        elif self.tag == "p":
            return f"{self.text}\n\n"
        else:
            return self.text


# AI! okay, so I noticed a couple things. I don't want to have to set the extra allow on model_config. I want all of these things to be strongly typed so there can't be. I don't want the dynamicness of HTML here because I'm basically wanting to make this sort of type checker on top of HTML in some ways and so I need this base component to have like all of the the the most used attributes of HTML and if I ever need another one I can just add it so there's no worry about having it to be too few of them. but you know you would put like data and you would put maybe ID maybe like class and the special_at the end of class you know you could and and so then I also want like other components like input box. I want like input to be a component and so I'm wanting you to like add more components here that would implement basic HTML tags. I'm sure they're wanting to wrap the basic HTML tags at the bottom to be able to kind of like give them powers. so I want like input. I want the a tag so I want you to make like a component that is just capital letter. a and like that's the a tag and then I'm basically wanting to be able to create custom tags that compose other tags and specifically I need you to not change the fact that it was or well, let's just go the whole way here. okay so so something that I want. I want bass component to inherit from Base model which it does I guess yeah? and so like if the for the input component that is like the generic input tag in HTML that one will have like the name field and it'll have like you know placeholder and like things the generic tags don't have. so I want you to have like sort of a taxonomy of tags because I want the attributes to be the attributes that only work for that tag. so I want you to make a tree structure of inheritance so that you can. you can add Fields to something and and have it be a strongly typed way. and I really don't like this super init thing for adding stuff. I don't want it to be that way. I want basically there to be a render function method saying on a component and that render method is similar to like react JS's render method. this is kind of a hyperscript implementation if you will. yeah and I'm just wanting it to like kind of mirror that syntax you. yeah put back in the render functions but instead of having it return strings it should return like these component objects. yeah I'm wanting to make a sort of like non-dynamic react to JS component structure here and so I would like the ergonomics of using this to basically be that their attributes which are just the pidentic model classes like attributes and then there's a render function or method that's sort of like the that's like the children basically if that makes sense. see what you can kind of do with that. I want my components to basically just be that the attributes are the typed pydantic Fields and then I want like some way to say like here's. here's how to render this component and it will basically be a recursive structure and basically it's a react component so I need like the child or the slot that goes into the tag and and so on
class Card(BaseComponent):
    tag: str = "div"

    def __init__(self, **data):
        super().__init__(**data)
        if not self.class_:
            self.class_ = "card"


class CardHeader(BaseComponent):
    tag: str = "div"

    def __init__(self, **data):
        super().__init__(**data)
        if not self.class_:
            self.class_ = "card-header"


class CardBody(BaseComponent):
    tag: str = "div"

    def __init__(self, **data):
        super().__init__(**data)
        if not self.class_:
            self.class_ = "card-body"


class CardFooter(BaseComponent):
    tag: str = "div"

    def __init__(self, **data):
        super().__init__(**data)
        if not self.class_:
            self.class_ = "card-footer"


class Head(BaseComponent):
    tag: str = "head"


class Body(BaseComponent):
    tag: str = "body"


class Meta(BaseComponent):
    tag: str = "meta"
    name: str = ""
    content: str = ""

    def render_html(self):
        attrs = []
        if self.name:
            attrs.append(f'name="{self.name}"')
        if self.content:
            attrs.append(f'content="{self.content}"')
        attrs_str = " " + " ".join(attrs) if attrs else ""
        return f"<meta{attrs_str} />"


class Title(BaseComponent):
    tag: str = "title"

    def __init__(self, text: str = "", **data):
        super().__init__(text=text, **data)


class HTML(BaseComponent):
    tag: str = "html"
    lang: str = "en"

    def render_html(self):
        children_html = "".join(child.render_html() for child in self.children)
        return f'<!doctype html>\n<html lang="{self.lang}">\n{children_html}\n</html>'


@app.get("/~/repos/colgandev")
async def dotfiles():
    html = HTML()(
        Head()(
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(name="description", content="David Colgan's dotfiles and development setup"),
            Meta(name="author", content="David Colgan"),
            Title("David Colgan Development Setup"),
        ),
        Body(class_="body-bg-secondary")(
            Card()(
                CardHeader()("Development Configuration"),
                CardBody()("These are my dotfiles and local development setup."),
                CardFooter()("Feel free to use them!"),
            ),
        ),
    )
    return HTMLResponse(html.render_html())


@app.post("/clipboard")
async def set_clipboard(request: Request):
    # Get the raw body as bytes and decode to string
    text = (await request.body()).decode("utf-8")

    subprocess.run(["/usr/bin/xclip"], input=text.encode())
    return Response("success")
