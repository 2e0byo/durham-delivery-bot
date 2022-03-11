from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path
from re import sub
from urllib.parse import unquote, urlparse, parse_qs

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def get_credentials():
    username = input("Enter username: ").strip()
    password = getpass("Enter password: ").strip()
    return username, password


def login(driver: Chrome):
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


def get_reserve_url(link: str, username: str, password: str) -> str:
    bib = link.split("record=")[1].replace("~S1", "a")
    url = f"https://{username}:{password}@community.dur.ac.uk/library.systems/password/request/?bib={bib}"
    return url


def request_delivery(link: str, driver: Chrome, username: str, password: str):
    url = get_reserve_url(link)
    driver.get(url)

    driver.find_element(By.NAME, "userStatus").send_keys(student_type)
    driver.find_element(By.NAME, "requestReason").send_keys(reason)
    driver.find_element(By.NAME, "deliveryMethod").send_keys(delivery_method)
    date = (datetime.now() + timedelta(weeks=useful_weeks)).strftime("%d/%m/%y")
    driver.find_element(By.NAME, "lastUsefulDate").send_keys(date)
    el = driver.find_element(By.XPATH, "//*[text()='Submit']")
    el.click()


def request(permalinks: list[str]):
    driver = Chrome()
    username, password = get_credentials()
    login(driver)
    for link in permalinks:
        request_delivery(link, driver, username, password)
