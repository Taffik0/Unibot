from unibot.commands.command import Command
from unibot.message.message import Message


class ResponseMessage:
    def __init__(self, message_id: str, chat_id: str, user_id: str):
        self.message_id: str = message_id
        self.chat_id = chat_id
        self.user_id = user_id

    @classmethod
    def from_message(cls, message: Message) -> "ResponseMessage":
        return ResponseMessage(message_id=message.id, chat_id=message.chat_id, user_id=message.user_id)

    @classmethod
    def from_command(cls, command: Command) -> "ResponseMessage":
        return ResponseMessage(message_id=command.message_id, chat_id=command.chat_id, user_id=command.user_id)
