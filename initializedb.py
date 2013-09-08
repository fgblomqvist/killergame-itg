import sys
import random
from app import db, models


argv = sys.argv
db.create_all()

if len(argv) != 2:
    sys.exit()

if argv[1] == 'sample':
    players = [
        {'id': 41244, 'name': 'Daniel Magnusson', 'score': 3},
        {'id': 35342, 'name': 'Linda Dunger', 'score': 0},
        {'id': 81242, 'name': 'Jens Printz', 'score': 42},
        {'id': 14943, 'name': 'Daniel Berg', 'score': 13}
    ]

    for p in players:
        p_new = models.Player(p['id'], p['name'], score=p['score'])
        db.session.add(p_new)

    db.session.commit()

elif argv[1] == 'assign':

    available_offers = db.session.query(models.Player.id).all()

    for player in models.Player.query.all():
        while True:
            i = random.randint(0, (len(available_offers) - 1))
            if player.id != available_offers[i].id:
                player.offer_id = available_offers.pop(i).id
                break

    db.session.commit()