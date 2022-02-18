from pathlib import Path

from bs4 import BeautifulSoup


def get_permalinks(fn: Path) -> list[str]:
    with fn.open() as f:
        soup = BeautifulSoup(f.read())

    return [x.a["href"] for x in soup.find_all(class_="permaRecordLink")]
