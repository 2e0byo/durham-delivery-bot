from pathlib import Path
from typing import Optional

import click

from . import process


@click.group()
def cli():
    pass


@cli.command()
@click.argument("fn")
@click.option("--in-person", multiple=True)
@click.option("--student-type", default="Postgraduate research")
@click.option("--reason", default="For my dissertation")
@click.option("--delivery-method", default="Collect from Bill Bryson")
def requests(
    fn: str,
    in_person: Optional[tuple[str]],
    student_type: str,
    reason: str,
    delivery_method: str,
):
    process(
        Path(fn).expanduser().resolve(),
        in_person,
        student_type,
        reason,
        delivery_method,
    )
