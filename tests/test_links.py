from pathlib import Path
import pytest

from durham_delivery_bot.bot import get_reserve_url, Chrome
from durham_delivery_bot.cart import get_permalinks, parse_records
from durham_delivery_bot import categorise


def test_get_permalinks(data_regression):
    permalinks = get_permalinks(Path(__file__).parent / "books.html")
    data_regression.check(permalinks)


def test_reserve_urls(data_regression):
    permalinks = get_permalinks(Path(__file__).parent / "books.html")
    username = "username"
    password = "password"
    urls = sorted([get_reserve_url(x, driver, username, password) for x in permalinks])
    data_regression.check(urls)


def test_parse_records(data_regression):
    records = parse_records(Path(__file__).parent / "books.html")
    data_regression.check(records)
@pytest.mark.parametrize(
    "in_person",
    [
        ["St John's", "Bryson"],
        ["John's"],
        ["Ushaw"],
    ],
)
def test_categorise(in_person, data_regression):
    records = parse_records(Path(__file__).parent / "books.html")
    collect, reserve = categorise(records, in_person)
    data_regression.check((collect, reserve))
