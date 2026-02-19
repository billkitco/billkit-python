from collections.abc import Sequence

from pydantic import BaseModel, Field

from .._base import (
    TemplateWarning,
    _BaseBatchStatusResponse,  # pyright: ignore[reportPrivateUsage]
    _BatchResponse,  # pyright: ignore[reportPrivateUsage]
)


class QuoteBatchResponse(_BatchResponse): ...


class QuoteBatchRecord(BaseModel):
    quote_number: str = Field(..., alias="quoteNumber")
    s3_key: str = Field(..., alias="s3Key")
    warnings: Sequence[TemplateWarning] | None = None


class QuoteBatchStatusResponse(_BaseBatchStatusResponse):
    records: Sequence[QuoteBatchRecord] | None
