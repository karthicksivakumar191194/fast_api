from uuid import UUID
from pydantic import BaseModel
from app.schemas.base_schema import CreateResponse, UpdateResponse

# Tenant
class OnboardRequest(BaseModel):
    company_name: str
    owner_name: str
    owner_email: str
    owner_password: str

class OnboardResponse(CreateResponse):
    pass

class ValidateTenantOTPRequest(BaseModel):
    tenant_id: UUID
    otp: str

class ValidateTenantOTPResponse(BaseModel):
    pass

class ResendOnboardOTPRequest(BaseModel):
    tenant_id: UUID

class ResendOnboardOTPResponse(BaseModel):
    pass

class CompleteTenantSetupRequest(BaseModel):
    company_name: str
    company_size: str
    company_location: str
    industry_type: str
    currently_manage: str
    solutions_interested: str
    workspace_name: str

class CompleteTenantSetupResponse(UpdateResponse):
    pass

# Admin
class OnboardOfflineRequest(BaseModel):
    company_name: str
    owner_name: str
    owner_email: str

class OnboardOfflineResponse(CreateResponse):
    pass