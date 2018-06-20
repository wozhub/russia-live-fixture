#!/usr/bin/env python3

from time import sleep
from selenium import webdriver
from sqlalchemy import exc
from xvfbwrapper import Xvfb

from database import Database


db = Database()

virtual_display = Xvfb()
virtual_display.start()
web_driver = webdriver.Chrome()
sleep(2)
#web_driver.maximize_window()

# Busco los partidos
MATCHES_URL = "https://www.fifa.com/worldcup/matches/"
web_driver.get(MATCHES_URL)
sleep(5)

# matches = []
for m in web_driver.find_elements_by_class_name('fi-mu__link'):
    if not "FULL-TIME" in m.text:
        continue

    score = m.find_element_by_class_name('fi-s__scoreText').text.split('-')
    teams = [x.text for x in m.find_elements_by_class_name('fi-t__nText')]

    match = {
        'id': m.find_element_by_class_name('result').get_attribute('data-id'),
        'url': m.get_attribute('href'),
        'home_id': db.session.query(db.teams).\
                    filter(db.teams.columns.name.like(teams[0]))[0].id,
        'home_score': int(score[0]),
        'away_id': db.session.query(db.teams).\
                    filter(db.teams.columns.name.like(teams[1]))[0].id,
        'away_score': int(score[1]),
    }

    try:
        db.matches.insert(match).execute()
        print("New: ", match)
#        matches.append(match)
    except exc.IntegrityError:
        print("Prexistent: ", match)
        continue

web_driver.close()
virtual_display.stop()
