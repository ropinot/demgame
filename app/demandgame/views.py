from __future__ import division
from app import app, db
# from app.views import error_view
from app.models import Player, Scenario, GameBoard, DemandData, DemandProfile
from app.table import TableDict
from app.demandgame.forms import OrderForm
from flask import render_template, redirect, session, url_for, Response
from flask.ext.login import login_required, login_user, logout_user,  current_user
from sqlalchemy import and_
from random import random, randint

import sys
import cPickle

@app.route('/demandgame/dashboard', methods=['GET', 'POST'])
@login_required
def demand_game_dashboard():
    # get the player, scenario and gameboard
    try:
        player, scenario, gameboard = get_game_data()
    except Exception as e:
        app.logger.error(e)
        return redirect(url_for('error_view'))

    #TODO: define a method in the Gameboard model to return the table
    #TEST: create a test before
    data = cPickle.loads(str(gameboard.table))
    current_period = gameboard.period
    data.set_current(gameboard.period)
    gameboard.period += 1


    if current_period > scenario.duration + 1:
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

    # display the stock
    if current_period == 1:
        data.set_cell('stock', current_period, demand_profile.initial_stock)
    else:
        previous_stock = data.get_cell('stock', current_period - 1)
        current_stock = max(0, previous_stock +\
                               data.get_cell('order', current_period - scenario.leadtime) -\
                               data.get_cell('demand', current_period-1))

        data.set_cell('stock', current_period, current_stock)

    # display sales and lost-sales
    #TODO: refactor the call to the data values
    sales = min((data.get_cell('stock', current_period - 1) + data.get_cell('received', current_period - 1)),
                 data.get_cell('demand', current_period - 1))

    data.set_cell('sales', current_period - 1, sales)

    # s = '<font color="{color}">{value}</font>'
    lost_sales = max(0, data.get_cell('demand', current_period - 1) - (data.get_cell('stock', current_period - 1) + data.get_cell('received', current_period - 1)))
    data.set_cell('lost_sales', current_period - 1, lost_sales)

    # display the forecast over the forecast horizon
    #TODO: jitter the data beyond the frozen horizon
    # generate the demand_jittering list with 1.0 for the frozen periods and random values beyond it

    demand_jittering = jittering(scenario.forecast_horizon, scenario.frozen_horizon)
    app.logger.debug('jittering: {}'.format(str(demand_jittering)))

    for t in xrange(scenario.forecast_horizon):
        #TODO: reduce to one query?
        demand_profile_data = demand_profile.data.filter(DemandData.period == current_period+t).first()
        try:
            data.set_cell('forecast', current_period+t,
                          int(demand_profile_data.forecast * demand_jittering[t]))
        except AttributeError:
            pass

    # display the error
    data.set_cell('error', current_period - 1,
                  data.get_cell('forecast', current_period - 1) - data.get_cell('demand', current_period - 1))

    mape = 0.0
    rolling_mape = 0.0
    if current_period > 1:
        # get data for the MAPE
        demand_all = data.get_interval('demand', 0, current_period-1)
        forecast_all = data.get_interval('forecast', 0, current_period-1)
        app.logger.debug('demand all: {}'.format(str(demand_all)))
        app.logger.debug('forecast all: {}'.format(str(forecast_all)))
        mape = float(MAPE(demand_all, forecast_all))
        app.logger.info('MAPE: {} %'.format(mape))

        # get data for the rolling MAPE (3 periods)
        demand_3_periods = data.get_interval('demand', current_period - 3, current_period-1)
        forecast_3_periods = data.get_interval('forecast', current_period - 3, current_period-1)
        app.logger.debug('demand 3: {}'.format(str(demand_3_periods)))
        app.logger.debug('forecast 3: {}'.format(str(forecast_3_periods)))
        rolling_mape = float(MAPE(demand_3_periods, forecast_3_periods))
        app.logger.info('ROLLING MAPE: {} %'.format(mape))

    # save the updated table on DB
    gameboard.table = cPickle.dumps(data)
    db.session.commit()
    form.qty.data = 0

    return render_template('demandgame/dashboard.html',
                            table=data.get_HTML(),
                            period=data.data['current'],
                            form=form,
                            leadtime=scenario.leadtime,
                            forecast_horizon=scenario.forecast_horizon,
                            mape=mape,
                            rolling_mape=rolling_mape)


@app.route('/demandgame/results', methods=['GET', 'POST'])
@login_required
def results_view():
    # get the info about the player and the scenario

    try:
        player, scenario, gameboard = get_game_data()
    except Exception as e:
        app.logger.error(e)
        return redirect(url_for('error_view'))

    data = cPickle.loads(str(gameboard.table))

    total_demand = sum(map(int, data.data['demand'].values()))
    total_sales = sum(data.data['sales'].values())
    total_lost_sales = sum(data.data['lost_sales'].values())
    total_purchase = sum(data.data['order'].values())

    return render_template('/demandgame/results.html',
                            total_demand=total_demand,
                            total_sales=total_sales,
                            total_lost_sales=total_lost_sales,
                            total_purchase=total_purchase)


def get_game_data():
    """ Get the data about the player, the scenario and the gameboard """

    player = Player.query.get(current_user.get_id())
    if not player:
        raise Exception('No player found')

    scenario = Scenario.query.get(session['scenario_id'])
    if not scenario:
        raise Exception('No scenario found')

    gameboard = player.gameboards.filter(GameBoard.scenario_id==session['scenario_id']).first()

    if not gameboard:
        raise Exception('No gameboard found')

    return (player, scenario, gameboard)


def MAPE(demand, forecast):
    """ Return the MAPE """
    if len(demand) != len(forecast):
        app.logger.error('In MAPE, demand and forecast have different len')
        return -1

    n = len(demand)
    mape = 0.0
    for d, f in zip(demand, forecast):
        mape += abs(d - f) / d

    return '{:.1f}'.format(mape * 100./ n)


def jittering(forecast_horizon, frozen_horizon):
    jittering = [1. for _ in xrange(frozen_horizon)]
    #TODO: increase jitter according to forecast horizon
    step = 5
    for t in xrange(frozen_horizon, forecast_horizon):
        delta = randint(5*t, 5*(t+1))/100.
        if randint(1, 100) <= 50:
            jittering.append(1. + delta)
        else:
            jittering.append(1. - delta)

    return jittering


