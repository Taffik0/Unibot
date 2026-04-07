from src.state.state import States


class ConversationStateRepository:
    def __init__(self, default_state: States) -> None:
        self.storage: dict[str, States] = {}
        self.default_state = default_state

    async def get_state(self, user_id: str) -> States:
        state = self.storage.get(user_id)
        if state is None:
            return self.default_state
        return state

    async def set_state(self, user_id: str, new_state: States):
        self.storage[user_id] = new_state
