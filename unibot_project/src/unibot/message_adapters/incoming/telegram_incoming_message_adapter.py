from datetime import datetime

from unibot.message_adapters.incoming.incoming_message_adapter import IncomingMessageAdapter

from aiogram.types import Message as TgMessage
from unibot.message.message import Message
from unibot.message.specific_data import FullNameSD


class TelegramIncomingMessageAdapter(IncomingMessageAdapter):
    def adapt_message(self, raw_message: TgMessage) -> Message:
        timestamp = raw_message.date          # timestamp в UTC
        dt = datetime.fromtimestamp(timestamp.timestamp())
        if raw_message.from_user is None:
            raise
        user_id = str(raw_message.from_user.id)
        text = raw_message.text if raw_message.text is not None else ""
        clean_message = Message(str(raw_message.message_id), user_id, str(
            raw_message.chat.id), text, dt)

        self.add_full_name(clean_message, raw_message)
        return clean_message

    def add_full_name(self, message: Message, raw_message: TgMessage):
        if raw_message.from_user is None:
            return
        first_name = raw_message.from_user.first_name
        surname = raw_message.from_user.last_name
        sd = FullNameSD(first_name, surname, "")
        message.specific_data.append(sd)
