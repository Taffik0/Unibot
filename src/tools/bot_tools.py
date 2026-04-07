from src.response.response_processor import ResponseProcessor
from src.response.response_container import ResponseContainer


class BotTools:
    def __init__(self, resp_processor: ResponseProcessor):
        self.resp_processor = resp_processor

    async def send_response(self, resp: ResponseContainer):
        await self.resp_processor.process(resp)
