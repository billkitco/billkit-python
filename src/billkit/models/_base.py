import os
from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from io import BytesIO
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PDFResponse(BytesIO):
    """
    BytesIO subclass used for PDF responses created by the API.

    Use as a file-like object for the PDF bytes; access `.file_id` to
    retrieve the stored file identifier when the PDF has been uploaded
    to external storage by the client.
    """

    file_id: str | None = None

    def __init__(self, initial_bytes: bytes = b"", file_id: str | None = None) -> None:
        super().__init__(initial_bytes)
        self.file_id = file_id

    def save(self, file_path: os.PathLike[str] | str) -> None:
        """
        Save the in-memory PDF bytes to a local file path.

        **Args:**
            file_path (os.PathLike[str] | str): Destination path where the PDF
                file will be written. If a file already exists at this path,
                it will be overwritten.

        **Raises:**
            OSError: If the path is invalid or the file cannot be written.

        **Usage example:**
            ```python
            pdf_response = client.invoices.create(...)
            pdf_response.save("invoice.pdf")
            ```
        """
        self.seek(0)
        with open(file_path, "wb") as f:
            f.write(self.getvalue())


class DiscountType(StrEnum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class _SendEmailRequest(BaseModel):  # pyright: ignore[reportUnusedClass]
    to: Sequence[str]
    subject: str
    body: str
    from_email: str | None
    file_ids: Sequence[str] | None


class _SendEmailResponse(BaseModel):  # pyright: ignore[reportUnusedClass]
    success: bool
    message_id: str | None
    status_code: int
    detail: str | None


class _BatchResponse(BaseModel):  # pyright: ignore[reportUnusedClass]
    job_id: str
    status: str
    webhook_url: str


class TemplateWarning(BaseModel):
    code: str
    message: str
    params: Sequence[str] | None = None
    """Union of all unused/mismatched params (kept for backwards compatibility)"""
    template_id: str | None = Field(default=None, alias="templateId")
    payload_params: Sequence[str] | None = Field(default=None, alias="payloadParams")
    """extra request fields not used by the template"""
    template_params: Sequence[str] | None = Field(default=None, alias="templateParams")
    """variables referenced in the template but not supplied in the payload"""

    model_config = {"populate_by_name": True}


class _BaseItem(BaseModel):
    description: str = Field(..., min_length=1)
    qty: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    tax: Decimal = Field(default=Decimal("0.00"), ge=0)
    discount_type: DiscountType | None = None
    discount_value: Decimal = Field(default=Decimal("0.00"), ge=0)

    model_config = ConfigDict(
        extra="allow",
        json_encoders={Decimal: str},
    )

    @model_validator(mode="after")
    def validate_discount(self) -> "_BaseItem":
        if self.discount_type is None:
            self.discount_value = Decimal("0.00")
            return self
        if self.discount_type == DiscountType.PERCENTAGE and self.discount_value > 100:
            raise ValueError("Percentage discount must be 100 or less")
        return self


class _BaseCreatePayload(BaseModel):  # pyright: ignore[reportUnusedClass]
    client_name: str
    client_email: str
    upload_to_s3: bool = True

    client_address: str | None = None
    currency_code: str = "GBP"
    style: str = "Classic Left Logo"

    reference_number: str | None = None

    from_name: str | None = None
    from_email: str | None = None
    from_address: str | None = None

    notes: str | None = None
    terms: str | None = None

    discount_type: DiscountType | None = None
    discount_value: float = 0
    """If discount_type is DiscountType.PERCENTAGE, you should use 50 for 50% instead of 0.5"""

    model_config = {"extra": "allow"}
    """**kwargs catch-all for advanced/less-common fields"""


class _BaseBatchStatusResponse(BaseModel):  # pyright: ignore[reportUnusedClass]
    job_id: str = Field(..., alias="job_id")
    status: str
    entity_type: str
    source: str
    total_count: int | None
    imported_count: int | None
    error: Any | None = None
    created_at: datetime = Field(..., alias="created_at")
    updated_at: datetime = Field(..., alias="updated_at")

    model_config = {"populate_by_name": True}


class _BaseDocumentResponse(BaseModel):  # pyright: ignore[reportUnusedClass]
    file_id: str
    created_at: str
    client_name: str
