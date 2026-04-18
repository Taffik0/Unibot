from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
from typing import TypeVar, Type, cast

from unibot.message.specific_data import SpecificData


T = TypeVar("T", bound=SpecificData)


@dataclass
class Message:
    id: str
    user_id: str
    chat_id: str
    text: str
    send_at: datetime
    specific_data: list[SpecificData] = field(
        default_factory=list[SpecificData])

    _index: dict[type[SpecificData], list[SpecificData]
                 ] = field(init=False, repr=False)

    def __post_init__(self):
        self._rebuild_index()

    def _rebuild_index(self):
        self._index = defaultdict(list)
        for item in self.specific_data:
            self._index[type(item)].append(item)

    def add_sd(self, item: SpecificData):
        self.specific_data.append(item)
        self._index[type(item)].append(item)

    def get_sd(self, cls: Type[T]) -> list[T]:
        return cast(list[T], self._index.get(cls, []))

    def has_sd(self, cls: Type[T]) -> bool:
        return bool(self._index.get(cls, []))
