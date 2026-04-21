from aiogram.filters import CommandObject
from aiogram.types import Message as TgMessage

from unibot.message_adapters.incoming.commands.incoming_command_adapter import IncomingCommandAdapter

from unibot.commands.command import Command
from unibot.commands.commands import Commands


class TelegramIncomingCommandAdapter(IncomingCommandAdapter):
    def __init__(self, commands_enums: list[Commands] | None = None) -> None:
        self.commands_enums: list[Commands] = []
        if commands_enums is not None:
            self.commands_enums = commands_enums

    def register_commands_enum(self, commands_enum: Commands):
        self.commands_enums.append(commands_enum)

    def _validate_command_type(self, command: str) -> Commands | None:
        for ce in self.commands_enums:
            try:
                return ce(command)
            except Exception as e:
                pass
        return None

    def adapt_command(self, raw_command: tuple[CommandObject, TgMessage]) -> Command | None:
        command_data, message_data = raw_command
        message_id = str(message_data.message_id)
        if message_data.from_user is None:
            raise
        user_id = str(message_data.from_user.id)
        chat_id = str(message_data.chat.id)
        command_type = self._validate_command_type(command_data.command)
        if command_type is None:
            return None
        return Command(message_id=message_id,
                       chat_id=chat_id,
                       user_id=user_id,
                       command=command_type,
                       args={})
