#!/usr/bin/env python3

from time import sleep
from sqlalchemy import exc

from database import Database
from webdriver import create_webdriver


db = Database()

WEB_DRIVER = create_webdriver()
sleep(2)

TEAMS_URL = "https://www.fifa.com/worldcup/teams/"
WEB_DRIVER.get(TEAMS_URL)

for t in WEB_DRIVER.find_elements_by_class_name('fi-team-card__team'):
    team = {
        'id': int(t.get_attribute('data-team')),
        'name': t.text,
        'url': t.get_attribute('href'),
    }

    try:
        db.teams.insert(team).execute()
        print("New: ", team)
    except exc.IntegrityError:
        continue

WEB_DRIVER.close()
