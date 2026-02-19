# from ..client import ClientDetails
from .._base import _BaseCreatePayload, _BaseItem


class InvoiceItem(_BaseItem): ...


class InvoiceCreatePayload(_BaseCreatePayload):
    invoice_number: str
    due_date: str
    items: list[InvoiceItem]
    invoice_date: str | None = None
