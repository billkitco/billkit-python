from pydantic import BaseModel


class InvoiceDeleteResponse(BaseModel):
    deleted: bool
    fileId: str
