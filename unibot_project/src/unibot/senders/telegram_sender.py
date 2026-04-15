from unibot.senders.sender import Sender
from unibot.response.response_container import ResponseContainer
from unibot.response.response import Response, TextResponse

from aiogram import Bot, Dispatcher, types


class TelegramSender(Sender):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send(self, response_container: ResponseContainer):
        text = ""
        chat_id = int(response_container.message.chat_id)
        if response_container.responses is None:
            return
        for resp in response_container.responses:
            if isinstance(resp, TextResponse):
                text += resp.text

        await self.bot.send_message(chat_id, text)
