from dataclasses import dataclass, field
from typing import Callable, Awaitable


@dataclass
class SpecificData:
    sd_type: str = field(init=False)


@dataclass
class FullNameSD(SpecificData):
    first_name: str
    surname: str
    middle_name: str

    def __post_init__(self):
        self.sd_type = "full_name"


@dataclass
class Picture:
    width: int
    height: int

    _download_func: Callable[[], Awaitable[bytes | None]] = field(
        repr=False, compare=False)

    async def download(self) -> bytes | None:
        return await self._download_func()


@dataclass
class PictureSD(SpecificData):
    picture_sizes: list[Picture]

    def __post_init__(self):
        self.sd_type = "picture"
        self.picture_sizes.sort(key=lambda p: p.width * p.height)

    def get_max(self) -> Picture:
        return self.picture_sizes[-1]

    def get_min(self) -> Picture:
        return self.picture_sizes[0]


@dataclass
class VKSD(SpecificData):
    random_id: int
    is_community: bool

    def __post_init__(self):
        self.sd_type = "vk"
