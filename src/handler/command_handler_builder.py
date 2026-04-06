from typing import AsyncGenerator
from dataclasses import dataclass
import inspect

from src.types.command_handler_factory import CommandHandlerFactory

from src.errors.handle_build_error import HandleBuildError

from src.handler.command_handler import CommandHandler


@dataclass
class BuildedCommandHandler:
    handler: CommandHandler
    _gen: AsyncGenerator[CommandHandler, None] | None


class CommandHandlerBuilder:
    async def build(self, factory: CommandHandlerFactory) -> BuildedCommandHandler:
        result = factory()
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
