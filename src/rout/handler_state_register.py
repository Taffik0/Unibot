from typing import Union, Callable, Awaitable, AsyncGenerator

from src.errors.handle_state_register_exceptions import StateHandlerConflictError

from src.state.state import States
from src.handler.handler import Handler

from src.types.handler_factory import HandlerFactory


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

    async def get(self, state: States) -> HandlerFactory:
        return self.base_layer[state]

    async def get_dedicated(self, state: States) -> HandlerFactory:
        return self.dedicated_layer[state]

    async def get_global(self, state: States) -> HandlerFactory:
        return self.global_layer[state]
