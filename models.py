from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        nullable=False
    )

    ratings = db.relationship(
        "Rating",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    top_picks = db.relationship(
        "TopPick",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Movie(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String,
        nullable=False
    )

    year = db.Column(
        db.Integer
    )

    tmdb_id = db.Column(
        db.Integer,
        unique=True
    )

    poster_url = db.Column(
        db.String
    )

    ratings = db.relationship(
        "Rating",
        back_populates="movie",
        cascade="all, delete-orphan"
    )

    top_picks = db.relationship(
        "TopPick",
        back_populates="movie",
        cascade="all, delete-orphan"
    )


class Rating(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "movie_id"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey("movie.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer
    )

    seen = db.Column(
        db.Boolean,
        default=True
    )

    user = db.relationship(
        "User",
        back_populates="ratings"
    )

    movie = db.relationship(
        "Movie",
        back_populates="ratings"
    )



class TopPick(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "movie_id"
        ),
        db.UniqueConstraint(
            "user_id",
            "rank"
        ),
    )
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey("movie.id"),
        nullable=False
    )

    rank = db.Column(
        db.Integer,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="top_picks"
    )

    movie = db.relationship(
        "Movie",
        back_populates="top_picks"
    )