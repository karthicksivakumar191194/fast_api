from pydantic import BaseModel, HttpUrl
from typing import Optional
from app.schemas.base_schema import CreateResponse, UpdateResponse

class OnboardRequest(BaseModel):
    company_name: str
    company_website: Optional[HttpUrl] = None
    company_size: str
    company_location: str
    industry_type: str
    owner_first_name: str
    owner_last_name: Optional[str] = None
    owner_email: str
    owner_mobile_no: Optional[str] = None

class OnboardResponse(CreateResponse):
    pass

class OnboardResendEmailRequest(BaseModel):
    tenant_id: str

class OnboardResendEmailResponse(UpdateResponse):
    pass