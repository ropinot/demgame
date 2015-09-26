from app import app, db
from app.models import Player, Scenario, GameBoard
from flask import render_template, redirect, session, url_for, Response
from app.table import TableDict
from flask.ext.login import login_required, login_user, logout_user,  current_user
from app.demandgame.forms import OrderForm
import sys
import cPickle

@app.route('/demandgame/dashboard', methods=['GET', 'POST'])
@login_required
def demand_game_dashboard():
    # get the currently played gameboard for the player
    form = OrderForm()
    player = Player.query.get(current_user.get_id())
    if not player:
        raise Exception('No player found')

    scenario = Scenario.query.get(session['scenario_id'])
    if not scenario:
        raise Exception('No scenario found')

    gameboard = player.gameboards.filter(GameBoard.scenario_id==session['scenario_id']).first()
    if not gameboard:
        raise Exception('No gameboard found')


    data = cPickle.loads(str(gameboard.table))
    current_period = gameboard.period
    data.set_current(gameboard.period)
    gameboard.period += 1
    # data.set_cell('order', 2, 1000)

    if gameboard.period > scenario.duration:
        return redirect(url_for('results_view'))


    gameboard.table = cPickle.dumps(data)
    db.session.commit()

    # print gameboard.table.print_table()
    return render_template('demandgame/dashboard.html',
                            table=data.get_HTML(),
                            period=data.data['current'],
                            form=form)

@app.route('/demandgame/results', methods=['GET', 'POST'])
@login_required
def results_view():
    return Response('<br><h3>Game ended</h3>')
