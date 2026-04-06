import asyncio
from asyncio import Queue

from src.handler.handler import Handler
from src.handler.handler_builder import HandlerBuilder
from src.message.message import Message
from src.types.handler_factory import HandlerFactory
from src.response.response_processor import ResponseProcessor

from src.errors.handle_build_error import HandleBuildError


class HandlerOrchestrator:
    def __init__(self, max_tasks: int, handler_builder: HandlerBuilder, response_processor: ResponseProcessor):
        self.handler_builder = handler_builder
        self.response_processor = response_processor

        self.max_tasks = max_tasks

        self.tasks_queue: Queue[tuple[HandlerFactory, Message]] = Queue()
        self.semaphore = asyncio.Semaphore(max_tasks)

        self._is_working = True
        self.async_worker_task = None

    async def start(self):
        self._is_working = True
        self.async_worker_task = asyncio.create_task(self.async_worker())

    async def stop(self):
        self._is_working = False
        self.async_worker_task.cancel()

    async def add_task(self, handler_factory: HandlerFactory, message: Message):
        await self.tasks_queue.put((handler_factory, message))

    async def async_worker(self):
        while self._is_working:
            factory, message = await self.tasks_queue.get()

            task = asyncio.create_task(self._process(factory, message))

    async def _process(self, handler_factory: HandlerFactory, message: Message):
        async with self.semaphore:
            try:
                builded_handler = await self.handler_builder.build(handler_factory)
            except HandleBuildError as e:
                print(
                    f"Твой {handler_factory} не работает, переделывай! Вот тебе на подумать - {e}")
                return
            try:
                response = await builded_handler.handler.handle(message)
            except Exception as e:
                print(
                    f"Твой {builded_handler.handler} - говно, так как - {e}")
            try:
                await self.handler_builder.clear(builded_handler)
            except Exception as e:
                print(f"Я даже не могу это очистить - {e}")
            if response is not None:
                await self.response_processor.process(response)
