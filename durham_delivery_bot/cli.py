from pathlib import Path

import click

from .bot import request_all


@click.group()
def cli():
    pass


@cli.command()
@click.argument("fn")
def requests(fn: str):
    request_all(Path(fn).expanduser().resolve())
