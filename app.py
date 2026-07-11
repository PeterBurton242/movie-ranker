from flask import Flask, render_template, request, redirect, url_for
from models import (
    db,
    User,
    Movie,
    Rating,
    TopPick
)
from tmdb import search_movies

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


    rated_movie_ids = {
        rating.movie_id
        for rating in user.ratings
    }


    movie = (
        Movie.query
        .filter(
            ~Movie.id.in_(rated_movie_ids)
        )
        .first()
    )


    if movie is None:
        return f"{user.name} has rated every movie!"


    total_movies = Movie.query.count()

    completed_movies = len(user.ratings)

    if movie.poster_url:

        poster_url = movie.poster_url

    else:

        results = search_movies(
            movie.title,
            movie.year
        )

        if results:

            tmdb_data = results[0]

            movie.tmdb_id = tmdb_data["tmdb_id"]
            movie.poster_url = tmdb_data["poster_url"]

            db.session.commit()

            poster_url = movie.poster_url

        else:

            poster_url = None

    return render_template(
        "rate_movie.html",
        user=user,
        movie=movie,
        total_movies=total_movies,
        completed_movies=completed_movies,
        poster_url=poster_url
    )


@app.route("/ratings")
def view_ratings():

    users = User.query.all()
    movies = Movie.query.all()

    ratings = {}
    movie_stats = {}

    for movie in movies:

        ratings[movie.id] = {
            rating.user_id: rating
            for rating in movie.ratings
        }


        seen_ratings = [
            rating.rating
            for rating in movie.ratings
            if rating.seen
        ]


        if seen_ratings:

            movie_stats[movie.id] = {
                "count": len(seen_ratings),
                "average": round(
                    sum(seen_ratings) / len(seen_ratings),
                    2
                )
            }

        else:

            movie_stats[movie.id] = {
                "count": 0,
                "average": None
            }


    return render_template(
        "ratings.html",
        users=users,
        movies=movies,
        ratings=ratings,
        movie_stats=movie_stats
    )

@app.route(
    "/edit_rating/<int:user_id>/<int:movie_id>",
    methods=["GET", "POST"]
)
def edit_rating(user_id, movie_id):

    user = User.query.get_or_404(user_id)
    movie = Movie.query.get_or_404(movie_id)

    rating = Rating.query.filter_by(
        user_id=user_id,
        movie_id=movie_id
    ).first_or_404()

    if request.method == "POST":

        rating_value = int(
            request.form["rating"]
        )

        if rating_value == -1:
            rating.rating = None
            rating.seen = False
        else:
            rating.rating = rating_value
            rating.seen = True

        db.session.commit()

        return redirect(
            url_for("view_ratings")
        )

    return render_template(
        "edit_rating.html",
        user=user,
        movie=movie,
        rating=rating
    )


@app.route(
    "/delete_movie/<int:movie_id>",
    methods=["POST"]
)
def delete_movie(movie_id):

    movie = Movie.query.get_or_404(
        movie_id
    )

    db.session.delete(movie)
    db.session.commit()

    return redirect(
        url_for("view_ratings")
    )


@app.route(
    "/top10/<int:user_id>",
    methods=["GET", "POST"]
)
def top10(user_id):

    user = User.query.get_or_404(
        user_id
    )

    movies = (
        Movie.query
        .join(Rating)
        .filter(
            Rating.user_id == user.id,
            Rating.seen == True
        )
        .order_by(Movie.title)
        .all()
    )

    if request.method == "POST":

        TopPick.query.filter_by(
            user_id=user.id
        ).delete()

        chosen_movies = set()

        for rank in range(1, 11):

            movie_id = request.form.get(
                f"rank_{rank}"
            )

            if movie_id:

                movie_id = int(movie_id)

                if movie_id in chosen_movies:
                    continue

                chosen_movies.add(movie_id)

                pick = TopPick(
                    user_id=user.id,
                    movie_id=movie_id,
                    rank=rank
                )

                db.session.add(pick)

        db.session.commit()

        return redirect(
            url_for("view_ratings")
        )

    existing = {
        pick.rank: pick.movie_id
        for pick in user.top_picks
    }

    return render_template(
        "top10.html",
        user=user,
        movies=movies,
        existing=existing
    )


@app.route("/top10s")
def view_top10s():

    users = User.query.all()

    return render_template(
        "top10s.html",
        users=users
    )

if __name__ == "__main__":
    app.run(debug=True)