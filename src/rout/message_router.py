from src.rout.handler_state_register import HandlerStateRegister
from src.rout.handler_orchestrator import HandlerOrchestrator
from src.state.conversation_state_repository import ConversationStateRepository

from src.message.message import Message


class MessageRouter:
    def __init__(self, handler_state_register: HandlerStateRegister,
                 handler_orchestrator: HandlerOrchestrator,
                 conversation_state_repository: ConversationStateRepository):
        self.handler_state_register = handler_state_register
        self.handler_orchestrator = handler_orchestrator
        self.conversation_state_repository = conversation_state_repository

    async def rout(self, message: Message):
        state = await self.conversation_state_repository.get_state(message.user_id)
        handler_factory = await self.handler_state_register.get(state)
        if handler_factory:
            await self.handler_orchestrator.add_task(handler_factory, message)
