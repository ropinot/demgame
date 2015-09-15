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


