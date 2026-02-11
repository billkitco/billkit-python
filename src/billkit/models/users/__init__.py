from pydantic import BaseModel

class UserDetails(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    business_name: str
    business_email: str
    business_address: str
    logo_url: str
    default_currency: str
    created_at: str
    updated_at: str
