from typing import Union, Callable, Awaitable, AsyncGenerator
from unibot.handler.command_handler import CommandHandler


CommandHandlerFactory = Union[
    Callable[[], Awaitable[CommandHandler]],
    Callable[[], AsyncGenerator[CommandHandler, None]]
]
