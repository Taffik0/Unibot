from src.senders.sender import Sender
from src.state.conversation_state_repository import ConversationStateRepository

from src.response.response_container import ResponseContainer


class ResponseProcessor:
    def __init__(self, sender: Sender, conversation_state_repository: ConversationStateRepository):
        self.sender = sender
        self.conversation_state_repository = conversation_state_repository

    async def process(self, response_container: ResponseContainer):
        if response_container.new_state is not None:
            await self.conversation_state_repository.set_state(response_container.message.user_id, response_container.new_state)
        await self.sender.send(response_container)
