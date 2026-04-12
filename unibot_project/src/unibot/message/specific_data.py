from dataclasses import dataclass, field


@dataclass
class SpecificData:
    type: str = field(init=False)


@dataclass
class FullNameSD(SpecificData):
    first_name: str
    surname: str
    middle_name: str

    def __post_init__(self):
        self.type = "full_name"


@dataclass
class VKSD(SpecificData):
    random_id: int
    is_community: bool

    def __post_init__(self):
        self.type = "vk"
