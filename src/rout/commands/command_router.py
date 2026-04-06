import asyncio
from asyncio import Queue

from src.types.command_handler_factory import CommandHandlerFactory
from src.handler.command_handler import CommandHandler
from src.commands.command import Command
from src.rout.commands.handler_command_register import HandlerCommandRegister

from src.rout.commands.command_handler_orchestrator import CommandHandlerOrchestration


class CommandRouter:
    def __init__(self, max_tasks: int,
                 command_handler_orchestrator: CommandHandlerOrchestration,
                 handler_command_register: HandlerCommandRegister) -> None:
        self.max_tasks = max_tasks
        self.command_handler_orch = command_handler_orchestrator
        self.handler_command_register = handler_command_register

        self.tasks_queue: Queue[Command] = Queue()
        self.semaphore = asyncio.Semaphore(max_tasks)

        self._is_working = True
        self.async_worker_task = None

    async def start(self):
        self._is_working = True
        self.async_worker_task = asyncio.create_task(self.async_worker())

    async def stop(self):
        self._is_working = False
        self.async_worker_task.cancel()

    async def rout(self, command: Command):
        await self.tasks_queue.put(command)

    async def async_worker(self):
        while self._is_working:
            command = await self.tasks_queue.get()

            task = asyncio.create_task(self._process(command))

    async def _process(self, command: Command):
        handler_factory = await self.handler_command_register.get(command.command)
        if handler_factory is None:
            raise
        await self.command_handler_orch.process(handler_factory, command)
