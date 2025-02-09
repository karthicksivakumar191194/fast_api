from pydantic import BaseModel
from typing import List, Literal, Optional

class Pagination(BaseModel):
    totalItems: int
    itemsPerPage: int
    currentPage: int
    totalPages: int
    nextPage: Optional[str] = None
    previousPage: Optional[str] = None

class DropdownItem(BaseModel):
    id: str
    value: str

class ListResponse(BaseModel):
    status: Literal["success"]
    count: int
    data: List[BaseModel]
    pagination: Pagination

class DetailResponse(BaseModel):
    status: Literal["success"]
    data: dict

class CreateResponse(BaseModel):
    status: Literal["success"]
    message: str
    data: Optional[BaseModel] = None
    created_id: Optional[str] = None

class UpdateResponse(BaseModel):
    status: Literal["success"]
    message: str
    data: Optional[BaseModel] = None
    updated_id: Optional[str] = None

class DeleteResponse(BaseModel):
    status: Literal["success"]
    message: str
    deleted_id: Optional[str] = None

class DropdownResponse(BaseModel):
    status: Literal["success"]
    data: List[DropdownItem]
