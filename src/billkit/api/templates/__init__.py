from collections.abc import Callable

from ...models.templates import (
    CreateCustomTemplateRequest,
    CreateCustomTemplateResponse,
    TemplatesListResponse,
)


class Templates:
    def __init__(self, requester: Callable) -> None:
        self._requester = requester

    def get_templates(self) -> TemplatesListResponse:
        """
        Returns all template names including custom html templates.
        These are to be used in create and batch create payloads in the invoice_style/quote_style fields.
        """
        return TemplatesListResponse(**self._requester("GET", "templates/all"))

    def create(self, template_name: str, *, html: str) -> CreateCustomTemplateResponse:
        """
        Create a custom template with HTML.
        """
        payload = CreateCustomTemplateRequest(name=template_name, html=html)
        response_data = self._requester("POST", "templates", json=payload.model_dump())
        return CreateCustomTemplateResponse(**response_data)
