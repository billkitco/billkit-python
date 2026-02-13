from pydantic import BaseModel


class InvoiceStatusUpdateRequest(BaseModel):
    file_id: str
    status: str


class InvoiceStatusUpdateResponse(BaseModel):
    fileId: str
    status: str
