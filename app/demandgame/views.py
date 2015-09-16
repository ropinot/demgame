from app import app, db
from app.models import Player, Scenario, GameBoard
from flask import render_template, redirect, session
from app.table import TableDict
from flask.ext.login import login_required, login_user, logout_user,  current_user
import sys


@app.route('/demandgame/dashboard', methods=['GET', 'POST'])
@login_required
def demand_game_dashboard():
    # get the currently played gameboard for the player
    player = Player.query.get(current_user.get_id())
    if not player:
        raise Exception('No player found')

    scenario = Scenario.query.get(session['scenario_id'])
    if not scenario:
        raise Exception('No scenario found')

    gameboard = player.gameboards.filter(GameBoard.scenario_id==session['scenario_id']).first()
    if not gameboard:
        raise Exception('No gameboard found')

    current_period = gameboard.period
    gameboard.period += 1
    gameboard.table.data['current'] = gameboard.period
    gameboard.table.set_cell('order', 2, 1000)
    if gameboard.period > scenario.duration:
        # finish the game
        pass

    db.session.commit()
    print gameboard.table.print_table()
    return render_template('demandgame/dashboard.html',
                            table=gameboard.table.get_HTML(),
                            period=gameboard.period)

