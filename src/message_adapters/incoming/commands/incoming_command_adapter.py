from abc import ABC, abstractmethod

from src.commands.commands import Commands
from src.commands.command import Command


class IncomingCommandAdapter(ABC):
    @abstractmethod
    def adapt_command(self, raw_command) -> Command:
        pass
