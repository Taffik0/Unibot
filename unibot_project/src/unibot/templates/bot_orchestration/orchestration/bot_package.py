from dataclasses import dataclass

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

from unibot.listeners.message_listener import MessageListener


@dataclass
class BotPackage:
    message_router: MessageRouter
    handler_state_register: HandlerStateRegister
    handler_builder: HandlerBuilder

    command_router: CommandRouter
    handler_command_register: HandlerCommandRegister
    command_handler_builder: CommandHandlerBuilder

    conversation_state_repository: ConversationStateRepository
    response_processor: ResponseProcessor
    bot_tools: BotTools

    message_listener: MessageListener
