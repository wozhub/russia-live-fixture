#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_webdriver():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    web_driver = webdriver.Chrome(chrome_options=options)

    return web_driver
