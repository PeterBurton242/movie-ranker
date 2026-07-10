from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movie.id')
    )

    rating = db.Column(db.Integer)
    seen = db.Column(db.Boolean)


class Top10(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movie.id')
    )

    rank = db.Column(db.Integer)