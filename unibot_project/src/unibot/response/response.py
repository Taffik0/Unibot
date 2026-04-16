from dataclasses import dataclass


@dataclass
class Response:
    pass


@dataclass
class TextResponse(Response):
    text: str


@dataclass
class PictureResponse(Response):
    image_bytes: bytes
    file_name: str
    caption: str | None = None


@dataclass
class PictureGroupResponse(Response):
    pictures: list[PictureResponse]
