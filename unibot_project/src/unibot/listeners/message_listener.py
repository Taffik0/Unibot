from abc import ABC, abstractmethod


class MessageListener(ABC):
    @abstractmethod
    async def start(self) -> bool:
        pass

    @abstractmethod
    async def stop(self) -> bool:
        pass
