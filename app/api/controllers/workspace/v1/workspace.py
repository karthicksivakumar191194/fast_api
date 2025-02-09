from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.workspace import WorkspaceListResponse, WorkspaceCreateRequest, WorkspaceCreateResponse

router = APIRouter()

@router.get("/", response_model=WorkspaceListResponse, status_code=status.HTTP_200_OK)
def list_workspaces(db: Session = Depends(get_db)) -> WorkspaceListResponse:
    """
    Endpoint to list all workspaces.
    """

    # If requested by account owner, get all workspaces under tenant
    # else get workspaces mapped to the user

    pass

@router.post("/", response_model=WorkspaceCreateResponse, status_code=status.HTTP_201_CREATED)
def create(request: WorkspaceCreateRequest, db: Session = Depends(get_db)) -> WorkspaceCreateResponse:
    """
    Endpoint to create workspace.
    """

    return WorkspaceCreateResponse(
        status="success",
        message="Workspace created successfully."
    )