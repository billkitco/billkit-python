from collections.abc import Callable
from typing import Any

from ...models.templates import (
    CreateCustomTemplateRequest,
    CreateCustomTemplateResponse,
    DeleteCustomTemplateResponse,
    TemplatesListResponse,
    UpdateCustomTemplateRequest,
    UpdateCustomTemplateResponse,
)


class Templates:
    def __init__(self, requester: Callable[..., dict[str, Any]]) -> None:
        self._requester = requester

    def get_templates(self) -> TemplatesListResponse:
        """
        Returns all template names including custom html templates.
        These are to be used in create and batch create payloads in the invoice_style/quote_style fields.
        """
        return TemplatesListResponse(**self._requester("GET", "templates/all"))

    def create(
        self, template_name: str, *, html: str, validate: bool = True
    ) -> CreateCustomTemplateResponse:
        """
        Create a custom template with HTML.
        """
        payload = CreateCustomTemplateRequest(name=template_name, html=html)

        if validate:
            payload.validate_html(html)

        response_data = self._requester("POST", "templates", json=payload.model_dump())
        return CreateCustomTemplateResponse(**response_data)

    def update(
        self,
        template_id: str,
        *,
        template_name: str | None = None,
        html: str | None = None,
        validate: bool = True,
    ) -> UpdateCustomTemplateResponse:
        payload = UpdateCustomTemplateRequest(name=template_name, html=html)

        if validate:
            payload.validate_html(html)

        response_data = self._requester(
            "PATCH", f"templates/{template_id}", json=payload.model_dump()
        )
        return UpdateCustomTemplateResponse(**response_data)

    def delete(self, template_id: str) -> DeleteCustomTemplateResponse:
        """
        Delete a custom template by ID.

        **Args:**
            template_id (str): UUID4 string identifier of the custom template to delete.

        **Template IDs source:**
            Retrieve available `custom` template IDs via `Templates.get_templates()` which returns
            `TemplatesListResponse`. Each item in `response.custom` has an `id` field:

            ```python
            templates = templates_service.get_templates()
            custom_ids = [t["id"] for t in templates.custom]
            ```

            Example custom template:
            ```python
            {
                "name": "My Custom Template",
                "id": "550e8400-e29b-41d4-a716-446655440001",  # UUID4 str
                "created_at": "2026-02-16T18:30:00Z"
            }
            ```

        **Raises:**
            ValueError: If `template_id` is invalid or template not found.
            PermissionError: If user lacks permission to delete this template.

        **Returns:**
            dict: Success confirmation, e.g. `{"message": "Template deleted", "id": template_id}`
        """
        response_data = self._requester("DELETE", f"templates/{template_id}")
        return DeleteCustomTemplateResponse(**response_data)
