from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Movie, Rating

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    users = User.query.all()
    return render_template(
        "select_user.html", users=users
    )

@app.route("/rate/<int:user_id>", methods=["GET", "POST"])
def rate_movie(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        movie_id = int(request.form["movie_id"])
        rating_value = int(request.form["rating"])

        if rating_value == -1:

            new_rating = Rating(
                user_id=user.id,
                movie_id=movie_id,
                rating=None,
                seen=False
            )

        else:

            new_rating = Rating(
                user_id=user.id,
                movie_id=movie_id,
                rating=rating_value,
                seen=True
            )

        db.session.add(new_rating)
        db.session.commit()

        return redirect(
            url_for(
                "rate_movie",
                user_id=user.id
            )
        )


    movie = (
        Movie.query
        .filter(
            ~Movie.id.in_(
                db.session.query(
                    Rating.movie_id
                ).filter_by(
                    user_id=user.id
                )
            )
        )
        .first()
    )


    if movie is None:
        return f"{user.name} has rated every movie!"


    total_movies = Movie.query.count()

    completed_movies = Rating.query.filter_by(
        user_id=user.id
    ).count()

    return render_template(
        "rate_movie.html",
        user=user,
        movie=movie,
        total_movies=total_movies,
        completed_movies=completed_movies
    )

if __name__ == "__main__":
    app.run(debug=True)