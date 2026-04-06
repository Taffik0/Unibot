import asyncio

from aiogram import Bot, Dispatcher, types

from src.listeners.message_listener import MessageListener

from src.message_adapters.incoming.incoming_message_adapter import IncomingMessageAdapter

from src.rout.message_router import MessageRouter


class TelegramMessageListener(MessageListener):
    def __init__(self, bot: Bot, incoming_message_adapter: IncomingMessageAdapter, message_router: MessageRouter):
        self.bot = bot
        self.dp = Dispatcher()

        self.incoming_message_adapter = incoming_message_adapter
        self.message_router = message_router

        self.listening_message = self.dp.message(
            lambda m: True)(self._listening_message)

        self.listening_task = None

    async def start(self):
        self.is_working = True
        task = asyncio.create_task(self._listening())
        self.listening_task = task

    async def stop(self):
        await self.dp.stop_polling()
        self.listening_task.cancel()

    async def _listening(self):
        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()

    async def _listening_message(self, message: types.Message):
        clear_message = self.incoming_message_adapter.adapt_message(message)
        print(clear_message)
        await self.message_router.rout(clear_message)
