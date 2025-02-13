from _storage.istorage import IStorage
import csv


class StorageCsv(IStorage):
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
                with open(self.file_path, "r") as fileobj:
                    reader = csv.DictReader(fileobj)
                    movies = [row for row in reader]
                return movies
            except FileNotFoundError:
                with open("movies.csv", 'w') as fileobject:
                    fileobject.write("title,year,rating,poster_url")


    def add_movie(self, title, year, rating, poster_url, imdb_id, note=""):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it.
        """
        movies = self.list_movies()
        movies.append({
            "title": title,
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "imdb_id": imdb_id,
            "note": note})
        with open(self.file_path, "w", newline="") as fileobject:
            writer = csv.DictWriter(fileobject,
                                    fieldnames=["title", "year", "rating", "poster_url", "imdb_id", "note"])
            writer.writeheader()
            for movie in movies:
                writer.writerow(movie)


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

        with open(self.file_path, "w", newline="") as fileobject:
            writer = csv.DictWriter(fileobject,
                                    fieldnames=["title", "year", "rating", "poster_url", "imdb_id", "note"])
            writer.writeheader()
            for updated_movie in updated_movies:
                writer.writerow(updated_movie)


    def update_movie(self, title, note):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it.
        """
        movies = self.list_movies()

        for movie in movies:
            if movie["title"] == title:
                movie["note"] = note
                break

        with open(self.file_path, "w", newline="") as fileobject:
            writer = csv.DictWriter(fileobject,
                                    fieldnames=["title", "year", "rating", "poster_url", "imdb_id", "note"])
            writer.writeheader()
            for movie in movies:
                writer.writerow(movie)
