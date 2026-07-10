from app import app
from models import db, User, Movie

with app.app_context():
    users = ["Peter", "Mom", "Dad", "Maddie"]

    for name in users:
        if not User.query.filter_by(name=name).first():
            db.session.add(User(name=name))

    movies = [
        ("The Dark Knight", 2008),
        ("Interstellar", 2014),
        ("The Shawshank Redemption", 1994),
        ("The Lord of the Rings: The Return of the King", 2003),
        ("Jaws", 1975)
    ]

    for title, year in movies:
        if not Movie.query.filter_by(
            title=title,
            year=year
        ).first():
            db.session.add(
                Movie(
                    title=title,
                    year=year
                )
            )

    db.session.commit()

print("Database seeded!")