from aiogram import Bot

from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter

# settings
from ..settings.main import COMMANDS

from unibot.listeners.message_listener import MessageListener
from unibot.listeners.telegram_message_listener import TelegramMessageListener
from unibot.senders.sender import Sender
from unibot.senders.telegram_sender import TelegramSender
from unibot.message_adapters.incoming.incoming_message_adapter import IncomingMessageAdapter
from unibot.message_adapters.incoming.telegram_incoming_message_adapter import TelegramIncomingMessageAdapter
from unibot.message_adapters.incoming.commands.incoming_command_adapter import IncomingCommandAdapter
from unibot.message_adapters.incoming.commands.telegram_incoming_command_adapter import TelegramIncomingCommandAdapter

from .infrastructure.telegram import sender_orchestration as tg_sender_orchestration, listener_orchestration as tg_listener_orchestration
from .infrastructure.vk import sender_orchestration as vk_sender_orchestration, listener_orchestration as vk_listener_orchestration


async def sender_orchestration(operating_mode: str) -> Sender:
    if operating_mode == "telegram":
        return await tg_sender_orchestration()
    if operating_mode == "vk":
        return await vk_sender_orchestration()
    raise


async def listener_orchestration(
        operating_mode: str,
        message_router: MessageRouter,
        command_router: CommandRouter) -> MessageListener:

    if operating_mode == "telegram":
        return await tg_listener_orchestration(COMMANDS.value(), message_router, command_router)
    if operating_mode == "vk":
        return await vk_listener_orchestration(COMMANDS.value(), message_router, command_router)
    raise
