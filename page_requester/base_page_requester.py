from abc import ABC, abstractmethod


class BasePageRequester(ABC):
    """
    Base class for page requesters.

    Page requester allows to get the URL without creating new ClientSessions for each request
    """
    
    @abstractmethod
    async def get(self, url: str) -> bytes:
        pass



    @abstractmethod
    async def close(self):
        pass