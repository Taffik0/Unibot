from datetime import datetime

from unibot.message_adapters.incoming.incoming_message_adapter import IncomingMessageAdapter

from aiogram.types import Message as TgMessage
from aiogram import Bot
from unibot.message.message import Message
from unibot.message.specific_data import FullNameSD, Picture, PictureSD, DocumentSD


class TelegramIncomingMessageAdapter(IncomingMessageAdapter):
    def adapt_message(self, raw_message: TgMessage) -> Message | None:
        timestamp = raw_message.date          # timestamp в UTC
        dt = raw_message.date
        if raw_message.from_user is None:
            raise
        user_id = str(raw_message.from_user.id)
        text = raw_message.text if raw_message.text is not None else ""
        text += raw_message.caption if raw_message.caption is not None else ""
        clean_message = Message(str(raw_message.message_id), user_id, str(
            raw_message.chat.id), text, dt)

        self.add_full_name(clean_message, raw_message)
        return clean_message

    def add_full_name(self, message: Message, raw_message: TgMessage):
        if raw_message.from_user is None:
            return
        first_name = raw_message.from_user.first_name
        surname = raw_message.from_user.last_name if raw_message.from_user.last_name else ""
        sd = FullNameSD(first_name, surname, "")
        message.add_sd(sd)

    async def add_picture(self, message: Message, raw_message: TgMessage, bot: Bot):
        pictures: list[Picture] = []
        photos = raw_message.photo
        if not photos:
            return
        for photo in photos:
            file = await bot.get_file(photo.file_id)
            file_path = file.file_path
            if file_path is not None:
                pictures.append(Picture(photo.width, photo.height,
                                self._gen_download_file(file_path, bot)))
        message.add_sd(PictureSD(pictures))

    async def add_document(self, message: Message, raw_message: TgMessage, bot: Bot):
        document = raw_message.document
        if document is None:
            return
        file = await bot.get_file(document.file_id)
        if file.file_path is None:
            return
        file_name = document.file_name if document.file_name else ""
        file_size = file.file_size if file.file_size else -1
        file_type = document.mime_type if document.mime_type else ""
        doc_sd = DocumentSD(file_name, file_size, file_type,
                            self._gen_download_file(file.file_path, bot))
        message.add_sd(doc_sd)

    @staticmethod
    def _gen_download_file(file_path: str, bot: Bot):
        async def download_file() -> bytes | None:
            stream = await bot.download_file(file_path)
            if stream is None:
                return None
            return stream.read()
        return download_file
