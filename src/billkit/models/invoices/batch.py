from pydantic import BaseModel, Field

from .._base import _BaseBatchStatusResponse, _CSVBatchResponse


class InvoiceCSVBatchResponse(_CSVBatchResponse): ...


class InvoiceBatchRecord(BaseModel):
    invoice_number: str = Field(..., alias="invoiceNumber")
    s3_key: str = Field(..., alias="s3Key")


class InvoiceBatchStatusResponse(_BaseBatchStatusResponse):
    records: list[InvoiceBatchRecord]
