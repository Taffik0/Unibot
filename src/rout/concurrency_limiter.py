import asyncio


class ConcurrencyLimiter:
    def __init__(self, max_tasks: int) -> None:
        self.max_tasks = max_tasks
        self.semaphore = asyncio.Semaphore(max_tasks)
