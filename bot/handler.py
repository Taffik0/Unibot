from src.handler.handler import Handler

from src.message.message import Message
from src.response.response_message import ResponseMessage

from src.response.response import Response, TextResponse
from src.response.response_container import ResponseContainer


class EchoHandler(Handler):
    async def handle(self, message: Message) -> ResponseContainer:
        return ResponseContainer(ResponseMessage.from_message(message), responses=[TextResponse(f"{message.text}")], new_state=None)


async def build_echo_handler() -> EchoHandler:
    return EchoHandler()
