from src.commands.commands import Commands
from src.handler.command_handler_builder import CommandHandler
from src.types.command_handler_factory import CommandHandlerFactory


class HandlerCommandRegister:
    def __init__(self) -> None:
        self.storage: dict[Commands, CommandHandlerFactory] = {}

    async def register(self, command: Commands, command_handler_factory: CommandHandlerFactory):
        if self.storage.get(command) is not None:
            return
        self.storage[command] = command_handler_factory

    async def get(self, command: Commands) -> CommandHandlerFactory | None:
        return self.storage.get(command)
