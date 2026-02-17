from pydantic import BaseModel, Field

from .._base import TemplateWarning, _BaseBatchStatusResponse, _BatchResponse


class InvoiceBatchResponse(_BatchResponse): ...


class InvoiceBatchRecord(BaseModel):
    invoice_number: str = Field(..., alias="invoiceNumber")
    s3_key: str = Field(..., alias="s3Key")
    warnings: list[TemplateWarning] | None = None


class InvoiceBatchStatusResponse(_BaseBatchStatusResponse):
    records: list[InvoiceBatchRecord] | None
