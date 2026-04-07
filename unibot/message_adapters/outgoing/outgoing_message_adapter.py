from abc import ABC, abstractmethod
from typing import Any

from src.message.message import Message


class OutgoingMessageAdapter(ABC):
    @abstractmethod
    def adapt_message(self, message: Message) -> Any:
        pass
