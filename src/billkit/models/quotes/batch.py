from pydantic import BaseModel, Field

from .._base import _BaseBatchStatusResponse, _BatchResponse


class QuoteBatchResponse(_BatchResponse): ...


class QuoteBatchRecord(BaseModel):
    quote_number: str = Field(..., alias="quoteNumber")
    s3_key: str = Field(..., alias="s3Key")


class QuoteBatchStatusResponse(_BaseBatchStatusResponse):
    records: list[QuoteBatchRecord] | None
