from dataclasses import dataclass

from unibot.commands.commands import Commands


@dataclass
class Command:
    message_id: str
    chat_id: str
    user_id: str
    command: Commands
    args: dict
