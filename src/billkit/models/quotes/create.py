from collections.abc import Sequence

from pydantic import BaseModel

from .._base import _BaseCreatePayload, _BaseItem  # pyright: ignore[reportPrivateUsage]


class QuoteItem(_BaseItem): ...


class QuoteCreatePayload(_BaseCreatePayload):
    quote_number: str
    items: Sequence[QuoteItem]
    quote_date: str | None = None


class QuoteGetResponse(QuoteCreatePayload): ...


class QuoteByIdResponse(BaseModel):
    """Response for GET /quotes/by-id/{file_id}. Wraps quote payload with file metadata."""

    file_id: str
    quote_number: str
    created_at: str
    data: QuoteGetResponse
