#!/usr/bin/env python3

from database import Database

from time import sleep
from selenium import webdriver
from xvfbwrapper import Xvfb


db = Database()

virtual_display = Xvfb()
virtual_display.start()
web_driver = webdriver.Chrome()
sleep(2)
# d.maximize_window()

# Busco los equipos
TEAMS_URL = "https://www.fifa.com/worldcup/teams/"
web_driver.get(TEAMS_URL)

# teams = []
for t in web_driver.find_elements_by_class_name('fi-team-card__team'):
    team = {
        'id': int(t.get_attribute('data-team')),
        'name': t.text,
        'url': t.get_attribute('href'),
    }

    # teams.append(team)
    print(team)
    db.teams.insert(team).execute()

web_driver.close()
virtual_display.stop()
