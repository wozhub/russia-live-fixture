#!/usr/bin/env python3

from time import sleep
from sys import exit
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from database import Database


def match_id_to_url(match_id):
    """Return match url given an id"""
    return "https://www.fifa.com/worldcup/matches/match/%s/" % match_id

def player_id_to_url(player_id):
    """Return player url given an id"""
    return "https://www.fifa.com/worldcup/players/player/%s/" % player_id


db = Database()

# use creds to create a client to interact with the Google Drive API
#scope = ['https://spreadsheets.google.com/feeds']
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

CREDS = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', SCOPE)
CLIENT = gspread.authorize(CREDS)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
DOC = CLIENT.open("Prode AA Rusia 2018")

FOUND = False
for sheet in DOC.worksheets():
    if sheet.title == "Goles":
        # print("Found it!")
        FOUND = True
        break

if not FOUND:
    exit()

GOALS = db.goals.select().execute().fetchall()
sheet.resize(len(GOALS), 6)
# jugador+jurl home home_score away away_score purl

for goal in GOALS:

    match = db.session.query(db.matches).filter(db.matches.columns.id == goal.match_id)[0]
    home = db.session.query(db.teams).filter(db.teams.columns.id == match.home_id)[0]
    away = db.session.query(db.teams).filter(db.teams.columns.id == match.away_id)[0]
    player = db.session.query(db.players).filter(db.players.columns.id == goal.player_id)[0]

    player_link = '=HYPERLINK("%s", "%s")' % (player_id_to_url(goal.player_id), player.name)
    match_link = '=HYPERLINK("%s", "match url")' % (match_id_to_url(goal.match_id))

    cells = sheet.range("A%d:F%d" % (goal.id, goal.id))
    values = [player_link,
              home.name, match.home_score,
              away.name, match.away_score,
              match_link]

    for c in cells:
        c.value = values[c.col - 1]

    #print(values)
    sheet.update_cells(cells, value_input_option='USER_ENTERED')
    sleep(0.5)
