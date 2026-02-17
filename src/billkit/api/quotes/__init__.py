import os
from collections.abc import Callable
from typing import Any

from typing_extensions import override

from ...models.quotes import (
    QuoteBatchResponse,
    QuoteBatchStatusResponse,
    QuoteDeleteResponse,
    QuoteSendEmailRequest,
    QuoteSendEmailResponse,
)
from .._base import _BaseDocuments


class Quotes(_BaseDocuments):
    def __init__(self, requester: Callable) -> None:
        super().__init__(requester)

    def delete(self, file_id: str) -> QuoteDeleteResponse:
        response_data = self._requester("DELETE", f"quotes?file_id={file_id}")
        return QuoteDeleteResponse(**response_data)

    def send_email(
        self,
        *,
        to: list[str],
        subject: str,
        body: str = "",
        from_email: str | None = None,
        file_ids: list[str] | None = None,
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

    def list(self): ...
