import os
from collections.abc import Callable, Sequence
from typing import Any, get_args

from typing_extensions import override

from ...models._base import PDFResponse
from ...models.invoices import (
    InvoiceBatchResponse,
    InvoiceBatchStatusResponse,
    InvoiceByIdResponse,
    InvoiceCreatePayload,
    InvoiceDeleteResponse,
    InvoiceDocumentResponse,
    InvoiceItem,
    InvoiceSendEmailRequest,
    InvoiceSendEmailResponse,
    InvoiceStatus,
    InvoiceStatusUpdateRequest,
    InvoiceStatusUpdateResponse,
)
from .._base import _BaseDocuments  # pyright: ignore[reportPrivateUsage]


class Invoices(_BaseDocuments[InvoiceItem]):
    """API client for creating, listing, and managing invoices."""

    def __init__(self, requester: Callable[..., Any]) -> None:
        super().__init__(requester)

    @override
    def create(
        self,
        *,
        client_name: str,
        client_email: str,
        items: Sequence[InvoiceItem],
        invoice_number: str,
        due_date: str,
        invoice_date: str | None = None,
        save_to_cloud: bool = True,
        **kwargs: Any,
    ) -> PDFResponse:
        """Generate a single invoice and return its PDF.

        Args:
            client_name: Name of the client or recipient.
            client_email: Email address of the client.
            items: Line items (description, quantity, unit price, etc.).
            invoice_number: Unique identifier for the invoice.
            due_date: Due date for payment (format as required by the API).
            invoice_date: Optional issue date of the invoice. Defaults to None.
            save_to_cloud: Whether to upload the generated PDF to cloud storage.
                Defaults to True.
            **kwargs: Additional payload fields passed through to the API.

        Returns:
            PDFResponse: File-like object containing the PDF bytes; may include
                file_id if save_to_cloud is True.
        """
        payload_dict: Any = dict(
            client_name=client_name,
            client_email=client_email,
            items=[item.model_dump(mode="json", exclude_unset=True) for item in items],
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            upload_to_s3=save_to_cloud,
            due_date=due_date,
            **kwargs,
        )
        payload = InvoiceCreatePayload(**payload_dict)
        response_data: PDFResponse = self._requester(
            "POST",
            "invoices/generate",
            json=payload.model_dump(mode="json", exclude_unset=True),
        )
        return response_data

    def update_status(
        self, file_id: str, *, invoice_status: InvoiceStatus
    ) -> InvoiceStatusUpdateResponse:
        """Update the status of an existing invoice by file_id.

        Args:
            file_id: Identifier of the stored invoice document.
            invoice_status: New status (e.g. paid, sent, overdue).

        Returns:
            InvoiceStatusUpdateResponse: Confirmation of the status update.

        Raises:
            ValueError: If invoice_status is not a valid InvoiceStatus value.
        """
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
        """Delete an invoice document by file_id.

        Args:
            file_id: Identifier of the stored invoice to delete.

        Returns:
            InvoiceDeleteResponse: Confirmation of the deletion.
        """
        response_data = self._requester("DELETE", f"invoices?file_id={file_id}")
        return InvoiceDeleteResponse(**response_data)

    def send_email(
        self,
        *,
        to: Sequence[str],
        subject: str,
        body: str = "",
        from_email: str | None = None,
        file_ids: Sequence[str] | None = None,
    ) -> InvoiceSendEmailResponse:
        """Send one or more invoice PDFs by email.

        Args:
            to: List of recipient email addresses.
            subject: Email subject line.
            body: Optional email body. Defaults to empty string.
            from_email: Optional sender address. Defaults to None.
            file_ids: Optional list of invoice file_ids to attach. Defaults to None.

        Returns:
            InvoiceSendEmailResponse: Result of the send operation.
        """
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
        """Create a batch invoices job from two CSV files (invoices data + line items).

        Args:
            data_file_path: Path to the CSV with invoice-level data.
            items_file_path: Path to the CSV with line items.

        Returns:
            InvoiceBatchResponse: Job details including job_id for status polling.
        """
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
        """Get the status and results of a batch invoices job.

        Args:
            job_id: Identifier of the batch job (from create_batch_from_csv or
                create_batch_from_json).

        Returns:
            InvoiceBatchStatusResponse: Current status and any completed outputs.
        """
        data = super().get_batch_status(job_id)
        return InvoiceBatchStatusResponse.model_validate(data)

    def create_batch_from_json(
        self,
        data: dict[str, Any],
    ) -> InvoiceBatchResponse:
        """Create a batch invoices job from a JSON payload.

        Args:
            data: JSON-serializable dict with batch invoice data (structure as
                required by the API).

        Returns:
            InvoiceBatchResponse: Job details including job_id for status polling.
        """
        return InvoiceBatchResponse(
            **self._requester("POST", "batch/invoices/json", json=data)
        )

    def list(
        self, *, limit: int = 50, offset: int = 0
    ) -> Sequence[InvoiceDocumentResponse]:
        """List invoice documents with optional pagination.

        Args:
            limit: Maximum number of documents to return. Defaults to 50.
            offset: Number of documents to skip. Defaults to 0.

        Returns:
            Sequence of InvoiceDocumentResponse for each invoice.
        """
        response_data = self._requester(
            "GET", "invoices", params={"limit": limit, "offset": offset}
        )
        return [InvoiceDocumentResponse.model_validate(item) for item in response_data]

    def download_pdf(self, file_id: str) -> PDFResponse:
        """Download the PDF of the specified invoice.

        Args:
            file_id: Identifier of the stored invoice.

        Returns:
            PDFResponse: File-like object containing the PDF bytes.

        Note:
            To get document metadata (invoice_number, due_date, status, etc.)
            instead of the PDF, use client.invoices.get_document(file_id).
        """
        response_data: PDFResponse = self._requester(
            "GET", f"invoices/download?file_id={file_id}"
        )
        return response_data

    def get_document(self, file_id: str) -> InvoiceByIdResponse:
        """Get full document details of an invoice (metadata and payload, not the PDF).

        Args:
            file_id: Identifier of the stored invoice.

        Returns:
            InvoiceByIdResponse: Wrapper with file_id, invoice_number, due_date,
                status, created_at, and data (invoice payload: client_name, items,
                etc.). Use .data for the invoice fields.

        Note:
            To get the PDF file instead, use client.invoices.download_pdf(file_id).
        """
        response_data = self._requester("GET", f"invoices/by-id/{file_id}")
        return InvoiceByIdResponse(**response_data)
