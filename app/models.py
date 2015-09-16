# -*- coding: utf-8 -*-
from app import db

players_scenario = db.Table('players_scenario',
                            db.Column('player_id', db.Integer, db.ForeignKey('players.id')),
                            db.Column('scenario_id', db.Integer, db.ForeignKey('scenarios.id')))

class GameBoard(db.Model):
    """docstring for GameBoard"""
    __tablename__ = 'gameboards'

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer)
    tablestring = db.Column(db.PickleType)      #string containing the pickled version of the TableDict

    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))

    # stock = db.Column(db.Integer)       #at the beginning of the period
    # demand = db.Column(db.Integer)      #in the period
    # order = db.Column(db.Integer)       #during the period
    # forecast = db.Column(db.Integer)    #for the period
    # received = db.Column(db.Integer)    #ordered current - LT -1 periods ago


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), unique=True)

    players = db.relationship('Player', backref='role', lazy='dynamic')


class Player(db.Model):
    """docstring for Player"""
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    gameboards = db.relationship('GameBoard', backref='player', lazy='dynamic')
    scenario_counters = db.relationship('ScenarioCounter', backref='player', lazy='dynamic')

    played_scenario = db.relationship('Scenario', secondary=players_scenario,
                                   backref=db.backref('players', lazy='dynamic')) # this is used to connect the scenario to the players

    #scenario = db.relationship('Scenario', backref='owner', lazy='dynamic') # this is used to connect the scenario to the admin, not for the players

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_role(self):
        return unicode(self.role)

    # Required for administrative interface
    def __unicode__(self):
        return self.login

    def __repr__(self):
        return '<Player (%d) %r>' % (self.id, self.login)


class ScenarioCounter(db.Model):
    __tablename__ = 'scenario_counters'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
    current = db.Column(db.Integer)


class Scenario(db.Model):
    """docstring for Scenario"""

    __tablename__ = 'scenarios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    duration = db.Column(db.Integer)    #number of periods in the game
    leadtime = db.Column(db.Integer)
    product_cost = db.Column(db.Float)
    stock_cost = db.Column(db.Float)
    lostsale_cost = db.Column(db.Float())

    gameboards = db.relationship('GameBoard', backref='scenario', lazy='dynamic')
    counters = db.relationship('ScenarioCounter', backref='scenario', lazy='dynamic')





