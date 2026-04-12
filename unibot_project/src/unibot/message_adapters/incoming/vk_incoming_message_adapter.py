from datetime import datetime

from unibot.message_adapters.incoming.incoming_message_adapter import IncomingMessageAdapter
from unibot.message.message import Message
from unibot.message.specific_data import VKSD


class VKIncomingMessageAdapter(IncomingMessageAdapter):
    def adapt_message(self, raw_message) -> Message:
        dt = datetime.fromtimestamp(raw_message["date"])
        id = raw_message["id"]
        user_id = abs(raw_message["from_id"])
        chat_id = raw_message["peer_id"]
        text = raw_message["text"]
        random_id = raw_message["random_id"]
        vksd = VKSD(random_id=random_id,
                    is_community=raw_message["from_id"] < 0)
        return Message(id, user_id, chat_id, text, dt, [vksd])
