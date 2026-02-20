from pydantic import BaseModel


class Quote2InvoiceRequest(BaseModel):
    file_id: str
    """UUID4 string"""
    upload_to_s3: bool = True
    invoice_number: str | None = None
    """
    Optional invoice number.

    If invoice_number is None, the account default
    naming convention for conversions is used
    """
