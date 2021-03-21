from app import app, db


class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    YardName = db.Column(db.String(128), index=True, unique=True)
    YardArea = db.Column(db.Float)
    YardType = db.Column(db.String(64), index=True)
    Coordinates = db.Column(db.String(32))
