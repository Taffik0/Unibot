import os

from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Generic

T = TypeVar('T')


class ABCSetting(ABC):
    @abstractmethod
    def value(self) -> Any:
        pass


class Setting(ABCSetting, Generic[T]):
    def __init__(self, val: T):
        self.val = val

    def value(self) -> T:
        return self.val


class TextSetting(ABCSetting):
    def __init__(self, val: str):
        self.val = val

    def value(self) -> str:
        return self.val


A = TypeVar("A")
R = TypeVar("R")


class ChangeSetting(ABCSetting):
    def __init__(self, val: Any | ABCSetting, func: Callable[[A], R]):
        self.val = val
        self.func = func

    def value(self) -> Any:
        if isinstance(self.val, ABCSetting):
            return self.func(self.val.value())
        return self.func(self.val)


class EmptySettingException(Exception):
    pass


class EmptySetting(ABCSetting):
    def __init__(self, msg: str):
        self.msg = msg

    def value(self) -> None:
        raise EmptySettingException(self.msg)


class ListSetting(ABCSetting):
    def __init__(self, *args):
        self.vals = args

    def value(self) -> list:
        l = []
        for val in self.vals:
            if isinstance(val, ABCSetting):
                l.append(val.value())
            else:
                l.append(val)
        return l


class ENVLoadException(Exception):
    pass


class EnvSetting(ABCSetting):
    def __init__(self, name: str, default: str | None = None, exception_if_none: bool = False):
        self.name = name
        self.default = default
        self.exception_if_none = exception_if_none

    def value(self) -> str | None:
        value = os.getenv(self.name, self.default)
        if self.exception_if_none and value is None:
            raise ENVLoadException()
        return value
