from app import app, db
from flask import render_template
from app.table import TableDict


@app.route('/demandgame')
def demand_game_dashboard():

    T = TableDict(30)
    T.current_period = 4
    T.set_cell('order', 4, 1000)
    T.set_cell('forecast', 2, 5000)
    return render_template('demandgame/welcome.html', table=T.get_HTML())
    #return "Hello from demandgame!"

