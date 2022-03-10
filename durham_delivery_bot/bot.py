from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path
from re import sub
from urllib.parse import unquote

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

try:
    from .cart import get_permalinks

    TESTING = False
except ImportError:
    from cart import get_permalinks

    TESTING = True


def login():
    global username, password
    username = input("Enter username: ").strip()
    password = getpass("Enter password: ").strip()
    LOGIN_PAGE = "https://library.dur.ac.uk/"
    driver.get(LOGIN_PAGE)
    el = driver.find_element(By.ID, "username")
    el.send_keys(username)
    el = driver.find_element(By.ID, "password")
    el.send_keys(password)

    [
        x
        for x in driver.find_elements(By.NAME, "submit")
        if x.get_attribute("value") == "submit"
    ][0].click()


student_type = "Postgraduate research"
reason = "For my dissertation"
delivery_method = "Collect from Bill Bryson"
useful_weeks = 3


def request_delivery(link: str):
    driver.get(link)
    try:
        el = driver.find_element(By.XPATH, "//*[text()='Request Postal Loan']")
    except NoSuchElementException:
        el = driver.find_element(By.XPATH, "//*[text()='Request delivery to Durham']")

    onclick = el.get_attribute("onclick")
    url = unquote(sub(r".+resurl=(.+)'.+", r"\1", onclick))
    bib = url.split("bib=")[1]
    url = f"https://{username}:{password}@community.dur.ac.uk/library.systems/password/request/?bib={bib}"
    driver.get(url)

    driver.find_element(By.NAME, "userStatus").send_keys(student_type)
    driver.find_element(By.NAME, "requestReason").send_keys(reason)
    driver.find_element(By.NAME, "deliveryMethod").send_keys(delivery_method)
    date = (datetime.now() + timedelta(weeks=useful_weeks)).strftime("%d/%m/%y")
    driver.find_element(By.NAME, "lastUsefulDate").send_keys(date)
    el = driver.find_element(By.XPATH, "//*[text()='Submit']")
    el.click()


def request_all(fn: Path):
    global driver

    driver = Chrome()
    permalinks = get_permalinks(fn)
    login()
    for link in permalinks:
        request_delivery(link)


if TESTING:
    permalinks = get_permalinks(Path("/tmp/out2.html"))
    login()
    link = permalinks[0]
