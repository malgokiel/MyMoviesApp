from movie_app import MovieApp
from _storage.storage_json import StorageJson
from termcolor import colored
from getkey import getkey, keys

def main():
    """
    Initializes storage and then a movie app and controls it.
    Runs the app in a loop until user terminates the program.
    """
    storage = StorageJson('_data/movies.json')
    movie_app = MovieApp(storage)

    print(colored("****** My Movies Database ******", "green", attrs=["bold"]), end="\n\n")

    first_use = True

    # Allows the program to run continuously
    try:
        while True:
            if first_use:
                movie_app.run()
                first_use = False
            else:
                print(colored("Press enter to continue", attrs=["underline"]))
                user_key = getkey()
                print()
                # second option added to accommodate codio
                if user_key in (keys.ENTER, "\r"):
                    movie_app.run()
    except KeyboardInterrupt:
        print(colored("\nYou manually ended the program. See u next time!", attrs=["bold"]))


if __name__ == "__main__":
    main()
