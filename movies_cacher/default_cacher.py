from datetime import datetime, timedelta

from models.movie import Movie
from page_requester.base_page_requester import BasePageRequester
from scraper.base_scraper import BaseScraper

from .base_cacher import BaseMoviesCacher


class DefaultMoviesCacher(BaseMoviesCacher):
    """
    Default movies cacher.

    Movies cacher fetches the movies from the site and updates them once in a given period.

    If the cache is expired, it would be updated after the next call of get_movies of get_movie_by_index
    """
    
    def __init__(self, 
                 period: timedelta, 
                 scraper: BaseScraper,
                 page_requester: BasePageRequester):
        
        self._period = period
        self.scraper = scraper
        self.page_requester = page_requester

        self.__cached_movies = None
        self.__last_update = datetime.now()

    
    async def get_movies(self) -> list[Movie]:
        return await self.__update_movies_if_expired_or_empty()
    

    async def get_movie_by_index(self, index: int) -> Movie:
        movies = await self.__update_movies_if_expired_or_empty()
        return movies[index]
    

    async def __update_movies(self) -> list[Movie]:
        movies_page = await self.page_requester.get(self.scraper.site_url)

        self.__last_update = datetime.now()

        self.__cached_movies = self.scraper.parse_page(movies_page)
        return self.__cached_movies
    

    async def __update_movies_if_expired_or_empty(self) -> list[Movie]:
        if not self.__cached_movies or self.__cache_expired:
            return await self.__update_movies()
        
        return self.__cached_movies
    

    @property
    def period(self) -> timedelta:
        return self._period
    

    @property
    def __cache_expired(self) -> bool:
        return datetime.now() - self.__last_update >= self.period