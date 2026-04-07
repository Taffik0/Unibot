import asyncio
from asyncio import Queue

from src.rout.concurrency_limiter import ConcurrencyLimiter

from src.rout.handler_state_register import HandlerStateRegister
from src.rout.handler_orchestrator import HandlerOrchestrator
from src.state.conversation_state_repository import ConversationStateRepository

from src.message.message import Message
from src.response.response_container import ResponseContainer

from src.errors.handle_process_error import HandleProcessError


class MessageRouter:
    def __init__(self, handler_state_register: HandlerStateRegister,
                 handler_orchestrator: HandlerOrchestrator,
                 conversation_state_repository: ConversationStateRepository, concurrency_limiter: ConcurrencyLimiter):
        self.handler_state_register = handler_state_register
        self.handler_orchestrator = handler_orchestrator
        self.conversation_state_repository = conversation_state_repository

        self.tasks_queue: Queue[Message] = Queue()
        self.semaphore = concurrency_limiter.semaphore

        self._is_working = True
        self.async_worker_task = None

    async def rout(self, message: Message):
        await self.tasks_queue.put(message)

    async def start(self):
        self._is_working = True
        self.async_worker_task = asyncio.create_task(self.async_worker())

    async def stop(self):
        self._is_working = False
        self.async_worker_task.cancel()

    async def async_worker(self):
        while self._is_working:
            message = await self.tasks_queue.get()

            task = asyncio.create_task(self._process(message))

    async def _process(self, message: Message):
        async with self.semaphore:
            state = await self.conversation_state_repository.get_state(message.user_id)
            handler_factory = await self.handler_state_register.get_global(state)
            if handler_factory is not None:
                resp = await self._process_handler(handler_factory, message)
                if resp is not None:
                    if resp.new_state is not None:
                        return
            handler_factory = await self.handler_state_register.get_dedicated(state)
            if handler_factory is not None:
                resp = await self._process_handler(handler_factory, message)
                if resp is not None:
                    if resp.new_state is not None:
                        return
            handler_factory = await self.handler_state_register.get(state)
            if handler_factory is not None:
                resp = await self._process_handler(handler_factory, message)

    async def _process_handler(self, handler_factory, message) -> ResponseContainer | None:
        try:
            resp = await self.handler_orchestrator.process(handler_factory, message)
            return resp
        except HandleProcessError as e:
            print(f"error - {e}")
            return None
