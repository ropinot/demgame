from app import app, db

@app.route('/demandgame')
def dgindex():
    return "Hello from demandgame!"
    