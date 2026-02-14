from pydantic import BaseModel


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


class _CSVBatchResponse(BaseModel):
    job_id: str
    status: str
    webhook_url: str
