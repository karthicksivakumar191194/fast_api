from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.schemas.location import (LocationListResponse, LocationSingleResponse, LocationCreateRequest,
                                  LocationCreateResponse, LocationUpdateRequest, LocationUpdateResponse,
                                  LocationDeleteResponse)

router = APIRouter()


@router.get("/", response_model=LocationListResponse, status_code=status.HTTP_200_OK)
def list_locations(db: Session = Depends(get_db)) -> LocationListResponse:
    """
    Endpoint to list all locations.
    """
    pass


@router.get("/{location_id}", response_model=LocationSingleResponse, status_code=status.HTTP_200_OK)
def get_single_location(location_id: UUID, db: Session = Depends(get_db)) -> LocationSingleResponse:
    """
    Endpoint to retrieve a location by ID.
    """

    # message - Location retrieved successfully.

    pass


@router.post("/", response_model=LocationCreateResponse, status_code=status.HTTP_201_CREATED)
def create_location(request: LocationCreateRequest, db: Session = Depends(get_db)) -> LocationCreateResponse:
    """
    Endpoint to create a new location.
    """

    return LocationCreateResponse(
        status="success",
        message="Location created successfully."
    )


@router.put("/{location_id}", response_model=LocationUpdateResponse, status_code=status.HTTP_200_OK)
def update_location(location_id: UUID, request: LocationUpdateRequest,
                    db: Session = Depends(get_db)) -> LocationUpdateResponse:
    """
    Endpoint to update an existing location.
    """

    return LocationUpdateResponse(
        status="success",
        message="Location updated successfully."
    )


@router.delete("/{location_id}", response_model=LocationDeleteResponse, status_code=status.HTTP_200_OK)
def delete_location(location_id: UUID, db: Session = Depends(get_db)) -> LocationDeleteResponse:
    """
    Endpoint to soft delete a location.
    """

    return LocationDeleteResponse(
        status="success",
        message="Location deleted successfully."
    )


# @router.post("/assign-user", response_model=None, status_code=status.HTTP_200_OK)
# def assign_user_to_location(request: None, db: Session = Depends(get_db)) -> None:
#     """
#     Endpoint to assign a user to a location.
#     """
#
#     # message - User assigned to location successfully.
#
#     pass
#
#
# @router.post("/assign-team", response_model=None, status_code=status.HTTP_200_OK)
# def assign_team_to_location(request: None, db: Session = Depends(get_db)) -> None:
#     """
#     Endpoint to assign a team to a location.
#     """
#
#     # message - Team assigned to location successfully.
#
#     pass