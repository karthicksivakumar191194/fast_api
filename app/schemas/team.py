from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from fastapi import UploadFile
from app.schemas.base_schema import CreateResponse

class TeamCreateRequest(BaseModel):
    tenant_id: UUID
    workspace_id: UUID
    name: str
    description: Optional[str] = None
    image: Optional[UploadFile] = None
    name: str

class TeamCreateResponse(CreateResponse):
    pass