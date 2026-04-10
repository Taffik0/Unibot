# Type and utils import
from unibot.utils.setting import Setting, EmptySetting
from unibot.commands.commands import Commands
from unibot.types.command_handler_factory import CommandHandlerFactory
from unibot.types.handler_factory import HandlerFactory
from unibot.types.handler_layers import Layers
from unibot.state.state import States

# Your code import


OPERATING_MOD = EmptySetting("OPERATING_MOD not specified (in main settings)")

MAX_TASKS: Setting[int] = Setting(50)

DEFAULT_STATE = EmptySetting("DEFAULT STATE not specified (in main settings)")

COMMANDS = Setting[list[Commands]]([
    # example
    # MyCommands
])

MESSAGE_HANDLERS = Setting[dict[tuple[Layers, States], HandlerFactory]]({
    # example
    # (Layers.BASE, MyStates.START): build_echo_handler
})

COMMAND_HANDLERS = Setting[dict[Commands, CommandHandlerFactory]]({
    # example
    # MyCommands.START: build_start_handler
})
