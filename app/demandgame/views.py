from app import app, db
from app.models import Player, Scenario, GameBoard
from flask import render_template, redirect, session
from app.table import TableDict
from flask.ext.login import login_required, login_user, logout_user,  current_user
import sys


@app.route('/demandgame/dashboard')
@login_required
def demand_game_dashboard():
    player = Player.query.get(current_user.get_id())
    if not player:
        raise Exception('No player found')
    scenario = Scenario.query.get(session['scenario_id'])
    if not scenario:
        raise Exception('No scenario found')

    gameboard = player.gameboards.filter(GameBoard.scenario_id==session['scenario_id']).first()
    if not gameboard:
        print 'No gameboard found'
        raise Exception('No gameboard found')

    return render_template('demandgame/welcome.html', table=gameboard.data.get_HTML())

