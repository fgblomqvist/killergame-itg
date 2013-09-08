from flask import render_template, request
from app import app, db, models

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        try:
            killer_id = int(request.form['killer'])
            victim_id = int(request.form['victim'])
        except ValueError:
            return 'Invalid data!'

        killer = models.Player.query.filter(models.Player.id == killer_id).one()
        victim = models.Player.query.filter(models.Player.id == victim_id).one()

        # verify that the killer killed the right person
        if killer.offer_id != victim_id:
            return "These are not the droids you're looking for"

        # give the killer cred
        killer.score += 1

        # transfer the victim
        killer.offer_id = victim.offer_id

        # declare the victim as dead by setting its offer_id to None
        victim.offer_id = None

        db.session.commit()

        return 'Dadadum dum dum...another bitch bites the dust!'

    else:
        return render_template('index.html')


@app.route('/players')
def players():

    players = models.Player.query.all()

    return render_template('players.html', players=players)

