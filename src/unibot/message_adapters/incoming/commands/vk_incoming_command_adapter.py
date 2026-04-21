from unibot.message_adapters.incoming.commands.incoming_command_adapter import IncomingCommandAdapter
from unibot.commands import Commands, Command


class VKIncomingCommandAdapter(IncomingCommandAdapter):
    def __init__(self, commands_enums: list[Commands] | None = None):
        self.commands_enums: list[Commands] = []
        if commands_enums:
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

    def adapt_command(self, raw_command: dict) -> Command | None:
        id = str(raw_command["id"])
        user_id = str(abs(raw_command["from_id"]))
        chat_id = str(raw_command["peer_id"])
        text: str = raw_command["text"]
        if not text:
            return None
        name = text.split()[0]
        command_type = self._validate_command_type(name)
        if command_type is None:
            return None
        return Command(message_id=id, chat_id=chat_id, user_id=user_id, command=command_type, args={})
