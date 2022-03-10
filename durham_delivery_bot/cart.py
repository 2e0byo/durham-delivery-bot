from pathlib import Path

from bs4 import BeautifulSoup


def get_permalinks(fn: Path) -> list[str]:
    with fn.open() as f:
        soup = BeautifulSoup(f.read())

    permalinks = set([x.a["href"] for x in soup.find_all(class_="permaRecordLink")])
    permalinks |= set(x["href"] for x in soup.find_all("a", id="recordnum"))
    return permalinks


def parse_records(fn: Path) -> list[dict]:
    with fn.open() as f:
        soup = BeautifulSoup(f.read(), features="html.parser")

    # can't use the div because it's broken! first entry commented out in source...
    trs = soup.find_all("tr", class_="bibInfoEntry")
    data = (x.find("tbody").find_all("td") for x in trs)
    texts = ([x.text.strip() for x in entry] for entry in data)
    records = [dict(zip(*[iter(x)] * 2)) for x in texts]

    groups = []
    grouped = {}
    for record in records:
        if "More information" in record.keys():
            groups.append(grouped)
            grouped = {}
        else:
            grouped |= record

    permalinks = [x["href"] for x in soup.find_all("a", id="recordnum")]
    assert len(permalinks) == len(groups)
    for link, record in zip(permalinks, groups):
        record["permalink"] = link

    tbls = soup.find_all("table", class_="bibItems")
    for tbl, record in zip(tbls, groups):
        copies = {}
        keys = [
            x.text.strip().title()
            for x in tbl.find("tr", class_="bibItemsHeader").find_all("th")
        ]
        rows = tbl.find_all("tr", class_="bibItemsEntry")
        for row in rows:
            copy = dict(zip(keys, [x.text.strip() for x in row.find_all("td")]))
            copies[copy["Location"]] = copy
        record["Copies"] = copies

    return groups
