from typing import Union, Callable, Awaitable, AsyncGenerator
from unibot.handler.handler import Handler


HandlerFactory = Union[
    Callable[[], Awaitable[Handler]],
    Callable[[], AsyncGenerator[Handler, None]]
]
