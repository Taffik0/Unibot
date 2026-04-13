from unibot.response import ResponseContainer, ResponseMessage, TextResponse

from unibot.handler import Handler, CommandHandler

from unibot.message.message import Message


class EchoHandler(Handler):
    async def handle(self, message: Message) -> ResponseContainer:
        return ResponseContainer(ResponseMessage.from_message(message),
                                 [TextResponse(f"{message.text}")])


async def gen_echo_handler() -> EchoHandler:
    return EchoHandler()
