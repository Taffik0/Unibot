from ...settings.tg_settings import TOKEN

from unibot.listeners.telegram_message_listener import TelegramMessageListener
from unibot.senders.telegram_sender import TelegramSender
from unibot.message_adapters.incoming.telegram_incoming_message_adapter import TelegramIncomingMessageAdapter
from unibot.message_adapters.incoming.commands.telegram_incoming_command_adapter import TelegramIncomingCommandAdapter

from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter

from unibot.commands.commands import Commands


bot = None


def get_bot():
    try:
        from aiogram import Bot
    except ImportError:
        raise ImportError(
            "Install telegram support: pip install unibot[telegram]"
        )
    global bot
    if bot is not None:
        return bot
    bot = Bot(token=str(TOKEN.value()))
    return bot


async def sender_orchestration() -> TelegramSender:
    return TelegramSender(get_bot())


async def listener_orchestration(
        command_enums: list[Commands],
        message_router: MessageRouter,
        command_router: CommandRouter) -> TelegramMessageListener:

    incoming_message_adapter = await incoming_message_adapter_orchestration()
    incoming_command_adapter = await incoming_command_adapter_orchestration(command_enums)
    return TelegramMessageListener(get_bot(), incoming_message_adapter, message_router, incoming_command_adapter, command_router)


async def incoming_message_adapter_orchestration() -> TelegramIncomingMessageAdapter:
    return TelegramIncomingMessageAdapter()


async def incoming_command_adapter_orchestration(command_enums: list[Commands]) -> TelegramIncomingCommandAdapter:
    return TelegramIncomingCommandAdapter(command_enums)
