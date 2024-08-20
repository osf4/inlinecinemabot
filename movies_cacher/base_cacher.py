from abc import ABC, abstractmethod
from datetime import timedelta
from models.movie import Movie


class BaseMoviesCacher(ABC):
    """
    Movies cacher fetches the movies from the site and updates them once in a given period.

    If the cache is expired, it would be updated after the next call of get_movies of get_movie_by_index
    """
    
    @abstractmethod
    async def get_movies(self) -> list[Movie]:
        pass


    @abstractmethod
    async def get_movie_by_index(self, index: int) -> Movie:
        pass

    
    @property
    @abstractmethod
    def period(self) -> timedelta:
        """
        Expiration time of the cache
        """

        pass