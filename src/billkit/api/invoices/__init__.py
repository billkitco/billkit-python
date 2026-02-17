import os
from collections.abc import Callable
from typing import Any, List, get_args

from typing_extensions import override

from ...models.invoices import (
    InvoiceBatchResponse,
    InvoiceBatchStatusResponse,
    InvoiceDeleteResponse,
    InvoiceDocumentResponse,
    InvoiceSendEmailRequest,
    InvoiceSendEmailResponse,
    InvoiceStatus,
    InvoiceStatusUpdateRequest,
    InvoiceStatusUpdateResponse,
)
from .._base import _BaseDocuments


class Invoices(_BaseDocuments):
    def __init__(self, requester: Callable) -> None:
        super().__init__(requester)

    def update_status(
        self, file_id: str, *, invoice_status: InvoiceStatus
    ) -> InvoiceStatusUpdateResponse:
        if invoice_status not in get_args(InvoiceStatus):
            raise ValueError(f"invoice_status must be either {get_args(InvoiceStatus)}")

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
        *,
        to: list[str],
        subject: str,
        body: str = "",
        from_email: str | None = None,
        file_ids: list[str] | None = None,
    ) -> InvoiceSendEmailResponse:
        payload = InvoiceSendEmailRequest(
            to=to,
            subject=subject,
            body=body,
            from_email=from_email,
            file_ids=file_ids,
        )

        response_data = self._requester("POST", "email/send", json=payload.model_dump())
        return InvoiceSendEmailResponse(**response_data)

    def create_batch_from_csv(
        self,
        data_file_path: os.PathLike[str],
        items_file_path: os.PathLike[str],
    ) -> InvoiceBatchResponse:
        """Create a batch invoices job from two CSV files (invoices data + line items)."""
        data_path = os.fspath(data_file_path)
        items_path = os.fspath(items_file_path)
        with open(data_path, "rb") as invoice_f, open(items_path, "rb") as items_f:
            files = {
                "invoice_csv": (os.path.basename(data_path), invoice_f, "text/csv"),
                "items_csv": (os.path.basename(items_path), items_f, "text/csv"),
            }
            return InvoiceBatchResponse(
                **self._requester("POST", "batch/invoices/csv", files=files)
            )

    @override
    def get_batch_status(self, job_id: str) -> InvoiceBatchStatusResponse:
        data = super().get_batch_status(job_id)
        return InvoiceBatchStatusResponse.model_validate(data)

    def create_batch_from_json(
        self,
        data: dict[str, Any],
    ) -> InvoiceBatchResponse:
        return InvoiceBatchResponse(
            **self._requester("POST", "batch/invoices/json", json=data)
        )

    def list(
        self, *, limit: int = 50, offset: int = 0
    ) -> List[InvoiceDocumentResponse]:
        response_data = self._requester(
            "GET", "invoices", params={"limit": limit, "offset": offset}
        )
        return [InvoiceDocumentResponse.model_validate(item) for item in response_data]
