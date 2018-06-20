#!/usr/bin/env python
# -*- coding: utf -*-

from sqlalchemy import create_engine, MetaData, func, select, and_
from sqlalchemy import Table, Column, Integer, Float, String, \
    ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker

import datetime

# TODO: Replace url column with a function that assembles the string

class Database():
    def __init__(self, echo=False):

        self.db = create_engine('sqlite:///db.sqlite',
                                convert_unicode=True,
                                echo=echo)
        # encoding defaults to utf8
        self.metadata = MetaData(bind=self.db)
        self.session = scoped_session(sessionmaker(self.db, autoflush=True,
                                                   autocommit=True))

        try:
            self.teams = Table('teams', self.metadata, autoload=True)
        except:
            self.teams = Table('teams', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', String(32)),
                               Column('url', String(64)),
                              )
            self.teams.create()

        try:
            self.matches = Table('matches', self.metadata, autoload=True)
        except:
            self.matches = Table('matches', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('url', String(64)),
                                 Column('home_id', String(32), ForeignKey('teams.id')),
                                 Column('away_id', String(32), ForeignKey('teams.id')),
                                 Column('home_score', Integer),
                                 Column('away_score', Integer),
                                 Column('last_updated', DateTime, onupdate=func.utc_timestamp()),
                                 UniqueConstraint('id', 'home_id', 'away_id'),
                                )
            self.matches.create()

        try:
            self.players = Table('players', self.metadata, autoload=True)
        except:
            self.players = Table('players', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('url', String(64)),
                                 Column('num', Integer),
                                 Column('pos', String(16)),
                                 Column('age', Integer),
                                 Column('height', Float),
                                 Column('name', String(64)),
                                 Column('team_id', String(32), ForeignKey('teams.id')),
                                 UniqueConstraint('name', 'team_id'))
            self.players.create()

        try:
            self.goals = Table('goals', self.metadata, autoload=True)
        except:
            self.goals = Table('goals', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('time', String(32)),
                               Column('player_id', String(32), ForeignKey('players.id')),
                               Column('match_id', String(32), ForeignKey('matches.id')),
                               UniqueConstraint('player_id', 'match_id', 'time'),
                              )
            self.goals.create()

"""def insertarJugador(j):
    try:
        j['equipo_id'] = db.session.query(db.teams).\
            filter_by(nombre=j['equipo'])[0][0]
    except:
        db.teams.insert({'nombre': j['equipo']}).execute()
        j['equipo_id'] = db.session.query(db.teams).\
            filter_by(nombre=j['equipo'])[0][0]

    try:
        j['posicion_id'] = db.session.query(db.posiciones).\
            filter_by(nombre=j['posicion'])[0][0]
    except:
        db.posiciones.insert({'nombre': j['posicion']}).execute()
        j['posicion_id'] = db.session.query(db.posiciones).\
            filter_by(nombre=j['posicion'])[0][0]

    j.pop('equipo')
    j.pop('posicion')
    try:
        db.players.insert(j).execute()
    except:
        print("Fallo: %s" % j)"""
