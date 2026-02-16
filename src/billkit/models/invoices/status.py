from pydantic import BaseModel

from .types import InvoiceStatus


class InvoiceStatusUpdateRequest(BaseModel):
    file_id: str
    status: InvoiceStatus


class InvoiceStatusUpdateResponse(BaseModel):
    fileId: str
    status: str
