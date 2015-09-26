# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, Response, redirect, url_for, request, jsonify, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from app.models import Scenario, Player, ScenarioCounter, ScenarioCode, DemandProfile, DemandData
from .forms import AdminLoginForm, CreateScenarioForm
from app.game_constants import *
from app.game_functions import admin_required
from admin_functions import get_new_scenario_code
from datetime import datetime
from sqlalchemy.exc import IntegrityError


@app.route('/admin')
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_view():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        admin = form.get_admin()
        login_user(admin)

        return redirect(url_for('admin_home_view', user=current_user))
    return render_template('admin/admin_login_form.html', form=form)


@app.route('/admin/logout')
@login_required
@admin_required
def admin_logout_view():
    session.clear()
    logout_user()
    return Response('<p align=center>Logged out<br/><br/><a href={}>Login again</a></p>'.format(url_for('admin_login_view')))


@app.route('/admin/create_scenario', methods=['GET', 'POST'])
@login_required
@admin_required
def create_new_scenario_view():
    form = CreateScenarioForm()
    form.demand_profile_id.choices = [(dp.id, dp.name) for dp in DemandProfile.query.all()]

    if form.validate_on_submit():

        # save the scenario
        scenario = Scenario()
        form.populate_obj(scenario)
        scenario.owner_id = current_user.get_id()
        scenario.code = get_new_scenario_code()
        scenario.status = IDLE
        scenario.creation_date = datetime.now()

        db.session.add(scenario)
        db.session.commit()


        # TODO: check the next parameter (?)
        # next = request.args.get('next')
        # if not next_is_valid(next):
        #     return abort(400)

        return redirect(url_for('admin_home_view'))
    return render_template('admin/create_scenario_form.html', user=current_user, form=form, action="Create")
#
#
# @app.route('/admin/edit_scenario/<scenario_code>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_scenario_view(scenario_code):
#     scenario = Scenario.query.get(get_scenario_id(scenario_code))
#     form = CreateScenarioForm(obj=scenario)
#     # the status of the economy can be set only when the scenario is created
#     # so we remove the field from the form
#     current_economy_status = scenario.economy_status
#     del form.economy_status
#
#     if request.method == 'GET':
#         # fill the form with the data from the DB
#         for supplier in scenario.supplier.all():
#             app.logger.info('--> update supp {}'.format(supplier.name))
#             app.logger.info('--> Initial capacity {}'.format(supplier.initial_capacity))
#             form['supp_{}_production_rate'.format(supplier.name)].data = supplier.production_rate
#             form['supp_{}_price_hoodie'.format(supplier.name)].data = supplier.wholesale_price_hoodie
#             form['supp_{}_price_trendy'.format(supplier.name)].data = supplier.wholesale_price_trendy
#             form['supp_{}_end_capacity'.format(supplier.name)].data = supplier.end_capacity
#             form['supp_{}_cancel_penalty'.format(supplier.name)].data = supplier.cancel_penalty
#
#         hoodie_costs = scenario.goodwillcost.filter(ProductGoodwillCost.product_family==HOODIE).first()
#         trendy_costs = scenario.goodwillcost.filter(ProductGoodwillCost.product_family==TRENDY).first()
#         for p in PRODUCTS:
#             form['goodwill_cost_hoodie_{}'.format(p)].data = getattr(hoodie_costs, p)
#             form['goodwill_cost_trendy_{}'.format(p)].data = getattr(trendy_costs, p)
#
#     if form.validate_on_submit():
#         #save form
#         form.populate_obj(scenario)
#
#         hoodie_costs = scenario.goodwillcost.filter(ProductGoodwillCost.product_family==HOODIE).first()
#         trendy_costs = scenario.goodwillcost.filter(ProductGoodwillCost.product_family==TRENDY).first()
#
#         for p in PRODUCTS:
#             setattr(hoodie_costs, p, form['goodwill_cost_hoodie_{}'.format(p)].data)
#             setattr(trendy_costs, p, form['goodwill_cost_trendy_{}'.format(p)].data)
#
#         db.session.add(scenario)
#         db.session.commit()
#
#         for supplier in scenario.supplier.all():
#             # supp = Supplier()
#             # supp.name = supplier
#             # app.logger.info('--> Supplier {} capacity: {}'.format(supplier, form['supp_{}_capacity'.format(supplier)].data))
#             supplier.production_rate = form['supp_{}_production_rate'.format(supplier.name)].data
#             supplier.current_capacity = supplier.production_rate
#             supplier.wholesale_price_hoodie = form['supp_{}_price_hoodie'.format(supplier.name)].data
#             supplier.wholesale_price_trendy = form['supp_{}_price_trendy'.format(supplier.name)].data
#             supplier.end_capacity = form['supp_{}_end_capacity'.format(supplier.name)].data
#             supplier.cancel_penalty = form['supp_{}_cancel_penalty'.format(supplier.name)].data
#             scenario.supplier.append(supplier)
#             db.session.add(supplier)
#             db.session.commit()
#
#
#
#         # TODO: save the demand data
#         return redirect(url_for('admin_home_view'))
#
#     return render_template('admin/create_scenario_form.html',
#                            user=current_user,
#                            form=form,
#                            action="Edit",
#                            current_economy_status=current_economy_status)


@app.route('/admin/demandprofile')
@login_required
@admin_required
def create_demand_profile():
    return render_template('admin/create_demand_profile.html', user=current_user)


@app.route('/admin/listdemandprofile')
@login_required
@admin_required
def list_demand_profiles():
    demand_profiles = DemandProfile.query.all()
    print demand_profiles
    return render_template('admin/list_demand_profiles.html', user=current_user)


@app.route('/admin/activate/<scenario_code>')
@login_required
@admin_required
def activate(scenario_code):
    scenario = Scenario.query.filter(Scenario.code == scenario_code).first()
    if scenario:
        scenario.status = ACTIVE
        db.session.commit()
        return redirect(url_for('list_scenario_view'))



@app.route('/admin/list_scenario')
@login_required
@admin_required
def list_scenario_view():
    player = Player.query.get(current_user.get_id())
    scenario = Scenario.query.filter_by(owner=player).order_by(Scenario.creation_date.desc())
    if scenario:
        return render_template('admin/list_scenario.html', user=current_user, scenario=scenario)
    else:
        return Response("<p>No scenario found</p>")
#
#
# @app.route('/admin/view_scenario/<scenario_code>')
# @login_required
# @admin_required
# def view_scenario_view(scenario_code):
#     scenario = Scenario.query.get(get_scenario_id(scenario_code))
#     if not scenario:
#         return list_scenario_view()
#
#     table_general = pt(['Parameter', 'Value'])
#     table_general.align['Parameter'] = 'l'
#     table_general.add_row(['Scenario name', scenario.name])
#     table_general.add_row(['Duration', str(scenario.duration)+' sec. per week'])
#     table_general.add_row(['Status of economy', scenario.economy_status])
#     table_general.add_row(['Order cost', str(scenario.order_cost)+' €/order'])
#     table_general.add_row(['Unit selling price Hoodie', str(scenario.selling_price_hoodie)+' €'])
#     table_general.add_row(['Unit selling price Trendy', str(scenario.selling_price_trendy)+' €'])
#     table_general.add_row(['Salvage value Hoodie', str(scenario.salvage_value_hoodie)+' €'])
#     table_general.add_row(['Salvage value Trendy', str(scenario.salvage_value_trendy)+' €'])
#     table_general.add_row(['Creation date', str(scenario.creation_date).split('.')[0]])
#     if scenario.activation_date:
#         table_general.add_row(['Activation date', str(scenario.activation_date).split('.')[0]])
#     if scenario.run_date:
#         table_general.add_row(['Run date', str(scenario.run_date).split('.')[0]])
#
#
#     table_general_html = table_general.get_html_string(attributes={'class': 'table table-striped table-condensed',
#                                                                    'style': 'width:60%',
#                                                                    'align': 'center'},
#                                                                    format=True)
#
#     table_suppliers = pt(['Parameter', 'Unit of measure', 'BR', 'CH', 'EU', 'US'])
#     table_suppliers.align['Parameter'] = 'l'
#     table_suppliers.align['Unit of measure'] = 'c'
#     table_suppliers.add_row(['Production rate', 'units/week']+[scenario.supplier.filter_by(name=p).first().production_rate for p in SUPPLIERS])
#     table_suppliers.add_row(['Wholesale unit price Hoodie', '€/unit']+[scenario.supplier.filter_by(name=p).first().wholesale_price_hoodie for p in SUPPLIERS])
#     table_suppliers.add_row(['Wholesale unit price Trendy', '€/unit']+[scenario.supplier.filter_by(name=p).first().wholesale_price_trendy for p in SUPPLIERS])
#     table_suppliers.add_row(['End capacity in period', 'period']+[scenario.supplier.filter_by(name=p).first().end_capacity for p in SUPPLIERS])
#     table_suppliers.add_row(['Cancel penalty', '% of wholesale price']+['{} %'.format(scenario.supplier.filter_by(name=p).first().cancel_penalty) for p in SUPPLIERS])
#
#     table_suppliers_html = table_suppliers.get_html_string(attributes={'class': 'table table-striped table-condensed',
#                                                                    'style': 'width:80%',
#                                                                    'align': 'center'},
#                                                                    format=True)
#
#     table_goodwill_cost = pt(['']+[p for p in PRODUCTS])
#     table_goodwill_cost.add_row(['Hoodie (€/unit)']+[getattr(scenario.goodwillcost.filter_by(product_family=HOODIE).first(), p) for p in PRODUCTS])
#     table_goodwill_cost.add_row(['Trendy (€/unit)']+[getattr(scenario.goodwillcost.filter_by(product_family=TRENDY).first(), p) for p in PRODUCTS])
#
#     table_goodwill_cost_html = table_goodwill_cost.get_html_string(attributes={'class': 'table table-striped table-condensed',
#                                                                    'style': 'width:80%',
#                                                                    'align': 'center'},
#                                                                    format=True)
#
#     table_demand = pt(['']+[p for p in PRODUCTS])
#     table_demand.add_row(['Hoodie (units)']+[getattr(scenario.demand.filter_by(product_family=HOODIE).first(), p) for p in PRODUCTS])
#     table_demand.add_row(['Trendy (units)']+[getattr(scenario.demand.filter_by(product_family=TRENDY).first(), p) for p in PRODUCTS])
#
#     table_demand_html = table_demand.get_html_string(attributes={'class': 'table table-striped table-condensed',
#                                                                    'style': 'width:80%',
#                                                                    'align': 'center'},
#                                                                    format=True)
#
#     return render_template('/admin/view_scenario.html', user=current_user,
#                                                         table_general=table_general_html,
#                                                         table_suppliers=table_suppliers_html,
#                                                         table_goodwill_cost=table_goodwill_cost_html,
#                                                         table_demand=table_demand_html)
#
#
#
# @app.route('/admin/run/<scenario_code>')
# @login_required
# @admin_required
# def run_view(scenario_code):
#     return render_template('admin/run.html',
#                            scenario_code=scenario_code,
#                            start_enabled=YES,
#                            pause_enabled=NO,
#                            resume_enabled=NO)
#
#
# @app.route('/admin/start_scenario/<scenario_code>', methods=['GET'])
# @login_required
# @admin_required
# def start_scenario(scenario_code):
#
#     def go_to_run_page(start_enabled, pause_enabled, resume_enabled):
#         """ Helper function to avoid repetitions """
#         return render_template("admin/run.html", status=msg,
#                                scenario_code=scenario_code,
#                                start_enabled=start_enabled,
#                                pause_enabled=pause_enabled,
#                                resume_enabled=resume_enabled)
#
#     msg = ''
#
#     # get the scenario from DB
#     scenario_id = get_scenario_id(scenario_code)
#     scenario = Scenario.query.get(scenario_id)
#
#     # save the scenario code and id
#     session['running_scenario'] = scenario_code
#     session['scenario_id'] = scenario_id
#
#     # change the status of the scenario in RUNNING
#     #set_scenario_status(scenario_id=scenario_id, status=RUNNING)
#
#     # check if a ScenarioCounter is already associated with the scenario
#     # (if yes, it means that the simulation has been already started)
#     if not scenario.counter:
#         # create and initialize the period counter
#         app.logger.debug('>> No counter associated with this scenario: create one')
#         scenario_counter = ScenarioCounter(scenario_id)
#         scenario.counter = scenario_counter
#
#     # check if a scheduler is already in place
#     if scenario.status == RUNNING:
#         app.logger.debug('The scenario is already running!')
#         msg += 'The scenario is already running (started {start_date})!<br/>Update every {update} seconds<br/>'.format(start_date=scenario.run_date,
#                                                                                                                         update=scenario.duration)
#         return go_to_run_page(start_enabled=NO,
#                               pause_enabled=YES,
#                               resume_enabled=NO)
#         # return render_template("admin/run.html", status=msg,
#         #                        scenario_code=scenario_code,
#         #                        start_enabled=NO,
#         #                        pause_enabled=YES,
#         #                        resume_enabled=NO)
#     elif scenario.status == PAUSED:
#         app.logger.debug('The scenario is paused!')
#         msg += 'The scenario is paused (started {start_date})!<br/>Update every {update} seconds<br/>'.format(start_date=scenario.run_date,
#                                                                                                                         update=scenario.duration)
#         return go_to_run_page(start_enabled=NO,
#                               pause_enabled=NO,
#                               resume_enabled=YES)
#         # return render_template("admin/run.html", status=msg,
#         #                        scenario_code=scenario_code,
#         #                        start_enabled=NO,
#         #                        pause_enabled=NO,
#         #                        resume_enabled=YES)
#     elif scenario.status == ACTIVE:
#         scheduler = BackgroundScheduler()
#         partial_tick = partial(tick, scenario_code, scheduler)
#
#         # add the job to the scheduler
#         try:
#             scheduler.add_job(partial_tick, 'interval', seconds=scenario.duration)
#             app.logger.info("Job addedd successfully")
#         except RuntimeError as e:
#             app.logger.info("Error on add_job(): {}".format(e))
#             msg += "Error on add_job(): {}<br/>".format(e)
#             return render_template("admin/run.html", status=msg,
#                                    scenario_code=scenario_code,
#                                    start_enabled=NO)
#
#         # start the scheduler
#         try:
#             scheduler.start()
#             app.logger.info("Scheduler started successfully!")
#             scenario.run_date = datetime.now()
#             scenario.status = RUNNING
#             db.session.commit()
#             msg += "<br/>Simulation started successfully. Update every {} seconds<br/>".format(scenario.duration)
#             # return render_template("admin/run.html", status=msg,
#             #                        scenario_code=scenario_code,
#             #                        start_enabled=NO)
#         except (RuntimeError, SchedulerAlreadyRunningError) as e:
#             app.logger.info("Scheduler already running!")
#             msg += "Scheduler already running!<br/>"
#
#         return go_to_run_page(start_enabled=NO,
#                               pause_enabled=YES,
#                               resume_enabled=NO)
#         # return render_template("admin/run.html", status=msg,
#         #                        scenario_code=scenario_code,
#         #                        start_enabled=NO)
#
#
#
# @app.route('/admin/pause_scenario/<scenario_code>')
# @login_required
# @admin_required
# def pause_scenario(scenario_code):
#     scenario = Scenario.query.get(get_scenario_id(scenario_code))
#     msg = '<br>Game paused'
#
#     if scenario and scenario.status == RUNNING:
#         scenario.status = PAUSED
#         db.session.commit()
#         app.logger.info('Game paused')
#
#     return render_template("admin/run.html",
#                            status=msg,
#                            scenario_code=scenario_code,
#                            start_enabled=NO,
#                            pause_enabled=NO,
#                            resume_enabled=YES)
#
#
# @app.route('/admin/resume_scenario/<scenario_code>')
# @login_required
# @admin_required
# def resume_scenario(scenario_code):
#     scenario = Scenario.query.get(get_scenario_id(scenario_code))
#     msg = 'Game is running. Update every {} seconds<br/>'.format(scenario.duration)
#
#     if scenario and scenario.status == PAUSED:
#         #restart the scheduler
#         scheduler = BackgroundScheduler()
#         partial_tick = partial(tick, scenario_code, scheduler)
#
#         # add the job to the scheduler
#         try:
#             scheduler.add_job(partial_tick, 'interval', seconds=scenario.duration)
#             app.logger.info("Job addedd successfully")
#         except RuntimeError as e:
#             app.logger.info("Error on add_job(): {}".format(e))
#             msg += "Error on add_job(): {}<br/>".format(e)
#             return render_template("admin/run.html", status=msg,
#                                    scenario_code=scenario_code,
#                                    start_enabled=NO)
#
#         # start the scheduler
#         try:
#             scheduler.start()
#             app.logger.info("Scheduler started successfully!")
#             scenario.run_date = datetime.now()
#             scenario.status = RUNNING
#             db.session.commit()
#             app.logger.info('Game resumed')
#
#             msg += "<br/>Simulation re-started successfully. Update every {} seconds<br/>".format(scenario.duration)
#             # return render_template("admin/run.html", status=msg,
#             #                        scenario_code=scenario_code,
#             #                        start_enabled=NO)
#         except (RuntimeError, SchedulerAlreadyRunningError) as e:
#             app.logger.info("Scheduler already running!")
#             msg += "Scheduler already running!<br/>"
#
#
#     return render_template("admin/run.html",
#                            status=msg,
#                            scenario_code=scenario_code,
#                            start_enabled=NO,
#                            pause_enabled=YES,
#                            resume_enabled=NO)
#
#
@app.route('/admin/home', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home_view():
    return render_template("admin/admin_home.html", user=current_user, status="Welcome admin")


@app.route('/admin/demandprofile/save',  methods=['GET', 'POST'])
def save_demand_profile():
    #0 = period
    #1 = demand
    #2 = error
    #3 = forecast
    # forecast is recalculated because it doesn't come from the call

    #TODO: save the number of periods
    dp = DemandProfile()
    dp.name = str(request.json['demand_profile_name'])
    dp.description = str(request.json['demand_profile_description'])
    dp.initial_stock = int(request.json['initial_stock'])

    try:
        db.session.add(dp)
        db.session.commit()
    except IntegrityError:
        return jsonify(status=-1)

    # app.logger.info(request.json['data'][1])
    # app.logger.info(request.json['data'][2])
    # app.logger.info(request.json['data'][3])
    demand = request.json['data'][1]
    error = request.json['data'][2]

    for period, value in enumerate(demand):
        if period == 0:
            continue
        if not value:
            break
        data = DemandData()
        data.period = period
        data.demand = value
        data.error = error[period]
        data.forecast = int(value) * (1+ int(error[period])/100.)
        dp.data.append(data)
        db.session.add(data)

    db.session.commit()
    return jsonify(status=1)



# @app.route('/admin/waiting/<scenario_code>')
# @login_required
# @admin_required
# def waiting_view(scenario_code):
#     """
#     Called when the scenario is ACTIVATED
#     :param scenario_code:
#     :return:
#     """
#
#     # get the scenario ID and the Scenario object
#     scenario_id = get_scenario_id(scenario_code)
#     scenario = Scenario.query.get(scenario_id)
#
#     # Activate the scenario
#     if scenario:
#         scenario.status = ACTIVE
#         scenario.activation_date = datetime.now()
#         db.session.commit()
#
#         return render_template('admin/waiting_players.html', scenario_code=scenario_code)
#     else:
#         return Response('<p>No scenario with code {}<br/>'.format(scenario_code))
#
#
#
# @app.route('/admin/pollplayers', methods=['GET', 'POST'])
# @admin_required
# def poll_players():
#     """
#     Function called (long polling) by the waiting page to collect the name of the players
#     :return: the list of players
#     """
#
#     scenario_id = get_scenario_id(request.json['scenario_code'])
#     scenario = Scenario.query.get(scenario_id)
#
#     if scenario:
#         return jsonify(status=0,
#                        num=len(scenario.players.all()),
#                        players=[dict(login=p.login) for p in scenario.players.all()])
#     else:
#         return jsonify(status=-1, num=0)
#
#
# @app.route('/admin/scenario_results/<scenario_code>')
# @admin_required
# def scenario_results_view(scenario_code):
#     """
#     Shows the results for the specified scenario
#     """
#     # if we are here, the game is ended. Thus, no remove the scheduler flag
#     session['scheduler_present'] = NO
#
#     ranking = {}
#     scenario = Scenario.query.get(get_scenario_id(scenario_code))
#     for res in enumerate(scenario.results.order_by(PlayerResult.final_profit.desc()).all()):
#         ranking[res[0]] = {'player_id': res[1].game_results.id,
#                            'login': res[1].game_results.login,
#                            'profit': res[1].final_profit}
#
#     return render_template('/admin/scenario_results.html',
#                            user=current_user,
#                            ranking=ranking,
#                            scenario_name=scenario.name,
#                            scenario_code=scenario.code)
#
#     # return Response('<center><h3>Result page</h3><br/><a href={}>Home</a></center>'.format(url_for('admin_home_view')))
#
#
#
# @app.route('/not_implemented_yet')
# def not_implemented_yet_view():
#     return Response('<center><h3>Not implemented yet</h3><br/><a href="{}">Home</a><center>'.format(url_for('admin_home_view')))
#
#
#
#
# @app.route('/admin/vardump')
# def vardump():
#     return Response("""<h4>Counter:  {}<br/>
#
#
#
#                     </h4>""".format(session['counter']))
