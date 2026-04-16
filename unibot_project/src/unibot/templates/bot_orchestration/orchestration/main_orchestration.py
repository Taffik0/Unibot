from ..settings.main import OPERATING_MODE, MAX_TASKS, DEFAULT_STATE, MESSAGE_HANDLERS, COMMAND_HANDLERS, COMMANDS

from .infrastructure_orchestration import sender_orchestration, listener_orchestration

from .bot_package import BotPackage

from unibot.rout.concurrency_limiter import ConcurrencyLimiter

from unibot.rout.message_router import MessageRouter
from unibot.rout.handler_orchestrator import HandlerOrchestrator
from unibot.rout.handler_state_register import HandlerStateRegister
from unibot.handler.handler_builder import HandlerBuilder

from unibot.rout.commands.command_router import CommandRouter
from unibot.rout.commands.command_handler_orchestrator import CommandHandlerOrchestration
from unibot.rout.commands.handler_command_register import HandlerCommandRegister
from unibot.handler.command_handler_builder import CommandHandlerBuilder

from unibot.state.conversation_state_repository import ConversationStateRepository

from unibot.response.response_processor import ResponseProcessor

from unibot.tools.bot_tools import BotTools

from unibot.types.handler_layers import Layers


async def orchestration() -> BotPackage:
    operating_mod = str(OPERATING_MODE.value())
    concurrency_limiter = ConcurrencyLimiter(int(MAX_TASKS.value()))

    sender = await sender_orchestration(operating_mod)

    conversation_state_repository = ConversationStateRepository(
        DEFAULT_STATE.value())

    response_processor = ResponseProcessor(
        sender, conversation_state_repository)

    bot_tools = BotTools(response_processor)

    # message
    handler_state_register = HandlerStateRegister()
    handler_builder = HandlerBuilder(bot_tools)
    message_router = MessageRouter(handler_state_register=handler_state_register,
                                   conversation_state_repository=conversation_state_repository,
                                   concurrency_limiter=concurrency_limiter,
                                   handler_builder=handler_builder,
                                   response_processor=response_processor)

    # command
    handler_command_register = HandlerCommandRegister()
    command_router = CommandRouter(handler_command_register=handler_command_register,
                                   concurrency_limiter=concurrency_limiter,
                                   handler_builder=handler_builder,
                                   response_processor=response_processor)

    listener = await listener_orchestration(operating_mod, message_router, command_router)

    bot_package = BotPackage(message_router=message_router,
                             handler_state_register=handler_state_register,
                             handler_builder=handler_builder,
                             command_router=command_router,
                             handler_command_register=handler_command_register,
                             conversation_state_repository=conversation_state_repository,
                             response_processor=response_processor,
                             bot_tools=bot_tools,
                             message_listener=listener)

    return bot_package


async def start(bot: BotPackage):
    print("starting message router")
    await bot.message_router.start()
    print("starting listener")
    await bot.message_listener.start()
    print("starting command router")
    await bot.command_router.start()


async def stop(bot: BotPackage):
    print("stopping message router")
    await bot.message_router.stop()
    print("stopping listener")
    await bot.message_listener.stop()
    print("stopping command router")
    await bot.command_router.stop()


async def register(bot: BotPackage):
    await _register_message_handlers(bot)
    await _register_command_handlers(bot)


async def _register_message_handlers(bot: BotPackage):
    global MESSAGE_HANDLERS
    message_handlers = MESSAGE_HANDLERS.value()
    for key in message_handlers:
        layer, state = key
        if layer == Layers.BASE:
            bot.handler_state_register.register(
                state=state, factory=message_handlers[key])
        # if layer == Layers.DEDICATED:
        #    bot.handler_state_register.register_dedicated(
        #        state=state, factory=message_handlers[key])
        if layer == Layers.GLOBAL:
            bot.handler_state_register.register_global(
                state=state, factory=message_handlers[key])


async def _register_command_handlers(bot: BotPackage):
    global COMMAND_HANDLERS
    command_handlers = COMMAND_HANDLERS.value()
    for command in command_handlers:
        await bot.handler_command_register.register(
            command, command_handlers[command])


async def _register_command(bot: BotPackage):
    global COMMANDS
    commands = COMMANDS.value()
