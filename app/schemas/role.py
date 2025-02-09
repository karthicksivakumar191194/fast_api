from pydantic import BaseModel
from uuid import UUID
from app.schemas.base_schema import CreateResponse

class RoleCreateRequest(BaseModel):
    tenant_id: UUID
    name: str

class RoleCreateResponse(CreateResponse):
    pass