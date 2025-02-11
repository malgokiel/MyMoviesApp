from _storage.istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path


    def list_movies(self):
        """
        Returns a list of dictionaries that
        contains the movies information in the database.
        The function loads the information from the JSON
        file and returns the data.
        If the file does not exist, creates a new one.
        """
        while True:
            try:
                with open(self.file_path, "r") as fileobject:
                    return json.load(fileobject)
            except FileNotFoundError:
                with open("_data/movies.json", 'w') as fileobject:
                    fileobject.write("[]")


    def add_movie(self, title, year, rating, poster_url):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it.
        """
        movies = self.list_movies()
        movies.append({"title": title, "year": year, "rating": rating, "poster_url": poster_url})

        with open(self.file_path, "w") as fileobject:
            json.dump(movies, fileobject)


    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it.
        """
        movies = self.list_movies()
        updated_movies = []
        for movie in movies:
            if movie["title"] != title:
                updated_movies.append(movie)

        with open(self.file_path, "w") as fileobject:
            json.dump(updated_movies, fileobject)


    def update_movie(self, title, rating):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it.
        """
        movies = self.list_movies()

        for movie in movies:
            if movie["title"] == title:
                movie["rating"] = rating
                break

        with open(self.file_path, "w") as fileobject:
            json.dump(movies, fileobject)