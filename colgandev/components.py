from colgandev.html.html_components import (
    HTML,
    Body,
    Component,
    Div,
    Head,
    Link,
    Meta,
    Title,
)


# Custom Components using render() method
class Card(Component):
    def render(self):
        return Div(class_="card")(*self.children)


class CardHeader(Component):
    def render(self):
        return Div(class_="card-header")(*self.children)


class CardBody(Component):
    def render(self):
        return Div(class_="card-body")(*self.children)


class CardFooter(Component):
    def render(self):
        return Div(class_="card-footer")(*self.children)


class Layout(Component):
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
            Body(class_="bg-light")(*self.children),
        )


class Container(Component):
    def render(self):
        return Div(class_="container py-4")(*self.children)


class Row(Component):
    def render(self):
        return Div(class_="row")(*self.children)


class Col(Component):
    size: str = "12"

    def render(self):
        return Div(class_=f"col-{self.size}")(*self.children)


class Alert(Component):
    variant: str = "primary"

    def render(self):
        return Div(class_=f"alert alert-{self.variant}")(*self.children)


class Badge(Component):
    variant: str = "primary"

    def render(self):
        return Div(class_=f"badge bg-{self.variant}")(*self.children)
