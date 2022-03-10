from pathlib import Path

from durham_delivery_bot.bot import get_permalinks, get_reserve_url, Chrome
from durham_delivery_bot.cart import get_permalinks


def test_get_permalinks(data_regression):
    permalinks = get_permalinks(Path(__file__).parent / "books.html")
    data_regression.check(permalinks)


def test_reserve_urls(data_regression):
    permalinks = get_permalinks(Path(__file__).parent / "books.html")
    driver = Chrome()
    driver.set_page_load_timeout(1)
    username = "username"
    password = "password"
    urls = [get_reserve_url(x, driver, username, password) for x in permalinks]
    data_regression.check(urls)
