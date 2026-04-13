# UniBot - universal messenger bot python library

⚠️ Проект находиться в начальной разработке, реализация очень сыра и недоработана(и почти ничего не умеет). Если у вас возникнут ошибки и трудности, будем очень рады обратной связи ^-^

UniBot - библиотека для создания ботов, которая унифицирует работу с API разных мессенджеров и упрощает архитектуру проектов

## Цель проекта

Уменьшить боль от работы с разными API мессенджеров и дать единый стандарт для написания ботов.

## Особенности

- Поддержка нескольких мессенджеров
- Реализация State пользователей
- Автоматическое создание базовой структуры проекта
- Удобные и простые функции-фабрики Handler'ов (обработчиков событий)
- Асинхронный код

## Структура проекты

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

В **src** находиться основной код: ваши handlers, состояния, команды, если есть сервисы, репозитории и т.п.

В bot_orchestration в основном интересна - **settings**, тут настройки вашего бота, какой режим работы (telegram, vk и т.п.), максимальное количество task, какие есть handler, команды, и т.п.

В **bot_orchestration/orchestration** находиться методы оркестрации, **вам не стоит тут что-то менять**, если вы не тестируете свои listeners и senders.

## Состояние разработки

На данный момент минимально поддерживается telegram, но большинство функций не реализовано (получение отправка файлов, изображений и т.п., не возможна работа с кнопками).

## State / Handler / Layers

В unibot осуществлена система состояния пользователей (по user_id в message), в зависимости от текущего State будет выбираться нужный Handler.

### Layers

существуют 3 слоя:

1. Global - ограничения, валидация, cancel
2. Dedicated - фичи для особых случаев
3. Base - основной обработчик

Важно: На одном слое может быть только один обработчик на состояние.
Во время обработки сообщения обработчики вызываются по порядку слоев (Global -> Dedicated -> Base). Если в одном из слое в ответе Handler сменит состояние (в ResponseContainer new_state будет не None), то следующие слои не будут вызваны.
Это может быть удобно, так как можно переиспользовать логику обработчиков, допустим создать CancelHandler который если получает в сообщении "forward" отменяет обработку ввода и изменяет state (на предыдущий или другой), или таким способом можно сделать универсальный ограничитель длинные ввода, который не даст ввести более n символов.

## Мини гайд/пример

Установите библиотеку `pip install git+<ссылка на github, пока нет>`
Создайте проект `python -m unibot.scripts.create_project echo_bot` или укажите `.`, что бы создать в текущей директории.

Зайдите в настройки `<bot_name>/bot_orchestration/settings` в main.py вы увидите, что-то подобное:

```python
OPERATING_MODE = EmptySetting("OPERATING_MOD not specified (in main settings)")

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
```

Замените поля с EmptySetting на Setting и заполните поля
OPERATING_MODE - мессенджер для которого бот (сейчас есть telegram)
DEFAULT_STATE - базовое состояние пользователя, при первом сообщении (например START), ждет ваш кастомный класс от State.
COMMANDS - команды которые ждет бот
MESSAGE_HANDLERS - обработчики сообщений
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

# Также фабрика может использовать yield (как async context manager, но без декоратора), оны будет закрыта, когда Handler перестанет использоваться (удобно для session и connection, которые нужно закрывать).
```

В states.py создайте, что-то похожее на -

```python
class MyStates(States):
    START = "start"
```

далее зарегистрируйте это в settings/main.py

```python
MESSAGE_HANDLERS = Setting[dict[tuple[Layers, States], HandlerFactory]]({
    (Layers.BASE, MyStates.START): gen_echo_handler,
})
```

в консоли перейдите в папку проекта `path/<bot_name>` и запусти main.py в src `python src/main.py` или `python -m src.main`, после этого бот будет запущен.
