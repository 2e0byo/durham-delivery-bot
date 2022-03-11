from pathlib import Path
import pytest

from durham_delivery_bot.bot import get_reserve_url, Chrome, request
from durham_delivery_bot.cart import parse_records
from durham_delivery_bot import format_records, categorise
from durham_delivery_bot import bot


def test_reserve_urls(data_regression):
    records = parse_records(Path(__file__).parent / "books.html")
    permalinks = [x["permalink"] for x in records]
    username = "username"
    password = "password"
    urls = sorted([get_reserve_url(x, username, password) for x in permalinks])
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


def test_format_records(data_regression):
    records = parse_records(Path(__file__).parent / "books.html")
    collect, reserve = categorise(records, ["John's", "Bryson"])
    data_regression.check(format_records(collect))
    print(format_records(collect))


def test_request(mocker):
    records = parse_records(Path(__file__).parent / "books.html")
    collect, reserve = categorise(records, ["John's", "Bryson"])
    links = []

    def side_effect(link, *args):
        links.append(link)

    request_delivery = mocker.patch(
        "durham_delivery_bot.bot.request_delivery", side_effect=side_effect
    )
    credentials = mocker.patch("durham_delivery_bot.bot.get_credentials")
    credentials.return_value = ("username", "password")
    login = mocker.patch("durham_delivery_bot.bot.login")

    assert login.call_args_list[0][0][1:] == ("username", "password")
    login.assert_called_once()
    request(reserve)

    assert request_delivery.call_count == len(reserve)
    assert links == [x["permalink"] for x in reserve]
