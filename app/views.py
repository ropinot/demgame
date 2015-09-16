from app import app, db
from flask import render_template, redirect, url_for, Response, session, request
from flask.ext.login import login_required, login_user, logout_user,  current_user
from forms import LoginForm, RegistrationForm, NewGameForm
from app.models import Player, Role


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


@app.route('/newgame')
@login_required
def enter_game_code_view():
    return Response('Enter game code')


@app.route('/listresults')
@login_required
def list_results_view():
    return Response('List results')
