from typing import Union, Callable, Awaitable, AsyncGenerator
from src.handler.handler import Handler


HandlerFactory = Union[
    Callable[[], Awaitable[Handler]],
    Callable[[], AsyncGenerator[Handler, None]]
]
