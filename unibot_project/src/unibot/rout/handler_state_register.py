from typing import Union, Callable, Awaitable, AsyncGenerator

from unibot.errors.handle_state_register_exceptions import StateHandlerConflictError

from unibot.state.state import States
from unibot.handler.handler import Handler

from unibot.types.handler_factory import HandlerFactory


class HandlerStateRegister:
    def __init__(self) -> None:
        self.base_layer: dict[States, HandlerFactory] = {}
        self.dedicated_layer: dict[States, HandlerFactory] = {}
        self.global_layer: dict[States, HandlerFactory] = {}

    def register(self, state: States, factory: HandlerFactory):
        if self.base_layer.get(state) is not None:
            raise StateHandlerConflictError(
                f"For {state} already have registered handler.")
        self.base_layer[state] = factory

    def register_dedicated(self, state: States, factory: HandlerFactory):
        if self.dedicated_layer.get(state) is not None:
            raise StateHandlerConflictError(
                f"For {state} already have registered handler.")
        self.dedicated_layer[state] = factory

    def register_global(self, state: States, factory: HandlerFactory):
        if self.global_layer.get(state) is not None:
            raise StateHandlerConflictError(
                f"For {state} already have registered handler.")
        self.global_layer[state] = factory

    async def get(self, state: States) -> HandlerFactory | None:
        return self.base_layer.get(state)

    async def get_dedicated(self, state: States) -> HandlerFactory | None:
        return self.dedicated_layer.get(state)

    async def get_global(self, state: States) -> HandlerFactory | None:
        return self.global_layer.get(state)
