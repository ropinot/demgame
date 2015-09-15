from app import app, db
from flask import render_template


@app.route('/demandgame')
def demand_game_dashboard():
    return render_template('demandgame/welcome.html')
    #return "Hello from demandgame!"
    