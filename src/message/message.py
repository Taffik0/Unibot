from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    id: str
    user_id: str
    chat_id: str
    text: str
    send_at: datetime
