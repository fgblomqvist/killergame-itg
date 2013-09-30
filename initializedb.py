import sys
import random
from app import db, models


argv = sys.argv
db.create_all()

if len(argv) < 2:
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

    players = models.Player.query.all()
    random.shuffle(players)

    previous = players[-1]

    for player in players:
        player.offer_id = previous.id
        previous = player

    db.session.commit()

else:
    # import players from a csv file in the following format:
    # Firstname;Lastname;SOD12345

    with open(argv[1], mode='r', encoding='iso-8859-1') as f:
        for line in f:
            data = line.rstrip().split(';', 2)
            player = models.Player(int(data[2][3:]), '{0} {1}'.format(data[0], data[1]))
            db.session.add(player)

    db.session.commit()