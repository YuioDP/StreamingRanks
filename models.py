from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    riot_id = db.Column(
        db.String(100),
        unique=True
    )

    puuid = db.Column(
        db.String(100),
        unique=True
    )

    region = db.Column(
        db.String(20)
    )


    twitch = db.Column(
        db.String(100)
    )


    kick = db.Column(
        db.String(100)
    )


    tier = db.Column(
        db.String(20)
    )


    rank = db.Column(
        db.String(10)
    )


    lp = db.Column(
        db.Integer
    )


    wins = db.Column(
        db.Integer
    )


    losses = db.Column(
        db.Integer
    )


    winrate = db.Column(
        db.Float
    )
