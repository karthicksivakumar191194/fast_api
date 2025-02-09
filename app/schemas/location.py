from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.schemas.base_schema import (ListResponse, DetailResponse, CreateResponse, UpdateResponse,
                                     DeleteResponse)

class LocationListResponse(ListResponse):
    pass

class LocationSingleResponse(DetailResponse):
    pass

class LocationCreateRequest(BaseModel):
    tenant_id: UUID
    workspace_id: UUID
    name: str
    description: Optional[str] = None
    address: Optional[str] = None

class LocationCreateResponse(CreateResponse):
    pass

class LocationUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None

class LocationUpdateResponse(UpdateResponse):
    pass

class LocationDeleteResponse(DeleteResponse):
    pass
