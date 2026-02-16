from pydantic import BaseModel
from typing_extensions import TypedDict


class _Template(TypedDict):
    name: str


class TemplatesListResponse(BaseModel):
    default: list[_Template]
    custom: list[_Template]
