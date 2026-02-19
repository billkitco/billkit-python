from collections.abc import Sequence

from .._base import _BaseCreatePayload, _BaseItem  # pyright: ignore[reportPrivateUsage]


class QuoteItem(_BaseItem): ...


class QuoteCreatePayload(_BaseCreatePayload):
    quote_number: str
    items: Sequence[QuoteItem]
    quote_date: str | None = None
