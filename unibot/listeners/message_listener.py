from abc import ABC, abstractmethod


class MessageListener(ABC):
    @abstractmethod
    def start(self) -> bool:
        pass

    @abstractmethod
    def stop(self) -> bool:
        pass
