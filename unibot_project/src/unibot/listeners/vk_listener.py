from unibot.listeners.message_listener import MessageListener
from unibot.message_adapters.incoming.vk_incoming_message_adapter import VKIncomingMessageAdapter
from unibot.message_adapters.incoming.commands.incoming_command_adapter import IncomingCommandAdapter
from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter


class VLMessageListener(MessageListener):
    def __init__(self, incoming_message_adapter: VKIncomingMessageAdapter, message_router: MessageRouter, incoming_command_adapter: IncomingCommandAdapter, command_router: CommandRouter):
        self.incoming_message_adapter = incoming_message_adapter
        self.message_router = message_router
        self.incoming_command_adapter = incoming_command_adapter
        self.command_router = command_router

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()
