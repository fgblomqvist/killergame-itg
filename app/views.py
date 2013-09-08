from flask import render_template, request
from app import app, models

@app.route('/')
def home():
    return 'ITG Killergame'


@app.route('/players')
def players():

    players = models.Player.query.all()

    return render_template('players.html', players=players)

