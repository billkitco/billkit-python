import os
from collections.abc import Callable, Sequence
from typing import Any

from typing_extensions import override

from ...models._base import PDFResponse
from ...models.quotes import (
    QuoteBatchResponse,
    QuoteBatchStatusResponse,
    QuoteCreatePayload,
    QuoteDeleteResponse,
    QuoteDocumentResponse,
    QuoteItem,
    QuoteSendEmailRequest,
    QuoteSendEmailResponse,
)
from .._base import _BaseDocuments  # pyright: ignore[reportPrivateUsage]


class Quotes(_BaseDocuments[QuoteItem]):
    def __init__(self, requester: Callable[..., Any]) -> None:
        super().__init__(requester)

    def delete(self, file_id: str) -> QuoteDeleteResponse:
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
        """Create a batch quotes job from two CSV files (quotes data + line items)."""
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
        data = super().get_batch_status(job_id)
        return QuoteBatchStatusResponse.model_validate(data)

    def create_batch_from_json(
        self,
        data: dict[str, Any],
    ) -> QuoteBatchResponse:
        return QuoteBatchResponse(
            **self._requester("POST", "batch/quotes/json", json=data)
        )

    def list(
        self, *, limit: int = 50, offset: int = 0
    ) -> Sequence[QuoteDocumentResponse]:
        response_data = self._requester(
            "GET", "quotes", params={"limit": limit, "offset": offset}
        )
        return [QuoteDocumentResponse(**item) for item in response_data]

    def download_pdf(self, file_id: str) -> PDFResponse:
        response_data = self._requester("GET", f"quotes/download?file_id={file_id}")
        return response_data

    def convert_to_invoice(self) -> PDFResponse:
        raise NotImplementedError("convert_to_invoice is not implemented")
