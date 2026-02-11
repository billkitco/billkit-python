from datetime import datetime
from pydantic import BaseModel


class _BaseHeader(BaseModel):
    client_name: str
    client_email: str
    client_address: str
    invoice_number: str
    reference_number: str
    po_number: str
    invoice_date: str
    due_date: datetime
    currency_code: str | None = None
    currency_symbol: str | None = None
    invoice_type: str | None = None


class QuoteHeader(_BaseHeader): ...


class InvoiceHeader(_BaseHeader): ...
