from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class DiscountType(StrEnum):
    Percentage = "percentage"
    Fixed = "fixed"


class _SendEmailRequest(BaseModel):
    to: list[str]
    subject: str
    body: str
    from_email: str | None
    file_ids: list[str] | None


class _SendEmailResponse(BaseModel):
    success: bool
    message_id: str | None
    status_code: int
    detail: str | None


class _BatchResponse(BaseModel):
    job_id: str
    status: str
    webhook_url: str


class TemplateWarning(BaseModel):
    code: str
    message: str
    # Union of all unused/mismatched params (kept for backwards compatibility)
    params: list[str] | None = None
    template_id: str | None = Field(default=None, alias="templateId")
    # New: extra request fields not used by the template
    payload_params: list[str] | None = Field(default=None, alias="payloadParams")
    # New: variables referenced in the template but not supplied in the payload
    template_params: list[str] | None = Field(default=None, alias="templateParams")

    model_config = {"populate_by_name": True}


class _BaseItem(BaseModel):
    description: str = Field(..., min_length=1)
    qty: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    tax: Decimal = Field(default=Decimal("0.00"), ge=0)
    discount_type: DiscountType | None = None
    discount_value: Decimal = Field(default=Decimal("0.00"), ge=0)

    @model_validator(mode="after")
    def validate_discount(self) -> "_BaseItem":
        if self.discount_type is None:
            self.discount_value = Decimal("0.00")
            return self
        if self.discount_type == DiscountType.Percentage and self.discount_value > 100:
            raise ValueError("Percentage discount must be 100 or less")
        return self


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


class _BaseBatchStatusResponse(BaseModel):
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


class _BaseDocumentResponse(BaseModel):
    file_id: str
    created_at: str
    client_name: str
