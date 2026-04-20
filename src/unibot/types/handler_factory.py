from typing import Union, Callable, Awaitable, AsyncGenerator, TYPE_CHECKING

if TYPE_CHECKING:
    from unibot.handler.handler import Handler


HandlerFactory = Union[
    Callable[..., Awaitable["Handler"]],
    Callable[..., AsyncGenerator["Handler", None]]
]
