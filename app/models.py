# -*- coding: utf-8 -*-
from app import db

class Decision(db.Model):
    """docstring for Decision"""
    __tablename__ = 'decisions'

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer)
    stock = db.Column(db.Integer)       #at the beginning of the period
    demand = db.Column(db.Integer)      #in the period
    order = db.Column(db.Integer)       #during the period
    forecast = db.Column(db.Integer)    #for the period
    received = db.Column(db.Integer)    #ordered current - LT -1 periods ago

    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))


class Player(db.Model):
    """docstring for Player"""
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))

    decisions = db.relationship('Decision', backref='decisionmaker', lazy='dynamic')
    scenario_counters = db.relationship('ScenarioCounter', backref='player', lazy='dynamic')


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

    decisions = db.relationship('Decision', backref='scenario', lazy='dynamic')
    scenario_counters = db.relationship('ScenarioCounter', backref='scenario', lazy='dynamic')





