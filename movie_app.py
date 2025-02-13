from termcolor import colored
from statistics import median
from matplotlib import cm
import content_validation
import random
import matplotlib.pyplot as plt
import numpy
import os
import sys
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')

class MovieApp:
    def __init__(self, storage):
        self._storage = storage


    def _list_movies(self):
        """
        Lists all movies from a list
        """
        movies = self._storage.list_movies()
        print(f"{len(movies)} movies in total")
        for movie in movies:
            title, year, rating, _, _, _ = movie.values()
            print(f"{colored(title, 'cyan')} ({year}), {rating}")
        print()


    def _add_movie(self):
        """
        Appends a list of dictionaries of movies with a passed movie
        """
        movies = self._storage.list_movies()
        title_to_search = input("Please enter a title: ")
        api_url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={title_to_search}'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                title_data_json = response.json()
            else:
                print(f"Error occurred: {response.status_code}")
                sys.exit()
        except requests.exceptions.ConnectionError:
            print(
                "We were not able to connect to www.omdbapi.com. "
                "Please check your Internet connection or try again later.")
            sys.exit()

        if title_data_json["Response"] == 'True' and title_data_json["Type"] != "series":
            title = title_data_json["Title"]
            year = title_data_json["Year"]
            rating = title_data_json["imdbRating"]
            poster_url = title_data_json["Poster"]
            imdb_id = title_data_json["imdbID"]
            if content_validation.validate_if_movie_exists(movies, title):
                print("The movie already exists.")
            else:
                try:
                    self._storage.add_movie(title, int(year), float(rating), poster_url, imdb_id)
                    print(colored(
                        "Your movie was successfully added!",
                        "green"), end="\n\n")
                except ValueError:
                    print("Year or rating is not numerical. Please try another movie.")
        else:
            print("Movie not found")


    def _delete_movie(self):
        """
        Deletes a movie from movies
        """
        movies = self._storage.list_movies()
        title = input("Enter a title you want to delete: ")

        if content_validation.validate_if_movie_exists(movies, title):
            self._storage.delete_movie(title)
            print(colored(
                "Your movie was successfully deleted!",
                "green"), end="\n\n")
        else:
            print(colored(
                "Sorry, this movie does not exist in the database.",
                "red"), end="\n\n")


    def _update_movie(self):
        """
        Updates movie by adding a note if movie in movies
        """
        movies = self._storage.list_movies()
        title = input("Enter a title to update: ")

        if content_validation.validate_if_movie_exists(movies, title):
            while True:
                note = input(f"Enter your note for '{colored(title, 'cyan')}' (max 100 chars): ")
                if 0 < len(note) <= 100:
                    self._storage.update_movie(title, note)
                    print(colored(
                        "The movie was successfully updated!",
                        "green"), end="\n\n")
                    break
                else:
                    print(colored(
                        "Check the length of your note. Has too be between 1 and 100 chars.",
                        "red"), end="\n\n")
        else:
            print(colored(
                "Sorry, this movie does not exist in the database and cannot be updated.",
                "red"), end="\n\n")


    def _stats(self):
        """
        Displays a series of statistics
        """
        movies = self._storage.list_movies()

        if movies:
            # Declare vars
            rates = []
            for movie in movies:
                rates.append(movie["rating"])

            sum_of_rates = sum(rates)
            highest_rate = max(rates)
            best_movies = []
            lowest_rate = min(rates)
            worst_movies = []

            # Calculates average rating of all movies in database
            average_rate = round(sum_of_rates / len(movies), 1)

            # Calculates median rating of all the movies in the database
            median_rate = round(median(rates), 1)

            # A list of movies with the highest_rating and the lowest_rating
            for movie in movies:
                title, year, rate, _, _, _ = movie.values()
                if rate == highest_rate:
                    best_movies.append([title, year, rate])
                elif rate == lowest_rate:
                    worst_movies.append([title, year, rate])

            print(f"""Average rating: {average_rate}
        Median rating: {median_rate}""")
            print("Best movie:",
                  '; '.join(
                      f"{colored(movie, 'cyan')} ({year}): {rate}" for movie, year, rate in best_movies))
            print("Worst movie:",
                  '; '.join(
                      f"{colored(movie, 'cyan')} ({year}): {rate}" for movie, year, rate in worst_movies),
                  end="\n\n")
        else:
            print("There are no movies in the database to fetch the ratings from.")


    def _random_movie(self):
        """
        Suggests a random movie to the user
        """
        movies = self._storage.list_movies()
        find_random_movie = random.choice(movies)
        title, year, rating, _, _, _ = find_random_movie.values()
        print(f"Your movie for today: {colored(title, 'cyan')} ({year}), {rating}", end="\n\n")


    def _search_movie(self):
        """
        Puts out a list of movies matching search criteria
        """
        movies = self._storage.list_movies()
        search_for = input("Enter part of a movie name: ")
        is_found = False

        for movie in movies:
            title, year, rating, _, _, _ = movie.values()
            if search_for.casefold() in title.casefold():
                print(f"{colored(title, 'cyan')} ({year}), {rating}")
                is_found = True

        if not is_found:
            decision = input("There is no such movie in the database. Would you like to add it? y/n: ")
            if decision in ["y", "Y"]:
                self._add_movie()
            else:
                print("You will now be redirected to main menu.", end="\n\n")
                self.run()
        print()


    def _movies_by_rating(self):
        """
        Displays a list of all movies sorted by rating
        """
        movies = self._storage.list_movies()
        sorted_movies = sorted(movies, key=lambda item: (-item["rating"], item["title"]))
        for movie in sorted_movies:
            title, year, rating, _, _, _ = movie.values()
            print(f"{colored(title, 'cyan')} ({year}): {rating}")
        print()


    def _rating_hist(self):
        """
        Creates a movie rating histogram
        """
        movies = self._storage.list_movies()
        rates = []
        for movie in movies:
            rates.append(movie["rating"])

        # Histogram's design
        plt.xlabel("rating")
        plt.ylabel("frequency")
        plt.title("rating histogram")
        n, bins, patches = plt.hist(rates, bins=20, edgecolor="black")
        colormap = cm.PuBuGn
        for patch, color in zip(patches, colormap(numpy.linspace(0, 1, len(patches)))):
            patch.set_facecolor(color)

        # Saving the histogram
        current_directory = os.getcwd()
        saved_path = os.path.join(current_directory, '_data', 'histogram.jpg')
        plt.savefig(saved_path)
        print(f"Your histogram was saved to: {saved_path}")
        plt.show()


    def _exit_program(self):
        """
        Closes the program
        """
        print("Goodbye!")
        sys.exit()


    def _generate_website(self):
        """
        The function loops through movies in DB, formats them and passes into an HTML template.
        """
        movies = self._storage.list_movies()
        movies_to_display = ""

        if len(movies) == 0:
            movies_to_display += f'<li>\n<div id="no-movies">There are no movies to display atm!</div>\n</li>'
        else:
            for movie in movies:
                title = movie["title"]
                year = movie["year"]
                poster_url = movie["poster_url"]
                imdb_id = movie["imdb_id"]
                rating = movie["rating"]
                note = movie["note"]
                movies_to_display += (f'\t<li>\n'
                                      f'\t<a href="https://www.imdb.com/title/{imdb_id}/" target="_blank" title="{note}">'
                                      f'\t<img class="movie-poster" src="{poster_url}"></a>\n'
                                      f'\t<div class="movie-title">{rating}/10 &#11088;</div>\n'
                                      f'\t<div class="movie-title">{title}</div>\n'
                                      f'\t<div class="movie-year">{year}</div>\n'
                                      f'\t</li>\n')

        with open("_static/index_template.html", "r") as file:
            html_content = file.read()

        html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movies_to_display)

        with open("_static/index.html", "w") as file:
            file.write(html_content)

        print("Website was generated successfully.")


    def run(self):
        """
        The function prints a menu, fetches user input and calls a relevant function based on it.
        """
        print(colored("""Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Create Rating Histogram
        10. Generate website
                """, "blue"))

        while True:
            try:
                choice = int(input("Enter choice (0-10): "))
                if choice < 0 or choice > 10:
                    print(colored(
                        "Please enter a number between 1 and 10 to proceed.",
                        "red"))
                else:
                    break
            except ValueError:
                print(colored(
                    "Please enter a number between 1 and 10 to proceed.",
                    "red"))

        commands = {0: self._exit_program,
                    1: self._list_movies,
                    2: self._add_movie,
                    3: self._delete_movie,
                    4: self._update_movie,
                    5: self._stats,
                    6: self._random_movie,
                    7: self._search_movie,
                    8: self._movies_by_rating,
                    9: self._rating_hist,
                    10: self._generate_website
                    }

        commands[choice]()
