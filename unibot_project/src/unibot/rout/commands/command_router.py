import asyncio
from asyncio import Queue

from unibot.errors.handle_build_error import HandleBuildError
from unibot.response.response_container import ResponseContainer
from unibot.rout.concurrency_limiter import ConcurrencyLimiter

from unibot.types.command_handler_factory import CommandHandlerFactory
from unibot.handler.command_handler import CommandHandler
from unibot.commands.command import Command
from unibot.rout.commands.handler_command_register import HandlerCommandRegister
from unibot.response.response_processor import ResponseProcessor
from unibot.handler.handler_builder import HandlerBuilder

from unibot.logger.logger import logger


class CommandRouter:
    def __init__(self, concurrency_limiter: ConcurrencyLimiter,
                 handler_builder: HandlerBuilder,
                 handler_command_register: HandlerCommandRegister,
                 response_processor: ResponseProcessor) -> None:
        self.handler_builder = handler_builder
        self.handler_command_register = handler_command_register
        self.response_processor = response_processor

        self.tasks_queue: Queue[Command] = Queue()
        self.semaphore = concurrency_limiter.semaphore
        self.max_task = concurrency_limiter.max_tasks

        self._is_working = True
        self.async_worker_task = None

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

    async def rout(self, command: Command):
        await self.tasks_queue.put(command)

    async def async_worker(self):
        workers = [asyncio.create_task(self._worker_loop())
                   for _ in range(self.max_tasks)]
        await asyncio.gather(*workers)

    async def _worker_loop(self):
        while self._is_working:
            async with self.semaphore:
                message = await self.tasks_queue.get()
                try:
                    await self._process(message)
                finally:
                    self.tasks_queue.task_done()

    async def _process(self, command: Command):
        handler_factory = await self.handler_command_register.get(command.command)
        if handler_factory is None:
            return

        resp = await self._process_handler(handler_factory, command)
        if resp is not None:
            await self.response_processor.process(resp)

        logger().info(
            f"Successfully handle command {command.command.name} id:{command.message_id} in chat:{command.chat_id} from user:{command.user_id}")

    async def _process_handler(self, handler_factory: CommandHandlerFactory, command: Command) -> ResponseContainer | None:
        try:
            async with self.handler_builder.use_command_handler(handler_factory) as handler:
                try:
                    return await handler.handle(command)
                except Exception as e:
                    logger().error(
                        f"error while processing handler {handler_factory} "
                        f"command={command.command} id={command.message_id} user_id={command.user_id} - {e}"
                    )
                    return None
        except HandleBuildError as e:
            logger().error(f"error while build {handler_factory} - {e}")
            return None
