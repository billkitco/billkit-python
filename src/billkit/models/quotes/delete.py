from pydantic import BaseModel


class QuoteDeleteResponse(BaseModel):
    deleted: bool
    fileId: str
