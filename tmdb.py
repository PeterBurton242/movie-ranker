import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def get_movie_poster(title, year=None):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": title
    }

    if year:
        params["year"] = year

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    if data["results"]:

        movie = data["results"][0]

        poster_path = movie["poster_path"]

        if poster_path:
            return (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

    return None