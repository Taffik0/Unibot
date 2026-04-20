import asyncio
from asyncio import Queue

from unibot.rout.concurrency_limiter import ConcurrencyLimiter

from unibot.rout.handler_state_register import HandlerStateRegister
from unibot.handler.handler_builder import HandlerBuilder
from unibot.errors.handle_build_error import HandleBuildError
from unibot.state.conversation_state_repository import ConversationStateRepository

from unibot.message.message import Message
from unibot.response.response_container import ResponseContainer
from unibot.response.response_processor import ResponseProcessor

from unibot.errors.handle_process_error import HandleProcessError

from unibot.logger.logger import logger


class MessageRouter:
    def __init__(self, handler_state_register: HandlerStateRegister,
                 handler_builder: HandlerBuilder,
                 conversation_state_repository: ConversationStateRepository,
                 concurrency_limiter: ConcurrencyLimiter,
                 response_processor: ResponseProcessor):
        self.handler_state_register = handler_state_register
        self.handler_builder = handler_builder
        self.conversation_state_repository = conversation_state_repository
        self.response_processor = response_processor

        self.tasks_queue: Queue[Message] = Queue()
        self.semaphore = concurrency_limiter.semaphore
        self.max_tasks = concurrency_limiter.max_tasks

        self._is_working = True
        self.async_worker_task = None

    async def rout(self, message: Message):
        await self.tasks_queue.put(message)

    async def start(self):
        self._is_working = True
        self.async_worker_task = asyncio.create_task(self.async_worker())

    async def stop(self):
        self._is_working = False
        if self.async_worker_task:
            self.async_worker_task.cancel()
        try:
            await self.async_worker_task
        except asyncio.CancelledError:
            pass

    async def async_worker(self):
        workers = [asyncio.create_task(self._worker_loop())
                   for _ in range(self.max_tasks)]
        await asyncio.gather(*workers)

    async def _worker_loop(self):
        while self._is_working:
            message = await self.tasks_queue.get()
            try:
                await self._process(message)
            finally:
                self.tasks_queue.task_done()

    async def _process(self, message: Message):
        async with self.semaphore:
            state = await self.conversation_state_repository.get_state(message.user_id)
            handlers: list = []
            # get from global layer
            global_handlers = await self.handler_state_register.get_global(state)
            if global_handlers:
                handlers.append(*global_handlers)
            # get from dedicated layer
            dedicated_handlers = await self.handler_state_register.get_dedicated(state)
            if dedicated_handlers:
                handlers.append(*dedicated_handlers)
            # get from base layer (max one handler always)
            base_handler = await self.handler_state_register.get(state)
            if base_handler is not None:
                handlers.append(base_handler)

            for handler_factory in handlers:
                if handler_factory is not None:
                    resp = await self._process_handler(handler_factory, message)
                    if resp is not None:
                        await self._process_response(resp)
                        if resp.new_state is not None:
                            return
            logger().info(
                f"Successfully handle message id:{message.id} in chat:{message.chat_id} from user:{message.user_id}")

    async def _process_handler(self, handler_factory, message) -> ResponseContainer | None:
        try:
            async with self.handler_builder.use_handler(handler_factory) as handler:
                try:
                    return await handler.handle(message)
                except Exception as e:
                    logger().error(
                        f"error while processing handler {handler_factory} "
                        f"message_id={message.id} user_id={message.user_id} - {e}"
                    )
                    return None
        except HandleBuildError as e:
            logger().error(f"error while build {handler_factory} - {e}")
            return None

    async def _process_response(self, resp: ResponseContainer):
        await self.response_processor.process(resp)
