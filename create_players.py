#!/usr/bin/env python3

from time import sleep
from sqlalchemy.exc import IntegrityError

from database import Database
from webdriver import create_webdriver

db = Database()

WEB_DRIVER = create_webdriver()
sleep(2)

# Busco los jugadores
for team in db.teams.select().execute().fetchall():
    WEB_DRIVER.get(team.url)
    sleep(5)

    players = []
    for p in WEB_DRIVER.find_elements_by_class_name('fi-p'):

        try:
            pos = p.find_element_by_class_name('fi-p__info--role').text
        except:
            continue

        if pos == "COACH":
            continue

        url = p.find_element_by_class_name('fi-p--link').get_attribute('href')
        player = {
            'id': int(url.split('/')[-2]),
            'team_id': team.id,
            'num': int(p.find_element_by_class_name('fi-p__num').text),
            'name': p.find_element_by_class_name('fi-p__nShorter').text,
            'pos': pos,
            'url': url,
        }

        try:
            db.players.insert(player).execute()
            players.append(player)
            print(player)
        except IntegrityError:
            continue

WEB_DRIVER.close()
