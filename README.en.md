# UniBot - universal messenger bot Python library

⚠️ The project is in an early stage of development. The implementation is very raw and incomplete (and can barely do anything yet). If you run into errors or difficulties, we’d really appreciate feedback ^-^

UniBot is a library for building bots that unifies working with different messenger APIs and simplifies development in large projects.

## Project Goal

Reduce the pain of working with different messenger APIs and provide a single standard for writing bots.

## Features

- Support for multiple messengers
- User State implementation
- Automatic generation of a base project structure
- Convenient and simple factory functions for Handlers (event processors)
- Asynchronous code

## Project Structure

```path
my_project
├─ src
│  ├─ handlers
│  │  ├─ commands
│  │  └─ message
│  ├─ commands.py
│  ├─ states.py
│  └─ main.py
└─ bot_orchestration
   ├─ orchestration
   └─ settings
      ├─ main.py
      └─ ...
```

The **src** folder contains the main code: your handlers, states, commands, and optionally services, repositories, etc.

In bot_orchestration, the most important part is **settings**. This is where your bot configuration lives: operating mode (telegram, vk, etc.), max number of tasks, available handlers, commands, and so on.

**bot_orchestration/orchestration** is a low-level layer for adding new platforms. Changing it may break the bot.

## State / Handler / Layers

UniBot implements a user state system (based on user_id in messages). Depending on the current State, the appropriate Handler is selected.

### Layers

There are 3 layers:

1. Global - things that must always execute, like handling cancel input.
2. Dedicated - restrictions, validation, filtering
3. Base - main handler

Important: in the Base layer there can only be one handler per state!
In Global and Dedicated layers, multiple handlers per state are allowed.

Layers are executed in strict order top to bottom: Global → Dedicated → Base. If any handler changes the state (returns `new_state` not None), the following handlers are not executed.

Do not rely on execution order inside a layer (Global, Dedicated). It is better to design handlers as order-independent — this makes the architecture cleaner, more reliable, and modular. In Global and Dedicated layers, avoid mutating system state (except for state changes), otherwise logic will become scattered and harder to test.

## About Specific Data (SD)

Important: this is not DTO. It may support lazy loading. Lazy loading exists in PictureSD (.download), DocumentSD (.download).
Therefore, passing it into Application or Domain layers is not recommended.

## Mini Guide / Example

Install the library:

```bash
pip install git+https://github.com/Taffik0/Unibot.git
```

Create a project:

```bash
python -m unibot.scripts.create_project echo_bot
```

Or use `.` to create it in the current directory.

Go to settings:
`<bot_name>/bot_orchestration/settings/main.py` and you will see something like:

```python
OPERATING_MODE = EmptySetting("OPERATING_MODE not specified (in main settings)")

MAX_TASKS: Setting[int] = Setting(50)

DEFAULT_STATE = EmptySetting("DEFAULT STATE not specified (in main settings)")

COMMANDS = Setting[list[Commands]]([
    # example
    # MyCommands
])

GLOBAL_HANDLERS = Setting[dict[States, list[HandlerFactory] | HandlerFactory]]({
    # example
    # MyStates.WRITE : build_cancel_handler
})

DEDICATED_HANDLERS = Setting[dict[States, list[HandlerFactory] | HandlerFactory]]({
    # example
    # MyStates.WRITE : build_length_limiter_handler
})

BASE_HANDLERS = Setting[dict[States, HandlerFactory]]({
    # example
    # MyStates.WRITE : build_echo_handler
})

COMMAND_HANDLERS = Setting[dict[Commands, CommandHandlerFactory]]({
    # example
    # MyCommands.START: build_start_handler
})
```

Replace `EmptySetting` fields with `Setting` and fill them in:

- OPERATING_MODE - messenger for the bot (currently only telegram is supported)
- DEFAULT_STATE - initial user state (e.g. START), expects your custom State class
- COMMANDS - commands the bot listens for
- GLOBAL_HANDLERS - handlers in Global layer
- DEDICATED_HANDLERS - handlers in Dedicated layer
- BASE_HANDLERS - handlers in Base layer
- COMMAND_HANDLERS - command handlers

Go to `src/<bot_name>/src`. In handler message/command you can create your own handlers by inheriting from Handler/CommandHandler (`unibot.handler`):

```python
from unibot.response import ResponseContainer, ResponseMessage, TextResponse
from unibot.handler import Handler, CommandHandler
from unibot.message.message import Message

class EchoHandler(Handler):
    async def handle(self, message: Message) -> ResponseContainer:
        return ResponseContainer(
            ResponseMessage.from_message(message),
            [TextResponse(f"{message.text}")]
        )

async def build_echo_handler() -> EchoHandler:
    return EchoHandler()

class WordsLimiterHandler(Handler):
    def __init__(self, max_words: int, current_state: States):
        self.max_words = max_words
        self.current_state = current_state

    async def handle(self, message: Message) -> ResponseContainer:
        count = len(message.text.split())
        if count > self.max_words:
            return ResponseContainer(
                ResponseMessage.from_message(message),
                [TextResponse(f"Over {self.max_words} words not supported!")],
                new_state=self.current_state
            )
        return ResponseContainer(ResponseMessage.from_message(message), None)


def gen_word_limiter_handler(max_words: int, current_state: States) -> HandlerFactory:
    async def build_word_limiter_handler() -> WordsLimiterHandler:
        return WordsLimiterHandler(max_words=max_words, current_state=current_state)
    return build_word_limiter_handler
```

Factories are async for API consistency; sync I/O would slow down processing.

In `states.py`, define your states:

```python
class MyStates(States):
    START = "start"
    MAIN = "main"
```

Then register them in `settings/main.py`:

```python
DEDICATED_HANDLERS = Setting[dict[States, list[HandlerFactory] | HandlerFactory]]({
    MyStates.MAIN: gen_word_limiter_handler(5, MyStates.MAIN)
})

BASE_HANDLERS = Setting[dict[States, HandlerFactory]]({
    MyStates.MAIN: build_echo_handler
})
```

Set default state:

```python
DEFAULT_STATE = Setting(MyStates.MAIN)
```

Then run the bot:

```bash
cd path/<bot_name>
python src/main.py
# or
python -m src.main
```

The bot will start and repeat your messages up to 8 words.

## Development Status

Currently only minimal Telegram support exists. Most features are not implemented yet (file sending/receiving, images, button handling are not available).

## Messenger Support

### Telegram

Install:

```bash
pip install unibot[telegram]
```

SpecificData support

| name       | status | description                 |
| ---------- | :----: | --------------------------- |
| PictureSD  |   ✅   |                             |
| FullNameSD |   ⚠️   | middle_name is always empty |

Response support

| name                 | status | description                         |
| -------------------- | :----: | ----------------------------------- |
| PictureResponse      |   ✅   |                                     |
| PictureGroupResponse |   ⚠️   | only the first caption is displayed |
