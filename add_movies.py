from app import app
from models import db, Movie
from tmdb import search_movies


# Stores movies that need manual selection later
ambiguous_movies = []


def save_movie(selected):

    existing = Movie.query.filter_by(
        tmdb_id=selected["tmdb_id"]
    ).first()


    if existing:
        print(
            f"Already exists: {selected['title']}"
        )
        return


    movie = Movie(
        title=selected["title"],
        year=selected["year"],
        tmdb_id=selected["tmdb_id"],
        poster_url=selected["poster_url"]
    )


    db.session.add(movie)

    print(
        f"Added: {movie.title}"
    )



def add_movie(title):

    title = title.strip()

    if not title:
        return


    print(f"\nSearching: {title}")


    results = search_movies(title)


    if not results:
        print(
            f"No results found for: {title}"
        )
        return


    # Automatically add if there is only one result
    if len(results) == 1:

        selected = results[0]

        print(
            f"Found: {selected['title']} ({selected['year']})"
        )

        save_movie(selected)


    else:

        print(
            f"Needs selection later: {title}"
        )

        ambiguous_movies.append({
            "input": title,
            "results": results
        })



def resolve_ambiguous_movies():

    if not ambiguous_movies:
        return


    print(
        "\n--- Resolving ambiguous movies ---"
    )


    for item in ambiguous_movies:

        print("\n")
        print(
            f"Choose match for: {item['input']}"
        )


        for i, movie in enumerate(item["results"]):

            print(
                f"{i+1}: {movie['title']} ({movie['year']})"
            )


        while True:

            choice = input(
                "Choose number (0 to skip): "
            )


            if choice.isdigit():

                choice = int(choice)

                if choice == 0:
                    print("Skipped")
                    break

                if 1 <= choice <= len(item["results"]):

                    selected = item["results"][choice - 1]

                    save_movie(selected)

                    break

            print("Invalid selection")



def add_movie_list():

    print(
        "Paste movie titles one per line."
    )
    print(
        "Press ENTER on an empty line when finished."
    )


    count = 0


    while True:

        title = input("> ")


        if title == "":
            break


        count += 1


        print(
            f"\nMovie {count}"
        )

        add_movie(title)


    print(
        f"\nProcessed {count} movies"
    )


    resolve_ambiguous_movies()

    db.session.commit()



if __name__ == "__main__":

    with app.app_context():

        add_movie_list()