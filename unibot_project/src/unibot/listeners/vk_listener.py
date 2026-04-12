from unibot.listeners.message_listener import MessageListener
from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.message_router import MessageRouter


class VLMessageListener(MessageListener):
    def __init__(self, incoming_message_adapter: TelegramIncomingMessageAdapter, message_router: MessageRouter, incoming_command_adapter: TelegramIncomingCommandAdapter, command_router: CommandRouter):
        pass

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()
