from abc import ABC, abstractmethod
from models.movie import Movie


class BaseScraper(ABC):
    """
    Base scraper of sites of the cinemas
    """
    
    @abstractmethod
    def parse_page(self, page: str | bytes) -> list[Movie]:
        pass


    @property
    @abstractmethod
    def site_url(self) -> str:
        pass