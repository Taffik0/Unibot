from src.errors.handle_build_error import HandleBuildError
from src.handler.command_handler_builder import CommandHandlerBuilder
from src.handler.command_handler import CommandHandler
from src.types.command_handler_factory import CommandHandlerFactory
from src.commands.command import Command

from src.response.response_processor import ResponseProcessor


class CommandHandlerOrchestration:
    def __init__(self, command_handler_builder: CommandHandlerBuilder, response_processor: ResponseProcessor):
        self.command_handler_builder = command_handler_builder
        self.response_processor = response_processor

    async def process(self, handler_factory: CommandHandlerFactory, command: Command):
        try:
            builded_handler = await self.command_handler_builder.build(handler_factory)
        except HandleBuildError as e:
            print(
                f"Твой {handler_factory} не работает, переделывай! Вот тебе на подумать - {e}")
            return
        try:
            response = await builded_handler.handler.handle(command)
        except Exception as e:
            print(
                f"Твой {builded_handler.handler} - говно, так как - {e}")
        try:
            await self.command_handler_builder.clear(builded_handler)
        except Exception as e:
            print(f"Я даже не могу это очистить - {e}")
        if response is not None:
            await self.response_processor.process(response)
