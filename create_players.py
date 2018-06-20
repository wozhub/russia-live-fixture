#!/usr/bin/env python3

from time import sleep
from selenium import webdriver

from database import Database


db = Database()

virtual_display = Xvfb()
virtual_display.start()
web_driver = webdriver.Chrome()
sleep(2)
# d.maximize_window()

# Busco los equipos
TEAMS_URL = "https://www.fifa.com/worldcup/teams/"
web_driver.get(TEAMS_URL)

TEAMS = []
for t in web_driver.find_elements_by_class_name('fi-team-card__team'):
    team = {
        'id': int(t.get_attribute('data-team')),
        'name': t.text,
        'url': t.get_attribute('href'),
    }
    print(team)
    TEAMS.append(team)
    db.teams.insert(team).execute()

# Busco los jugadores
for team in TEAMS:
    web_driver.get(team['url'])
    sleep(5)

    players = []
    for p in web_driver.find_elements_by_class_name('fi-p'):
        pos = p.find_element_by_class_name('fi-p__info--role').text
        if pos == "COACH":
            continue

        url = p.find_element_by_class_name('fi-p--link').get_attribute('href')
        player = {
            'id': int(url.split('/')[-2]),
            'team_id': team['id'],
            'num': int(p.find_element_by_class_name('fi-p__num').text),
            'name': p.find_element_by_class_name('fi-p__nShorter').text,
            'pos': pos,
            'url': url,
        }
        print(player)
        players.append(player)
        db.players.insert(player).execute()

web_driver.close()
virtual_display.stop()
