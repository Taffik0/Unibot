import asyncio
from aiovk import TokenSession, API
from aiovk.longpoll import LongPoll

from unibot.listeners.message_listener import MessageListener
from unibot.message_adapters.incoming.vk_incoming_message_adapter import VKIncomingMessageAdapter
from unibot.message_adapters.incoming.commands.incoming_command_adapter import IncomingCommandAdapter
from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter


class VLMessageListener(MessageListener):
    def __init__(self,
                 incoming_message_adapter: VKIncomingMessageAdapter,
                 message_router: MessageRouter,
                 incoming_command_adapter: IncomingCommandAdapter,
                 command_router: CommandRouter,
                 session: TokenSession):
        self.incoming_message_adapter = incoming_message_adapter
        self.message_router = message_router
        self.incoming_command_adapter = incoming_command_adapter
        self.command_router = command_router
        self.session = session

        self.api = API(session)
        self.longpoll = LongPoll(session)

        self.listening_messages_task = None

    async def start(self):
        if self.listening_messages_task is None:
            self.listening_messages_task = asyncio.create_task(
                self.listening_messages)

    async def stop(self):
        if self.listening_messages_task is not None:
            self.listening_messages_task.cancel()
            try:
                await self.listening_messages_task
            except Exception as e:
                print(e)

    async def listening_messages(self):
        async for event in self.longpoll.iter():
            if event.type == "message_new":
                clear_message = self.incoming_message_adapter.adapt_message(
                    event.object.message)
                if clear_message is None:
                    return
                await self.message_router.rout(clear_message)
