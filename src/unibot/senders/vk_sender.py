import random

from unibot.senders.sender import Sender
from unibot.response.response_container import ResponseContainer
from aiovk.api import API
from aiovk import TokenSession, API

from unibot.response.response import TextResponse


class VKSender(Sender):
    def __init__(self, session: TokenSession):
        self.session = session
        self.api = API(session)

    async def send(self, response_container: ResponseContainer):
        if response_container.responses is None:
            return
        user_id = int(response_container.message.user_id)
        text = ""
        for rs in response_container.responses:
            if isinstance(rs, TextResponse):
                text += rs.text
        if not text:
            text = " "

        await self.api.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(1, 1_000_000)
        )
