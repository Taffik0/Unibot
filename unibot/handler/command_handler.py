from abc import ABC, abstractmethod

from src.commands.command import Command
from src.response.response_container import ResponseContainer


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> ResponseContainer:
        pass
