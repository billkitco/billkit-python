from pydantic import BaseModel, Field
from typing_extensions import Self, TypedDict


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

    def validate_html(self) -> Self:
        """Optional html validation"""
        MAX_HTML_SIZE = 500_000
        html = self.html

        if len(html) > MAX_HTML_SIZE:
            raise ValueError("HTML too large (>500KB)")

        stripped = html.lstrip().lower()

        if not stripped.startswith("<!doctype html"):
            raise ValueError("HTML must start with <!DOCTYPE html>")

        # very cheap structural sanity checks
        if "<html" not in stripped or "</html>" not in stripped:
            raise ValueError("Missing <html> root element")

        # lightweight Jinja balance check
        if stripped.count("{{") != stripped.count("}}"):
            raise ValueError("Unbalanced {{ }} template tags")

        if stripped.count("{%") != stripped.count("%}"):
            raise ValueError("Unbalanced {% %} template tags")

        return self


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
