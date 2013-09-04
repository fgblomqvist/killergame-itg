from app import db

class Player(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    score = db.Column(db.Integer)
    offer_id = db.Column(db.Integer)

    def __init__(self, id, name, offer_id, score=0):
        self.id = id
        self.name = name
        self.score = score
        self.offer_id = offer_id