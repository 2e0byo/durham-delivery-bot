from pathlib import Path

import click

from . import process


@click.group()
def cli():
    pass


@cli.command()
@click.argument("fn")
@click.option("--in-person", multiple=True)
def requests(fn: str, in_person: tuple[str] = None):
    process(Path(fn).expanduser().resolve(), in_person)
