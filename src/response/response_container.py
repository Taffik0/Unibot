from dataclasses import dataclass
from src.response.response import Response
from src.state.state import States
from src.response.response_message import ResponseMessage


@dataclass
class ResponseContainer:
    message: ResponseMessage
    responses: list[Response]
    new_state: None | States = None
