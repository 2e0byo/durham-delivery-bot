from itertools import chain
from pathlib import Path
from typing import Optional

from .bot import request
from .cart import parse_records
from .log import logger


def format_records(records: list[dict]) -> str:
    out = ""
    libraries = sorted(set(chain.from_iterable(x["Copies"].keys() for x in records)))
    for library in libraries:
        out += f"# {library}\n\n"
        holdings = [r for r in records if library in r["Copies"].keys()]
        for record in sorted(holdings, key=lambda x: x["Copies"][library]["Shelfmark"]):
            out += "{} {:>40.40} {:>20.20}\n".format(
                record["Copies"][library]["Shelfmark"],
                record["Title"],
                record.get("Author", record.get("Other Author", "")),
            )
        out += "\n"

    return out


def categorise(records: list[dict], in_person: list[str]) -> tuple[dict, dict]:
    collect = []
    reserve = []
    for record in records:
        sources = record["Copies"].keys()
        if any(x in src for src in sources for x in in_person):
            collect.append(record)
        else:
            reserve.append(record)
    return collect, reserve


def process(
    fn: Path,
    in_person: Optional[list[str]],
    student_type: str,
    reason: str,
    delivery_method: str,
):
    records = parse_records(fn)
    collect, reserve = categorise(records, in_person)

    if collect:
        logger.info("Books to collect:")
        formatted = format_records(collect)
        print(formatted)
    if reserve:
        logger.info("Reserving books to reserve")
        request(reserve)
