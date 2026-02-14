from collections.abc import Callable
from typing import Any, Literal

from ...models.invoices import (
    InvoiceDeleteResponse,
    InvoiceSendEmailRequest,
    InvoiceStatusUpdateRequest,
    InvoiceStatusUpdateResponse,
    SendEmailResponse,
)
from .._base import _BaseDocuments


class Invoices(_BaseDocuments):
    def __init__(self, requester: Callable) -> None:
        super().__init__(requester)

    def update_status(
        self, file_id: str, invoice_status: Literal["not_paid", "paid"]
    ) -> InvoiceStatusUpdateResponse:
        if invoice_status not in ("not_paid", "paid"):
            raise ValueError("invoice_status must be either 'not_paid' or 'paid'")

        payload: InvoiceStatusUpdateRequest = InvoiceStatusUpdateRequest(
            file_id=file_id,
            status=invoice_status,
        )

        request_data: dict[str, Any] = self._requester(
            "PATCH", "invoices/status", json=payload.model_dump()
        )
        return InvoiceStatusUpdateResponse(**request_data)

    def delete(self, file_id: str) -> InvoiceDeleteResponse:
        response_data = self._requester("DELETE", f"invoices?file_id={file_id}")
        return InvoiceDeleteResponse(**response_data)

    def send_email(
        self,
        to: list[str],
        subject: str,
        body: str = "",
        from_email: str | None = None,
        file_ids: list[str] | None = None,
    ) -> SendEmailResponse:
        payload = InvoiceSendEmailRequest(
            to=to,
            subject=subject,
            body=body,
            from_email=from_email,
            file_ids=file_ids,
        )

        response_data = self._requester("POST", "email/send", json=payload.model_dump())
        return SendEmailResponse(**response_data)
