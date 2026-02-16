from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class _CustomTemplate(TypedDict):
    name: str
    id: str
    created_at: str


class _BuiltinTemplate(TypedDict):
    name: str


class TemplatesListResponse(BaseModel):
    default: list[_BuiltinTemplate]
    custom: list[_CustomTemplate]


class CreateCustomTemplateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    html: str = Field(..., min_length=1)


class CreateCustomTemplateResponse(BaseModel):
    id: str
    """UUID4 string"""
    name: str
    """Template name"""
    created_at: str


class DeleteCustomTemplateResponse(BaseModel):
    id: str
    """UUID4 string"""
    deleted: bool
