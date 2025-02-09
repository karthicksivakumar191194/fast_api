from pydantic import BaseModel
from uuid import UUID
from app.schemas.base_schema import ListResponse, CreateResponse

class WorkspaceListResponse(ListResponse):
    pass

class WorkspaceCreateRequest(BaseModel):
    tenant_id: UUID
    name: str

class WorkspaceCreateResponse(CreateResponse):
    pass