from pydantic import model_validator
from typing_extensions import get_args

from .._base import _BaseDocumentResponse  # pyright: ignore[reportPrivateUsage]
from .types import InvoiceStatus


class InvoiceDocumentResponse(_BaseDocumentResponse):
    invoice_number: str
    due_date: str
    status: str

    @model_validator(mode="after")
    def validate_status(self) -> "InvoiceDocumentResponse":
        if self.status not in get_args(InvoiceStatus):
            raise ValueError(
                f"InvoiceDocumentResponse.status should be in {get_args(InvoiceStatus)}"
            )
        return self
