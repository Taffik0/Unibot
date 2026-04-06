import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import BaseFilter, Command as TgCommand, CommandObject
from aiogram.types import Message as TgMessage

from src.listeners.message_listener import MessageListener

from src.message_adapters.incoming.telegram_incoming_message_adapter import TelegramIncomingMessageAdapter
from src.message_adapters.incoming.commands.telegram_incoming_command_adapter import TelegramIncomingCommandAdapter

from src.rout.message_router import MessageRouter
from src.rout.commands.command_router import CommandRouter


class AnyCommand(BaseFilter):
    async def __call__(self, message: TgMessage) -> bool:
        return message.text and message.text.startswith("/")


class TelegramMessageListener(MessageListener):
    def __init__(self, bot: Bot, incoming_message_adapter: TelegramIncomingMessageAdapter, message_router: MessageRouter, incoming_command_adapter: TelegramIncomingCommandAdapter, command_router: CommandRouter):
        self.bot = bot
        self.dp = Dispatcher()

        self.incoming_message_adapter = incoming_message_adapter
        self.incoming_command_adapter = incoming_command_adapter
        self.message_router = message_router
        self.command_router = command_router

        self.listening_message = self.dp.message(
            ~AnyCommand())(self._listening_message)
        self.listening_command = self.dp.message(
            AnyCommand())(self._listening_commands)

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

    async def _listening_message(self, message: TgMessage):
        clear_message = self.incoming_message_adapter.adapt_message(message)
        print(clear_message)
        await self.message_router.rout(clear_message)

    async def _listening_commands(self, message: TgMessage):
        text = message.text or ""
        if not text.startswith("/"):
            return  # Это не команда

        # Разбираем команду вручную
        parts = text.split(maxsplit=1)
        command_name = parts[0][1:].split("@")[0]  # убираем '/'
        mention = parts[0][1:].split("@")[1] if "@" in parts[0] else None
        args = parts[1] if len(parts) > 1 else ""

        command = CommandObject(command=command_name,
                                args=args, mention=mention)

        clear_command = self.incoming_command_adapter.adapt_command(
            (command, message))
        print(clear_command)
        await self.command_router.rout(clear_command)
