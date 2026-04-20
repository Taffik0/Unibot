# Type and utils import
from unibot.utils.setting import Setting, EmptySetting
from unibot.commands.commands import Commands
from unibot.types.command_handler_factory import CommandHandlerFactory
from unibot.types.handler_factory import HandlerFactory
from unibot.types.handler_layers import Layers
from unibot.state.state import States
# -----------------

# Your code import

# -----------------

OPERATING_MODE = EmptySetting(
    "OPERATING_MODE not specified (in main settings)")

MAX_TASKS: Setting[int] = Setting(50)

DEFAULT_STATE = EmptySetting("DEFAULT STATE not specified (in main settings)")

COMMANDS = Setting[list[Commands]]([
    # example
    # MyCommands
])

# Handlers in Global Layer
GLOBAL_HANDLERS = Setting[dict[States, list[HandlerFactory] | HandlerFactory]]({
    # example
    # MyStates.WRITE : build_cancel_handler
})

# Handlers in Dedicated Layer
DEDICATED_HANDLERS = Setting[dict[States, list[HandlerFactory] | HandlerFactory]]({
    # example
    # MyStates.WRITE : build_length_limiter_handler
})

# Handler in Base layer (max one for state)
BASE_HANDLERS = Setting[dict[States, HandlerFactory]]({
    # example
    # MyStates.WRITE : build_echo_handler
})

# Handler process command
COMMAND_HANDLERS = Setting[dict[Commands, CommandHandlerFactory]]({
    # example
    # MyCommands.START: build_start_handler
})
