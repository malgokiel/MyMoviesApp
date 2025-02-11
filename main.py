from movie_app import MovieApp
from _storage.storage_json import StorageJson
from termcolor import colored
from getkey import getkey, keys
import sys
import argparse

def get_file_name():
    """
    This function takes a CL argument, parses and validates it and returns a desired file name and its extension
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name of the file with 'your_name.csv' or 'your_name.json' extension")
    args = parser.parse_args()
    name, extension = args.filename.split(".")
    if extension not in ["csv", "json"]:
        print(f"File extension {extension} is currently not supported. Use '.csv' or '.json'.")
        sys.exit()
    else:
        return name, extension


def main():
    """
    Initializes storage and then a movie app and controls it.
    Runs the app in a loop until user terminates the program.
    """
    name, extension = get_file_name()
    if extension == "csv":
        storage = StorageJson(f'_data/{name}.csv')
    elif extension == "json":
        storage = StorageJson(f'_data/{name}.json')

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
