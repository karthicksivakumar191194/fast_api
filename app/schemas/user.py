from pydantic import BaseModel
from uuid import UUID
from app.schemas.base_schema import CreateResponse

class InviteUserRequest(BaseModel):
    tenant_id: UUID
    workspace_id: UUID

class InviteUserResponse(CreateResponse):
    pass