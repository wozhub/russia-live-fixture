#!/usr/bin/env python3

from time import sleep
from selenium import webdriver
from sqlalchemy import exc
from xvfbwrapper import Xvfb

from database import Database


def parse_goal(web_element, match_id):
    """Return a goal dict ready to be inserted to base"""
    pid = int(web_element.find_element_by_tag_name('a').get_attribute('href').split('/')[-1])
    return {'player_id': pid,
            'time': web_element.find_element_by_class_name("fi-mh__scorer__minute").text,
            'match_id': match_id}


db = Database()

virtual_display = Xvfb()
virtual_display.start()

#sleep(5)
#d.maximize_window()

# Compruebo tener los goles de cada partido
for match in db.matches.select().execute().fetchall():
    goals = db.session.query(db.goals).filter(db.goals.columns.match_id == match.id)
    if match.home_score + match.away_score == goals.count():
        continue

    web_driver.get(match.url)
    sleep(10)

    for team in ['home', 'away']:
        for scorers in web_driver.find_elements_by_class_name("fi-mh__scorers__%s" % team):
            for html in scorers.find_elements_by_class_name("fi-mh__scorer"):
                goal = parse_goal(html, match.id)

                try:
                    db.goals.insert(goal).execute()
                    print("New: ", goal)
                except exc.IntegrityError:
                    print("Prexistent: ", goal)
                    continue

web_driver.close()
virtual_display.stop()
