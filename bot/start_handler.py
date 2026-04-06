from src.handler.command_handler import CommandHandler

from src.commands.command import Command
from src.response.response_message import ResponseMessage
from bot.states import MyStates

from src.response.response import Response, TextResponse
from src.response.response_container import ResponseContainer


class StartHandler(CommandHandler):
    async def handle(self, command: Command) -> ResponseContainer:
        return ResponseContainer(ResponseMessage.from_command(command), [TextResponse("прив")], new_state=MyStates.START)


async def build_start_handler() -> StartHandler:
    return StartHandler()
