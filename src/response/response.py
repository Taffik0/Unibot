from dataclasses import dataclass


@dataclass
class Response:
    pass


@dataclass
class TextResponse(Response):
    text: str
