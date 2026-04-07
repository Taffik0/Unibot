from typing import Any, AsyncGenerator
from dataclasses import dataclass
import inspect

from src.types.command_handler_factory import CommandHandlerFactory

from src.errors.handle_build_error import HandleBuildError

from src.handler.command_handler import CommandHandler
from src.tools.bot_tools import BotTools


@dataclass
class BuildedCommandHandler:
    handler: CommandHandler
    _gen: AsyncGenerator[CommandHandler, None] | None


class CommandHandlerBuilder:
    def __init__(self, bot_tools: BotTools):
        self.bot_tools = bot_tools

    async def build(self, factory: CommandHandlerFactory) -> BuildedCommandHandler:
        result = factory(**self.dependency_injection(factory))
        if inspect.isasyncgen(result):
            try:
                return BuildedCommandHandler(await result.__anext__(), result)
            except Exception as e:
                await result.aclose()
                raise HandleBuildError from e
        else:
            try:
                return BuildedCommandHandler(await result, None)
            except Exception as e:
                raise HandleBuildError from e

    async def clear(self, builded_handler: BuildedCommandHandler):
        if builded_handler._gen is not None:
            await builded_handler._gen.aclose()

    def dependency_injection(self, factory: CommandHandlerFactory) -> dict[str, Any]:
        args = {}
        if getattr(factory, "_require_bot_tools", False):
            args["bot_tools"] = self.bot_tools
        return args
