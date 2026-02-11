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
    id: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    business_name: str | None = None
    business_email: str | None = None
    business_address: str | None = None
    logo_url: str | None = None
    default_currency: str | None
