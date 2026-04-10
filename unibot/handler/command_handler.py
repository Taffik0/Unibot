from abc import ABC, abstractmethod

from unibot.commands.command import Command
from unibot.response.response_container import ResponseContainer


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> ResponseContainer:
        pass
