from unibot.response.response_container import ResponseContainer

from abc import ABC, abstractmethod


class Sender(ABC):
    @abstractmethod
    async def send(self, response_container: ResponseContainer):
        pass
