from pathlib import Path
from typing import Optional

import click

from . import process


@click.command()
@click.argument("fn")
@click.option("--in-person", multiple=True, help="Library to collect from in person")
@click.option("--student-type", default="Postgraduate research")
@click.option("--reason", default="For my dissertation")
@click.option("--delivery-method", default="Collect from Bill Bryson")
@click.option("-o", "--out", type=Path, help="Path to save books to collect in")
@click.option("--dry-run/-no-dry-run", default=False)
def cli(
    fn: str,
    in_person: Optional[tuple[str]],
    student_type: str,
    reason: str,
    delivery_method: str,
    out: Optional[Path],
    dry_run: bool,
):
    process(
        Path(fn).expanduser().resolve(),
        in_person,
        student_type,
        reason,
        delivery_method,
        out,
        dry_run,
    )
