from dataclasses import dataclass
from src.response.response import Response
from src.state.state import States
from src.message.message import Message


@dataclass
class ResponseContainer:
    message: Message
    responses: list[Response]
    new_state: None | States
