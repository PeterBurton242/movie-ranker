import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def search_movies(title, year=None):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": title,
        "include_adult": False
    }

    if year:
        params["year"] = year


    response = requests.get(
        url,
        params=params,
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    results = []


    for movie in data.get("results", [])[:5]:

        results.append({
            "tmdb_id": movie["id"],
            "title": movie["title"],
            "original_title": movie.get("original_title"),
            "year": (
                movie.get("release_date", "")[:4]
            ),
            "poster_url": (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
                if movie["poster_path"]
                else None
            )
        })


    return results