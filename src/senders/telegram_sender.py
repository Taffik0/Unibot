from src.senders.sender import Sender
from src.response.response_container import ResponseContainer
from src.response.response import Response, TextResponse

from aiogram import Bot, Dispatcher, types


class TelegramSender(Sender):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send(self, response_container: ResponseContainer):
        text = ""
        chat_id = int(response_container.message.chat_id)
        for resp in response_container.responses:
            if isinstance(resp, TextResponse):
                text += resp.text

        await self.bot.send_message(chat_id, text)
