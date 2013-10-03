from flask import render_template, request, url_for, redirect
from sqlalchemy import orm
from killergame_itg import app, db, models

@app.route('/', methods=['GET', 'POST'])
def home():
    alive_count = models.Player.query.filter(models.Player.offer_id != None).count()
    return render_template('index.html', alive_count=alive_count)


@app.route('/player', methods=['POST'])
def player():

    try:
        player_id = int(request.form['player'][3:])
    except ValueError:
        return render_template('invalid_input.html')

    try:
        player = models.Player.query.filter(models.Player.id == player_id).one()
    except orm.exc.NoResultFound:
        return render_template('invalid_id.html')

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
        target_id = int(request.form['target'][3:])
    except ValueError:
        return render_template('invalid_input.html')

    # if the ids match, go back to home
    if killer_id == target_id:
        return redirect(url_for('home'), code=303)

    killer = models.Player.query.filter(models.Player.id == killer_id).one()
    target = models.Player.query.filter(models.Player.id == target_id).one()

    # if the killer is dead, go back
    if not killer.offer_id:
        return redirect(url_for('home'), code=303)

    # verify that the killer killed the right person
    if killer.offer_id != target_id:
        right_target = models.Player.query.filter(models.Player.id == killer.offer_id).one()
        return render_template('wrong_target.html', target=right_target)

    # give the killer cred
    killer.score += 1

    if killer.id == target.offer_id:
        # the killer has won the game
        killer.offer_id = 1

        # the target got on second place
        target.offer_id = 2

        db.session.commit()
        return redirect(url_for('gameover'), code=303)

    # transfer the target
    killer.offer_id = target.offer_id

    # check if the target ended up at third place
    if models.Player.query.filter(models.Player.offer_id != None).count() == 3:
        target.offer_id = 3
    else:
        # just set it as dead
        target.offer_id = None

    db.session.commit()

    # fetch the info about the new target
    target = models.Player.query.filter(models.Player.id == killer.offer_id).one()

    return render_template('target_killed.html', player=killer, target=target)


@app.route('/gameover')
def gameover():

    try:
        winner = models.Player.query.filter(models.Player.offer_id == 1).one()
        second = models.Player.query.filter(models.Player.offer_id == 2).one()
        third = models.Player.query.filter(models.Player.offer_id == 3).one()
    except orm.exc.NoResultFound:
        return redirect(url_for('home'), code=303)

    return render_template('gameover.html', winner=winner, second=second, third=third)