from app import app, db
from flask import render_template, redirect, url_for, Response, session, request
from flask.ext.login import login_required, login_user, logout_user,  current_user
from forms import LoginForm, RegistrationForm, NewGameForm
from app.models import Player, Role, Scenario, GameBoard
from game_constants import *
from sqlalchemy import and_, func
from app.demandgame import views
from app.table import TableDict


@app.route('/')
@app.route('/index')
def to_login():
    return redirect(url_for('login_view'))


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        player = form.get_player()
        login_user(player)

        # TODO: check the next parameter
        next = request.args.get('next')
        # if not next_is_valid(next):
        #     return abort(400)

        # check if the player has ACTIVE or RUNNING scenarios
        # if so, redirect to the game
        for scenario in player.played_scenario:
            if scenario.status in [ACTIVE, RUNNING]:
                session['scenario_code'] = scenario.code
                session['scenario_id'] = scenario.id
                return redirect(url_for('play_view'))

        return redirect(url_for('player_home_view'))
    return render_template('login_form.html', form=form)


@app.route('/register', methods=('GET', 'POST'))
def register_view():
    # TODO: add the registration date
    form = RegistrationForm()
    if form.validate_on_submit():
        player = Player()

        role = Role.query.filter_by(role='player').first()
        player.role_id = role.id

        form.populate_obj(player)
        db.session.add(player)
        db.session.commit()

        login_user(player)
        return redirect(url_for('player_home_view'))

    return render_template('registration_form.html', form=form)


@app.route('/home')
@login_required
def player_home_view():
    return render_template('player_home.html', user=current_user)


@app.route('/logout')
@login_required
def logout_view():
    session.clear()
    logout_user()
    return redirect(url_for('login_view'))


@app.route('/newgame', methods=['GET', 'POST'])
@login_required
def enter_game_code_view():
    form = NewGameForm()
    if form.validate_on_submit():
        # get the id of the scenario corresponding to the code
        scenario = db.session.query(Scenario).filter(and_(Scenario.code == form.code.data,
                                                          Scenario.status == ACTIVE)).first()
        if scenario:  # the code is valid
            player = db.session.query(Player).get(current_user.get_id())
            player.played_scenario.append(scenario)
            db.session.commit()
            session['scenario_id'] = scenario.id
            session['scenario_code'] = scenario.code

            scenario = Scenario.query.get(scenario.id)

            #init the gameboard
            gameboard = GameBoard()
            gameboard.period = 1
            gameboard.current_user = 1

            gameboard.data = TableDict(scenario.duration)

            #print gameboard.data.get_HTML()
            player.gameboards.append(gameboard)
            scenario.gameboards.append(gameboard)

            db.session.add(gameboard)

            db.session.commit()

            return redirect(url_for('demand_game_dashboard'))
        else:
            form = NewGameForm()
            return render_template('new_game_form.html', form=form, message='Code not valid')

    return render_template('new_game_form.html', form=form)


@app.route('/listresults')
@login_required
def list_results_view():
    return Response('List results')


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/sitemap")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))

    print links
    return Response('OK')
