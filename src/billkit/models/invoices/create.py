# from ..client import ClientDetails
from collections.abc import Sequence

from pydantic import BaseModel

from .._base import _BaseCreatePayload, _BaseItem  # pyright: ignore[reportPrivateUsage]


class InvoiceItem(_BaseItem): ...


class InvoiceCreatePayload(_BaseCreatePayload):
    invoice_number: str
    due_date: str
    items: Sequence[InvoiceItem]
    invoice_date: str | None = None


class InvoiceGetResponse(InvoiceCreatePayload): ...


class InvoiceByIdResponse(BaseModel):
    """Response for GET /invoices/by-id/{file_id}. Wraps invoice payload with file metadata."""

    file_id: str
    invoice_number: str
    due_date: str | None = None
    status: str
    created_at: str
    data: InvoiceGetResponse
