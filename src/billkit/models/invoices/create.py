from datetime import datetime

from pydantic import BaseModel

# from ..client import ClientDetails
from ..enums import InvoiceStyle
from ..items import DiscountType, ItemsBase
from ..sender import SenderDetails


class InvoiceItem(ItemsBase): ...


class InvoiceCreate(BaseModel):
    """
    Schema for creating a new invoice.

    Defines all required and optional fields for an invoice, including client and sender
    information, line items, dates, styling, and monetary details such as currency
    and discount.

    Attributes:
        client_name: Full name of the client.
        client_email: Email address of the client.
        invoice_number: Unique identifier of the invoice.
        due_date: Deadline by which the invoice must be paid.
        item: List of line-item details for the invoice.

        from_name: Name of the sender / issuing entity.
        from_email: Email of the sender / issuing entity.
        from_address: Physical or mailing address of the sender.

        client_address: Optional physical or mailing address of the client.
        reference_number: Optional external invoice or account reference.
        po_number: Optional purchase order number.
        _save_client: Whether to persist client details for reuse (internal flag).
        invoice_date: Optional date when the invoice is issued; defaults to now.
        style: Layout style for the rendered invoice (e.g., logo position etc.).
        logo_url: Optional URL to the logo image to display on the invoice.
        currency_code: ISO currency code (e.g., 'GBP', 'USD').
        currency_symbol: Display symbol for the currency (e.g., '£', '$').

        notes: Optional notes included on the invoice.
        terms: Optional terms and conditions text.
        discount_types: Type of discount applied (e.g., percentage vs fixed).
        discount_value: Numeric value of the discount (default 0.0).
    """

    # client_details: ClientDetails
    invoice_number: str
    due_date: datetime
    items: list[InvoiceItem]

    sender_details: SenderDetails | None = None

    reference_number: str | None = None
    po_number: str | None = None
    invoice_date: datetime | None = None
    style: InvoiceStyle = InvoiceStyle.ClassicLeftLogo
    logo_url: str | None = None
    """
    Optional URL of a logo image to display on this invoice.
    If omitted or None, the invoice will fall back to the logo saved in the client's account.
    """
    currency_code: str | None = None
    currency_symbol: str | None = None

    notes: str | None = None
    terms: str | None = None
    discount_types: DiscountType | None = None
    """
    Document level discount. This applies the discount to all items before tax
    """
    discount_value: float = 0.0
    """
    Document level discount. This applies the discount to all items before tax
    """
    _save_client: bool = False
    """
    Whether to add client information to gui for autofill function. Largely irrelevant for programmatic access
    """
