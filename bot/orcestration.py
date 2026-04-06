import asyncio

from aiogram import Bot

from src.listeners.telegram_message_listener import TelegramMessageListener
from src.senders.telegram_sender import TelegramSender
from src.message_adapters.incoming.telegram_incoming_message_adapter import TelegramIncomingMessageAdapter
from src.rout.message_router import MessageRouter
from src.rout.handler_orchestrator import HandlerOrchestrator
from src.rout.handler_state_register import HandlerStateRegister
from src.state.conversation_state_repository import ConversationStateRepository

from src.handler.handler_builder import HandlerBuilder

from src.response.response_processor import ResponseProcessor

from bot.states import MyStates
from bot.handler import EchoHandler, build_echo_handler


API_TOKEN = "7125067226:AAFUzHXjzImkmzZ7jUbAq-eZxOd4rVJM7yg"


async def main():
    print("create tg bot")
    bot = Bot(token=API_TOKEN)

    print("build conversation state repository")
    conversation_state_repository = ConversationStateRepository(MyStates.START)

    print("build response processor")
    response_processor = ResponseProcessor(
        TelegramSender(bot), conversation_state_repository)

    print("build handler orchestrator")
    handler_orchestrator = HandlerOrchestrator(
        max_tasks=50, handler_builder=HandlerBuilder(), response_processor=response_processor)

    print("build handler state register")
    handler_state_register = HandlerStateRegister()

    handler_state_register.register(MyStates.START, build_echo_handler)

    print("build message rout")
    message_rout = MessageRouter(handler_state_register=handler_state_register,
                                 handler_orchestrator=handler_orchestrator, conversation_state_repository=conversation_state_repository)

    print("build tg listener")
    tg_listener = TelegramMessageListener(bot=bot,
                                          message_router=message_rout, incoming_message_adapter=TelegramIncomingMessageAdapter())

    print("start handler orchestrator")
    await handler_orchestrator.start()
    print("start tg listener")
    await tg_listener.start()
    print("bot started")

    try:
        while True:
            await asyncio.sleep(3600)  # 1 час
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("stopping bot...")

        await tg_listener.stop()
        await handler_orchestrator.stop()

        print("bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
