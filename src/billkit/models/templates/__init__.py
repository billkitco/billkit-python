from pydantic import BaseModel, Field, model_validator, field_validator
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


class _BaseTemplateRequest(BaseModel):
    @field_validator("html")
    @classmethod
    def validate_html(cls, v: str | None) -> str | None:
        """Validates HTML content: size, structure, Jinja balance, and required template vars."""
        if v is None:
            return v

        MAX_HTML_SIZE = 500_000

        if len(v) > MAX_HTML_SIZE:
            raise ValueError("HTML too large (>500KB)")

        stripped = v.lstrip().lower()

        if not stripped.startswith("<!doctype html"):
            raise ValueError("HTML must start with <!DOCTYPE html>")

        if "<html" not in stripped or "</html>" not in stripped:
            raise ValueError("Missing <html> root element")

        if stripped.count("{{") != stripped.count("}}"):
            raise ValueError("Unbalanced {{ }} template tags")

        if stripped.count("{%") != stripped.count("%}"):
            raise ValueError("Unbalanced {% %} template tags")

        REQUIRED_TEMPLATE_VARS = (
            "client_name",
            "client_email",
            "items",
            "invoice_number",
            "due_date",
            "quote_number",
        )
        for name in REQUIRED_TEMPLATE_VARS:
            if name not in v:
                raise ValueError(
                    f"Template must include Jinja2 variable for invoice and quote support: {name!r}. "
                    "Required: client_name, client_email, items, invoice_number, due_date, quote_number."
                )

        return v


class CreateCustomTemplateRequest(_BaseTemplateRequest):
    name: str = Field(..., min_length=1, max_length=200)
    html: str = Field(..., min_length=1)


class UpdateCustomTemplateRequest(_BaseTemplateRequest):
    """Update name and/or HTML; at least one field must be provided."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    html: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "UpdateCustomTemplateRequest":
        if self.name is None and self.html is None:
            raise ValueError("At least one of name or html must be provided")
        return self


class UpdateCustomTemplateResponse(BaseModel):
    id: str
    """UUID4 string"""
    name: str
    html: str


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
