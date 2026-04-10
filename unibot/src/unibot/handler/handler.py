from abc import ABC, abstractmethod

from unibot.message.message import Message
from unibot.response.response_container import ResponseContainer


class Handler(ABC):
    @abstractmethod
    async def handle(self, message: Message) -> ResponseContainer:
        pass
