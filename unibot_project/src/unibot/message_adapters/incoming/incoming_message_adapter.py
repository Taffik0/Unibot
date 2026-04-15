from abc import ABC, abstractmethod

from unibot.message.message import Message


class IncomingMessageAdapter(ABC):
    @abstractmethod
    def adapt_message(self, raw_message) -> Message | None:
        pass
