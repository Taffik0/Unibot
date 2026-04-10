from dataclasses import dataclass
from unibot.response.response import Response
from unibot.state.state import States
from unibot.response.response_message import ResponseMessage


@dataclass
class ResponseContainer:
    message: ResponseMessage
    responses: list[Response]
    new_state: None | States = None
