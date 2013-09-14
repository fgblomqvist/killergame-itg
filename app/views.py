from flask import render_template, request, url_for, redirect
from sqlalchemy import orm
from app import app, db, models

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/player', methods=['POST'])
def player():

    try:
        player_id = int(request.form['player'])
    except ValueError:
        return 'Invalid player ID'

    try:
        player = models.Player.query.filter(models.Player.id == player_id).one()
    except orm.exc.NoResultFound:
        return "A player with this ID doesn't exist"

    if player.offer_id:
        target = models.Player.query.filter(models.Player.id == player.offer_id).one()
    else:
        target = None

    return render_template('player.html', player=player, target=target)


@app.route('/players')
def players():

    players = models.Player.query.order_by(models.Player.score.desc()).all()

    return render_template('players.html', players=players)


@app.route('/confirm', methods=['POST'])
def confirm():

    try:
        killer_id = int(request.form['player'])
        target_id = int(request.form['target'])
    except ValueError:
        return 'Invalid data!'

    # if the ids match, go back to home
    if killer_id == target_id:
        return redirect(url_for('home'), code=307)

    killer = models.Player.query.filter(models.Player.id == killer_id).one()
    target = models.Player.query.filter(models.Player.id == target_id).one()

    # if the killer is dead, go back
    if not killer.offer_id:
        return redirect(url_for('home'), code=307)

    # verify that the killer killed the right person
    if killer.offer_id != target_id:
        return render_template('wrong_target.html', target=target)

    # give the killer cred
    killer.score += 1

    # transfer the target
    killer.offer_id = target.offer_id

    # declare the victim as dead by setting its offer_id to None
    target.offer_id = None

    # fetch the info about the new target
    target = models.Player.query.filter(models.Player.id == killer.offer_id).one()

    db.session.commit()

    return render_template('target_killed.html', player=killer, target=target)