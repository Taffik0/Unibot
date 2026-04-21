import ssl
import certifi
import aiohttp

import aiohttp

from unibot.commands.commands import Commands
from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter

from ...settings.vk_settings import TOKEN, GROUP_ID, IGNORE_SSL

from unibot.listeners.vk_listener import VKMessageListener
from unibot.message_adapters.incoming.vk_incoming_message_adapter import VKIncomingMessageAdapter
from unibot.message_adapters.incoming.commands.vk_incoming_command_adapter import VKIncomingCommandAdapter
from unibot.senders.vk_sender import VKSender


session = None

ssl_context = ssl._create_unverified_context()


async def get_session():
    try:
        from aiovk import TokenSession
        from aiovk.drivers import HttpDriver
    except ImportError:
        raise ImportError(
            "Install vk support: pip install unibot[vk]"
        )
    global session
    if not session:
        if IGNORE_SSL.value():
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            a_session = aiohttp.ClientSession(connector=connector)
            session = TokenSession(
                TOKEN.value(), driver=HttpDriver(session=a_session))
        else:
            session = TokenSession(TOKEN.value())
    return session


async def sender_orchestration() -> VKSender:
    return VKSender(await get_session())


async def listener_orchestration(
        command_enums: list[Commands],
        message_router: MessageRouter,
        command_router: CommandRouter) -> VKMessageListener:

    incoming_message_adapter = await incoming_message_adapter_orchestration()
    incoming_command_adapter = await incoming_command_adapter_orchestration(command_enums)

    return VKMessageListener(incoming_message_adapter, message_router, incoming_command_adapter, command_router, await get_session(), GROUP_ID.value())


async def incoming_message_adapter_orchestration() -> VKIncomingMessageAdapter:
    return VKIncomingMessageAdapter()


async def incoming_command_adapter_orchestration(command_enums: list[Commands]) -> VKIncomingCommandAdapter:
    return VKIncomingCommandAdapter(command_enums)
