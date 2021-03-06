from flask import render_template, request, url_for, redirect
from sqlalchemy import orm
from killergame_itg import app, db, models

@app.route('/', methods=['GET', 'POST'])
def home():
    alive_count = models.Player.query.filter(models.Player.offer_id != None).count()
    top_players = models.Player.query.filter(models.Player.score > 0).order_by(models.Player.score.desc()).limit(3).all()
    return render_template('index.html', alive_count=alive_count, top_players=top_players)


@app.route('/player', methods=['POST'])
def player():

    try:
        player_id = int(request.form['player'][3:])
    except ValueError:
        return render_template('invalid_input.html')

    try:
        player = get_player(player_id)
    except orm.exc.NoResultFound:
        return render_template('invalid_id.html')

    if player.offer_id:
        target = get_player(player.offer_id)
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

    try:
        killer = get_player(killer_id)
        target = get_player(target_id)
    except orm.exc.NoResultFound:
        return render_template('invalid_id.html')

    # if the killer is dead, go back
    if not killer.offer_id:
        return redirect(url_for('home'), code=303)

    # verify that the killer killed the right person
    if killer.offer_id != target_id:
        right_target = get_player(killer.offer_id)
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
    target = get_player(killer.offer_id)

    return render_template('target_killed.html', player=killer, target=target)


@app.route('/gameover')
def gameover():

    try:
        winner = get_player(1)
        second = get_player(2)
        third = get_player(3)
    except orm.exc.NoResultFound:
        return redirect(url_for('home'), code=303)

    return render_template('gameover.html', winner=winner, second=second, third=third)


@app.route('/manage', methods=['GET', 'POST'])
def manage():

    if request.method == 'GET':
        return render_template('manage.html')

    action = request.form['action']

    if action == 'kill':
        try:
            player_id = int(request.form['id'])
        except ValueError:
            return render_template('generic_error.html', error_msg='Ogiltligt ID, det måste vara ett heltal!')

        try:
            kill_player(player_id)
            return render_template('action_success.html')
        except orm.exc.NoResultFound:
            return render_template('generic_error.html', error_msg='En spelare med det ID\'t hittades inte!')
        except PlayerAlreadyDead:
            return render_template('generic_error.html', error_msg='Spelaren du försökte döda är redan död!')


def get_player(id):
    return models.Player.query.filter(models.Player.id == id).one()


def kill_player(id):
    # get the player that should be killed
    player = get_player(id)

    # verify that the player is not already dead
    if player.offer_id is None:
        raise PlayerAlreadyDead

    # get that player's killer
    killer = models.Player.query.filter(models.Player.offer_id == id).one()

    killer.offer_id = player.offer_id
    player.offer_id = None
    db.session.commit()


class PlayerAlreadyDead(Exception):

    def __str__(self):
        return 'The player is already dead!'