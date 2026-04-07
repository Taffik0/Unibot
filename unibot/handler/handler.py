from abc import ABC, abstractmethod

from src.message.message import Message
from src.response.response_container import ResponseContainer


class Handler(ABC):
    @abstractmethod
    async def handle(self, message: Message) -> ResponseContainer:
        pass
