import asyncio

from aiogram import Bot

from src.rout.concurrency_limiter import ConcurrencyLimiter

from src.listeners.telegram_message_listener import TelegramMessageListener
from src.senders.telegram_sender import TelegramSender
from src.message_adapters.incoming.telegram_incoming_message_adapter import TelegramIncomingMessageAdapter
from src.message_adapters.incoming.commands.telegram_incoming_command_adapter import TelegramIncomingCommandAdapter
from src.rout.message_router import MessageRouter
from src.rout.handler_orchestrator import HandlerOrchestrator
from src.rout.handler_state_register import HandlerStateRegister
from src.state.conversation_state_repository import ConversationStateRepository

from src.rout.commands.command_router import CommandRouter
from src.rout.commands.command_handler_orchestrator import CommandHandlerOrchestration
from src.rout.commands.handler_command_register import HandlerCommandRegister
from src.handler.command_handler_builder import CommandHandlerBuilder

from src.tools.bot_tools import BotTools

from src.handler.handler_builder import HandlerBuilder

from src.response.response_processor import ResponseProcessor

from bot.states import MyStates
from bot.commands import MyCommand
from bot.handler import EchoHandler, build_echo_handler
from bot.start_handler import StartHandler, build_start_handler


API_TOKEN = "7125067226:AAFUzHXjzImkmzZ7jUbAq-eZxOd4rVJM7yg"


async def main():
    print("create tg bot")
    bot = Bot(token=API_TOKEN)

    print("bot building...")
    concurrency_limiter = ConcurrencyLimiter(max_tasks=50)

    print("build conversation state repository")
    conversation_state_repository = ConversationStateRepository(MyStates.START)

    print("build response processor")
    response_processor = ResponseProcessor(
        TelegramSender(bot), conversation_state_repository)

    bot_tools = BotTools(response_processor)

    print("build handler orchestrator")
    handler_orchestrator = HandlerOrchestrator(
        handler_builder=HandlerBuilder(bot_tools), response_processor=response_processor)

    print("build handler state register")
    handler_state_register = HandlerStateRegister()

    handler_state_register.register(MyStates.START, build_echo_handler)

    print("build message rout")
    message_rout = MessageRouter(handler_state_register=handler_state_register,
                                 handler_orchestrator=handler_orchestrator,
                                 conversation_state_repository=conversation_state_repository,
                                 concurrency_limiter=concurrency_limiter)

    handler_command_register = HandlerCommandRegister()

    await handler_command_register.register(MyCommand.START, build_start_handler)

    command_rout = CommandRouter(concurrency_limiter, CommandHandlerOrchestration(
        CommandHandlerBuilder(bot_tools), response_processor), handler_command_register)

    print("build tg listener")
    tg_listener = TelegramMessageListener(bot=bot,
                                          message_router=message_rout, incoming_message_adapter=TelegramIncomingMessageAdapter(),
                                          incoming_command_adapter=TelegramIncomingCommandAdapter([MyCommand]), command_router=command_rout)

    print("bot starting...")
    print("start handler orchestrator")
    await message_rout.start()
    print("start tg listener")
    await tg_listener.start()
    print("start command rout")
    await command_rout.start()
    print("bot started")

    try:
        while True:
            await asyncio.sleep(3600)  # 1 час
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("stopping bot...")

        await tg_listener.stop()
        await message_rout.stop()
        await command_rout.stop()

        print("bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
