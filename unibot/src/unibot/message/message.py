from dataclasses import dataclass, field
from datetime import datetime

from unibot.message.specific_data import SpecificData


@dataclass
class Message:
    id: str
    user_id: str
    chat_id: str
    text: str
    send_at: datetime
    specific_data: list[SpecificData] = field(
        default_factory=list[SpecificData])
