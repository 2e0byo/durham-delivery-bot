from pathlib import Path
from devtools import debug
from itertools import chain

from .bot import request
from .cart import parse_records


def format_records(records: list[dict]) -> str:
    out = ""
    libraries = sorted(set(chain.from_iterable(x["Copies"].keys() for x in records)))
    debug(libraries)
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
