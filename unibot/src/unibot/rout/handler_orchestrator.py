import asyncio
from asyncio import Queue

from unibot.handler.handler import Handler
from unibot.handler.handler_builder import HandlerBuilder
from unibot.message.message import Message
from unibot.types.handler_factory import HandlerFactory
from unibot.response.response_processor import ResponseProcessor
from unibot.response.response_container import ResponseContainer

from unibot.errors.handle_build_error import HandleBuildError
from unibot.errors.handle_process_error import HandleProcessError


class HandlerOrchestrator:
    def __init__(self, handler_builder: HandlerBuilder, response_processor: ResponseProcessor):
        self.handler_builder = handler_builder
        self.response_processor = response_processor

    async def process(self, handler_factory: HandlerFactory, message: Message) -> ResponseContainer:
        try:
            builded_handler = await self.handler_builder.build(handler_factory)
        except HandleBuildError as e:
            print(
                f"Твой {handler_factory} не работает, переделывай! Вот тебе на подумать - {e}")
            raise HandleProcessError from e
        try:
            response = await builded_handler.handler.handle(message)
        except Exception as e:
            print(
                f"Твой {builded_handler.handler} - говно, так как - {e}")
            raise HandleProcessError from e
        try:
            await self.handler_builder.clear(builded_handler)
        except Exception as e:
            print(f"Я даже не могу это очистить - {e}")
        if response is not None:
            await self.response_processor.process(response)
        return response
