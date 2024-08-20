from bs4 import BeautifulSoup

from models.movie import Movie
from .base_scraper import BaseScraper


class BenderyScraper(BaseScraper):
    """
    Scraper for https://kino-bendery.info
    """
    
    def parse_page(self, page: str | bytes) -> list[Movie]:
        soup = BeautifulSoup(page, features = 'lxml')
        movies_info = soup.find_all('div', class_ = 'basetext')
        
        movies = []
        for info in movies_info:
            title = info.find('a').text
            preview_url = info.find('div', class_ = 'maincont').find('img').get('src')

            fonts = info.find_all('font')
            
            duration = fonts[0].text.strip()
            format = fonts[1].text.strip()
            sessions = self.__split_sessions_string(fonts[2].text)

            description = info.find('ul', class_ = 'about_film').find('div').text
            
            movies.append(
                Movie(
                    title = title,
                    preview_url = preview_url,
                    duration = duration,
                    format = format,
                    sessions = sessions,
                    description = description,
                )
            )

        return movies
    

    @property
    def site_url(self) -> str:
        return 'https://kino-bendery.info'
    

    def __split_sessions_string(self, sessions: str) -> str:
        """Convert strings like 'Сеансы: 14.30, 16.30' into '14.30, 16.30'"""
        return sessions.split(' ', maxsplit = 1)[1]