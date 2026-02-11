from pydantic import BaseModel


class UserDetails(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: str
    updated_at: str
    default_currency: str
    business_name: str | None = None
    business_email: str | None = None
    business_address: str | None = None
    logo_url: str | None = None


class PartialUserDetails(BaseModel):
    business_name: str | None = None
    business_email: str | None = None
    business_address: str | None = None
    logo_url: str | None = None
    default_currency: str | None


class LogoUploadResponse(BaseModel):
    logo_url: str
    public_id: str
