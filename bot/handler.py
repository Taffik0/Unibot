from src.handler.handler import Handler

from src.message.message import Message
from src.response.response_message import ResponseMessage

from src.response.response import Response, TextResponse
from src.response.response_container import ResponseContainer

from src.tools.bot_tools_require_decorator import require_bot_tools
from src.tools.bot_tools import BotTools


class EchoHandler(Handler):
    def __init__(self, boot_tools: BotTools):
        self.bot_tools = boot_tools

    async def handle(self, message: Message) -> ResponseContainer:
        print(self.bot_tools)
        await self.bot_tools.send_response(ResponseContainer(ResponseMessage.from_message(
            message), responses=[TextResponse(f"Привет деградант ^-^")]))
        return ResponseContainer(ResponseMessage.from_message(message), responses=[TextResponse(f"{message.text}")])


@require_bot_tools
async def build_echo_handler(bot_tools=None) -> EchoHandler:
    return EchoHandler(bot_tools)
