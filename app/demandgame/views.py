from app import app, db
# from app.views import error_view
from app.models import Player, Scenario, GameBoard, DemandData, DemandProfile
from app.table import TableDict
from app.demandgame.forms import OrderForm
from flask import render_template, redirect, session, url_for, Response
from flask.ext.login import login_required, login_user, logout_user,  current_user
from sqlalchemy import and_
import sys
import cPickle

@app.route('/demandgame/dashboard', methods=['GET', 'POST'])
@login_required
def demand_game_dashboard():
    # get the currently played gameboard for the player

    # player = Player.query.get(current_user.get_id())
    # if not player:
    #     raise Exception('No player found')

    # scenario = Scenario.query.get(session['scenario_id'])
    # if not scenario:
    #     raise Exception('No scenario found')

    # gameboard = player.gameboards.filter(GameBoard.scenario_id==session['scenario_id']).first()

    # if not gameboard:
    #     raise Exception('No gameboard found')
    try:
        player, scenario, gameboard = get_game_data()
    except Exception as e:
        app.logger.error(e)
        return redirect(url_for('error_view'))

    #TODO: define a method in the Gameboard model to return the table
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
    for t in xrange(scenario.forecast_horizon):
        #TODO: reduce to one query without for loop
        demand_profile_data = demand_profile.data.filter(DemandData.period == current_period+t).first()
        try:
            data.set_cell('forecast', current_period+t, demand_profile_data.forecast)
        except AttributeError:
            pass

    # display the error
    data.set_cell('error', current_period - 1,
                  data.get_cell('forecast', current_period - 1) - data.get_cell('demand', current_period - 1))

    #TODO: calculate the MAPE and the rolling MAPE

    # save the updated table on DB
    gameboard.table = cPickle.dumps(data)
    db.session.commit()
    form.qty.data = 0

    #TODO: add MAPE and rolling MAPE data
    return render_template('demandgame/dashboard.html',
                            table=data.get_HTML(),
                            period=data.data['current'],
                            form=form,
                            leadtime=scenario.leadtime,
                            forecast_horizon=scenario.forecast_horizon)


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
