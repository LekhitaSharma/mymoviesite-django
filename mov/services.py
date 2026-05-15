import requests

def fetch_movie_data(query):
    url = f"http://www.omdbapi.com/?t={query}&apikey=88679313"
    response = requests.get(url)
    return response.json()

def get_wikipedia_link(name):
    return f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"