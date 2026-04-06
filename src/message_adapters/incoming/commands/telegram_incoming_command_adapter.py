from aiogram.filters import CommandObject
from aiogram.types import Message as TgMessage

from src.message_adapters.incoming.commands.incoming_command_adapter import IncomingCommandAdapter

from src.commands.command import Command
from src.commands.commands import Commands


class TelegramIncomingCommandAdapter(IncomingCommandAdapter):
    def __init__(self, commands_enums: Commands) -> None:
        self.commands_enums = commands_enums

    def _validate_command_type(self, command: str) -> Commands:
        for ce in self.commands_enums:
            try:
                return ce(command)
            except:
                pass
        raise

    def adapt_command(self, raw_command: tuple[CommandObject, TgMessage]) -> Command:
        command_data, message_data = raw_command
        message_id = str(message_data.message_id)
        if message_data.from_user is None:
            raise
        user_id = str(message_data.from_user.id)
        chat_id = str(message_data.chat.id)
        command_type = self._validate_command_type(command_data.command)
        # Доделать
        pass
        return Command(message_id=message_id,
                       chat_id=chat_id,
                       user_id=user_id,
                       command=command_type,
                       args={})
