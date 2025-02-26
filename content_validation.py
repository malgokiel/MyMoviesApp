def validate_if_movie_exists(movies, title):
    """
    The function searches the database of movies for title.
    The function returns True, if the title already exists in the DB,
    and False if it does not.
    """
    movie_exists = False
    for movie in movies:
        if movie["title"].casefold() == title:
            movie_exists = True
            break
    return movie_exists
