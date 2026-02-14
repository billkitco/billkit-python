from pydantic import BaseModel


class SendEmailRequest(BaseModel):
    to: list[str]
    subject: str
    body: str
    from_email: str | None
    file_ids: list[str] | None


class SendEmailResponse(BaseModel):
    success: bool
    message_id: str | None
    status_code: int
    detail: str | None
