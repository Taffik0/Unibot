import asyncio
import traceback
from aiovk import TokenSession, API
from aiovk.longpoll import BotsLongPoll

from unibot.listeners.message_listener import MessageListener
from unibot.message_adapters.incoming.vk_incoming_message_adapter import VKIncomingMessageAdapter
from unibot.message_adapters.incoming.commands.vk_incoming_command_adapter import VKIncomingCommandAdapter
from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter


class VKMessageListener(MessageListener):
    def __init__(self,
                 incoming_message_adapter: VKIncomingMessageAdapter,
                 message_router: MessageRouter,
                 incoming_command_adapter: VKIncomingCommandAdapter,
                 command_router: CommandRouter,
                 session: TokenSession,
                 group_id: int):
        self.incoming_message_adapter = incoming_message_adapter
        self.message_router = message_router
        self.incoming_command_adapter = incoming_command_adapter
        self.command_router = command_router
        self.session = session

        self.api = API(session)
        self.longpoll = BotsLongPoll(self.api, group_id=group_id)

        self.listening_messages_task = None

    async def start(self):
        if self.listening_messages_task is None:
            self.listening_messages_task = asyncio.create_task(
                self.listening_messages())

    async def stop(self):
        if self.listening_messages_task is not None:
            self.listening_messages_task.cancel()
            try:
                await self.listening_messages_task
            except Exception as e:
                print(e)

    def _is_command(self, text: str) -> bool:
        if text:
            if text[0] == "/":
                return True
        return False

    async def listening_messages(self):
        try:
            async for event in self.longpoll.iter():
                if event["type"] == "message_new":
                    clear_message = self.incoming_message_adapter.adapt_message(
                        event["object"]["message"])
                    if self._is_command(event["object"]["message"]["text"]):
                        command_event = event["object"]["message"]
                        command_event["text"] = command_event["text"][1:]
                        clear_command = self.incoming_command_adapter.adapt_command(
                            command_event)
                        if clear_command:
                            await self.command_router.rout(clear_command)
                        return
                    if clear_message is None:
                        return
                    await self.message_router.rout(clear_message)
        except Exception as e:
            traceback.print_exc()
