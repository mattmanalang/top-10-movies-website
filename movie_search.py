import requests
import os


class MovieFinder:
    _API_KEY = os.getenv("TMDB_API")
    TMDB_poster_url = "https://image.tmdb.org/t/p/original"

    @staticmethod
    def fetch_movie_list(movie_title):
        """Fetch movies from the TMDB API that matches the title"""
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {"query": movie_title, "language": "en-US"}
        headers = {
            "accept": "application/json",
            "Authorization": MovieFinder._API_KEY
        }
        response = requests.get(search_url, params=params, headers=headers).json()["results"]
        return response

    @staticmethod
    def fetch_movie_details(movie_id):
        """Fetch and return a particular movie's details from the TMDB API."""
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {"language": "en-US"}
        headers = {
            "accept": "application/json",
            "Authorization": MovieFinder._API_KEY
        }
        response = requests.get(movie_details_url, params=params, headers=headers).json()
        return response

