from abc import ABC, abstractmethod
from typing import Any

from unibot.message.message import Message


class OutgoingMessageAdapter(ABC):
    @abstractmethod
    def adapt_message(self, message: Message) -> Any:
        pass
