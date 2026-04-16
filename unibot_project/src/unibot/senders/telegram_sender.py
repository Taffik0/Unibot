from unibot.senders.sender import Sender
from unibot.response.response_container import ResponseContainer
from unibot.response.response import Response, TextResponse, PictureResponse, PictureGroupResponse

from aiogram.types import BufferedInputFile, InputMediaPhoto

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
            if isinstance(resp, PictureResponse):
                await self._send_pictures([resp], chat_id)
            if isinstance(resp, PictureGroupResponse):
                await self._send_pictures(resp.pictures, chat_id)

        await self.bot.send_message(chat_id, text)

    async def _send_pictures(self, pictures: list[PictureResponse], chat_id: int):
        media: list[InputMediaPhoto] = []

        for i, pic in enumerate(pictures):
            media.append(
                InputMediaPhoto(
                    media=BufferedInputFile(pic.image_bytes, pic.file_name),
                    caption=(
                        pic.caption if pic.caption else None) if i == 0 else None
                )
            )
        if not media:
            return

        await self.bot.send_media_group(chat_id, media)
