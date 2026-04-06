from typing import AsyncGenerator
from dataclasses import dataclass
import inspect

from src.types.handler_factory import HandlerFactory

from src.errors.handle_build_error import HandleBuildError

from src.handler.handler import Handler


@dataclass
class BuildedHandler:
    handler: Handler
    _gen: AsyncGenerator[Handler, None] | None


class HandlerBuilder:
    async def build(self, factory: HandlerFactory) -> BuildedHandler:
        result = factory()
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
