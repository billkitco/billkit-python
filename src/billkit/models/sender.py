from pydantic import BaseModel

class SenderDetails(BaseModel):
    """
    Sender (your business) details for invoices/quotes.

    All fields are optional and default to your account settings if omitted.
    If no account defaults exist, invoices will lack sender information.
    Explicitly setting fields is recommended for reliability.
    """
    from_name: str | None = None
    from_email: str | None = None
    from_address: str | None = None
