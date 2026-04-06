from abc import ABC, abstractmethod

from src.message.message import Message


class IncomingMessageAdapter(ABC):
    @abstractmethod
    def adapt_message(self, raw_message) -> Message:
        pass
