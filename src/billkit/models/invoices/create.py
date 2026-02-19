# from ..client import ClientDetails
from collections.abc import Sequence

from .._base import _BaseCreatePayload, _BaseItem  # pyright: ignore[reportPrivateUsage]


class InvoiceItem(_BaseItem): ...


class InvoiceCreatePayload(_BaseCreatePayload):
    invoice_number: str
    due_date: str
    items: Sequence[InvoiceItem]
    invoice_date: str | None = None
