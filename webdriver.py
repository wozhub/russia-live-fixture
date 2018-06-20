#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_web_driver():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")

    web_driver = webdriver.Chrome(chrome_options=chrome_options)

    return web_driver
