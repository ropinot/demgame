from app import app, db
from app.table import TableDict
from nose.tools import assert_equal, assert_in, with_setup
from app.models import Player, Scenario, GameBoard, ScenarioCounter


def setup_func():
    "set up test fixtures"
    app.config.from_object('config.TestingConfig')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'sekrit!'
    db.create_all()

def teardown_func():
    "tear down test fixtures"
    db.session.remove()
    db.drop_all()
    app.config.from_object('config.DevelopmentConfig')
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['CSRF_ENABLED'] = True


@with_setup(setup_func, teardown_func)
def test_DB():

    player = Player()
    player.login = 'Pippo'
    scenario = Scenario()
    scenario.name = 'scenario 1'
    scenario.leadtime = 10
    scenario.duration = 20
    gameboard = GameBoard()
    gameboard.period = 1
#    T = TableDict(10)
#    T.set_cell('order', 5, 1000)
#    T.set_cell('forecast', 8, 10)

    gameboard.data = TableDict(10)
    gameboard.data.set_cell('order', 5, 1000)
    gameboard.data.set_cell('forecast', 8, 10)

    scenario_counter = ScenarioCounter()

    player.gameboards.append(gameboard)
    player.played_scenario.append(scenario)
    player.scenario_counters.append(scenario_counter)
    scenario.gameboards.append(gameboard)
    scenario.counters.append(scenario_counter)

    db.session.add(player)
    db.session.add(scenario)
    db.session.add(gameboard)
    db.session.add(scenario_counter)

    db.session.commit()

    pl = db.session.query(Player).first()
    assert_equal('Pippo', pl.login)
    assert_equal('scenario 1', pl.played_scenario[0].name)
    d = pl.gameboards.filter(GameBoard.scenario_id==scenario.id).first()

    assert_in('<table', d.data.get_HTML())
    assert_equal(d.data.get_cell('order', 5), 1000)
    assert_equal(d.data.get_cell('order', 8), 0)
    assert_equal(d.data.get_cell('forecast', 8), 10)
    assert_equal(d.data.get_cell('forecast', 1), 0)
    assert_equal(d.data.get_cell('forecast', 15), None)

