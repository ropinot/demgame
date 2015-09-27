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
    table = db.Column(db.Text)      #string containing the pickled version of the TableDict

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

    scenario = db.relationship('Scenario', backref='owner', lazy='dynamic') # this is used to connect the scenario to the admin, not for the players


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
        return unicode(self.role.role)

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
    status = db.Column(db.String(15))
    code = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(50))
    duration = db.Column(db.Integer)    #number of periods in the game
    leadtime = db.Column(db.Integer)    # from order to receipt (1 = today for tomorrow)
    forecast_horizon = db.Column(db.Integer) # number of forecasts visible
    frozen_horizon = db.Column(db.Integer)   # number of frozen periods
    product_cost = db.Column(db.Float)
    stock_cost = db.Column(db.Float)
    lostsale_cost = db.Column(db.Float())
    creation_date = db.Column(db.DateTime)
    activation_date = db.Column(db.DateTime)
    run_date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    demand_profile_id = db.Column(db.Integer, db.ForeignKey('demand_profiles.id'))

    gameboards = db.relationship('GameBoard', backref='scenario', lazy='dynamic')
    counters = db.relationship('ScenarioCounter', backref='scenario', lazy='dynamic')


class ScenarioCode(db.Model):
    """
    Store the scenario codes already used
    """
    __tablename__ = 'scenario_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True)


class DemandProfile(db.Model):
    """docstring for DemandProfile"""
    __tablename__ = 'demand_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text)
    initial_stock = db.Column(db.Integer)
    periods = db.Column(db.Integer)

    scenarios = db.relationship('Scenario', backref='demand_profile', lazy='dynamic')
    data = db.relationship('DemandData', backref='demand_profile', lazy='dynamic')


class DemandData(db.Model):
    """docstring for DemandData"""

    __tablename__ = 'demand_data'
    id = db.Column(db.Integer, primary_key=True)
    demand_profile_id = db.Column(db.Integer, db.ForeignKey('demand_profiles.id'))
    period = db.Column(db.Integer)
    demand = db.Column(db.Integer)
    forecast = db.Column(db.Integer)
    error = db.Column(db.Integer)










