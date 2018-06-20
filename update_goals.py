#!/usr/bin/env python3

from time import sleep
from sqlalchemy import exc

from database import Database
from webdriver import create_webdriver

def parse_goal(web_element, match_id):
    """Return a goal dict ready to be inserted to base"""
    pid = int(web_element.find_element_by_tag_name('a').get_attribute('href').split('/')[-1])
    return {'player_id': pid,
            'time': web_element.find_element_by_class_name("fi-mh__scorer__minute").text,
            'match_id': match_id}


db = Database()
WD = create_webdriver()
sleep(2)

# Compruebo tener los goles de cada partido
for match in db.matches.select().execute().fetchall():
    goals = db.session.query(db.goals).filter(db.goals.columns.match_id == match.id)
    if match.home_score + match.away_score == goals.count():
        continue

    WD.get(match.url)
    sleep(10)

    for team in ['home', 'away']:
        for scorers in WD.find_elements_by_class_name("fi-mh__scorers__%s" % team):
            for html in scorers.find_elements_by_class_name("fi-mh__scorer"):
                goal = parse_goal(html, match.id)

                try:
                    db.goals.insert(goal).execute()
                    print("New: ", goal)
                except exc.IntegrityError:
                    continue

WD.close()
