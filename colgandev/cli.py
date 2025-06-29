import click

# from scripts.resolve import Resolve


@click.group()
def cli():
    pass


# @cli.command()
# def resolve():
#     click.echo(Resolve())


@cli.command()
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=5555)
def serve(host, port):
    import uvicorn

    uvicorn.run(
        app="colgandev.api:app",
        host=host,
        port=port,
        loop="uvloop",
        reload=True,
    )
    click.echo("done")
