import os
from collections.abc import Callable, Sequence
from typing import Any

from typing_extensions import override

from ...models._base import PDFResponse
from ...models.quotes import (
    Quote2InvoiceRequest,
    QuoteBatchResponse,
    QuoteBatchStatusResponse,
    QuoteByIdResponse,
    QuoteCreatePayload,
    QuoteDeleteResponse,
    QuoteDocumentResponse,
    QuoteItem,
    QuoteSendEmailRequest,
    QuoteSendEmailResponse,
)
from .._base import _BaseDocuments  # pyright: ignore[reportPrivateUsage]


class Quotes(_BaseDocuments[QuoteItem]):
    """API client for creating, listing, and managing quotes."""

    def __init__(self, requester: Callable[..., Any]) -> None:
        super().__init__(requester)

    def delete(self, file_id: str) -> QuoteDeleteResponse:
        """Delete a quote document by file_id.

        Args:
            file_id: Identifier of the stored quote to delete.

        Returns:
            QuoteDeleteResponse: Confirmation of the deletion.
        """
        response_data = self._requester("DELETE", f"quotes?file_id={file_id}")
        return QuoteDeleteResponse(**response_data)

    @override
    def create(
        self,
        *,
        client_name: str,
        client_email: str,
        items: Sequence[QuoteItem],
        quote_number: str,
        quote_date: str | None = None,
        save_to_cloud: bool = True,
        **kwargs: Any,
    ) -> PDFResponse:
        """Generate a single quote and return its PDF.

        Args:
            client_name: Name of the client or recipient.
            client_email: Email address of the client.
            items: Line items (description, quantity, unit price, etc.).
            quote_number: Unique identifier for the quote.
            quote_date: Optional date of the quote. Defaults to None.
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
            quote_number=quote_number,
            quote_date=quote_date,
            upload_to_s3=save_to_cloud,
            **kwargs,
        )
        payload = QuoteCreatePayload(**payload_dict)
        response_data: PDFResponse = self._requester(
            "POST",
            "quotes/generate",
            json=payload.model_dump(mode="json", exclude_unset=True),
        )
        return response_data

    def send_email(
        self,
        *,
        to: Sequence[str],
        subject: str,
        body: str = "",
        from_email: str | None = None,
        file_ids: Sequence[str] | None = None,
    ) -> QuoteSendEmailResponse:
        """Send one or more quote PDFs by email.

        Args:
            to: List of recipient email addresses.
            subject: Email subject line.
            body: Optional email body. Defaults to empty string.
            from_email: Optional sender address. Defaults to None.
            file_ids: Optional list of quote file_ids to attach. Defaults to None.

        Returns:
            QuoteSendEmailResponse: Result of the send operation.
        """
        payload = QuoteSendEmailRequest(
            to=to,
            subject=subject,
            body=body,
            from_email=from_email,
            file_ids=file_ids,
        )

        response_data = self._requester("POST", "email/send", json=payload.model_dump())
        return QuoteSendEmailResponse(**response_data)

    def create_batch_from_csv(
        self,
        data_file_path: os.PathLike[str],
        items_file_path: os.PathLike[str],
    ) -> QuoteBatchResponse:
        """Create a batch quotes job from two CSV files (quotes data + line items).

        Args:
            data_file_path: Path to the CSV with quote-level data.
            items_file_path: Path to the CSV with line items.

        Returns:
            QuoteBatchResponse: Job details including job_id for status polling.
        """
        data_path = os.fspath(data_file_path)
        items_path = os.fspath(items_file_path)
        with open(data_path, "rb") as quote_f, open(items_path, "rb") as items_f:
            files = {
                "quote_csv": (os.path.basename(data_path), quote_f, "text/csv"),
                "items_csv": (os.path.basename(items_path), items_f, "text/csv"),
            }
            return QuoteBatchResponse(
                **self._requester("POST", "batch/quotes/csv", files=files)
            )

    @override
    def get_batch_status(self, job_id: str) -> QuoteBatchStatusResponse:
        """Get the status and results of a batch quotes job.

        Args:
            job_id: Identifier of the batch job (from create_batch_from_csv or
                create_batch_from_json).

        Returns:
            QuoteBatchStatusResponse: Current status and any completed outputs.
        """
        data = super().get_batch_status(job_id)
        return QuoteBatchStatusResponse.model_validate(data)

    def create_batch_from_json(
        self,
        data: dict[str, Any],
    ) -> QuoteBatchResponse:
        """Create a batch quotes job from a JSON payload.

        Args:
            data: JSON-serializable dict with batch quote data (structure as
                required by the API).

        Returns:
            QuoteBatchResponse: Job details including job_id for status polling.
        """
        return QuoteBatchResponse(
            **self._requester("POST", "batch/quotes/json", json=data)
        )

    def list(
        self, *, limit: int = 50, offset: int = 0
    ) -> Sequence[QuoteDocumentResponse]:
        """List quote documents with optional pagination.

        Args:
            limit: Maximum number of documents to return. Defaults to 50.
            offset: Number of documents to skip. Defaults to 0.

        Returns:
            Sequence of QuoteDocumentResponse for each quote.
        """
        response_data = self._requester(
            "GET", "quotes", params={"limit": limit, "offset": offset}
        )
        return [QuoteDocumentResponse(**item) for item in response_data]

    def download_pdf(self, file_id: str) -> PDFResponse:
        """Download the PDF of the specified quote.

        Args:
            file_id: Identifier of the stored quote.

        Returns:
            PDFResponse: File-like object containing the PDF bytes.

        Note:
            To get document metadata (quote_number, created_at, etc.) instead of
            the PDF, use client.quotes.get_document(file_id).
        """
        response_data: PDFResponse = self._requester(
            "GET", f"quotes/download?file_id={file_id}"
        )
        return response_data

    def convert_to_invoice(
        self,
        *,
        file_id: str,
        invoice_number: str | None = None,
        save_to_cloud: bool = True,
    ) -> PDFResponse:
        """Convert an existing quote to an invoice and return the invoice PDF.

        Args:
            file_id: Identifier of the stored quote to convert.
            invoice_number: Optional invoice number for the new invoice.
                Defaults to None (API may assign one).
            save_to_cloud: Whether to upload the generated invoice PDF to cloud
                storage. Defaults to True.

        Returns:
            PDFResponse: File-like object containing the new invoice PDF bytes.
        """
        payload = Quote2InvoiceRequest(
            file_id=file_id,
            invoice_number=invoice_number,
            upload_to_s3=save_to_cloud,
        )
        return self._requester("POST", "quotes/convert", json=payload.model_dump())

    def get_document(self, file_id: str) -> QuoteByIdResponse:
        """Get full document details of a quote (metadata and payload, not the PDF).

        Args:
            file_id: Identifier of the stored quote.

        Returns:
            QuoteByIdResponse: Wrapper with file_id, quote_number, created_at, and
                data (quote payload: client_name, items, etc.). Use .data for the
                quote fields.

        Note:
            To get the PDF file instead, use client.quotes.download_pdf(file_id).
        """
        response_data = self._requester("GET", f"quotes/by-id/{file_id}")
        return QuoteByIdResponse(**response_data)
