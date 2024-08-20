from aiohttp import ClientSession, TCPConnector, StreamReader
from urllib.parse import urlparse

from .base_page_requester import BasePageRequester
from .exceptions import HttpUnknownSchemeError


def _create_client_session(verify_ssl: bool) -> ClientSession:
    return ClientSession(
        connector = TCPConnector(verify_ssl = verify_ssl),
    )


class DefaultPageRequester(BasePageRequester):
    """
    Page requester that is used by default.

    Page requester allows to get the URL without creating new ClientSessions for each request
    """
    
    def __init__(self):
        self.__http_session = _create_client_session(verify_ssl = False)
        self.__https_session = _create_client_session(verify_ssl = True)


    async def get(self, url: str) -> bytes:
        """
        Return the content of the page

        Raise HttpUnknownSchemeError, if the scheme is not 'http' or 'https'
        """
        
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ['http', 'https']:
            raise HttpUnknownSchemeError(f'Unknown scheme: {parsed_url.scheme}')

        session = self.__get_session_by_scheme(parsed_url.scheme)        
        async with session.get(url) as response:
            return await response.read()


    async def close(self):
        """
        Close the sessions
        """
        
        await self.__http_session.close()
        await self.__https_session.close()


    def __get_session_by_scheme(self, scheme: str) -> ClientSession:
        """
        Return the session by scheme:
        __http_session for 'http',
        __https_session for 'https'
        """
        
        match scheme:
            case 'http':
                return self.__http_session
            
            case 'https':
                return self.__https_session
