# UniBot - universal messenger bot python library

⚠️ Проект находиться в начальной стадии разработки, реализация очень сыра и недоработана(и почти ничего не умеет). Если у вас возникнут ошибки и трудности, будем очень рады обратной связи ^-^

UniBot - библиотека для создания ботов, которая унифицирует работу с API разных мессенджеров и упрощает архитектуру проектов

## Цель проекта

Уменьшить боль от работы с разными API мессенджеров и дать единый стандарт для написания ботов.

## Особенности

- Поддержка нескольких мессенджеров
- Реализация State пользователей
- Автоматическое создание базовой структуры проекта
- Удобные и простые функции-фабрики Handler'ов (обработчиков событий)
- Асинхронный код

## Структура проекта

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

В **src** находится основной код: ваши handlers, состояния, команды, если есть сервисы, репозитории и т.п.

В bot_orchestration в основном интересна - **settings**, тут настройки вашего бота, какой режим работы (telegram, vk и т.п.), максимальное количество task, какие есть handler, команды, и т.п.

**bot_orchestration/orchestration** - это low-level слой для добавления новых платформ. При изменение можно сломать работу бота.

## State / Handler / Layers

В unibot осуществлена система состояния пользователей (по user_id в message), в зависимости от текущего State будет выбираться нужный Handler.

### Layers

существуют 2 слоя:

1. Global - то что должно выполниться в любом случае, как переход при вводе cancel.
2. Dedicated - ограничения, валидация, фильтрация
3. Base - основной обработчик

Важно - в слое Base может быть только один обработчик на состояние!
В Global и Dedicated на одно состояние может быть несколько обработчиков.

Слои будут вызываться в строгом порядке сверху вниз Global -> Dedicated -> Base, если один из обработчиков сменит состояние (new_state в return не None), то следующие обработчики не вызовутся.

Не стоит рассчитывать на порядок выполнения в одном слое (Global, Dedicated),лучше делать их не зависимыми от порядка - это делает архитектуру более чистой, надежной и модульной. В Global, Dedicated не стоит мутировать систему (за исключением state), так как это будет размазывать основную логику по множеству обработчиков и это будет сложно тестировать.

## Про Specific Data (SD)

Важно - Это не DTO, он может иметь lazy load (ленивую загрузку). Lazy load есть в PictureSD (.download), DocumentSD (.download).
Поэтому передавать его в Application или Domain слой не рекомендуется.

## Мини гайд/пример

Установите библиотеку `pip install git+https://github.com/Taffik0/Unibot.git`
Создайте проект `python -m unibot.scripts.create_project echo_bot` или укажите `.`, что бы создать в текущей директории.

Зайдите в настройки `<bot_name>/bot_orchestration/settings` в main.py вы увидите, что-то подобное:

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

COMMAND_HANDLERS = Setting[dict[Commands, CommandHandlerFactory]]({
    # example
    # MyCommands.START: build_start_handler
})
```

Замените поля с EmptySetting на Setting и заполните поля
OPERATING_MODE - мессенджер для которого бот (сейчас есть telegram)
DEFAULT_STATE - базовое состояние пользователя, при первом сообщении (например START), ждет ваш кастомный класс от State.
COMMANDS - команды которые ждет бот
GLOBAL_HANDLERS - обработчики в Global layer
DEDICATED_HANDLERS - обработчики в Dedicated layer
BASE_HANDLERS - обработчики в Base layer
COMMAND_HANDLERS - обработчики команд

Зайдите в src `<bot_name>/src` в handler message/command вы можете создавать своих обработчиков наследуя их соответственно от Handler/CommandHandler (из `unibot.handler`)

```python
from unibot.response import ResponseContainer, ResponseMessage, TextResponse
from unibot.handler import Handler, CommandHandler
from unibot.message.message import Message

class EchoHandler(Handler):
    async def handle(self, message: Message) -> ResponseContainer:
        return ResponseContainer(ResponseMessage.from_message(message),
                                 [TextResponse(f"{message.text}")])

async def build_echo_handler() -> EchoHandler: # фабрика обработчика
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
                [TextResponse(f"Over {self.max_words} words not support!")],
                new_state=self.current_state)
        return ResponseContainer(ResponseMessage.from_message(message), None)


def gen_word_limiter_handler(max_words: int, current_state: States) -> HandlerFactory: # получение фабрики с заготовленными параметрами
    async def build_word_limiter_handler() -> WordsLimiterHandler:
        return WordsLimiterHandler(max_words=max_words, current_state=current_state)
    return build_word_limiter_handler

# Также фабрика может использовать yield (как async context manager, но без декоратора), она будет закрыта, когда Handler перестанет использоваться (удобно для session и connection, которые нужно закрывать).
```

Вве фабрики - async для единобрачия API, sync io затормозит процесс обработки.

В states.py опишите ваши состояния, это может выглядеть так -

```python
class MyStates(States):
    START = "start"
    MAIN = "main"
```

далее зарегистрируйте это в settings/main.py

```python
# Handlers in Dedicated Layer
DEDICATED_HANDLERS = Setting[dict[States, list[HandlerFactory] | HandlerFactory]]({
    MyStates.MAIN: gen_word_limiter_handler(5, MyStates.MAIN)
})

# Handler in Base layer (max one for state)
BASE_HANDLERS = Setting[dict[States, HandlerFactory]]({
    MyStates.MAIN: build_echo_handler
})
```

Задайте базовое состояние

```python
DEFAULT_STATE = Setting(MyStates.MAIN)
```

в консоли перейдите в папку проекта `path/<bot_name>` и запусти main.py в src `python src/main.py` или `python -m src.main`, после этого бот будет запущен.

Бот будет повторять ваши сообщения длинной не более 8 слов.

## Состояние разработки

На данный момент минимально поддерживается telegram, но большинство функций не реализовано (получение отправка файлов, изображений и т.п., не возможна работа с кнопками).

## Messengers Support

### Telegram

install unibot[telegram] - `pip install unibot[telegram]`

SpecificData support

| name       | status | des                       |
| ---------- | :----: | ------------------------- |
| PicturePC  |   ✅   |                           |
| FullNamePC |   ⚠️   | middle_name всегда пустой |

Response support

| name                 | status | des                              |
| -------------------- | :----: | -------------------------------- |
| PictureResponse      |   ✅   |                                  |
| PictureGroupResponse |   ⚠️   | отображается только 1'ый caption |
