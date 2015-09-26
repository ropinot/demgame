from app import app, db
from app.models import Player, Scenario, GameBoard, DemandData, DemandProfile
from flask import render_template, redirect, session, url_for, Response
from app.table import TableDict
from flask.ext.login import login_required, login_user, logout_user,  current_user
from app.demandgame.forms import OrderForm
from sqlalchemy import and_
import sys
import cPickle

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


    data = cPickle.loads(str(gameboard.table))
    current_period = gameboard.period
    data.set_current(gameboard.period)
    gameboard.period += 1


    if gameboard.period > scenario.duration:
        return redirect(url_for('results_view'))

    # fill up the table with data to show

    # record the order
    try:
        form = OrderForm()
        if form.validate():
            app.logger.debug('Form is valid')
            if int(form.qty.data) > 0:
                app.logger.info('Record an order for {} units in period {}'.format(form.qty.data, current_period))
                data.set_cell('order', current_period-1, int(form.qty.data)) # current_period - 1 because the current period has already been updated
            else:
                app.logger.info('No order to record in period {}'.format(current_period))
        else:
            app.logger.debug('Form is NOT valid')
    except UnboundLocalError:
        app.logger.debug('No form')

    # get the demand profile
    demand_profile = scenario.demand_profile

    # get the current period data
    demand_profile_data = demand_profile.data.filter(DemandData.period == current_period).first()

    # display the demand
    data.set_cell('demand', current_period-1, demand_profile_data.demand)

    # display the received quantity
    data.set_cell('received',
                   current_period,
                   data.get_cell('order', current_period - scenario.leadtime)) # get the order of leadtime periods ago

    # display the forecast over the forecast horizon
    for t in xrange(scenario.forecast_horizon):
        #TODO: reduce to one query without for loop
        demand_profile_data = demand_profile.data.filter(DemandData.period == current_period+t).first()
        try:
            data.set_cell('forecast', current_period+t, demand_profile_data.forecast)
        except AttributeError:
            pass

    # calculate the current stock



    # save the updated table on DB
    gameboard.table = cPickle.dumps(data)
    db.session.commit()
    form.qty.data = 0

    return render_template('demandgame/dashboard.html',
                            table=data.get_HTML(),
                            period=data.data['current'],
                            form=form,
                            leadtime=scenario.leadtime,
                            forecast_horizon=scenario.forecast_horizon)

@app.route('/demandgame/results', methods=['GET', 'POST'])
@login_required
def results_view():
    return Response('<br><h3>Game ended</h3>')
