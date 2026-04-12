from typing import Any, AsyncGenerator, AsyncIterator
from dataclasses import dataclass
import inspect

from unibot.types.handler_factory import HandlerFactory
from unibot.types.command_handler_factory import CommandHandlerFactory

from unibot.errors.handle_build_error import HandleBuildError

from unibot.handler.handler import Handler
from unibot.handler.command_handler import CommandHandler

from unibot.tools.bot_tools import BotTools

from contextlib import asynccontextmanager


@dataclass
class BuildedHandler:
    handler: Handler | CommandHandler
    _gen: AsyncGenerator[Handler, None] | None


class HandlerBuilder:
    def __init__(self, bot_tools: BotTools):
        self.bot_tools = bot_tools

    async def build(self, factory: HandlerFactory | CommandHandlerFactory) -> BuildedHandler:
        result = factory(**self.dependency_injection(factory))
        if inspect.isasyncgen(result):
            try:
                return BuildedHandler(await result.__anext__(), result)
            except Exception as e:
                await result.aclose()
                raise HandleBuildError from e
        else:
            try:
                return BuildedHandler(await result, None)
            except Exception as e:
                raise HandleBuildError from e

    async def clear(self, builded_handler: BuildedHandler):
        if builded_handler._gen is not None:
            await builded_handler._gen.aclose()

    def dependency_injection(self, factory: HandlerFactory | CommandHandlerFactory) -> dict[str, Any]:
        args = {}
        if getattr(factory, "_require_bot_tools", False):
            args["bot_tools"] = self.bot_tools
        return args

    @asynccontextmanager
    async def use_handler(self, handler_factory: HandlerFactory) -> AsyncIterator[Handler]:
        build_handler = await self.build(handler_factory)
        try:
            yield build_handler.handler
        finally:
            await self.clear(builded_handler=build_handler)

    @asynccontextmanager
    async def use_command_handler(self, handler_factory: CommandHandlerFactory) -> AsyncIterator[CommandHandler]:
        build_handler = await self.build(handler_factory)
        try:
            yield build_handler.handler
        finally:
            await self.clear(builded_handler=build_handler)
