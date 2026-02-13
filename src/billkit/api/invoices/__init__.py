from collections.abc import Callable
from typing import Any, Literal

from ...models.invoices import InvoiceStatusUpdateRequest, InvoiceStatusUpdateResponse
from .._base import _BaseDocuments


class Invoices(_BaseDocuments):
    def __init__(self, requester: Callable):
        self._requester = requester

    def update_status(self, file_id: str, invoice_status: Literal["not_paid", "paid"]):
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

    def delete(self, file_id: str):
        response_data = self._requester("DELETE", f"invoices?file_id={file_id}")
        return response_data
