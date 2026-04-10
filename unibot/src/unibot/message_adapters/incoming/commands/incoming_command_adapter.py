from abc import ABC, abstractmethod

from unibot.commands.commands import Commands
from unibot.commands.command import Command


class IncomingCommandAdapter(ABC):
    @abstractmethod
    def adapt_command(self, raw_command) -> Command | None:
        pass

    @abstractmethod
    def register_commands_enum(self, commands_enum: Commands):
        pass
